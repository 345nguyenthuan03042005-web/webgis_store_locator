from django.shortcuts import render


def home(request):
    return render(request, "store/home.html")


def store_list_page(request):
    return render(request, "store/store_list.html")


def map_page(request):
    return render(request, "store/map.html")


INFO_PAGES = {
    "gioi-thieu-circle-k": {
        "title": "Giới thiệu Circle K",
        "kicker": "Về Chúng Tôi",
        "summary": "Từ cửa hàng đầu tiên tại Texas (1951), Circle K phát triển thành thương hiệu cửa hàng tiện lợi toàn cầu và đang mở rộng mạnh tại Việt Nam.",
        "sections": [
            {
                "heading": "Circle K Toàn Cầu",
                "content": "Circle K hiện diện tại nhiều quốc gia như Mỹ, Canada, Mexico, châu Âu, Nhật Bản, Đài Loan và nhiều thị trường khác, phục vụ hàng triệu khách hàng mỗi ngày.",
            },
            {
                "heading": "Lịch sử phát triển",
                "content": "Trong hơn 70 năm, thương hiệu không ngừng mở rộng hệ thống, chuẩn hóa vận hành và nâng cấp trải nghiệm mua sắm tiện lợi 24/7 cho cộng đồng đô thị.",
            },
            {
                "heading": "Circle K Việt Nam",
                "content": "Circle K Việt Nam hoạt động từ năm 2008 và phát triển nhanh tại TP.HCM cùng nhiều tỉnh thành lớn, tập trung vào nhu cầu mua sắm linh hoạt của người trẻ và dân văn phòng.",
            },
            {
                "heading": "Điểm khác biệt",
                "content": "Hệ thống mở cửa 24/7, danh mục sản phẩm đa dạng, vị trí thuận tiện và dịch vụ thân thiện giúp khách hàng mua nhanh, dùng ngay, tiết kiệm thời gian.",
            },
            {
                "heading": "Tầm nhìn",
                "content": "Trở thành chuỗi cửa hàng tiện lợi được ưu tiên lựa chọn hàng đầu tại Việt Nam bằng mô hình vận hành hiệu quả, tiêu chuẩn dịch vụ ổn định và đổi mới liên tục.",
            },
            {
                "heading": "Sứ mệnh tại Việt Nam",
                "content": "Cung cấp sản phẩm và dịch vụ đáng tin cậy với tốc độ nhanh, góp phần nâng cao chất lượng sống của khách hàng trong từng khu phố và điểm dân cư.",
            },
        ],
    },
    "tin-tuc-su-kien": {
        "title": "Tin tức và Sự kiện",
        "kicker": "Cập Nhật",
        "summary": "Tổng hợp thông tin nổi bật về chương trình khuyến mãi, hoạt động cộng đồng và sự kiện mới trong hệ thống Circle K và GS25.",
        "sections": [
            {
                "heading": "Khuyến mãi theo mùa",
                "content": "Ưu đãi theo tuần, combo giờ vàng và các chương trình đồng giá cho nhóm sản phẩm thiết yếu.",
            },
            {
                "heading": "Sự kiện tại cửa hàng",
                "content": "Mini game, trải nghiệm sản phẩm mới, hoạt động tri ân khách hàng tại các điểm bán trọng điểm.",
            },
            {
                "heading": "Hoạt động cộng đồng",
                "content": "Chiến dịch xanh, hỗ trợ sinh viên và các chương trình đồng hành cùng khu dân cư địa phương.",
            },
        ],
    },
    "tuyen-dung": {
        "title": "Tuyển dụng",
        "kicker": "Cơ Hội Nghề Nghiệp",
        "summary": "Làm việc tại Circle K là cơ hội phát triển trong môi trường năng động, tôn trọng con người và có lộ trình nghề nghiệp rõ ràng.",
        "sections": [
            {
                "heading": "Môi trường làm việc",
                "content": "Đội ngũ trẻ, tinh thần hợp tác cao, quy trình chuyên nghiệp và văn hóa hỗ trợ lẫn nhau giúp nhân sự mới nhanh hòa nhập và phát huy năng lực.",
            },
            {
                "heading": "4 Giá trị EVP",
                "content": "Phúc lợi cạnh tranh, phát triển sự nghiệp, văn hóa tích cực và ghi nhận thành tích là nền tảng giữ chân và tạo động lực cho nhân viên.",
            },
            {
                "heading": "Phúc lợi nổi bật",
                "content": "Hỗ trợ theo ca, đào tạo định kỳ, phụ cấp theo vị trí, chế độ thưởng hiệu suất và chính sách gắn bó dành cho nhân sự ổn định lâu dài.",
            },
            {
                "heading": "Lộ trình phát triển",
                "content": "Từ nhân viên cửa hàng có thể thăng tiến lên ca trưởng, quản lý cửa hàng, giám sát khu vực hoặc chuyển sang các bộ phận vận hành và văn phòng.",
            },
            {
                "heading": "Vị trí tuyển dụng",
                "content": "Nhân viên bán hàng, ca trưởng, quản lý cửa hàng, hỗ trợ vận hành, marketing, chuỗi cung ứng và các vị trí chuyên môn khác theo từng giai đoạn.",
            },
            {
                "heading": "Cách ứng tuyển",
                "content": "Ứng viên có thể nộp hồ sơ trực tuyến, gửi email tuyển dụng hoặc đăng ký trực tiếp tại cửa hàng gần nhất để được hướng dẫn phỏng vấn.",
            },
        ],
    },
    "chinh-sach-bao-mat": {
        "title": "Chính sách bảo mật",
        "kicker": "Bảo Mật Dữ Liệu",
        "summary": "Cam kết bảo vệ thông tin cá nhân của khách hàng khi truy cập website, đăng ký nhận tin và sử dụng dịch vụ trực tuyến.",
        "sections": [
            {
                "heading": "Phạm vi thu thập",
                "content": "Chỉ thu thập thông tin cần thiết để xử lý yêu cầu, chăm sóc khách hàng và nâng cao chất lượng dịch vụ.",
            },
            {
                "heading": "Mục đích sử dụng",
                "content": "Dùng cho xác nhận liên hệ, gửi thông báo dịch vụ, cải thiện trải nghiệm và tuân thủ quy định pháp luật.",
            },
            {
                "heading": "Bảo vệ thông tin",
                "content": "Áp dụng biện pháp kỹ thuật và quy trình nội bộ để ngăn truy cập trái phép, rò rỉ hoặc lạm dụng dữ liệu.",
            },
        ],
    },
    "chinh-sach-thanh-toan": {
        "title": "Chính sách thanh toán",
        "kicker": "Thanh Toán",
        "summary": "Quy định về phương thức thanh toán, xác nhận giao dịch và xử lý các vấn đề phát sinh liên quan đến thanh toán.",
        "sections": [
            {
                "heading": "Phương thức hỗ trợ",
                "content": "Tiền mặt, thẻ ngân hàng, ví điện tử và các hình thức thanh toán số được chấp nhận theo từng cửa hàng.",
            },
            {
                "heading": "Xác nhận giao dịch",
                "content": "Mọi giao dịch được ghi nhận trên hệ thống và thể hiện bằng hóa đơn hoặc biên nhận điện tử tương ứng.",
            },
            {
                "heading": "Xử lý sai lệch",
                "content": "Trường hợp thanh toán lỗi hoặc trừ tiền bất thường sẽ được tiếp nhận, kiểm tra và phản hồi theo quy trình hỗ trợ.",
            },
        ],
    },
    "dieu-khoan-su-dung": {
        "title": "Điều khoản sử dụng",
        "kicker": "Điều Khoản",
        "summary": "Các điều kiện áp dụng khi truy cập website và sử dụng nội dung, công cụ tra cứu cửa hàng và dịch vụ liên quan.",
        "sections": [
            {
                "heading": "Quyền và trách nhiệm",
                "content": "Người dùng có trách nhiệm cung cấp thông tin đúng mục đích, không sử dụng website vào hành vi gây hại.",
            },
            {
                "heading": "Nội dung và bản quyền",
                "content": "Mọi nội dung hiển thị thuộc quyền quản lý của hệ thống, nghiêm cấm sao chép trái phép khi chưa được chấp thuận.",
            },
            {
                "heading": "Cập nhật điều khoản",
                "content": "Điều khoản có thể được cập nhật theo nhu cầu vận hành và quy định pháp lý, phiên bản mới có hiệu lực khi công bố.",
            },
        ],
    },
}


