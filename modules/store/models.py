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
