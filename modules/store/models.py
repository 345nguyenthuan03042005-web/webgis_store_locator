from django.conf import settings
from django.db import models


class ThuongHieu(models.Model):
    ten = models.CharField("Tên thương hiệu", max_length=50, unique=True)

    class Meta:
        verbose_name = "Thương hiệu"
        verbose_name_plural = "Thương hiệu"

    def __str__(self) -> str:
        return self.ten


class NhaCungCap(models.Model):
    ten = models.CharField("Tên nhà cung cấp", max_length=120)
    ghi_chu = models.TextField("Ghi chú", blank=True)

    class Meta:
        verbose_name = "Nhà cung cấp"
        verbose_name_plural = "Nhà cung cấp"

    def __str__(self) -> str:
        return self.ten


class NhomSanPham(models.Model):
    ten = models.CharField("Tên nhóm sản phẩm", max_length=80, unique=True)

    class Meta:
        verbose_name = "Nhóm sản phẩm"
        verbose_name_plural = "Nhóm sản phẩm"

    def __str__(self) -> str:
        return self.ten


class SanPham(models.Model):
    ten = models.CharField("Tên sản phẩm", max_length=120)
    gia_ban = models.DecimalField(
        "Giá bán",
        max_digits=12,
        decimal_places=0,
        default=0,
    )

    nhom_san_pham = models.ForeignKey(
        "NhomSanPham",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Nhóm sản phẩm",
    )

    nha_cung_cap = models.ForeignKey(
        "NhaCungCap",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Nhà cung cấp",
    )

    thuong_hieu = models.ForeignKey(
        "ThuongHieu",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Thương hiệu",
    )

    hinh_anh = models.ImageField(
        "Hình ảnh sản phẩm",
        upload_to="images/",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"

    def __str__(self) -> str:
        return self.ten


class ChuoiCuaHang(models.Model):
    ten = models.CharField("Tên chuỗi cửa hàng", max_length=100)
    mo_ta = models.TextField("Mô tả", blank=True)

    logo = models.ImageField(
        "Logo chuỗi",
        upload_to="logo/",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Chuỗi cửa hàng"
        verbose_name_plural = "Chuỗi cửa hàng"

    def __str__(self) -> str:
        return self.ten


class CuaHang(models.Model):
    chuoi = models.ForeignKey(
        "ChuoiCuaHang",
        on_delete=models.CASCADE,
        verbose_name="Chuỗi cửa hàng",
    )

    ten = models.CharField("Tên cửa hàng", max_length=100)
    dia_chi = models.CharField("Địa chỉ", max_length=255)
    quan_huyen = models.CharField("Quận/Huyện", max_length=50)

    vi_do = models.FloatField("Vĩ độ (lat)")
    kinh_do = models.FloatField("Kinh độ (lng)")
    mo_cua = models.TimeField("Giờ mở cửa", null=True, blank=True)
    dong_cua = models.TimeField("Giờ đóng cửa", null=True, blank=True)
    hoat_dong_24h = models.BooleanField("Hoạt động 24h", default=False)

    san_pham = models.ManyToManyField(
        "SanPham",
        blank=True,
        verbose_name="Sản phẩm",
    )

    class Meta:
        verbose_name = "Cửa hàng"
        verbose_name_plural = "Cửa hàng"

    def __str__(self) -> str:
        return f"{self.ten} ({self.chuoi.ten})"


class NhanVien(models.Model):
    cua_hang = models.ForeignKey(
        "CuaHang",
        on_delete=models.CASCADE,
        verbose_name="Cửa hàng",
    )

    ho_ten = models.CharField("Họ và tên", max_length=120)
    chuc_vu = models.CharField("Chức vụ", max_length=50, blank=True)

    so_dien_thoai = models.CharField(
        "Số điện thoại",
        max_length=15,
        blank=True,
    )

    email = models.EmailField(
        "Email",
        blank=True,
    )

    dia_chi = models.CharField(
        "Địa chỉ",
        max_length=255,
        blank=True,
    )

    avatar = models.ImageField(
        "Ảnh nhân viên",
        upload_to="avatar/",
        blank=True,
        null=True,
        default="avatar/default.jpg",
    )

    class Meta:
        verbose_name = "Nhân viên"
        verbose_name_plural = "Nhân viên"

    def __str__(self) -> str:
        return f"{self.ho_ten} - {self.cua_hang.ten}"


class KhuyenMai(models.Model):
    ten = models.CharField("Tên khuyến mãi", max_length=150)
    mo_ta = models.TextField("Mô tả", blank=True)

    thuong_hieu = models.ManyToManyField(
        "ThuongHieu",
        blank=True,
        verbose_name="Áp dụng cho thương hiệu",
    )

    cua_hang = models.ManyToManyField(
        "CuaHang",
        blank=True,
        verbose_name="Áp dụng cho cửa hàng",
    )

    class Meta:
        verbose_name = "Khuyến mãi"
        verbose_name_plural = "Khuyến mãi"

    def __str__(self) -> str:
        return self.ten


class Notification(models.Model):
    level = models.CharField("Mức độ", max_length=20, default="error")
    title = models.CharField("Tiêu đề", max_length=200)
    message = models.TextField("Nội dung", blank=True)
    path = models.CharField("Đường dẫn", max_length=255, blank=True)
    method = models.CharField("Phương thức", max_length=10, blank=True)
    status_code = models.IntegerField("Mã lỗi", null=True, blank=True)
    resolved = models.BooleanField("Đã xử lý", default=False)
    created_at = models.DateTimeField("Thời gian", auto_now_add=True)

    class Meta:
        verbose_name = "Thông báo"
        verbose_name_plural = "Thông báo"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.title} ({self.status_code or '-'})"


class HoSoKhachHang(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ho_so_khach_hang",
        verbose_name="Tài khoản",
    )
    so_dien_thoai = models.CharField("Số điện thoại", max_length=20, blank=True)
    dia_chi = models.CharField("Địa chỉ", max_length=255, blank=True)

    class Meta:
        verbose_name = "Hồ sơ khách hàng"
        verbose_name_plural = "Hồ sơ khách hàng"

    def __str__(self) -> str:
        return f"Hồ sơ {self.user.username}"


class DonHang(models.Model):
    STATUS_CHOICES = (
        ("pending", "Chờ xử lý"),
        ("confirmed", "Đã xác nhận"),
        ("shipping", "Đang giao"),
        ("delivered", "Đã giao"),
        ("done", "Hoàn tất"),
        ("cancelled", "Đã hủy"),
    )

    khach_hang = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Khách hàng",
    )
    ho_ten_nguoi_nhan = models.CharField("Họ tên người nhận", max_length=120)
    so_dien_thoai = models.CharField("Số điện thoại", max_length=20)
    dia_chi_giao_hang = models.CharField("Địa chỉ giao hàng", max_length=255)
    ghi_chu = models.TextField("Ghi chú", blank=True)
    trang_thai = models.CharField("Trạng thái", max_length=20, choices=STATUS_CHOICES, default="pending")
    tong_so_luong = models.PositiveIntegerField("Tổng số lượng", default=0)
    tong_tien = models.DecimalField("Tổng tiền", max_digits=12, decimal_places=0, default=0)
    created_at = models.DateTimeField("Thời gian tạo", auto_now_add=True)

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Đơn hàng #{self.pk} - {self.khach_hang.username}"


class ChiTietDonHang(models.Model):
    don_hang = models.ForeignKey(
        "DonHang",
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Đơn hàng",
    )
    san_pham = models.ForeignKey(
        "SanPham",
        on_delete=models.CASCADE,
        verbose_name="Sản phẩm",
    )
    so_luong = models.PositiveIntegerField("Số lượng", default=1)
    don_gia = models.DecimalField("Đơn giá", max_digits=12, decimal_places=0, default=0)

    class Meta:
        verbose_name = "Chi tiết đơn hàng"
        verbose_name_plural = "Chi tiết đơn hàng"

    def __str__(self) -> str:
        return f"{self.san_pham.ten} x {self.so_luong}"