PAGE_MEDIA = {
    "gioi-thieu-circle-k": {
        "hero_image": "https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=1400&q=80",
        "section_images": [
            "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1556740738-b6a63e27c4df?auto=format&fit=crop&w=900&q=80",
        ],
    },
    "tin-tuc-su-kien": {
        "hero_image": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=1400&q=80",
        "section_images": [
            "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1511578314322-379afb476865?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1529390079861-591de354faf5?auto=format&fit=crop&w=900&q=80",
        ],
    },
    "tuyen-dung": {
        "hero_image": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=1400&q=80",
        "section_images": [
            "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=900&q=80",
        ],
    },
    "chinh-sach-bao-mat": {
        "hero_image": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?auto=format&fit=crop&w=1400&q=80",
        "section_images": [
            "https://images.unsplash.com/photo-1510511459019-5dda7724fd87?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1633265486064-086b219458ec?auto=format&fit=crop&w=900&q=80",
        ],
    },
    "chinh-sach-thanh-toan": {
        "hero_image": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=1400&q=80",
        "section_images": [
            "https://images.unsplash.com/photo-1559526324-593bc073d938?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1563013544-824ae1b704d3?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1579621970795-87facc2f976d?auto=format&fit=crop&w=900&q=80",
        ],
    },
    "dieu-khoan-su-dung": {
        "hero_image": "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?auto=format&fit=crop&w=1400&q=80",
        "section_images": [
            "https://images.unsplash.com/photo-1589578527966-fdac0f44566c?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1521791136064-7986c2920216?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=900&q=80",
        ],
    },
}


