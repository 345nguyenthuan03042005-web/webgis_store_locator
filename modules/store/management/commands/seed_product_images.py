from pathlib import Path

from django.core.management.base import BaseCommand

from modules.store.models import SanPham


IMAGE_MAPPING = {
    "Froster Cau Vong (Size L)": "froster_cau_vong.jpg",
    "Mi Tron Indomie Trung Op La Xuc Xich": "mi_tron_indomio_trung_op_la_xuc_xich_1.jpg",
    "Banh Bao Trung Muoi (Hap nong)": "BB_Trung_Muoi_1.jpg",
    "Banh Mi Op La 2 Trung": "BM_Op_La_2Trung_1.jpg",
    "Ca Phe Bac Xiu Da (Ly lon)": "CF_Bac_Xiu.jpg",
    "Xoi La Chuoi (Thit Kho Tau)": "xoi_la_chuoi_thit_kho_tau_1.jpg",
    "Tokbokki Xuc Xich Sot Cay (Ly)": "tokbokki_xuc_xich_sot_cay_ly_2.jpg",
    "Nuoc Ep Dua Hau Youus 230ml": "nuoc_ep_dua_hau_youus_1.jpg",
    "Sandwich Inkigayo": "sandwich_inkigayo_1.jpg",
    "Bap Rang Bo Vi Pho Mai Youus": "bap_rang_bo_pho_mai_youus_1.jpg",
    "Lau Cha Ca Omok (Ly)": "lau_cha_ca_omok_ly.jpg",
    "Com Nam Tom Mayonnaise": "C_Nam_Tom_my.jpg",
    "Mi Hao Hao Tom Chua Cay (Goi)": "mi_hao_hao_tom_chua_cay.jpg",
    "Mi Ly Modern Lau Thai Tom": "mi_ly_modern_lau_thai_tom_1.jpg",
    "Nuoc Ngot Coca-Cola Zero 320ml": "caca_zero_1.jpg",
    "Nuoc Tang Luc Sting Dau 330ml": "sting_dau_1.jpg",
    "Nuoc Tinh Khiet Aquafina 500ml": "aquafina_1.jpg",
    "Snack Khoai Tay O'Star Vi Kim Chi 63g": "ostar_kimchi_1.jpg",
    "Sua Tuoi TH True Milk Co Duong 180ml": "TH_180_co_duong_1.jpg",
}


class Command(BaseCommand):
    help = "Gan anh san pham tu thu muc media/images vao cac ban ghi san pham."

    def add_arguments(self, parser):
        parser.add_argument(
            "--source-dir",
            default="media/images",
            help="Thu muc chua anh san pham, mac dinh la media/images",
        )

    def handle(self, *args, **options):
        source_dir = Path(options["source_dir"])
        updated = 0
        missing = []

        for product_name, filename in IMAGE_MAPPING.items():
            image_path = source_dir / filename
            if not image_path.exists():
                missing.append(filename)
                continue

            updated += SanPham.objects.filter(ten=product_name).update(hinh_anh=f"images/{filename}")

        self.stdout.write(self.style.SUCCESS(f"Da cap nhat {updated} anh san pham."))
        if missing:
            self.stdout.write(self.style.WARNING(f"Thieu {len(missing)} file anh: {', '.join(missing)}"))
