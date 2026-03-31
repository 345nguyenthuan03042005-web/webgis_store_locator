from django.core.management.base import BaseCommand

from modules.store.models import NhaCungCap, NhomSanPham, SanPham, ThuongHieu


PRODUCT_NAME_MAP = {
    "Froster Cau Vong (Size L)": "Froster Cầu Vồng (Size L)",
    "Mi Tron Indomie Trung Op La Xuc Xich": "Mì Trộn Indomie Trứng Ốp La Xúc Xích",
    "Banh Bao Trung Muoi (Hap nong)": "Bánh Bao Trứng Muối (Hấp nóng)",
    "Banh Mi Op La 2 Trung": "Bánh Mì Ốp La 2 Trứng",
    "Ca Phe Bac Xiu Da (Ly lon)": "Cà Phê Bạc Xỉu Đá (Ly lớn)",
    "Xoi La Chuoi (Thit Kho Tau)": "Xôi Lá Chuối (Thịt Kho Tàu)",
    "Tokbokki Xuc Xich Sot Cay (Ly)": "Tokbokki Xúc Xích Sốt Cay (Ly)",
    "Nuoc Ep Dua Hau Youus 230ml": "Nước Ép Dưa Hấu Youus 230ml",
    "Bap Rang Bo Vi Pho Mai Youus": "Bắp Rang Bơ Vị Phô Mai Youus",
    "Lau Cha Ca Omok (Ly)": "Lẩu Chả Cá Omok (Ly)",
    "Com Nam Tom Mayonnaise": "Cơm Nắm Tôm Mayonnaise",
    "Mi Hao Hao Tom Chua Cay (Goi)": "Mì Hảo Hảo Tôm Chua Cay (Gói)",
    "Mi Ly Modern Lau Thai Tom": "Mì Ly Modern Lẩu Thái Tôm",
    "Nuoc Ngot Coca-Cola Zero 320ml": "Nước Ngọt Coca-Cola Zero 320ml",
    "Nuoc Tang Luc Sting Dau 330ml": "Nước Tăng Lực Sting Dâu 330ml",
    "Nuoc Tinh Khiet Aquafina 500ml": "Nước Tinh Khiết Aquafina 500ml",
    "Snack Khoai Tay O'Star Vi Kim Chi 63g": "Snack Khoai Tây O'Star Vị Kim Chi 63g",
    "Sua Tuoi TH True Milk Co Duong 180ml": "Sữa Tươi TH True Milk Có Đường 180ml",
}

GROUP_NAME_MAP = {
    "Do an che bien nong (Hot Food)": "Đồ ăn chế biến nóng (Hot Food)",
    "Do uong pha che (Barista/Froster)": "Đồ uống pha chế (Barista/Froster)",
    "Mi an lien & Thuc pham dong hop": "Mì ăn liền & Thực phẩm đóng hộp",
    "Nuoc giai khat & Do uong lanh": "Nước giải khát & Đồ uống lạnh",
    "Snack & Banh keo": "Snack & Bánh kẹo",
    "Sua & Che pham tu sua": "Sữa & Chế phẩm từ sữa",
    "Hoa my pham & Ca nhan": "Hóa mỹ phẩm & Cá nhân",
}

SUPPLIER_NAME_MAP = {
    "Cong ty TNHH Vong Tron Do (Red Circle)": "Công ty TNHH Vòng Tròn Đỏ (Red Circle)",
    "Cong ty TNHH Thuc Pham Orion Vina": "Công ty TNHH Thực Phẩm Orion Vina",
}

BRAND_NAME_MAP = {
    "Youus (Han Quoc)": "Youus (Hàn Quốc)",
}


def _apply_mapping(queryset, mapping):
    updated = 0
    for source, target in mapping.items():
        updated += queryset.filter(ten=source).update(ten=target)
    return updated


class Command(BaseCommand):
    help = "Chuan hoa ten danh muc san pham sang tieng Viet co dau."

    def handle(self, *args, **options):
        product_updated = _apply_mapping(SanPham.objects, PRODUCT_NAME_MAP)
        group_updated = _apply_mapping(NhomSanPham.objects, GROUP_NAME_MAP)
        supplier_updated = _apply_mapping(NhaCungCap.objects, SUPPLIER_NAME_MAP)
        brand_updated = _apply_mapping(ThuongHieu.objects, BRAND_NAME_MAP)

        self.stdout.write(
            self.style.SUCCESS(
                "Da chuan hoa tieng Viet: "
                f"{product_updated} san pham, "
                f"{group_updated} nhom, "
                f"{supplier_updated} nha cung cap, "
                f"{brand_updated} thuong hieu."
            )
        )