NEWS_EVENTS = {
    "featured": {
        "title": "Circle K Việt Nam bổ nhiệm tân Tổng Giám đốc, đặt mục tiêu mở rộng lên 1.000 cửa hàng",
        "excerpt": "Circle K Việt Nam công bố lãnh đạo mới cho giai đoạn tăng trưởng tiếp theo, tập trung mở rộng mạng lưới, chuẩn hóa vận hành và nâng cao trải nghiệm khách hàng.",
        "image": "https://images.unsplash.com/photo-1556740738-b6a63e27c4df?auto=format&fit=crop&w=1400&q=80",
        "category": "Tin doanh nghiệp",
    },
    "items": [
        {
            "title": "Circle K x What It IsNt: đồng phục mới 2025",
            "excerpt": "Bộ đồng phục mới lấy cảm hứng từ văn hóa đường phố, tăng nhận diện thương hiệu và sự linh hoạt khi vận hành tại cửa hàng.",
            "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=1000&q=80",
            "category": "Văn hóa",
        },
        {
            "title": "Thư viện Ước Mơ đến với học sinh Ba Vì",
            "excerpt": "Hoạt động cộng đồng hỗ trợ sách và không gian đọc cho học sinh, tiếp tục hành trình phát triển bền vững tại địa phương.",
            "image": "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=1000&q=80",
            "category": "Cộng đồng",
        },
        {
            "title": "Circle K hợp tác cùng đối tác bất động sản đô thị",
            "excerpt": "Mô hình cửa hàng tiện lợi trong khu dân cư và tòa nhà văn phòng giúp khách hàng tiếp cận dịch vụ nhanh hơn.",
            "image": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1000&q=80",
            "category": "Hợp tác",
        },
        {
            "title": "Nước sạch đến trường: chương trình vì cộng đồng",
            "excerpt": "Dự án tài trợ máy lọc nước và nâng cao điều kiện sinh hoạt học đường tại các khu vực còn hạn chế nguồn nước sạch.",
            "image": "https://images.unsplash.com/photo-1473445361085-b9a07f55608b?auto=format&fit=crop&w=1000&q=80",
            "category": "CSR",
        },
        {
            "title": "Ưu đãi tháng mới cho nhóm sản phẩm ăn nhanh",
            "excerpt": "Loạt combo hotdog, gà rán, cà phê và đồ uống mát với mức giá tối ưu cho khách hàng trẻ và dân văn phòng.",
            "image": "https://images.unsplash.com/photo-1525059696034-4967a8e1dca2?auto=format&fit=crop&w=1000&q=80",
            "category": "Ưu đãi",
        },
        {
            "title": "Mở rộng khung giờ chăm sóc khách hàng",
            "excerpt": "Kênh tiếp nhận phản hồi được tăng cường theo nhiều nền tảng để xử lý yêu cầu nhanh và nhất quán hơn.",
            "image": "https://images.unsplash.com/photo-1552581234-26160f608093?auto=format&fit=crop&w=1000&q=80",
            "category": "Dịch vụ",
        },
    ],
}


