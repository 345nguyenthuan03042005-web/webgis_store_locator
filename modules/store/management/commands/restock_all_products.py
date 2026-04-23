from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from modules.store.models import CuaHang, GiaoDichKho, NhanVien, SanPham, TonKhoCuaHang


SIGNATURE_GIF_BYTES = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!"
    b"\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00"
    b"\x00\x02\x02D\x01\x00;"
)
SIGNATURE_RELATIVE_PATH = "signatures/restock-bulk.gif"


def _ensure_signature_file() -> str:
    signature_path = Path(settings.MEDIA_ROOT) / SIGNATURE_RELATIVE_PATH
    signature_path.parent.mkdir(parents=True, exist_ok=True)
    if not signature_path.exists():
        signature_path.write_bytes(SIGNATURE_GIF_BYTES)
    return SIGNATURE_RELATIVE_PATH


def restock_products(*, target_stock: int, note: str, store_ids=None):
    if target_stock <= 0:
        raise ValueError("--target-stock must be greater than 0.")
    if not (note or "").strip():
        raise ValueError("Vui lòng nhập lý do điều chỉnh tồn kho.")

    requested_store_ids = sorted({int(store_id) for store_id in (store_ids or [])})
    stores_qs = CuaHang.objects.order_by("pk")
    if requested_store_ids:
        stores_qs = stores_qs.filter(pk__in=requested_store_ids)
    stores = list(stores_qs)
    products = list(SanPham.objects.order_by("pk"))

    if requested_store_ids:
        found_store_ids = {store.pk for store in stores}
        missing_store_ids = [store_id for store_id in requested_store_ids if store_id not in found_store_ids]
        if missing_store_ids:
            raise LookupError("Store IDs not found: " + ", ".join(str(store_id) for store_id in missing_store_ids))

    if not stores:
        raise LookupError("No stores found to restock.")
    if not products:
        raise LookupError("No products found to restock.")

    signature_path = _ensure_signature_file()
    product_totals = {product.pk: int(product.ton_kho or 0) for product in products}
    stock_rows = list(
        TonKhoCuaHang.objects.filter(
            cua_hang_id__in=[store.pk for store in stores],
            san_pham_id__in=[product.pk for product in products],
        )
    )
    stock_map = {(row.cua_hang_id, row.san_pham_id): row for row in stock_rows}

    employee_map = {}
    for employee in NhanVien.objects.filter(cua_hang_id__in=[store.pk for store in stores]).order_by("cua_hang_id", "pk"):
        employee_map.setdefault(employee.cua_hang_id, employee)

    store_product_pairs = {(store.pk, product.pk) for store in stores for product in products}
    through_model = CuaHang.san_pham.through
    existing_links = set(
        through_model.objects.filter(
            cuahang_id__in=[store.pk for store in stores],
            sanpham_id__in=[product.pk for product in products],
        ).values_list("cuahang_id", "sanpham_id")
    )

    created_employees = 0
    created_movements = 0
    imported_units = 0

    with transaction.atomic():
        for store in stores:
            if store.pk in employee_map:
                continue
            employee = NhanVien.objects.create(
                cua_hang=store,
                ho_ten=f"Nhân viên nhập kho {store.ten}",
                chuc_vu="Kho",
            )
            employee_map[store.pk] = employee
            created_employees += 1

        missing_links = [
            through_model(cuahang_id=store_id, sanpham_id=product_id)
            for (store_id, product_id) in store_product_pairs - existing_links
        ]
        if missing_links:
            through_model.objects.bulk_create(missing_links, ignore_conflicts=True, batch_size=1000)

        new_movements = []
        rows_to_create = []
        rows_to_update = []
        products_to_update = []
        created_at = timezone.now()

        for product in products:
            running_total = product_totals[product.pk]
            for store in stores:
                row = stock_map.get((store.pk, product.pk))
                current_stock = int(row.ton_kho or 0) if row is not None else 0
                if current_stock >= target_stock:
                    continue

                delta = target_stock - current_stock
                new_movements.append(
                    GiaoDichKho(
                        san_pham_id=product.pk,
                        cua_hang_id=store.pk,
                        nhan_vien_id=employee_map[store.pk].pk,
                        loai="import",
                        so_luong=delta,
                        ton_truoc=running_total,
                        ton_sau=running_total + delta,
                        ghi_chu=note,
                        chu_ky=signature_path,
                        created_at=created_at,
                    )
                )
                running_total += delta
                imported_units += delta
                created_movements += 1

                if row is None:
                    row = TonKhoCuaHang(
                        cua_hang_id=store.pk,
                        san_pham_id=product.pk,
                        ton_kho=target_stock,
                    )
                    stock_map[(store.pk, product.pk)] = row
                    rows_to_create.append(row)
                else:
                    row.ton_kho = target_stock
                    rows_to_update.append(row)

            if running_total != product_totals[product.pk]:
                product.ton_kho = running_total
                products_to_update.append(product)

        if new_movements:
            GiaoDichKho.objects.bulk_create(new_movements, batch_size=1000)
        if rows_to_create:
            TonKhoCuaHang.objects.bulk_create(rows_to_create, batch_size=1000)
        if rows_to_update:
            TonKhoCuaHang.objects.bulk_update(rows_to_update, ["ton_kho", "updated_at"], batch_size=1000)
        if products_to_update:
            SanPham.objects.bulk_update(products_to_update, ["ton_kho"], batch_size=500)

    return {
        "store_count": len(stores),
        "created_movements": created_movements,
        "imported_units": imported_units,
        "created_employees": created_employees,
    }


class Command(BaseCommand):
    help = (
        "Ensure every product has stock in every store by creating missing "
        "import movements up to a target quantity."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--target-stock",
            type=int,
            default=25,
            help="Target stock quantity for each store-product pair. Default: 25",
        )
        parser.add_argument(
            "--store-id",
            dest="store_ids",
            action="append",
            type=int,
            help="Restock a specific store by ID. Repeat this option to target multiple stores.",
        )
        parser.add_argument(
            "--store-ids",
            dest="store_ids_bulk",
            nargs="+",
            type=int,
            help="Restock multiple stores by ID in one command, e.g. --store-ids 1 2 3",
        )
        parser.add_argument(
            "--note",
            default="Nhập kho đồng loạt để mở bán toàn bộ sản phẩm",
            help="Lý do điều chỉnh tồn kho cho các phiếu nhập tự động.",
        )

    def handle(self, *args, **options):
        target_stock = options["target_stock"]
        note = (options["note"] or "").strip()
        single_store_ids = options.get("store_ids") or []
        bulk_store_ids = options.get("store_ids_bulk") or []
        requested_store_ids = []
        if single_store_ids:
            requested_store_ids.extend(single_store_ids)
        if bulk_store_ids:
            requested_store_ids.extend(bulk_store_ids)
        try:
            summary = restock_products(
                target_stock=target_stock,
                note=note,
                store_ids=requested_store_ids,
            )
        except ValueError as exc:
            self.stderr.write(self.style.ERROR(str(exc)))
            return
        except LookupError as exc:
            self.stderr.write(self.style.ERROR(str(exc)))
            return

        self.stdout.write(
            self.style.SUCCESS(
                "Đã nhập kho xong: "
                f"{summary['store_count']} cửa hàng, "
                f"{summary['created_movements']} phiếu nhập, "
                f"{summary['imported_units']} đơn vị hàng, "
                f"{summary['created_employees']} nhân viên kho được tạo bổ sung."
            )
        )