NEWS_DETAILS = {
    "bo-nhiem-tan-tong-giam-doc-1000-cua-hang": {
        "lead": "Circle K Việt Nam chính thức bổ nhiệm ông TC Cheng vào vị trí Tổng Giám đốc mới từ ngày 30 tháng 10 năm 2025, đánh dấu bước chuyển quan trọng trong giai đoạn tăng trưởng tiếp theo.",
        "paragraphs": [
            "Trong vai trò mới, ông TC sẽ điều hành toàn bộ hoạt động của Circle K Việt Nam với trọng tâm là mở rộng mạng lưới, nâng chuẩn vận hành và nâng cao trải nghiệm khách hàng trên toàn quốc.",
            "Với hơn 35 năm kinh nghiệm quản trị bán lẻ tại nhiều thị trường lớn, ông TC từng đảm nhiệm các vai trò lãnh đạo chiến lược trong các mô hình cửa hàng tiện lợi, siêu thị và thương mại điện tử.",
            "Mục tiêu giai đoạn mới là mở rộng lên 1.000 cửa hàng, đồng thời đẩy mạnh chuyển đổi số, chuẩn hóa vận hành chuỗi và tăng cường năng lực đội ngũ.",
            "Circle K cam kết tiếp tục mang đến dịch vụ tiện lợi chất lượng cao, lấy khách hàng làm trung tâm và duy trì vai trò tiên phong trong ngành bán lẻ tiện lợi.",
        ],
        "images": [
            "https://images.unsplash.com/photo-1556740738-b6a63e27c4df?auto=format&fit=crop&w=1400&q=80",
            "https://images.unsplash.com/photo-1600880292203-757bb62b4baf?auto=format&fit=crop&w=1400&q=80",
        ],
    },
    "dong-phuc-moi-2025": {
        "lead": "Bộ nhận diện đồng phục mới giúp đội ngũ cửa hàng thể hiện tinh thần trẻ trung, hiện đại và nhất quán thương hiệu.",
        "paragraphs": [
            "Thiết kế tập trung vào độ thoải mái khi làm việc theo ca, đồng thời nâng cao trải nghiệm thị giác tại điểm bán.",
            "Đây là một phần trong chương trình nâng cấp toàn diện hình ảnh vận hành tại các cửa hàng trọng điểm.",
        ],
        "images": [
            "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=1400&q=80",
        ],
    },
    "thu-vien-uoc-mo-ba-vi": {
        "lead": "Dự án cộng đồng tiếp tục được mở rộng với mục tiêu tạo thêm không gian học tập thân thiện cho học sinh.",
        "paragraphs": [
            "Chương trình hỗ trợ sách, kệ đọc và các hoạt động khuyến đọc cho học sinh tại khu vực ngoại thành.",
            "Hoạt động nằm trong chuỗi dự án phát triển bền vững và gắn kết cộng đồng địa phương.",
        ],
        "images": [
            "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=1400&q=80",
        ],
    },
}


def _news_entries():
    featured = dict(NEWS_EVENTS["featured"])
    featured["slug"] = "bo-nhiem-tan-tong-giam-doc-1000-cua-hang"
    featured["date"] = "28/02/2026"

    items = [
        {
            **NEWS_EVENTS["items"][0],
            "slug": "dong-phuc-moi-2025",
            "date": "24/02/2026",
        },
        {
            **NEWS_EVENTS["items"][1],
            "slug": "thu-vien-uoc-mo-ba-vi",
            "date": "25/02/2026",
        },
        {
            **NEWS_EVENTS["items"][2],
            "slug": "hop-tac-bat-dong-san-do-thi",
            "date": "26/02/2026",
        },
        {
            **NEWS_EVENTS["items"][3],
            "slug": "nuoc-sach-den-truong",
            "date": "27/02/2026",
        },
        {
            **NEWS_EVENTS["items"][4],
            "slug": "uu-dai-thang-moi",
            "date": "28/02/2026",
        },
        {
            **NEWS_EVENTS["items"][5],
            "slug": "mo-rong-khung-gio-cham-soc",
            "date": "01/03/2026",
        },
    ]
    return featured, items


def info_page(request, slug):
    page = INFO_PAGES.get(slug)
    if not page:
        return render(
            request,
            "store/info_page.html",
            status=404,
            context={
                "title": "Không tìm thấy nội dung",
                "kicker": "404",
                "summary": "Trang bạn yêu cầu không tồn tại hoặc đã được di chuyển.",
                "sections": [],
                "hero_image": "https://images.unsplash.com/photo-1585238342024-78d387f4a707?auto=format&fit=crop&w=1400&q=80",
                "is_not_found": True,
            },
        )

    media = PAGE_MEDIA.get(slug, {})
    section_images = media.get("section_images", [])

    sections = []
    for idx, section in enumerate(page.get("sections", [])):
        section_data = dict(section)
        if section_images:
            section_data["image"] = section_images[idx % len(section_images)]
        sections.append(section_data)

    context = dict(page)
    context["page_slug"] = slug
    context["sections"] = sections
    context["hero_image"] = media.get(
        "hero_image",
        "https://images.unsplash.com/photo-1521791136064-7986c2920216?auto=format&fit=crop&w=1400&q=80",
    )
    if slug == "tin-tuc-su-kien":
        featured_news, news_items = _news_entries()
        context["featured_news"] = featured_news
        context["news_items"] = news_items
    return render(request, "store/info_page.html", context=context)


def news_detail(request, slug):
    featured_news, news_items = _news_entries()
    all_news = [featured_news] + news_items
    article = next((n for n in all_news if n.get("slug") == slug), None)

    if not article:
        return render(
            request,
            "store/news_detail.html",
            status=404,
            context={
                "title": "Không tìm thấy bài viết",
                "article": None,
                "related_news": all_news[:6],
                "is_not_found": True,
            },
        )

    details = NEWS_DETAILS.get(slug, {})
    article_data = dict(article)
    article_data["lead"] = details.get("lead", article.get("excerpt", ""))
    article_data["paragraphs"] = details.get(
        "paragraphs",
        [
            article.get("excerpt", ""),
            "Nội dung bài viết đang được cập nhật chi tiết để phản ánh đầy đủ các hoạt động mới nhất.",
        ],
    )
    article_data["images"] = details.get("images", [article.get("image")])

    related_news = [n for n in all_news if n.get("slug") != slug][:8]
    return render(
        request,
        "store/news_detail.html",
        context={
            "title": article_data["title"],
            "article": article_data,
            "related_news": related_news,
            "page_slug": "tin-tuc-su-kien",
        },
    )


# CMS Section
import os

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.forms import modelform_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import (
    ChuoiCuaHang,
    CuaHang,
    KhuyenMai,
    NhaCungCap,
    NhanVien,
    NhomSanPham,
    SanPham,
    ThuongHieu,
)


MODEL_REGISTRY = {
    "thuong-hieu": ThuongHieu,
    "nha-cung-cap": NhaCungCap,
    "nhom-san-pham": NhomSanPham,
    "san-pham": SanPham,
    "chuoi-cua-hang": ChuoiCuaHang,
    "cua-hang": CuaHang,
    "nhan-vien": NhanVien,
    "khuyen-mai": KhuyenMai,
}

MODULE_LABELS = {
    "thuong-hieu": {"vi_singular": "Thương hiệu", "vi_plural": "Thương hiệu", "en_singular": "Brand", "en_plural": "Brands"},
    "nha-cung-cap": {"vi_singular": "Nhà cung cấp", "vi_plural": "Nhà cung cấp", "en_singular": "Supplier", "en_plural": "Suppliers"},
    "nhom-san-pham": {"vi_singular": "Nhóm sản phẩm", "vi_plural": "Nhóm sản phẩm", "en_singular": "Product Group", "en_plural": "Product Groups"},
    "san-pham": {"vi_singular": "Sản phẩm", "vi_plural": "Sản phẩm", "en_singular": "Product", "en_plural": "Products"},
    "chuoi-cua-hang": {"vi_singular": "Chuỗi cửa hàng", "vi_plural": "Chuỗi cửa hàng", "en_singular": "Store Chain", "en_plural": "Store Chains"},
    "cua-hang": {"vi_singular": "Cửa hàng", "vi_plural": "Cửa hàng", "en_singular": "Store", "en_plural": "Stores"},
    "nhan-vien": {"vi_singular": "Nhân viên", "vi_plural": "Nhân viên", "en_singular": "Employee", "en_plural": "Employees"},
    "khuyen-mai": {"vi_singular": "Khuyến mãi", "vi_plural": "Khuyến mãi", "en_singular": "Promotion", "en_plural": "Promotions"},
}

CMS_TRANSLATIONS = {
    "vi": {
        "system_settings": "Cài đặt hệ thống",
        "dashboard": "Tổng quan",
        "navigation": "Điều hướng",
        "data": "Dữ liệu",
        "logout": "Đăng xuất",
        "add_new": "Thêm mới",
        "save_changes": "Lưu thay đổi",
        "back_to_list": "Quay lại danh sách",
        "search_placeholder": "Tìm theo nội dung...",
        "actions": "Thao tác",
        "previous": "Trước",
        "next": "Sau",
        "first": "Đầu",
        "last": "Cuối",
        "page": "Trang",
        "no_data": "Chưa có dữ liệu.",
        "language": "Ngôn ngữ",
        "theme": "Giao diện",
        "light_theme": "Nền sáng",
        "dark_theme": "Nền tối",
        "vietnamese": "Tiếng Việt",
        "english": "Tiếng Anh",
        "save_settings": "Lưu cài đặt",
        "settings_saved": "Đã lưu cài đặt hệ thống.",
        "logged_in_as": "Đăng nhập bởi",
        "internal_cms": "CMS noi bo",
        "custom_internal_management": "Hệ thống quản trị nội bộ tự tạo",
        "manage": "Quản lý",
        "confirm_delete": "Xác nhận xóa",
        "you_are_deleting": "Bạn đang xóa một bản ghi của",
        "confirm_delete_btn": "Xác nhận xóa",
        "cancel": "Huy",
        "total_records": "Tổng bản ghi",
        "all_modules": "Tất cả module dữ liệu trong hệ thống",
        "total_modules": "Số module",
        "module_hint": "Bao gồm danh mục, cửa hàng, nhân viên, khuyến mãi...",
        "manage_module": "Quản lý",
        "edit": "Sửa",
        "delete": "Xóa",
        "create_prefix": "Thêm",
        "edit_prefix": "Sửa",
        "file_current": "Tệp hiện tại",
        "saved_successfully": "Lưu thành công.",
        "deleted_successfully": "Xóa thành công.",
        "no_access": "Tài khoản không có quyền truy cập CMS.",
        "store_front": "Cửa hàng",
        "notifications": "Thông báo",
        "login_title": "Đăng nhập CMS",
        "login_only_staff": "Chỉ tài khoản staff/superuser được phép truy cập.",
        "username": "Tài khoản",
        "password": "Mật khẩu",
        "login": "Đăng nhập",
        "cancel": "Hủy",
        "coord_pick_hint": "Tọa độ chỉ được lấy từ bản đồ.",
        "pick_on_map": "Chọn trên bản đồ",
        "coord_saved_from_map": "Đã nhận tọa độ từ bản đồ. Hãy bấm Lưu thay đổi để chốt.",
        "coord_required_from_map": "Cần chốt tọa độ bằng cách click trên bản đồ trước khi lưu.",
    },
    "en": {
        "system_settings": "System Settings",
        "dashboard": "Dashboard",
        "navigation": "Navigation",
        "data": "Data",
        "logout": "Log Out",
        "add_new": "Add New",
        "save_changes": "Save Changes",
        "back_to_list": "Back to List",
        "search_placeholder": "Search by content...",
        "actions": "Actions",
        "previous": "Previous",
        "next": "Next",
        "first": "First",
        "last": "Last",
        "page": "Page",
        "no_data": "No data yet.",
        "language": "Language",
        "theme": "Theme",
        "light_theme": "Light",
        "dark_theme": "Dark",
        "vietnamese": "Vietnamese",
        "english": "English",
        "save_settings": "Save Settings",
        "settings_saved": "System settings saved.",
        "logged_in_as": "Logged in as",
        "internal_cms": "Internal CMS",
        "custom_internal_management": "Custom internal management system",
        "manage": "Manage",
        "confirm_delete": "Confirm Deletion",
        "you_are_deleting": "You are deleting a record of",
        "confirm_delete_btn": "Confirm Delete",
        "cancel": "Cancel",
        "total_records": "Total Records",
        "all_modules": "All data modules in the system",
        "total_modules": "Total Modules",
        "module_hint": "Including categories, stores, employees, promotions...",
        "manage_module": "Manage",
        "edit": "Edit",
        "delete": "Delete",
        "create_prefix": "Create",
        "edit_prefix": "Edit",
        "file_current": "Current file",
        "store_front": "Storefront",
        "notifications": "Notifications",
        "coord_pick_hint": "Coordinates must be selected from the map.",
        "pick_on_map": "Pick on map",
        "coord_saved_from_map": "Coordinates received from map. Click Save Changes to confirm.",
        "coord_required_from_map": "Please pick coordinates on map before saving.",
    },
}

FIELD_LABELS = {
    "en": {
        "ten": "Name",
        "ghi_chu": "Notes",
        "mo_ta": "Description",
        "nhom_san_pham": "Category",
        "nha_cung_cap": "Supplier",
        "thuong_hieu": "Brand",
        "hinh_anh": "Product Image",
        "logo": "Logo",
        "chuoi": "Store Chain",
        "dia_chi": "Address",
        "quan_huyen": "District",
        "vi_do": "Latitude (lat)",
        "kinh_do": "Longitude (lng)",
        "mo_cua": "Open Time",
        "dong_cua": "Close Time",
        "hoat_dong_24h": "Open 24h",
        "san_pham": "Products",
        "cua_hang": "Store",
        "ho_ten": "Full Name",
        "chuc_vu": "Position",
        "so_dien_thoai": "Phone",
        "email": "Email",
        "avatar": "Avatar",
    }
}


def _is_admin_user(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def _require_admin_user(request):
    if _is_admin_user(request.user):
        return None
    return redirect("store:admin_login")


def _resolve_model(model_slug):
    model = MODEL_REGISTRY.get(model_slug)
    if model is None:
        raise Http404("Không tìm thấy model.")
    return model


def _admin_pref_context(request):
    lang = request.session.get("admin_lang", "vi")
    if lang not in CMS_TRANSLATIONS:
        lang = "vi"
    theme = request.session.get("admin_theme", "light")
    if theme not in {"light", "dark"}:
        theme = "light"
    return {
        "admin_lang": lang,
        "admin_theme": theme,
        "t": CMS_TRANSLATIONS[lang],
    }


def _model_label(model_slug, lang, plural=True):
    labels = MODULE_LABELS.get(model_slug, {})
    if lang == "en":
        return labels.get("en_plural" if plural else "en_singular", model_slug)
    return labels.get("vi_plural" if plural else "vi_singular", model_slug)


def _field_label(field, lang):
    if lang != "en":
        return field.verbose_name
    return FIELD_LABELS.get("en", {}).get(field.name, field.verbose_name)


def _menu_context(lang="vi"):
    menu = []
    for slug, model in MODEL_REGISTRY.items():
        menu.append(
            {
                "slug": slug,
                "name": _model_label(slug, lang, plural=True),
                "count": model.objects.count(),
            }
        )
    return menu


def _build_file_preview_context(model, obj=None):
    previews = {}
    image_exts = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".jfif"}
    for field in model._meta.fields:
        if field.get_internal_type() not in {"ImageField", "FileField"}:
            continue
        is_image_field = field.get_internal_type() == "ImageField"
        if obj is None:
            previews[field.name] = {"url": "", "is_image": is_image_field}
            continue
        value = getattr(obj, field.name, None)
        if value:
            is_image = is_image_field
            if not is_image:
                try:
                    ext = os.path.splitext(str(value.name))[1].lower()
                    is_image = ext in image_exts
                except Exception:
                    is_image = False
            try:
                previews[field.name] = {"url": value.url, "is_image": is_image}
            except Exception:
                previews[field.name] = {"url": "", "is_image": is_image}
        else:
            previews[field.name] = {"url": "", "is_image": is_image_field}
    return previews


def _sanitize_admin_form(form):
    # Remove Django's default "---------" empty option labels for select fields.
    for field in form.fields.values():
        if hasattr(field, "empty_label") and field.empty_label == "---------":
            field.empty_label = ""
        try:
            choices = list(getattr(field, "choices", []))
            if choices and choices[0][1] == "---------":
                choices[0] = (choices[0][0], "")
                field.choices = choices
        except Exception:
            pass
    return form


def _validate_coord_from_map(request, form, instance=None):
    if not form.is_valid():
        return False

    source = (request.POST.get("_coord_from_map") or "").strip()
    lat = form.cleaned_data.get("vi_do")
    lon = form.cleaned_data.get("kinh_do")

    changed = not bool(instance and instance.pk)
    if instance and instance.pk and lat is not None and lon is not None:
        try:
            old_lat = float(instance.vi_do)
            old_lon = float(instance.kinh_do)
            changed = abs(float(lat) - old_lat) > 1e-12 or abs(float(lon) - old_lon) > 1e-12
        except Exception:
            changed = True

    if changed and source != "map":
        pref = _admin_pref_context(request)
        msg = pref["t"]["coord_required_from_map"]
        form.add_error("vi_do", msg)
        form.add_error("kinh_do", msg)
        return False
    return True


class AdminLoginView(LoginView):
    template_name = "admin/login.html"
    authentication_form = AuthenticationForm
    redirect_authenticated_user = False

    def dispatch(self, request, *args, **kwargs):
        if _is_admin_user(request.user):
            return redirect("store:admin_dashboard")
        if request.user.is_authenticated:
            # Avoid redirect loop: authenticated but not CMS-authorized users
            # must be signed out before showing CMS login form.
            logout(request)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("store:admin_dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pref = _admin_pref_context(self.request)
        context.update(pref)
        return context

    def form_valid(self, form):
        if not _is_admin_user(form.get_user()):
            pref = _admin_pref_context(self.request)
            messages.error(self.request, pref["t"]["no_access"])
            return self.form_invalid(form)
        return super().form_valid(form)


def admin_logout(request):
    logout(request)
    return redirect("store:admin_login")


def admin_dashboard(request):
    unauthorized = _require_admin_user(request)
    if unauthorized:
        return unauthorized

    pref = _admin_pref_context(request)
    lang = pref["admin_lang"]
    modules = _menu_context(lang)
    return render(
        request,
        "admin/index.html",
        {
            "modules": modules,
            "total_records": sum(item["count"] for item in modules),
            **pref,
        },
    )


def admin_settings(request):
    unauthorized = _require_admin_user(request)
    if unauthorized:
        return unauthorized

    if request.method == "POST":
        lang = request.POST.get("language", "vi")
        theme = request.POST.get("theme", "light")
        if lang not in CMS_TRANSLATIONS:
            lang = "vi"
        if theme not in {"light", "dark"}:
            theme = "light"
        request.session["admin_lang"] = lang
        request.session["admin_theme"] = theme
        messages.success(request, CMS_TRANSLATIONS[lang]["settings_saved"])
        return redirect("store:admin_settings")

    pref = _admin_pref_context(request)
    return render(request, "admin/settings.html", {"modules": _menu_context(pref["admin_lang"]), **pref})


def admin_list(request, model_slug):
    unauthorized = _require_admin_user(request)
    if unauthorized:
        return unauthorized

    pref = _admin_pref_context(request)
    lang = pref["admin_lang"]

    model = _resolve_model(model_slug)
    query = request.GET.get("q", "").strip()
    qs = model.objects.all().order_by("-pk")
    if query:
        text_fields = [f.name for f in model._meta.fields if f.get_internal_type() in {"CharField", "TextField"}]
        if text_fields:
            from django.db.models import Q

            conditions = Q()
            for field_name in text_fields:
                conditions |= Q(**{f"{field_name}__icontains": query})
            qs = qs.filter(conditions)

    fields = [
        {"name": f.name, "verbose_name": _field_label(f, lang)}
        for f in model._meta.fields
        if f.name != "id"
    ]
    paginator = Paginator(qs, 15)
    page_obj = paginator.get_page(request.GET.get("page"))

    rows = []
    for item in page_obj.object_list:
        values = []
        for field in fields:
            raw_value = getattr(item, field["name"])
            field_obj = model._meta.get_field(field["name"])
            field_type = field_obj.get_internal_type()
            if field_type in {"ImageField", "FileField"}:
                if raw_value:
                    try:
                        values.append({"type": "image", "url": raw_value.url, "text": str(raw_value)})
                    except Exception:
                        values.append({"type": "text", "text": str(raw_value)})
                else:
                    values.append({"type": "text", "text": ""})
            elif field_type == "BooleanField":
                values.append({"type": "bool", "value": bool(raw_value)})
            else:
                values.append({"type": "text", "text": "" if raw_value is None else str(raw_value)})
        rows.append({"object": item, "values": values})

    return render(
        request,
        "admin/change_list.html",
        {
            "modules": _menu_context(lang),
            "model_slug": model_slug,
            "model_name": _model_label(model_slug, lang, plural=True),
            "fields": fields,
            "rows": rows,
            "query": query,
            "page_obj": page_obj,
            "paginator": paginator,
            **pref,
        },
    )


def admin_create(request, model_slug):
    unauthorized = _require_admin_user(request)
    if unauthorized:
        return unauthorized

    pref = _admin_pref_context(request)
    lang = pref["admin_lang"]

    model = _resolve_model(model_slug)
    form_cls = modelform_factory(model, fields="__all__")
    coord_picker_enabled = model_slug == "cua-hang"
    if request.method == "POST":
        form = _sanitize_admin_form(form_cls(request.POST, request.FILES))
        valid = _validate_coord_from_map(request, form) if coord_picker_enabled else form.is_valid()
        if valid:
            form.save()
            messages.success(request, pref["t"]["saved_successfully"])
            return redirect("store:admin_list", model_slug=model_slug)
    else:
        form = _sanitize_admin_form(form_cls())

    return render(
        request,
        "admin/change_form.html",
        {
            "modules": _menu_context(lang),
            "form": form,
            "model_slug": model_slug,
            "model_name": _model_label(model_slug, lang, plural=False),
            "mode": "create",
            "file_previews": _build_file_preview_context(model),
            "coord_picker_enabled": coord_picker_enabled,
            **pref,
        },
    )


def admin_update(request, model_slug, pk):
    unauthorized = _require_admin_user(request)
    if unauthorized:
        return unauthorized

    pref = _admin_pref_context(request)
    lang = pref["admin_lang"]

    model = _resolve_model(model_slug)
    obj = get_object_or_404(model, pk=pk)
    form_cls = modelform_factory(model, fields="__all__")
    coord_picker_enabled = model_slug == "cua-hang"

    if request.method == "POST":
        form = _sanitize_admin_form(form_cls(request.POST, request.FILES, instance=obj))
        valid = _validate_coord_from_map(request, form, instance=obj) if coord_picker_enabled else form.is_valid()
        if valid:
            form.save()
            messages.success(request, pref["t"]["saved_successfully"])
            return redirect("store:admin_list", model_slug=model_slug)
    else:
        form = _sanitize_admin_form(form_cls(instance=obj))

    return render(
        request,
        "admin/change_form.html",
        {
            "modules": _menu_context(lang),
            "form": form,
            "model_slug": model_slug,
            "model_name": _model_label(model_slug, lang, plural=False),
            "mode": "update",
            "object": obj,
            "file_previews": _build_file_preview_context(model, obj),
            "coord_picker_enabled": coord_picker_enabled,
            **pref,
        },
    )


def admin_delete(request, model_slug, pk):
    unauthorized = _require_admin_user(request)
    if unauthorized:
        return unauthorized

    pref = _admin_pref_context(request)
    lang = pref["admin_lang"]

    model = _resolve_model(model_slug)
    obj = get_object_or_404(model, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, pref["t"]["deleted_successfully"])
        return redirect("store:admin_list", model_slug=model_slug)

    return render(
        request,
        "admin/delete_confirmation.html",
        {
            "modules": _menu_context(lang),
            "model_slug": model_slug,
            "model_name": _model_label(model_slug, lang, plural=False),
            "object": obj,
            **pref,
        },
    )







