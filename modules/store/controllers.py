from django.shortcuts import render
from django.views.decorators.cache import never_cache

from modules.store.management.commands.restock_all_products import restock_products


def home(request):
    featured_products = list(
        SanPham.objects.prefetch_related("hinh_anh_phu").order_by("ten")[:8]
    )
    for product in featured_products:
        product.display_price = _format_currency(product.gia_ban)
        product.card_gallery = _build_product_card_gallery(product)
    return render(
        request,
        "store/home.html",
        {
            "featured_products": featured_products,
            "cart_total_quantity": _cart_items(request)[1],
            **_admin_pref_context(request),
        },
    )


def store_list_page(request):
    pref = _admin_pref_context(request)
    qs = CuaHang.objects.select_related("chuoi").order_by("ten")
    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "store/store_list.html",
        {
            "stores": page_obj.object_list,
            "page_obj": page_obj,
            "paginator": paginator,
            "cart_total_quantity": _cart_items(request)[1],
            **pref,
        },
    )


@never_cache
def map_page(request):
    return render(
        request,
        "store/map.html",
        {
            "cart_total_quantity": _cart_items(request)[1],
            **_admin_pref_context(request),
        },
    )


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
    pref = _admin_pref_context(request)
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
                **pref,
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
    context.update(pref)
    return render(request, "store/info_page.html", context=context)


def news_detail(request, slug):
    pref = _admin_pref_context(request)
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
                **pref,
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
            **pref,
        },
    )


# CMS Section
import json
import os
import re
import unicodedata
from urllib.parse import urlencode
from datetime import timedelta
from decimal import Decimal

from django.apps import apps
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm, UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.core.mail import send_mail, get_connection
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.core.serializers.json import DjangoJSONEncoder
from django import forms
from django.db import models as dj_models, transaction
from django.db.models import Q
from django.db.models.functions import Coalesce
from django.forms import modelform_factory
from django.forms.models import model_to_dict
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime
from django.views.decorators.http import require_POST

from .models import (
    ChiTietDonHang,
    DiaChiKhachHang,
    DonHang,
    GiaoDichKho,
    GopYKhachHang,
    HinhAnhSanPham,
    HoSoKhachHang,
    Notification,
    TrashRecord,
    ChuoiCuaHang,
    CuaHang,
    KhuyenMai,
    NhaCungCap,
    NhanVien,
    NhomSanPham,
    SanPham,
    TonKhoCuaHang,
    ThuongHieu,
    XacNhanThanhToan,
)


MODEL_REGISTRY = {
    "thuong-hieu": ThuongHieu,
    "nha-cung-cap": NhaCungCap,
    "nhom-san-pham": NhomSanPham,
    "san-pham": SanPham,
    "giao-dich-kho": GiaoDichKho,
    "ton-kho-cua-hang": TonKhoCuaHang,
    "chuoi-cua-hang": ChuoiCuaHang,
    "cua-hang": CuaHang,
    "nhan-vien": NhanVien,
    "khuyen-mai": KhuyenMai,
    "gop-y-khach-hang": GopYKhachHang,
    "ho-so-khach-hang": HoSoKhachHang,
    "dia-chi-khach-hang": DiaChiKhachHang,
    "don-hang": DonHang,
    "chi-tiet-don-hang": ChiTietDonHang,
}

User = get_user_model()
ROLE_SYSTEM_ADMIN = "SystemAdmin"
ROLE_STOCK_MANAGER = "StockManager"
ROLE_ORDER_MANAGER = "OrderManager"
ROLE_CUSTOMER_SUPPORT = "CustomerSupport"
ROLE_CUSTOMER = "Customer"
ROLE_ADMIN = ROLE_SYSTEM_ADMIN
ROLE_USER = ROLE_CUSTOMER
ROLE_CHOICES = (
    (ROLE_SYSTEM_ADMIN, "Quản trị hệ thống"),
    (ROLE_STOCK_MANAGER, "Quản lý kho"),
    (ROLE_ORDER_MANAGER, "Quản lý đơn hàng"),
    (ROLE_CUSTOMER_SUPPORT, "Nhân viên CSKH"),
    (ROLE_CUSTOMER, "Khách hàng"),
)
ROLE_LABELS = dict(ROLE_CHOICES)
INTERNAL_ROLES = {
    ROLE_SYSTEM_ADMIN,
    ROLE_STOCK_MANAGER,
    ROLE_ORDER_MANAGER,
    ROLE_CUSTOMER_SUPPORT,
}
LEGACY_ROLE_MAP = {
    "Admin": ROLE_SYSTEM_ADMIN,
    "User": ROLE_CUSTOMER,
}
MODULE_ROLE_ACTIONS = {
    "thuong-hieu": {
        "view": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER, ROLE_ORDER_MANAGER},
        "create": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER},
        "update": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER},
        "delete": {ROLE_SYSTEM_ADMIN},
    },
    "nha-cung-cap": {
        "view": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER},
        "create": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER},
        "update": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER},
        "delete": {ROLE_SYSTEM_ADMIN},
    },
    "nhom-san-pham": {
        "view": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER, ROLE_ORDER_MANAGER},
        "create": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER},
        "update": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER},
        "delete": {ROLE_SYSTEM_ADMIN},
    },
    "san-pham": {
        "view": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER, ROLE_ORDER_MANAGER, ROLE_CUSTOMER_SUPPORT},
        "create": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER},
        "update": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER},
        "delete": {ROLE_SYSTEM_ADMIN},
    },
    "giao-dich-kho": {
        "view": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER},
        "create": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER},
        "update": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER},
        "delete": {ROLE_SYSTEM_ADMIN},
        "print": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER},
    },
    "ton-kho-cua-hang": {
        "view": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER, ROLE_ORDER_MANAGER},
        "create": {ROLE_SYSTEM_ADMIN},
        "update": {ROLE_SYSTEM_ADMIN},
        "delete": {ROLE_SYSTEM_ADMIN},
    },
    "hinh-anh-san-pham": {
        "view": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER},
        "create": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER},
        "update": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER},
        "delete": {ROLE_SYSTEM_ADMIN},
    },
    "chuoi-cua-hang": {
        "view": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER},
        "create": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER},
        "update": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER},
        "delete": {ROLE_SYSTEM_ADMIN},
    },
    "cua-hang": {
        "view": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER, ROLE_ORDER_MANAGER},
        "create": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER},
        "update": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER},
        "delete": {ROLE_SYSTEM_ADMIN},
    },
    "nhan-vien": {
        "view": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER, ROLE_CUSTOMER_SUPPORT},
        "create": {ROLE_SYSTEM_ADMIN},
        "update": {ROLE_SYSTEM_ADMIN},
        "delete": {ROLE_SYSTEM_ADMIN},
    },
    "khuyen-mai": {
        "view": {ROLE_SYSTEM_ADMIN, ROLE_ORDER_MANAGER},
        "create": {ROLE_SYSTEM_ADMIN, ROLE_ORDER_MANAGER},
        "update": {ROLE_SYSTEM_ADMIN, ROLE_ORDER_MANAGER},
        "delete": {ROLE_SYSTEM_ADMIN},
    },
    "gop-y-khach-hang": {
        "view": {ROLE_SYSTEM_ADMIN, ROLE_CUSTOMER_SUPPORT},
        "create": {ROLE_SYSTEM_ADMIN, ROLE_CUSTOMER_SUPPORT},
        "update": {ROLE_SYSTEM_ADMIN, ROLE_CUSTOMER_SUPPORT},
        "delete": {ROLE_SYSTEM_ADMIN},
    },
    "ho-so-khach-hang": {
        "view": {ROLE_SYSTEM_ADMIN, ROLE_CUSTOMER_SUPPORT},
        "create": {ROLE_SYSTEM_ADMIN, ROLE_CUSTOMER_SUPPORT},
        "update": {ROLE_SYSTEM_ADMIN, ROLE_CUSTOMER_SUPPORT},
        "delete": {ROLE_SYSTEM_ADMIN},
    },
    "dia-chi-khach-hang": {
        "view": {ROLE_SYSTEM_ADMIN, ROLE_CUSTOMER_SUPPORT},
        "create": {ROLE_SYSTEM_ADMIN, ROLE_CUSTOMER_SUPPORT},
        "update": {ROLE_SYSTEM_ADMIN, ROLE_CUSTOMER_SUPPORT},
        "delete": {ROLE_SYSTEM_ADMIN},
    },
    "don-hang": {
        "view": {ROLE_SYSTEM_ADMIN, ROLE_ORDER_MANAGER, ROLE_CUSTOMER_SUPPORT},
        "create": {ROLE_SYSTEM_ADMIN},
        "update": {ROLE_SYSTEM_ADMIN, ROLE_ORDER_MANAGER, ROLE_CUSTOMER_SUPPORT},
        "delete": {ROLE_SYSTEM_ADMIN},
        "status": {ROLE_SYSTEM_ADMIN, ROLE_ORDER_MANAGER, ROLE_CUSTOMER_SUPPORT},
        "payment_status": {ROLE_SYSTEM_ADMIN, ROLE_ORDER_MANAGER},
    },
    "chi-tiet-don-hang": {
        "view": {ROLE_SYSTEM_ADMIN, ROLE_ORDER_MANAGER, ROLE_CUSTOMER_SUPPORT},
        "create": {ROLE_SYSTEM_ADMIN},
        "update": {ROLE_SYSTEM_ADMIN},
        "delete": {ROLE_SYSTEM_ADMIN},
    },
}
ADMIN_PAGE_ROLE_ACTIONS = {
    "dashboard": {"view": INTERNAL_ROLES},
    "inventory_hub": {"view": {ROLE_SYSTEM_ADMIN, ROLE_STOCK_MANAGER}},
    "settings": {"view": {ROLE_SYSTEM_ADMIN}},
    "user_management": {"view": {ROLE_SYSTEM_ADMIN}},
    "trash": {"view": {ROLE_SYSTEM_ADMIN}, "restore": {ROLE_SYSTEM_ADMIN}, "delete": {ROLE_SYSTEM_ADMIN}},
    "notifications": {"view": INTERNAL_ROLES},
}


def _default_payment_status_for_method(method: str) -> str:
    if method == "bank_transfer":
        return "awaiting_confirmation"
    return "unpaid"


def _momo_demo_context(order):
    qr_svg = ""
    qr_payload = f"MOMO-DEMO|ORDER:{order.pk}|AMOUNT:{int(order.tong_tien or 0)}"
    try:
        from reportlab.graphics import renderSVG
        from reportlab.graphics.barcode.qr import QrCodeWidget
        from reportlab.graphics.shapes import Drawing

        qr_widget = QrCodeWidget(qr_payload)
        bounds = qr_widget.getBounds()
        qr_width = bounds[2] - bounds[0]
        qr_height = bounds[3] - bounds[1]
        qr_drawing = Drawing(180, 180, transform=[180 / qr_width, 0, 0, 180 / qr_height, 0, 0])
        qr_drawing.add(qr_widget)
        qr_svg = renderSVG.drawToString(qr_drawing)
        if isinstance(qr_svg, bytes):
            qr_svg = qr_svg.decode("utf-8")
    except Exception:
        qr_svg = ""
    return {
        "order": order,
        "order_amount_display": _format_currency(order.tong_tien),
        "momo_demo_code": f"MOMO-DEMO-{order.pk}",
        "momo_demo_qr_svg": qr_svg,
        "momo_demo_qr_payload": qr_payload,
    }

MODULE_LABELS = {
    "thuong-hieu": {"vi_singular": "Thương hiệu", "vi_plural": "Thương hiệu", "en_singular": "Brand", "en_plural": "Brands"},
    "nha-cung-cap": {"vi_singular": "Nhà cung cấp", "vi_plural": "Nhà cung cấp", "en_singular": "Supplier", "en_plural": "Suppliers"},
    "nhom-san-pham": {"vi_singular": "Nhóm sản phẩm", "vi_plural": "Nhóm sản phẩm", "en_singular": "Product Group", "en_plural": "Product Groups"},
    "san-pham": {"vi_singular": "Sản phẩm", "vi_plural": "Sản phẩm", "en_singular": "Product", "en_plural": "Products"},
    "giao-dich-kho": {"vi_singular": "Giao dịch kho", "vi_plural": "Giao dịch kho", "en_singular": "Stock Movement", "en_plural": "Stock Movements"},
    "ton-kho-cua-hang": {"vi_singular": "Tồn kho cửa hàng", "vi_plural": "Tồn kho cửa hàng", "en_singular": "Store Stock", "en_plural": "Store Stocks"},
    "hinh-anh-san-pham": {"vi_singular": "Hình ảnh sản phẩm", "vi_plural": "Hình ảnh sản phẩm", "en_singular": "Product Image", "en_plural": "Product Images"},
    "chuoi-cua-hang": {"vi_singular": "Chuỗi cửa hàng", "vi_plural": "Chuỗi cửa hàng", "en_singular": "Store Chain", "en_plural": "Store Chains"},
    "cua-hang": {"vi_singular": "Cửa hàng", "vi_plural": "Cửa hàng", "en_singular": "Store", "en_plural": "Stores"},
    "nhan-vien": {"vi_singular": "Nhân viên", "vi_plural": "Nhân viên", "en_singular": "Employee", "en_plural": "Employees"},
    "khuyen-mai": {"vi_singular": "Khuyến mãi", "vi_plural": "Khuyến mãi", "en_singular": "Promotion", "en_plural": "Promotions"},
    "gop-y-khach-hang": {"vi_singular": "Góp ý khách hàng", "vi_plural": "Góp ý khách hàng", "en_singular": "Customer Feedback", "en_plural": "Customer Feedback"},
    "ho-so-khach-hang": {"vi_singular": "Hồ sơ khách hàng", "vi_plural": "Hồ sơ khách hàng", "en_singular": "Customer Profile", "en_plural": "Customer Profiles"},
    "dia-chi-khach-hang": {"vi_singular": "Địa chỉ khách hàng", "vi_plural": "Địa chỉ khách hàng", "en_singular": "Customer Address", "en_plural": "Customer Addresses"},
    "don-hang": {"vi_singular": "Đơn hàng", "vi_plural": "Đơn hàng", "en_singular": "Order", "en_plural": "Orders"},
    "chi-tiet-don-hang": {"vi_singular": "Chi tiết đơn hàng", "vi_plural": "Chi tiết đơn hàng", "en_singular": "Order Item", "en_plural": "Order Items"},
}

CMS_TRANSLATIONS = {
    "vi": {
        "system_settings": "Cài đặt hệ thống",
        "dashboard": "Tổng quan",
        "inventory_hub": "Kho",
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
        "internal_cms": "Hệ thống nội bộ",
        "custom_internal_management": "Hệ thống quản trị nội bộ tự tạo",
        "manage": "Quản lý",
        "confirm_delete": "Xác nhận xóa",
        "you_are_deleting": "Bạn đang xóa một bản ghi của",
        "confirm_delete_btn": "Xác nhận xóa",
        "cancel": "Hủy",
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
        "no_access": "Tài khoản không có quyền truy cập trang quản trị.",
        "store_front": "Cửa hàng",
        "notifications": "Thông báo",
        "user_management": "Quản lý người dùng",
        "role": "Vai trò",
        "admin_role": "Admin",
        "user_role": "User",
        "account_status": "Trạng thái",
        "active": "Hoạt động",
        "inactive": "Ngưng",
        "create_user": "Tạo người dùng",
        "full_name": "Họ tên",
        "update_role": "Cập nhật quyền",
        "user_area": "Trang người dùng",
        "user_portal": "Khu vực người dùng",
        "welcome_user": "Xin chào",
        "user_intro": "Trang dành cho tài khoản người dùng đã đăng nhập.",
        "access_admin": "Vào trang quản trị",
        "user_login_title": "Đăng nhập tài khoản của bạn",
        "user_login_hint": "",
        "user_created": "Đã tạo tài khoản mới.",
        "user_updated": "Đã cập nhật quyền người dùng.",
        "register": "Đăng ký",
        "products_page": "Sản phẩm",
        "cart": "Giỏ hàng",
        "checkout": "Thanh toán",
        "my_orders": "Đơn hàng của tôi",
        "buy_now": "Mua ngay",
        "add_to_cart": "Thêm vào giỏ",
        "cart_empty": "Giỏ hàng đang trống.",
        "continue_shopping": "Tiếp tục mua sắm",
        "place_order": "Đặt hàng",
        "receiver_name": "Người nhận",
        "delivery_address": "Địa chỉ giao hàng",
        "quantity": "Số lượng",
        "order_success": "Đã tạo đơn hàng thành công.",
        "login_to_buy": "Bạn cần đăng nhập tài khoản khách hàng để mua sản phẩm.",
        "product_added": "Đã thêm sản phẩm vào giỏ hàng.",
        "cart_updated": "Đã cập nhật giỏ hàng.",
        "order_status": "Trạng thái đơn",
        "order_code": "Mã đơn",
        "order_time": "Thời gian đặt",
        "product_catalog_intro": "Khách có thể xem hàng tự do, nhưng cần tài khoản để thêm giỏ và đặt mua.",
        "customer_profile": "Hồ sơ khách hàng",
        "update_profile": "Cập nhật hồ sơ",
        "profile_saved": "Đã lưu hồ sơ khách hàng.",
        "all_statuses": "Tất cả trạng thái",
        "confirm_order": "Xác nhận đơn",
        "ship_order": "Bắt đầu giao",
        "deliver_order": "Đã giao",
        "complete_order": "Hoàn tất đơn",
        "cancel_order": "Hủy đơn",
        "order_status_updated": "Đã cập nhật trạng thái đơn hàng.",
        "trash": "Thùng rác",
        "restore": "Khôi phục",
        "delete_permanently": "Xóa hẳn",
        "deleted_at": "Thời gian xóa",
        "expires_at": "Tự xóa sau",
        "trash_empty": "Thùng rác đang trống.",
        "unit_price": "Đơn giá",
        "line_total": "Thành tiền",
        "total_amount": "Tổng tiền",
        "featured_products": "Sản phẩm nổi bật",
        "password_strength": "Độ mạnh mật khẩu",
        "password_weak": "Yếu",
        "password_medium": "Trung bình",
        "password_strong": "Mạnh",
        "password_hint": "Nên có ít nhất 8 ký tự, gồm chữ hoa, chữ thường, số và ký tự đặc biệt.",
        "password_too_weak": "Mật khẩu đang quá yếu. Hãy dùng ít nhất 8 ký tự, có chữ hoa, chữ thường, số và ký tự đặc biệt.",
        "change_password": "Đổi mật khẩu",
        "reset_password": "Đặt lại mật khẩu",
        "password_updated": "Đã cập nhật mật khẩu.",
        "current_password": "Mật khẩu hiện tại",
        "new_password": "Mật khẩu mới",
        "confirm_password": "Xác nhận mật khẩu",
        "notification_title": "Thông báo hệ thống",
        "notification_empty": "Chưa có thông báo.",
        "support_request": "Yêu cầu hỗ trợ",
        "retry_request": "Yêu cầu thử lại",
        "login_title": "Đăng nhập quản trị",
        "login_only_staff": "Chỉ tài khoản Admin mới được phép truy cập.",
        "username": "Tài khoản",
        "password": "Mật khẩu",
        "login": "Đăng nhập",
        "cancel": "Hủy",
        "coord_pick_hint": "Tọa độ chỉ được lấy từ bản đồ.",
        "pick_on_map": "Chọn trên bản đồ",
        "coord_saved_from_map": "Đã nhận tọa độ từ bản đồ. Hãy bấm Lưu thay đổi để chốt.",
        "coord_required_from_map": "Cần chốt tọa độ bằng cách click trên bản đồ trước khi lưu.",
        "inventory_overview": "Tổng quan kho",
        "stock_summary": "Tóm tắt tồn kho",
        "suggest_import": "Đề xuất nhập thêm",
        "suggest_export": "Đề xuất ưu tiên xuất",
        "view_all_products": "Xem toàn bộ sản phẩm",
        "view_stock_movements": "Xem giao dịch kho",
    },
    "en": {
        "system_settings": "System Settings",
        "dashboard": "Dashboard",
        "inventory_hub": "Inventory",
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
        "internal_cms": "Internal System",
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
        "user_management": "User Management",
        "role": "Role",
        "admin_role": "Admin",
        "user_role": "User",
        "account_status": "Status",
        "active": "Active",
        "inactive": "Inactive",
        "create_user": "Create User",
        "full_name": "Full Name",
        "update_role": "Update Role",
        "user_area": "User Area",
        "user_portal": "User Portal",
        "welcome_user": "Welcome",
        "user_intro": "This page is for authenticated user accounts.",
        "access_admin": "Open Admin",
        "user_login_title": "User Login",
        "user_login_hint": "Regular users enter the user area. Admin accounts are redirected to the admin panel.",
        "user_created": "New user created.",
        "user_updated": "User role updated.",
        "register": "Register",
        "products_page": "Products",
        "cart": "Cart",
        "checkout": "Checkout",
        "my_orders": "My Orders",
        "buy_now": "Buy Now",
        "add_to_cart": "Add to Cart",
        "cart_empty": "Your cart is empty.",
        "continue_shopping": "Continue Shopping",
        "place_order": "Place Order",
        "receiver_name": "Receiver",
        "delivery_address": "Delivery Address",
        "quantity": "Quantity",
        "order_success": "Order created successfully.",
        "login_to_buy": "Please sign in with a customer account before purchasing.",
        "product_added": "Product added to cart.",
        "cart_updated": "Cart updated.",
        "order_status": "Order Status",
        "order_code": "Order Code",
        "order_time": "Order Time",
        "product_catalog_intro": "Visitors can browse products freely, but must sign in to add to cart and checkout.",
        "customer_profile": "Customer Profile",
        "update_profile": "Update Profile",
        "profile_saved": "Customer profile saved.",
        "all_statuses": "All Statuses",
        "confirm_order": "Confirm Order",
        "ship_order": "Start Delivery",
        "deliver_order": "Delivered",
        "complete_order": "Complete Order",
        "cancel_order": "Cancel Order",
        "order_status_updated": "Order status updated.",
        "trash": "Trash",
        "restore": "Restore",
        "delete_permanently": "Delete permanently",
        "deleted_at": "Deleted at",
        "expires_at": "Expires at",
        "trash_empty": "Trash is empty.",
        "unit_price": "Unit Price",
        "line_total": "Line Total",
        "total_amount": "Total Amount",
        "featured_products": "Featured Products",
        "password_strength": "Password Strength",
        "password_weak": "Weak",
        "password_medium": "Medium",
        "password_strong": "Strong",
        "password_hint": "Use at least 8 characters with uppercase, lowercase, numbers, and special characters.",
        "password_too_weak": "Password is too weak. Use at least 8 characters with uppercase, lowercase, numbers, and special characters.",
        "change_password": "Change Password",
        "reset_password": "Reset Password",
        "password_updated": "Password updated.",
        "current_password": "Current Password",
        "new_password": "New Password",
        "confirm_password": "Confirm Password",
        "notification_title": "System Notifications",
        "notification_empty": "No notifications yet.",
        "support_request": "Support Request",
        "retry_request": "Retry Request",
        "coord_pick_hint": "Coordinates must be selected from the map.",
        "pick_on_map": "Pick on map",
        "coord_saved_from_map": "Coordinates received from map. Click Save Changes to confirm.",
        "coord_required_from_map": "Please pick coordinates on map before saving.",
        "inventory_overview": "Inventory Overview",
        "stock_summary": "Stock Summary",
        "suggest_import": "Suggested Restock",
        "suggest_export": "Suggested Sell-Through",
        "view_all_products": "View all products",
        "view_stock_movements": "View stock movements",
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
        "gia_ban": "Price",
        "ton_kho": "Stock",
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
        "chu_thich": "Caption",
        "thu_tu": "Display Order",
        "cua_hang": "Store",
        "ho_ten": "Full Name",
        "chuc_vu": "Position",
        "so_dien_thoai": "Phone",
        "email": "Email",
        "avatar": "Avatar",
        "chu_de": "Subject",
        "noi_dung": "Feedback Content",
        "da_phan_hoi": "Responded",
        "user": "User",
        "tinh_thanh": "Province / City",
        "quan_huyen": "District",
        "phuong_xa": "Ward / Commune",
        "dia_chi_cu_the": "Street Address",
        "loai_dia_chi": "Address Type",
        "mac_dinh": "Default Address",
        "khach_hang": "Customer",
        "ho_ten_nguoi_nhan": "Receiver",
        "dia_chi_giao_hang": "Delivery Address",
        "ghi_chu": "Note",
        "trang_thai": "Status",
        "tong_so_luong": "Total Quantity",
        "tong_tien": "Total Amount",
        "giam_gia": "Discount",
        "khuyen_mai": "Voucher",
        "ma_voucher_ap_dung": "Voucher Code Applied",
        "vi_do_giao_hang": "Delivery Latitude",
        "kinh_do_giao_hang": "Delivery Longitude",
        "ma_code": "Voucher Code",
        "loai_giam": "Discount Type",
        "gia_tri_giam": "Discount Value",
        "gia_tri_don_hang_toi_thieu": "Minimum Order",
        "giam_toi_da": "Maximum Discount",
        "dang_ap_dung": "Active",
        "ngay_bat_dau": "Start At",
        "ngay_ket_thuc": "End At",
        "don_hang": "Order",
        "so_luong": "Quantity",
        "don_gia": "Unit Price",
        "created_at": "Created At",
    }
}


class MultipleImageInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.FileField):
    widget = MultipleImageInput

    def clean(self, data, initial=None):
        single_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_clean(item, initial) for item in data]
        if not data:
            return []
        return [single_clean(data, initial)]


class SanPhamAdminForm(forms.ModelForm):
    product_images = MultipleImageField(
        label="Ảnh sản phẩm",
        required=False,
        widget=MultipleImageInput(attrs={"multiple": True, "accept": "image/*"}),
        help_text="Chọn một hoặc nhiều ảnh. Ảnh đầu tiên sẽ làm ảnh chính, các ảnh còn lại tự thêm vào gallery.",
    )

    class Meta:
        model = SanPham
        exclude = ("hinh_anh", "ton_kho")


class GiaoDichKhoAdminForm(forms.ModelForm):
    class Meta:
        model = GiaoDichKho
        exclude = ("ton_truoc", "ton_sau", "created_by")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        store_field = self.fields.get("cua_hang")
        if store_field is not None:
            store_field.help_text = "Bắt buộc với phiếu xuất kho. Phiếu nhập sẽ tự lấy theo cửa hàng của nhân viên ký nếu để trống."
        nhan_vien_field = self.fields.get("nhan_vien")
        if nhan_vien_field is not None:
            nhan_vien_field.help_text = "Bắt buộc với phiếu nhập kho."
        chu_ky_field = self.fields.get("chu_ky")
        if chu_ky_field is not None:
            chu_ky_field.help_text = "Tải ảnh chữ ký của nhân viên khi nhập kho."


class KhuyenMaiAdminForm(forms.ModelForm):
    class Meta:
        model = KhuyenMai
        fields = "__all__"
        widgets = {
            "ma_code": forms.TextInput(
                attrs={
                    "placeholder": "Ví dụ: GIAM10 hoặc FREESHIP50",
                    "style": "text-transform:uppercase;",
                }
            ),
            "ten": forms.TextInput(attrs={"placeholder": "Ví dụ: Giảm 10% cho đơn online"}),
            "mo_ta": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Giải thích ngắn: áp dụng cho đơn online, giới hạn theo thương hiệu hoặc thời gian...",
                }
            ),
            "gia_tri_giam": forms.NumberInput(attrs={"placeholder": "Ví dụ: 10 hoặc 50000", "min": "0"}),
            "gia_tri_don_hang_toi_thieu": forms.NumberInput(attrs={"placeholder": "Ví dụ: 100000", "min": "0"}),
            "giam_toi_da": forms.NumberInput(attrs={"placeholder": "Để trống nếu không giới hạn", "min": "0"}),
            "ngay_bat_dau": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "ngay_ket_thuc": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ma_code"].help_text = "Mã khách hàng nhập ở checkout. Nên dùng chữ in hoa, không dấu, không khoảng trắng."
        self.fields["loai_giam"].help_text = "Chọn 'Giảm theo phần trăm' nếu muốn nhập 10, 15, 20...; chọn 'Giảm số tiền' nếu muốn nhập trực tiếp số tiền."
        self.fields["gia_tri_giam"].help_text = "Nếu giảm theo phần trăm: nhập từ 1 đến 100. Nếu giảm số tiền: nhập số tiền giảm theo VND."
        self.fields["gia_tri_don_hang_toi_thieu"].help_text = "Chỉ cho phép áp dụng voucher khi đơn hàng đạt ít nhất số tiền này."
        self.fields["giam_toi_da"].help_text = "Chỉ dùng khi giảm theo phần trăm để giới hạn số tiền giảm tối đa."
        self.fields["dang_ap_dung"].help_text = "Bỏ chọn nếu muốn tạm khóa voucher mà không cần xóa."
        self.fields["ngay_bat_dau"].help_text = "Để trống nếu voucher có hiệu lực ngay."
        self.fields["ngay_ket_thuc"].help_text = "Để trống nếu voucher không có ngày hết hạn."
        self.fields["thuong_hieu"].help_text = "Nếu chọn thương hiệu, voucher chỉ áp dụng cho các sản phẩm thuộc thương hiệu đó."
        self.fields["cua_hang"].help_text = "Nếu chọn cửa hàng, voucher hiện được xem là ưu đãi mua tại cửa hàng và sẽ không áp dụng cho checkout online."

    def clean_ma_code(self):
        code = _normalize_voucher_code(self.cleaned_data.get("ma_code"))
        if not code:
            raise forms.ValidationError("Vui lòng nhập mã voucher.")
        qs = KhuyenMai.objects.filter(ma_code__iexact=code)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Mã voucher này đã tồn tại. Vui lòng dùng mã khác.")
        return code

    def clean(self):
        cleaned_data = super().clean()
        discount_type = cleaned_data.get("loai_giam")
        discount_value = cleaned_data.get("gia_tri_giam") or Decimal("0")
        max_discount = cleaned_data.get("giam_toi_da")
        start_at = cleaned_data.get("ngay_bat_dau")
        end_at = cleaned_data.get("ngay_ket_thuc")

        if discount_value <= 0:
            self.add_error("gia_tri_giam", "Giá trị giảm phải lớn hơn 0.")
        if discount_type == "percent" and discount_value > 100:
            self.add_error("gia_tri_giam", "Voucher phần trăm chỉ được nhập tối đa 100.")
        if discount_type == "fixed" and max_discount:
            self.add_error("giam_toi_da", "Giảm tối đa chỉ nên dùng cho voucher phần trăm.")
        if start_at and end_at and end_at <= start_at:
            self.add_error("ngay_ket_thuc", "Ngày kết thúc phải sau ngày bắt đầu.")
        return cleaned_data


def _is_admin_user(user):
    if not user.is_authenticated:
        return False
    return _ensure_user_role(user) in INTERNAL_ROLES


def _is_regular_user(user):
    return user.is_authenticated and not _is_admin_user(user)


def _require_regular_user(request):
    if _is_regular_user(request.user):
        return None
    if _is_admin_user(request.user):
        return redirect("store:admin_dashboard")
    return redirect("store:user_login")


def _require_customer_account(request):
    if _is_regular_user(request.user):
        return None
    next_url = request.POST.get("next") or request.get_full_path() or reverse("store:product_catalog")
    if _is_admin_user(request.user):
        logout(request)
    login_url = reverse("store:user_login")
    if next_url:
        login_url = f"{login_url}?next={next_url}"
    return redirect(login_url)


def _cart_session(request):
    return request.session.setdefault("cart", {})


def _remember_post_login_cart_action(request, product_id, next_url):
    request.session["post_login_cart_action"] = {
        "product_id": int(product_id),
        "next": next_url or reverse("store:cart"),
    }
    request.session.modified = True


def _resume_post_login_cart_action(request):
    payload = request.session.pop("post_login_cart_action", None)
    if not payload:
        return None

    product_id = payload.get("product_id")
    if product_id:
        cart = _cart_session(request)
        key = str(product_id)
        cart[key] = int(cart.get(key, 0)) + 1
        request.session.modified = True
    return payload.get("next") or reverse("store:cart")


def _format_currency(value):
    try:
        amount = int(Decimal(value))
    except Exception:
        amount = 0
    return f"{amount:,}".replace(",", ".") + " đ"


def _parse_coordinate(raw_value):
    text = (raw_value or "").strip()
    if not text:
        return None
    try:
        value = float(text)
    except (TypeError, ValueError):
        raise ValidationError("Tọa độ giao hàng không hợp lệ.")
    return value


def _parse_latitude(raw_value):
    value = _parse_coordinate(raw_value)
    if value is None:
        return None
    if value < -90 or value > 90:
        raise ValidationError("Vĩ độ giao hàng phải nằm trong khoảng từ -90 đến 90.")
    return value


def _parse_longitude(raw_value):
    value = _parse_coordinate(raw_value)
    if value is None:
        return None
    if value < -180 or value > 180:
        raise ValidationError("Kinh độ giao hàng phải nằm trong khoảng từ -180 đến 180.")
    return value


def _normalize_voucher_code(value):
    return re.sub(r"\s+", "", (value or "").upper())


def _line_total_for_item(item):
    line_total = item.get("line_total")
    if line_total is not None:
        return Decimal(line_total)
    return (item.get("unit_price") or Decimal("0")) * (item.get("quantity") or 0)


VOUCHER_PRODUCT_RULES = {
    "COMBO5K": {"all_keywords": ["mi tron", "pepsi"]},
    "FROSTER33": {"any_keywords": ["froster"]},
    "YOUUS50": {"any_keywords": ["youus"]},
    "TOK10": {"any_keywords": ["tokbokki"]},
}


def _normalize_matching_text(value):
    value = unicodedata.normalize("NFKD", str(value or ""))
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = re.sub(r"\s+", " ", value).strip().lower()
    return value


def _filter_voucher_eligible_items(voucher, items):
    eligible_items = list(items)

    allowed_brand_ids = list(voucher.thuong_hieu.values_list("pk", flat=True))
    if allowed_brand_ids:
        eligible_items = [
            item for item in eligible_items if item["product"].thuong_hieu_id in allowed_brand_ids
        ]

    rule = VOUCHER_PRODUCT_RULES.get(_normalize_voucher_code(voucher.ma_code))
    if not rule:
        return eligible_items

    normalized_items = [
        (item, _normalize_matching_text(getattr(item["product"], "ten", "")))
        for item in eligible_items
    ]

    any_keywords = [_normalize_matching_text(keyword) for keyword in rule.get("any_keywords", [])]
    if any_keywords:
        normalized_items = [
            (item, normalized_name)
            for item, normalized_name in normalized_items
            if any(keyword in normalized_name for keyword in any_keywords)
        ]

    all_keywords = [_normalize_matching_text(keyword) for keyword in rule.get("all_keywords", [])]
    if all_keywords:
        matched_keywords = {
            keyword
            for _, normalized_name in normalized_items
            for keyword in all_keywords
            if keyword in normalized_name
        }
        if not all(keyword in matched_keywords for keyword in all_keywords):
            return []
        normalized_items = [
            (item, normalized_name)
            for item, normalized_name in normalized_items
            if any(keyword in normalized_name for keyword in all_keywords)
        ]

    return [item for item, _ in normalized_items]


def _resolve_checkout_voucher(raw_code, items, subtotal_amount):
    code = _normalize_voucher_code(raw_code)
    if not code:
        return None, Decimal("0")

    voucher = (
        KhuyenMai.objects.prefetch_related("thuong_hieu", "cua_hang")
        .filter(ma_code__iexact=code)
        .order_by("-id")
        .first()
    )
    if voucher is None:
        raise ValidationError("Mã voucher không tồn tại.")
    if not voucher.dang_ap_dung:
        raise ValidationError("Voucher này hiện không còn áp dụng.")

    now = timezone.now()
    if voucher.ngay_bat_dau and voucher.ngay_bat_dau > now:
        raise ValidationError("Voucher này chưa đến thời gian sử dụng.")
    if voucher.ngay_ket_thuc and voucher.ngay_ket_thuc < now:
        raise ValidationError("Voucher này đã hết hạn.")
    if voucher.cua_hang.exists():
        raise ValidationError("Voucher này chỉ áp dụng cho mua tại cửa hàng.")

    subtotal_amount = Decimal(subtotal_amount or 0)
    minimum_order = Decimal(voucher.gia_tri_don_hang_toi_thieu or 0)
    if subtotal_amount < minimum_order:
        raise ValidationError(
            f"Đơn hàng cần tối thiểu {_format_currency(minimum_order)} để áp dụng voucher này."
        )

    eligible_items = _filter_voucher_eligible_items(voucher, items)
    eligible_total = sum((_line_total_for_item(item) for item in eligible_items), Decimal("0"))
    if eligible_total <= 0:
        raise ValidationError("Voucher này không áp dụng cho sản phẩm đang có trong giỏ hàng.")

    discount_value = Decimal(voucher.gia_tri_giam or 0)
    if discount_value <= 0:
        raise ValidationError("Voucher này chưa được cấu hình giá trị giảm hợp lệ.")

    if voucher.loai_giam == "percent":
        discount_amount = (eligible_total * discount_value) / Decimal("100")
        if voucher.giam_toi_da:
            discount_amount = min(discount_amount, Decimal(voucher.giam_toi_da))
    else:
        discount_amount = discount_value

    discount_amount = min(discount_amount, eligible_total, subtotal_amount)
    if discount_amount <= 0:
        raise ValidationError("Voucher này không tạo ra giá trị giảm hợp lệ.")

    return voucher, discount_amount


def _get_checkout_available_vouchers(items, subtotal_amount):
    vouchers = (
        KhuyenMai.objects.prefetch_related("thuong_hieu", "cua_hang")
        .exclude(ma_code__isnull=True)
        .exclude(ma_code__exact="")
        .filter(dang_ap_dung=True)
        .order_by("-id")[:20]
    )
    available = []
    for voucher in vouchers:
        code = _normalize_voucher_code(voucher.ma_code)
        if not code:
            continue
        try:
            _, discount_amount = _resolve_checkout_voucher(code, items, subtotal_amount)
        except ValidationError:
            continue
        available.append(
            {
                "code": code,
                "title": voucher.ten,
                "description": voucher.mo_ta,
                "discount_amount": discount_amount,
                "display_discount_amount": _format_currency(discount_amount),
                "minimum_order_amount": Decimal(voucher.gia_tri_don_hang_toi_thieu or 0),
                "display_minimum_order_amount": _format_currency(voucher.gia_tri_don_hang_toi_thieu or 0),
            }
        )
    return available


def _get_customer_profile(user):
    profile, _ = HoSoKhachHang.objects.get_or_create(user=user)
    return profile


def _refresh_authenticated_user(request):
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return user
    try:
        user.refresh_from_db()
    except Exception:
        return user
    return user


def _purge_expired_trash():
    TrashRecord.objects.filter(expires_at__lt=timezone.now()).delete()


def _serialize_for_trash(obj):
    data = model_to_dict(obj)
    # Ensure file fields are stored as plain paths
    for field in obj._meta.fields:
        if field.get_internal_type() in {"ImageField", "FileField"}:
            value = getattr(obj, field.name)
            data[field.name] = str(value) if value else ""
    data = json.loads(json.dumps(data, cls=DjangoJSONEncoder))
    data.pop("id", None)
    return data


def _move_to_trash(obj, data=None):
    payload = data if data is not None else _serialize_for_trash(obj)
    retention_days = getattr(settings, "TRASH_RETENTION_DAYS", 15)
    TrashRecord.objects.create(
        model_label=obj._meta.label_lower,
        object_id=str(obj.pk),
        data=payload,
        expires_at=timezone.now() + timedelta(days=retention_days),
    )


def _model_slug_from_label(label: str) -> str:
    try:
        model = apps.get_model(label)
    except Exception:
        return label.split(".")[-1]
    for slug, registered in MODEL_REGISTRY.items():
        if registered is model:
            return slug
    return model._meta.model_name


def _trash_display_name(data: dict, model_label: str = "") -> str:
    model_key = (model_label or "").split(".")[-1].lower()

    if model_key == "giaodichkho":
        movement_type = (data.get("loai") or "").strip().lower()
        quantity = data.get("so_luong")
        product_id = data.get("san_pham")
        product_name = ""
        if product_id not in (None, ""):
            product_name = SanPham.objects.filter(pk=product_id).values_list("ten", flat=True).first() or f"SP #{product_id}"
        type_label = "Nhập kho" if movement_type == "import" else "Xuất kho" if movement_type == "export" else "Giao dịch kho"
        if product_name and quantity not in (None, ""):
            return f"{type_label} - {product_name} x {quantity}"
        if product_name:
            return f"{type_label} - {product_name}"
        if quantity not in (None, ""):
            return f"{type_label} x {quantity}"
        return type_label

    if model_key == "donhang":
        order_id = data.get("id") or data.get("object_id")
        receiver = data.get("ho_ten_nguoi_nhan")
        if order_id and receiver:
            return f"Đơn hàng #{order_id} - {receiver}"
        if order_id:
            return f"Đơn hàng #{order_id}"

    if model_key == "chitietdonhang":
        quantity = data.get("so_luong")
        product_id = data.get("san_pham")
        product_name = ""
        if product_id not in (None, ""):
            product_name = SanPham.objects.filter(pk=product_id).values_list("ten", flat=True).first() or f"SP #{product_id}"
        if product_name and quantity not in (None, ""):
            return f"{product_name} x {quantity}"

    for key in ("ten", "ho_ten", "ho_ten_nguoi_nhan", "username", "email"):
        value = data.get(key)
        if value:
            return str(value)
    return ""


def _address_type_label(address):
    return dict(DiaChiKhachHang.LOAI_DIA_CHI_CHOICES).get(address.loai_dia_chi, "Khác")


def _format_customer_address(address):
    if not address:
        return ""
    parts = [
        (address.dia_chi_cu_the or "").strip(),
        (address.phuong_xa or "").strip(),
        (address.quan_huyen or "").strip(),
        (address.tinh_thanh or "").strip(),
    ]
    return ", ".join(part for part in parts if part)


def _customer_addresses_qs(user):
    return DiaChiKhachHang.objects.filter(user=user).order_by("-mac_dinh", "-created_at", "-id")


def _get_default_customer_address(user):
    return _customer_addresses_qs(user).filter(mac_dinh=True).first() or _customer_addresses_qs(user).first()


def _sync_legacy_profile_address(user):
    profile = _get_customer_profile(user)
    default_address = _get_default_customer_address(user)
    full_address = _format_customer_address(default_address)
    if profile.dia_chi != full_address:
        profile.dia_chi = full_address
        profile.save(update_fields=["dia_chi"])


def _normalize_customer_address_defaults(user, target=None):
    addresses = list(_customer_addresses_qs(user))
    if not addresses:
        profile = _get_customer_profile(user)
        if profile.dia_chi:
            profile.dia_chi = ""
            profile.save(update_fields=["dia_chi"])
        return

    selected = None
    if target is not None:
        selected = next((item for item in addresses if item.pk == target.pk), None)
    if selected is None:
        selected = next((item for item in addresses if item.mac_dinh), None) or addresses[0]

    DiaChiKhachHang.objects.filter(user=user).exclude(pk=selected.pk).update(mac_dinh=False)
    if not selected.mac_dinh:
        selected.mac_dinh = True
        selected.save(update_fields=["mac_dinh"])

    _sync_legacy_profile_address(user)


def _send_feedback_emails(feedback):
    user_subject = "Circle K & GS25 đã nhận góp ý của bạn"
    user_message = (
        f"Xin chào {feedback.ho_ten},\n\n"
        "Chúng tôi đã nhận được góp ý của bạn và sẽ phản hồi sớm nhất có thể.\n\n"
        f"Chủ đề: {feedback.chu_de}\n"
        f"Nội dung: {feedback.noi_dung}\n\n"
        "Cảm ơn bạn đã đồng hành cùng Circle K & GS25."
    )
    admin_subject = f"Góp ý mới từ website: {feedback.chu_de}"
    admin_message = (
        "Hệ thống vừa ghi nhận một góp ý mới.\n\n"
        f"Họ tên: {feedback.ho_ten}\n"
        f"Email: {feedback.email}\n"
        f"Số điện thoại: {feedback.so_dien_thoai or '-'}\n"
        f"Chủ đề: {feedback.chu_de}\n"
        f"Nội dung:\n{feedback.noi_dung}\n"
    )

    send_mail(
        user_subject,
        user_message,
        settings.DEFAULT_FROM_EMAIL,
        [feedback.email],
        fail_silently=False,
    )
    send_mail(
        admin_subject,
        admin_message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.FEEDBACK_NOTIFICATION_EMAIL],
        fail_silently=False,
    )


def _send_order_confirmation(order, items):
    customer_email = (order.khach_hang.email or "").strip()
    if not customer_email:
        return False
    created_at = timezone.localtime(order.created_at) if order.created_at else timezone.localtime(timezone.now())
    created_text = created_at.strftime("%d/%m/%Y %H:%M")
    item_lines = []
    for item in items:
        line_total = item.get("line_total")
        if line_total is None:
            line_total = (item.get("unit_price") or Decimal("0")) * (item.get("quantity") or 0)
        item_lines.append(
            f"- {item['product'].ten} x {item['quantity']} = {_format_currency(line_total)}"
        )
    items_text = "\n".join(item_lines) if item_lines else "-"
    subject = f"Xác nhận đơn hàng {order.pk} - Circle K & GS25"
    message = (
        f"Xin chào {order.ho_ten_nguoi_nhan},\n\n"
        "Cảm ơn bạn đã đặt hàng tại Circle K & GS25.\n"
        f"Mã đơn: {order.pk}\n"
        f"Thời gian đặt: {created_text}\n"
        f"Người nhận: {order.ho_ten_nguoi_nhan}\n"
        f"Số điện thoại: {order.so_dien_thoai}\n"
        f"Địa chỉ giao hàng: {order.dia_chi_giao_hang}\n"
        f"Ghi chú: {order.ghi_chu or '-'}\n\n"
        "Chi tiết đơn hàng:\n"
        f"{items_text}\n\n"
        f"Tổng số lượng: {order.tong_so_luong}\n"
        f"Tạm tính: {_format_currency(order.tong_tien_truoc_giam or order.tong_tien)}\n"
        f"Voucher: {order.ma_voucher_ap_dung or '-'}\n"
        f"Giảm giá: {_format_currency(order.giam_gia)}\n"
        f"Tổng tiền: {_format_currency(order.tong_tien)}\n\n"
        "Chúng tôi sẽ liên hệ với bạn để xác nhận và giao hàng sớm nhất.\n"
        "Trân trọng."
    )
    customer_conn = get_connection(
        host=settings.ORDER_EMAIL_HOST,
        port=settings.ORDER_EMAIL_PORT,
        username=settings.ORDER_EMAIL_HOST_USER,
        password=settings.ORDER_EMAIL_HOST_PASSWORD,
        use_tls=settings.ORDER_EMAIL_USE_TLS,
        use_ssl=settings.ORDER_EMAIL_USE_SSL,
        timeout=settings.EMAIL_TIMEOUT,
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [customer_email],
        fail_silently=False,
        connection=customer_conn,
    )
    return True


def _cart_items(request):
    cart = _cart_session(request)
    product_ids = [int(pid) for pid in cart.keys() if str(pid).isdigit()]
    products = {p.pk: p for p in SanPham.objects.filter(pk__in=product_ids)}
    items = []
    total_quantity = 0
    total_amount = Decimal("0")
    for pid, quantity in cart.items():
        try:
            product = products[int(pid)]
        except Exception:
            continue
        qty = min(max(int(quantity), 0), product.ton_kho)
        if qty <= 0:
            continue
        unit_price = product.gia_ban or Decimal("0")
        line_total = unit_price * qty
        total_quantity += qty
        total_amount += line_total
        items.append({"product": product, "quantity": qty, "unit_price": unit_price, "line_total": line_total})
        if qty != int(quantity):
            cart[str(pid)] = qty
            request.session.modified = True
    return items, total_quantity, total_amount


def _ensure_role_groups():
    groups = {}
    for role_value, _role_label in ROLE_CHOICES:
        groups[role_value], _ = Group.objects.get_or_create(name=role_value)
    return groups


def _ensure_user_role(user):
    groups = _ensure_role_groups()
    if not user or not user.is_authenticated:
        return None

    target_role = None
    for role_value, _role_label in ROLE_CHOICES:
        if user.groups.filter(name=role_value).exists():
            target_role = role_value
            break
    if target_role is None:
        for legacy_name, mapped_role in LEGACY_ROLE_MAP.items():
            if user.groups.filter(name=legacy_name).exists():
                target_role = mapped_role
                break
    if target_role is None:
        if user.is_superuser or user.is_staff:
            target_role = ROLE_SYSTEM_ADMIN
        else:
            target_role = ROLE_CUSTOMER

    target_group = groups[target_role]
    needs_group_sync = not user.groups.filter(pk=target_group.pk).exists() or user.groups.exclude(pk=target_group.pk).exists()
    expected_is_staff = target_role in INTERNAL_ROLES
    needs_staff_sync = user.is_staff != expected_is_staff

    if needs_group_sync:
        user.groups.set([target_group])
    if needs_staff_sync:
        user.is_staff = expected_is_staff
        user.save(update_fields=["is_staff"])

    return target_role


def _get_user_role(user):
    return _ensure_user_role(user) or ROLE_CUSTOMER


def _sync_user_role(user, role: str):
    groups = _ensure_role_groups()
    if role not in groups:
        role = ROLE_CUSTOMER
    user.groups.set([groups[role]])
    user.is_staff = role in INTERNAL_ROLES
    user.save(update_fields=["is_staff"])


def _role_label(role: str) -> str:
    return ROLE_LABELS.get(role, role)


def _current_user_role(user):
    return _get_user_role(user) if user and user.is_authenticated else ROLE_CUSTOMER


def _has_admin_page_access(user, page_key: str, action: str = "view") -> bool:
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    role = _current_user_role(user)
    allowed_roles = ADMIN_PAGE_ROLE_ACTIONS.get(page_key, {}).get(action, set())
    return role in allowed_roles


def _has_module_access(user, model_slug: str, action: str = "view") -> bool:
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    role = _current_user_role(user)
    action_map = MODULE_ROLE_ACTIONS.get(model_slug, {})
    allowed_roles = action_map.get(action, action_map.get("view", set()))
    return role in allowed_roles


def _require_admin_permission(request, page_key: str, action: str = "view"):
    unauthorized = _require_admin_user(request)
    if unauthorized:
        return unauthorized
    if _has_admin_page_access(request.user, page_key, action):
        return None
    messages.error(request, _admin_pref_context(request)["t"]["no_access"])
    return redirect("store:admin_dashboard")


def _require_module_permission(request, model_slug: str, action: str = "view"):
    unauthorized = _require_admin_user(request)
    if unauthorized:
        return unauthorized
    if _has_module_access(request.user, model_slug, action):
        return None
    messages.error(request, _admin_pref_context(request)["t"]["no_access"])
    return redirect("store:admin_dashboard")


def _clean_user_email(raw_email: str, exclude_user_id=None):
    email = (raw_email or "").strip().lower()
    if not email:
        return "", None

    try:
        validate_email(email)
    except ValidationError:
        return email, "Email không đúng định dạng."

    query = User.objects.filter(email__iexact=email)
    if exclude_user_id is not None:
        query = query.exclude(pk=exclude_user_id)
    if query.exists():
        return email, "Email đã tồn tại."

    return email, None


def _split_full_name(raw_name: str):
    full_name = " ".join((raw_name or "").split()).strip()
    if not full_name:
        return "", ""

    parts = full_name.split(" ")
    if len(parts) == 1:
        return parts[0], ""

    first_name = parts[-1]
    last_name = " ".join(parts[:-1])
    return first_name, last_name


def _user_display_name(user):
    full_name = " ".join(part for part in [user.last_name, user.first_name] if part).strip()
    if full_name:
        if (not user.first_name or not user.last_name) and user.username:
            username = user.username.strip()
            if username and username.lower() != full_name.lower() and username.isalpha():
                return f"{full_name} {username}"
        return full_name
    return user.get_full_name().strip() or user.username


def _user_header_notifications(user):
    notifications = _user_all_notifications(user, limit=4)

    if not notifications:
        notifications.append(
            {
                "title": "Chưa có thông báo mới",
                "body": "Khi có đơn hàng hoặc cập nhật mới, bạn sẽ thấy tại đây.",
                "href": reverse("store:user_profile"),
                "is_new": False,
            }
        )

    return notifications


def _admin_header_notifications(limit=4):
    notifications = []
    for notice in Notification.objects.filter(resolved=False).order_by("-created_at")[:limit]:
        notifications.append(
            {
                "title": notice.title,
                "body": notice.message or "Có cập nhật mới trong hệ thống quản trị.",
                "href": reverse("store:admin_notifications"),
                "is_new": True,
                "timestamp": notice.created_at,
            }
        )
    return notifications


def _create_admin_notification(title, message, *, level="info", path="", method="", status_code=None):
    Notification.objects.create(
        level=(level or "info")[:20],
        title=(title or "Thông báo hệ thống")[:200],
        message=message or "",
        path=(path or "")[:255],
        method=(method or "")[:10],
        status_code=status_code,
    )


def _user_all_notifications(user, limit=None):
    notifications = []
    orders_qs = (
        DonHang.objects.filter(khach_hang=user)
        .prefetch_related("items__san_pham__hinh_anh_phu")
        .order_by("-created_at")
    )
    if limit is not None:
        orders_qs = orders_qs[:limit]

    for order in orders_qs:
        first_item = order.items.all().first()
        item_name = first_item.san_pham.ten if first_item and first_item.san_pham_id else "đơn hàng của bạn"
        thumb_url = ""
        if first_item and first_item.san_pham_id:
            product = first_item.san_pham
            if product.hinh_anh:
                thumb_url = product.hinh_anh.url
            else:
                extra_image = product.hinh_anh_phu.all().first()
                thumb_url = extra_image.hinh_anh.url if extra_image and extra_image.hinh_anh else ""

        status_label = order.get_trang_thai_display()
        action_label = "Xem chi tiết"
        accent = "warm"
        if order.trang_thai == "done":
            action_label = "Mua lại"
            accent = "success"
        elif order.trang_thai == "cancelled":
            action_label = "Xem chi tiết"
            accent = "muted"

        notifications.append(
            {
                "title": f"Đơn #{order.pk} đang {status_label.lower()}",
                "body": f"{item_name} • {timezone.localtime(order.created_at).strftime('%d/%m/%Y %H:%M')}",
                "message": f"Đơn hàng #{order.pk} với sản phẩm {item_name} hiện ở trạng thái {status_label.lower()}.",
                "href": reverse("store:order_detail", args=[order.pk]),
                "is_new": order.created_at >= timezone.now() - timedelta(days=2),
                "created_at": order.created_at,
                "created_text": timezone.localtime(order.created_at).strftime("%H:%M %d/%m/%Y"),
                "thumbnail_url": thumb_url,
                "status_label": status_label,
                "action_label": action_label,
                "accent": accent,
                "order_code": f"#{order.pk}",
            }
        )

    return notifications


def _order_status_timeline(order):
    created_at = order.created_at or timezone.now()
    raw_steps = [
        ("pending", "Đơn hàng đã đặt", created_at),
        ("confirmed", "Đã xác nhận", created_at + timedelta(hours=2)),
        ("shipping", "Đang giao", created_at + timedelta(hours=8)),
        ("delivered", "Đã giao hàng", created_at + timedelta(days=1)),
        ("done", "Hoàn tất", created_at + timedelta(days=2)),
    ]
    order_statuses = [item[0] for item in raw_steps]
    active_index = order_statuses.index(order.trang_thai) if order.trang_thai in order_statuses else -1

    timeline = []
    if order.trang_thai == "cancelled":
        for code, label, moment in raw_steps:
            timeline.append(
                {
                    "code": code,
                    "label": label,
                    "time": moment,
                    "state": "done" if code == "pending" else "pending",
                }
            )
        timeline.append(
            {
                "code": "cancelled",
                "label": "Đã hủy",
                "time": created_at + timedelta(hours=4),
                "state": "active",
            }
        )
        return timeline

    for index, (code, label, moment) in enumerate(raw_steps):
        if index < active_index:
            state = "done"
        elif index == active_index:
            state = "active"
        else:
            state = "pending"
        timeline.append(
            {
                "code": code,
                "label": label,
                "time": moment if state in {"done", "active"} else None,
                "state": state,
            }
        )
    return timeline


def _password_strength(password: str):
    password = password or ""
    score = 0
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"\d", password):
        score += 1
    if re.search(r"[^A-Za-z0-9]", password):
        score += 1

    if score <= 3:
        return "weak"
    if score <= 4:
        return "medium"
    return "strong"


def _enforce_password_strength(form, pref):
    password = (
        form.data.get("new_password1")
        or form.data.get("password1")
        or ""
    )
    strength = _password_strength(password)
    if password and strength == "weak":
        target_field = "new_password1" if "new_password1" in form.fields else "password1"
        form.add_error(target_field, pref["t"]["password_too_weak"])
    return strength


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
    unread_count = Notification.objects.filter(resolved=False).count()
    return {
        "admin_lang": lang,
        "admin_theme": theme,
        "admin_unread_notifications": unread_count,
        "show_admin_link": _is_admin_user(request.user),
        "current_admin_role": _current_user_role(request.user),
        "current_admin_role_label": _role_label(_current_user_role(request.user)),
        "can_manage_settings": _has_admin_page_access(request.user, "settings"),
        "can_manage_users": _has_admin_page_access(request.user, "user_management"),
        "can_view_inventory_hub": _has_admin_page_access(request.user, "inventory_hub"),
        "can_view_trash": _has_admin_page_access(request.user, "trash"),
        "can_view_notifications": _has_admin_page_access(request.user, "notifications"),
        "t": CMS_TRANSLATIONS[lang],
    }

def _model_label(model_slug, lang, plural=True):
    labels = MODULE_LABELS.get(model_slug, {})
    if lang == "en":
        return labels.get("en_plural" if plural else "en_singular", model_slug)
    return labels.get("vi_plural" if plural else "vi_singular", model_slug)


def _inventory_hub_context():
    cutoff_30d = timezone.now() - timedelta(days=30)
    stock_qs = (
        SanPham.objects.select_related("nhom_san_pham", "thuong_hieu").annotate(
            import_30d=dj_models.Sum(
                "giao_dich_kho__so_luong",
                filter=Q(giao_dich_kho__loai="import", giao_dich_kho__created_at__gte=cutoff_30d),
            ),
            export_30d=dj_models.Sum(
                "giao_dich_kho__so_luong",
                filter=Q(giao_dich_kho__loai="export", giao_dich_kho__created_at__gte=cutoff_30d),
            ),
        )
        .order_by("ten")
    )

    products = list(stock_qs)
    total_skus = len(products)
    total_units = sum(int(product.ton_kho or 0) for product in products)
    out_of_stock_count = sum(1 for product in products if (product.ton_kho or 0) <= 0)
    low_stock_count = sum(
        1
        for product in products
        if 0 < (product.ton_kho or 0) <= SanPham.LOW_STOCK_THRESHOLD
    )
    overstock_count = sum(
        1
        for product in products
        if (product.ton_kho or 0) >= max(SanPham.LOW_STOCK_THRESHOLD * 4, 20)
    )

    for product in products:
        product.import_30d = int(product.import_30d or 0)
        product.export_30d = int(product.export_30d or 0)
        product.net_30d = product.import_30d - product.export_30d
        product.stock_label_display = SanPham.stock_label.fget(product)
        product.stock_hint_display = SanPham.stock_hint.fget(product)

    import_suggestions = sorted(
        [
            product
            for product in products
            if (product.ton_kho or 0) <= SanPham.LOW_STOCK_THRESHOLD
        ],
        key=lambda item: (item.ton_kho, -(item.export_30d or 0), item.ten.lower()),
    )[:8]

    export_suggestions = sorted(
        [
            product
            for product in products
            if (product.ton_kho or 0) > SanPham.LOW_STOCK_THRESHOLD
        ],
        key=lambda item: (-(item.ton_kho or 0), item.export_30d or 0, item.ten.lower()),
    )[:8]

    movement_totals = GiaoDichKho.objects.aggregate(
        import_30d=Coalesce(
            dj_models.Sum("so_luong", filter=Q(loai="import", created_at__gte=cutoff_30d)),
            0,
        ),
        export_30d=Coalesce(
            dj_models.Sum("so_luong", filter=Q(loai="export", created_at__gte=cutoff_30d)),
            0,
        ),
    )

    recent_movements = list(
        GiaoDichKho.objects.select_related("san_pham", "nhan_vien", "cua_hang")
        .order_by("-created_at", "-id")[:10]
    )

    store_stock_rows = list(
        CuaHang.objects.select_related("chuoi").annotate(
            total_units=Coalesce(dj_models.Sum("ton_kho_san_pham__ton_kho"), 0),
            sku_count=Coalesce(
                dj_models.Count(
                    "ton_kho_san_pham",
                    filter=Q(ton_kho_san_pham__ton_kho__gt=0),
                    distinct=True,
                ),
                0,
            ),
            low_stock_count=Coalesce(
                dj_models.Count(
                    "ton_kho_san_pham",
                    filter=Q(
                        ton_kho_san_pham__ton_kho__gt=0,
                        ton_kho_san_pham__ton_kho__lte=SanPham.LOW_STOCK_THRESHOLD,
                    ),
                    distinct=True,
                ),
                0,
            ),
            empty_stock_count=Coalesce(
                dj_models.Count(
                    "ton_kho_san_pham",
                    filter=Q(ton_kho_san_pham__ton_kho__lte=0),
                    distinct=True,
                ),
                0,
            ),
        ).order_by("-total_units", "ten")[:8]
    )

    return {
        "inventory_stats": {
            "total_skus": total_skus,
            "total_units": total_units,
            "out_of_stock_count": out_of_stock_count,
            "low_stock_count": low_stock_count,
            "overstock_count": overstock_count,
            "import_30d": int(movement_totals["import_30d"] or 0),
            "export_30d": int(movement_totals["export_30d"] or 0),
        },
        "import_suggestions": import_suggestions,
        "export_suggestions": export_suggestions,
        "recent_stock_movements": recent_movements,
        "store_stock_rows": store_stock_rows,
    }


def _dashboard_context():
    now = timezone.now()
    today = now.date()
    paid_statuses = {"paid"}
    zero_money = dj_models.Value(0, output_field=dj_models.DecimalField(max_digits=12, decimal_places=0))

    order_qs = DonHang.objects.select_related("khach_hang", "cua_hang_xu_ly", "khuyen_mai")
    total_orders = order_qs.count()
    today_orders = order_qs.filter(created_at__date=today).count()
    pending_orders = order_qs.filter(trang_thai="pending").count()
    awaiting_transfer_orders = order_qs.filter(
        phuong_thuc_thanh_toan="bank_transfer",
        trang_thai_thanh_toan="awaiting_confirmation",
    ).count()
    paid_revenue = order_qs.filter(trang_thai_thanh_toan__in=paid_statuses).aggregate(
        total=Coalesce(dj_models.Sum("tong_tien"), zero_money)
    )["total"]
    today_revenue = order_qs.filter(
        created_at__date=today,
        trang_thai_thanh_toan__in=paid_statuses,
    ).aggregate(total=Coalesce(dj_models.Sum("tong_tien"), zero_money))["total"]

    product_qs = SanPham.objects.all()
    product_count = product_qs.count()
    low_stock_count = product_qs.filter(
        ton_kho__gt=0,
        ton_kho__lte=SanPham.LOW_STOCK_THRESHOLD,
    ).count()
    out_stock_count = product_qs.filter(ton_kho__lte=0).count()

    recent_orders = list(order_qs.order_by("-created_at")[:8])
    for order in recent_orders:
        order.display_total_amount = _format_currency(order.tong_tien)

    payment_mix = []
    payment_rows = (
        order_qs.values("phuong_thuc_thanh_toan")
        .annotate(total=dj_models.Count("id"))
        .order_by("-total")
    )
    method_labels = dict(DonHang.PAYMENT_METHOD_CHOICES)
    for row in payment_rows:
        payment_mix.append(
            {
                "label": method_labels.get(row["phuong_thuc_thanh_toan"], row["phuong_thuc_thanh_toan"]),
                "value": row["total"],
            }
        )

    seven_day_series = []
    revenue_points = []
    order_points = []
    max_revenue = Decimal("0")
    max_orders = 0
    for offset in range(6, -1, -1):
        day = today - timedelta(days=offset)
        day_orders = order_qs.filter(created_at__date=day)
        order_count = day_orders.count()
        day_revenue = day_orders.filter(trang_thai_thanh_toan__in=paid_statuses).aggregate(
            total=Coalesce(dj_models.Sum("tong_tien"), zero_money)
        )["total"]
        if day_revenue > max_revenue:
            max_revenue = day_revenue
        if order_count > max_orders:
            max_orders = order_count
        seven_day_series.append(
            {
                "label": day.strftime("%d/%m"),
                "day_name": day.strftime("%a"),
                "order_count": order_count,
                "revenue": day_revenue,
                "display_revenue": _format_currency(day_revenue),
            }
        )

    max_revenue = max_revenue or Decimal("1")
    max_orders = max_orders or 1
    for item in seven_day_series:
        revenue_percent = float((Decimal(item["revenue"]) / Decimal(max_revenue)) * Decimal("100"))
        order_percent = (int(item["order_count"]) / max_orders) * 100
        item["revenue_percent"] = max(8, round(revenue_percent, 2)) if item["revenue"] else 8
        item["order_percent"] = max(8, round(order_percent, 2)) if item["order_count"] else 8
        revenue_points.append(str(round(item["revenue_percent"], 2)))
        order_points.append(str(round(item["order_percent"], 2)))

    store_leaderboard = list(
        CuaHang.objects.select_related("chuoi").annotate(
            total_orders=Coalesce(dj_models.Count("don_hang_xu_ly", distinct=True), 0),
            total_revenue=Coalesce(
                dj_models.Sum(
                    "don_hang_xu_ly__tong_tien",
                    filter=Q(don_hang_xu_ly__trang_thai_thanh_toan="paid"),
                ),
                zero_money,
            ),
            total_units=Coalesce(dj_models.Sum("ton_kho_san_pham__ton_kho"), 0),
        ).order_by("-total_orders", "-total_revenue", "ten")[:8]
    )
    for store in store_leaderboard:
        store.display_total_revenue = _format_currency(store.total_revenue)

    return {
        "dashboard_stats": {
            "total_orders": total_orders,
            "today_orders": today_orders,
            "pending_orders": pending_orders,
            "awaiting_transfer_orders": awaiting_transfer_orders,
            "paid_revenue": _format_currency(paid_revenue),
            "today_revenue": _format_currency(today_revenue),
            "product_count": product_count,
            "low_stock_count": low_stock_count,
            "out_stock_count": out_stock_count,
        },
        "recent_orders_dashboard": recent_orders,
        "payment_mix": payment_mix,
        "store_leaderboard": store_leaderboard,
        "seven_day_series": seven_day_series,
        "dashboard_chart_meta": {
            "max_revenue": _format_currency(max_revenue),
            "max_orders": max_orders,
            "revenue_points": ",".join(revenue_points),
            "order_points": ",".join(order_points),
        },
    }


def _select_fulfillment_store(items):
    if not items:
        return None

    product_ids = sorted({item["product"].pk for item in items if item.get("product")})
    if not product_ids:
        return None

    rows = (
        TonKhoCuaHang.objects.filter(san_pham_id__in=product_ids)
        .select_related("cua_hang")
        .order_by("cua_hang__ten", "san_pham__ten")
    )
    store_map = {}
    for row in rows:
        store_bucket = store_map.setdefault(
            row.cua_hang_id,
            {"store": row.cua_hang, "stock": {}},
        )
        store_bucket["stock"][row.san_pham_id] = int(row.ton_kho or 0)

    candidates = []
    for data in store_map.values():
        if all(data["stock"].get(item["product"].pk, 0) >= int(item["quantity"]) for item in items):
            score = sum(data["stock"].get(item["product"].pk, 0) for item in items)
            candidates.append((score, data["store"].ten.lower(), data["store"]))

    if not candidates:
        return None

    candidates.sort(key=lambda item: (-item[0], item[1]))
    return candidates[0][2]


def _admin_redirect_with_preserved_query(request, model_slug="don-hang"):
    redirect_url = reverse("store:admin_list", kwargs={"model_slug": model_slug})
    query = (request.POST.get("return_query") or request.GET.urlencode() or "").strip("&?")
    if query:
        redirect_url = f"{redirect_url}?{query}"
    return redirect(redirect_url)


def _release_order_inventory_if_needed(order, *, reason=""):
    if order is None or order.trang_thai_thanh_toan == "paid":
        return False

    movements = list(
        GiaoDichKho.objects.filter(don_hang=order, loai="export")
        .select_related("san_pham")
        .order_by("-created_at", "-id")
    )
    if not movements:
        return False

    for movement in movements:
        product_name = movement.san_pham.ten if movement.san_pham_id else f"SP #{movement.pk}"
        movement.delete()
        _create_admin_notification(
            f"Hoàn tồn kho cho đơn #{order.pk}",
            (
                f"Đã hoàn {movement.so_luong} sản phẩm của {product_name} "
                f"về kho do {reason or 'đơn chưa thanh toán bị hủy'}."
            ),
            level="warning",
            path=reverse("store:admin_list", kwargs={"model_slug": "giao-dich-kho"}),
            method="PATCH",
            status_code=200,
        )
    return True


def _log_payment_confirmation(order, action, *, performed_by=None, note=""):
    if order is None:
        return None
    return XacNhanThanhToan.objects.create(
        don_hang=order,
        hanh_dong=action,
        ghi_chu=note or "",
        performed_by=performed_by if getattr(performed_by, "is_authenticated", False) else None,
    )


def _field_label(field, lang):
    if lang != "en":
        return field.verbose_name
    return FIELD_LABELS.get("en", {}).get(field.name, field.verbose_name)


def _menu_context(lang="vi", user=None):
    menu = []
    for slug, model in MODEL_REGISTRY.items():
        if user is not None and not _has_module_access(user, slug, "view"):
            continue
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


def _build_product_image_preview_context(obj=None):
    previews = {
        "product_images": {"url": "", "is_image": True},
        "gallery_items": [],
    }
    if obj is None:
        return previews

    try:
        if obj.hinh_anh:
            previews["product_images"]["url"] = obj.hinh_anh.url
    except Exception:
        pass

    related_images = list(obj.hinh_anh_phu.all().order_by("thu_tu", "id"))
    previews["gallery_items"] = [
        {
            "id": image.pk,
            "url": image.hinh_anh.url,
            "caption": image.chu_thich or f"Ảnh phụ {index}",
            "order": index,
        }
        for index, image in enumerate(related_images, start=1)
        if getattr(image, "hinh_anh", None)
    ]
    return previews


def _save_product_gallery(product, files, post_data=None):
    uploaded_images = list(files.getlist("product_images"))
    post_data = post_data or {}
    post_values = post_data.getlist if hasattr(post_data, "getlist") else lambda key: []

    if uploaded_images and not product.hinh_anh:
        product.hinh_anh = uploaded_images.pop(0)
        product.save(update_fields=["hinh_anh"])

    delete_ids = {value for value in post_values("delete_image_ids") if str(value).isdigit()}
    if delete_ids:
        product.hinh_anh_phu.filter(pk__in=delete_ids).delete()

    related_images = list(product.hinh_anh_phu.all().order_by("thu_tu", "id"))

    order_map = {}
    for image in related_images:
        raw_order = (post_data.get(f"image_order_{image.pk}") or "").strip()
        if raw_order.isdigit():
            order_map[image.pk] = int(raw_order)
    if order_map:
        related_images.sort(key=lambda item: (order_map.get(item.pk, item.thu_tu or 9999), item.thu_tu, item.pk))
        for index, image in enumerate(related_images, start=1):
            if image.thu_tu != index:
                image.thu_tu = index
                image.save(update_fields=["thu_tu"])

    if uploaded_images:
        current_order = (
            product.hinh_anh_phu.aggregate(max_order=dj_models.Max("thu_tu")).get("max_order") or 0
        )
        for uploaded in uploaded_images:
            current_order += 1
            HinhAnhSanPham.objects.create(
                san_pham=product,
                hinh_anh=uploaded,
                thu_tu=current_order,
                chu_thich=f"Ảnh phụ {current_order}",
            )

    normalized_images = list(product.hinh_anh_phu.all().order_by("thu_tu", "id"))
    for index, image in enumerate(normalized_images, start=1):
        if image.thu_tu != index:
            image.thu_tu = index
            image.save(update_fields=["thu_tu"])


def _build_product_card_gallery(product):
    images = []
    if product.hinh_anh:
        try:
            images.append(product.hinh_anh.url)
        except Exception:
            pass

    for image in product.hinh_anh_phu.all():
        try:
            if image.hinh_anh:
                images.append(image.hinh_anh.url)
        except Exception:
            continue

    if not images:
        images.append("https://www.circlek.com/sites/default/files/2024-03/our_products_920x575.jpg")
    return images[:8]


def _attach_stock_ui_fields(product):
    product.catalog_stock_label = SanPham.stock_label.fget(product)
    product.catalog_stock_hint = SanPham.stock_hint.fget(product)
    product.stock_css = {
        "out": "out-stock",
        "low": "low-stock",
        "ok": "in-stock",
    }.get(product.stock_level, "in-stock")
    return product


def _admin_form_class_for_model(model_slug, model):
    if model_slug == "san-pham":
        return SanPhamAdminForm
    if model_slug == "giao-dich-kho":
        return GiaoDichKhoAdminForm
    if model_slug == "khuyen-mai":
        return KhuyenMaiAdminForm
    return modelform_factory(model, fields="__all__")


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


@method_decorator(never_cache, name="dispatch")
class AdminLoginView(LoginView):
    template_name = "user/login.html"
    authentication_form = AuthenticationForm
    redirect_authenticated_user = False

    def dispatch(self, request, *args, **kwargs):
        if _is_admin_user(request.user):
            return redirect("store:admin_dashboard")
        if _is_regular_user(request.user):
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            return redirect("store:user_dashboard")
        if request.user.is_authenticated:
            logout(request)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        user = self.request.user
        if _is_admin_user(user):
            return reverse("store:admin_dashboard")
        resumed_url = _resume_post_login_cart_action(self.request)
        if resumed_url:
            return resumed_url
        next_url = self.request.POST.get("next") or self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse("store:user_dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pref = _admin_pref_context(self.request)
        context.update(pref)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        _ensure_user_role(self.request.user)
        return response


@method_decorator(never_cache, name="dispatch")
class UserLoginView(LoginView):
    template_name = "user/login.html"
    authentication_form = AuthenticationForm
    redirect_authenticated_user = False

    def dispatch(self, request, *args, **kwargs):
        if _is_admin_user(request.user) and not request.GET.get("next"):
            return redirect("store:admin_dashboard")
        if _is_regular_user(request.user):
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            return redirect("store:user_dashboard")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        user = self.request.user
        if _is_admin_user(user):
            return reverse("store:admin_dashboard")
        resumed_url = _resume_post_login_cart_action(self.request)
        if resumed_url:
            return resumed_url
        next_url = self.request.POST.get("next") or self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse("store:user_dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pref = _admin_pref_context(self.request)
        context.update(pref)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        _ensure_user_role(self.request.user)
        return response


def user_register(request):
    pref = _admin_pref_context(request)
    form = UserCreationForm()
    email_value = ""
    full_name_value = ""
    password_strength = ""

    if request.user.is_authenticated:
        if _is_admin_user(request.user):
            return redirect("store:admin_dashboard")
        return redirect("store:user_dashboard")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        email_value = (request.POST.get("email") or "").strip()
        full_name_value = (request.POST.get("full_name") or "").strip()
        password_strength = _password_strength(request.POST.get("password1") or "")
        email, email_error = _clean_user_email(email_value)
        if email_error:
            form.add_error(None, email_error)
        if password_strength == "weak":
            form.add_error("password1", pref["t"]["password_too_weak"])
        if form.is_valid():
            user = form.save(commit=False)
            if full_name_value:
                user.first_name, user.last_name = _split_full_name(full_name_value)
            user.email = email
            user.is_active = True
            user.save()
            _sync_user_role(user, ROLE_USER)
            _get_customer_profile(user)
            login(request, user)
            messages.success(request, pref["t"]["user_created"])
            return redirect("store:user_dashboard")

    return render(
        request,
        "user/register.html",
        {
            "form": form,
            "email_value": email_value,
            "full_name_value": full_name_value,
            "password_strength_value": password_strength,
            **pref,
        },
    )


def admin_logout(request):
    logout(request)
    return redirect("store:admin_login")


def user_logout(request):
    logout(request)
    return redirect("store:user_login")


def admin_dashboard(request):
    unauthorized = _require_admin_permission(request, "dashboard")
    if unauthorized:
        return unauthorized

    pref = _admin_pref_context(request)
    lang = pref["admin_lang"]
    modules = _menu_context(lang, request.user)
    return render(
        request,
        "admin/index.html",
        {
            "modules": modules,
            "total_records": sum(item["count"] for item in modules),
            **_dashboard_context(),
            **pref,
        },
    )


def admin_inventory_hub(request):
    unauthorized = _require_admin_permission(request, "inventory_hub")
    if unauthorized:
        return unauthorized

    pref = _admin_pref_context(request)
    lang = pref["admin_lang"]
    return render(
        request,
        "admin/inventory_hub.html",
        {
            "modules": _menu_context(lang, request.user),
            **_inventory_hub_context(),
            **pref,
        },
    )


def admin_inventory_restock(request):
    unauthorized = _require_module_permission(request, "giao-dich-kho", "create")
    if unauthorized:
        return unauthorized

    pref = _admin_pref_context(request)
    lang = pref["admin_lang"]
    stores = list(CuaHang.objects.select_related("chuoi").order_by("chuoi__ten", "ten", "pk"))
    selected_store_ids = [str(store.pk) for store in stores]
    target_stock = 25
    note = "Nhap kho dong loat de mo ban toan bo san pham"

    if request.method == "POST":
        selected_store_ids = [value for value in request.POST.getlist("store_ids") if value.strip()]
        note = (request.POST.get("note") or note).strip()
        try:
            target_stock = int(request.POST.get("target_stock") or 25)
        except (TypeError, ValueError):
            target_stock = 0

        if not selected_store_ids:
            messages.error(request, "Vui l?ng ch?n ?t nh?t m?t c?a h?ng ?? nh?p kho.")
        else:
            try:
                summary = restock_products(
                    target_stock=target_stock,
                    note=note,
                    store_ids=[int(store_id) for store_id in selected_store_ids],
                )
            except ValueError as exc:
                messages.error(request, str(exc))
            except LookupError as exc:
                messages.error(request, str(exc))
            else:
                messages.success(
                    request,
                    (
                        "?? nh?p kho th?nh c?ng cho "
                        f"{summary['store_count']} c?a h?ng, "
                        f"t?o {summary['created_movements']} phi?u nh?p v? "
                        f"b? sung {summary['imported_units']} ??n v? h?ng."
                    ),
                )
                return redirect("store:admin_inventory_restock")

    return render(
        request,
        "admin/inventory_restock.html",
        {
            "modules": _menu_context(lang, request.user),
            "stores": stores,
            "selected_store_ids": selected_store_ids,
            "target_stock": target_stock,
            "note_value": note,
            "model_slug": "giao-dich-kho",
            **pref,
        },
    )


def admin_user_password(request, pk):
    unauthorized = _require_admin_permission(request, "user_management")
    if unauthorized:
        return unauthorized

    pref = _admin_pref_context(request)
    user_obj = get_object_or_404(User, pk=pk)
    form = SetPasswordForm(user=user_obj)
    password_strength = ""

    if request.method == "POST":
        form = SetPasswordForm(user=user_obj, data=request.POST)
        password_strength = _enforce_password_strength(form, pref)
        if form.is_valid():
            form.save()
            messages.success(request, pref["t"]["password_updated"])
            return redirect("store:admin_user_management")

    return render(
        request,
        "admin/password_form.html",
        {
            "modules": _menu_context(pref["admin_lang"], request.user),
            "form": form,
            "page_heading": f'{pref["t"]["reset_password"]}: {user_obj.username}',
            "password_strength_value": password_strength,
            **pref,
        },
    )


@require_POST
def admin_order_status_action(request, pk, status):
    unauthorized = _require_module_permission(request, "don-hang", "status")
    if unauthorized:
        return unauthorized

    if status not in {"confirmed", "shipping", "delivered", "done", "cancelled"}:
        return _admin_redirect_with_preserved_query(request)

    order = get_object_or_404(DonHang, pk=pk)
    allowed_transitions = {
        "pending": {"confirmed", "cancelled"},
        "confirmed": {"shipping", "cancelled"},
        "shipping": {"delivered", "cancelled"},
        "delivered": {"done"},
        "done": set(),
        "cancelled": set(),
    }
    if status not in allowed_transitions.get(order.trang_thai, set()):
        return _admin_redirect_with_preserved_query(request)

    with transaction.atomic():
        order.trang_thai = status
        order.save(update_fields=["trang_thai"])
        if status == "cancelled":
            _release_order_inventory_if_needed(order, reason="đơn hàng bị hủy")
    _create_admin_notification(
        f"Cập nhật đơn hàng #{order.pk}",
        (
            f"Đơn #{order.pk} của khách hàng {order.khach_hang.username} "
            f"đã được chuyển sang trạng thái {order.get_trang_thai_display().lower()}."
        ),
        level="info",
        path=reverse("store:admin_list", kwargs={"model_slug": "don-hang"}),
        method="PATCH",
        status_code=200,
    )
    messages.success(request, _admin_pref_context(request)["t"]["order_status_updated"])

    return _admin_redirect_with_preserved_query(request)


@require_POST
def admin_order_payment_status_action(request, pk, status):
    unauthorized = _require_module_permission(request, "don-hang", "payment_status")
    if unauthorized:
        return unauthorized

    if status not in {"unpaid", "paid", "awaiting_confirmation", "refunded"}:
        return _admin_redirect_with_preserved_query(request)

    order = get_object_or_404(DonHang, pk=pk)
    allowed_transitions = {
        "unpaid": {"paid", "awaiting_confirmation"},
        "awaiting_confirmation": {"paid", "unpaid", "refunded"},
        "paid": {"refunded"},
        "refunded": set(),
    }
    if status not in allowed_transitions.get(order.trang_thai_thanh_toan, set()):
        return _admin_redirect_with_preserved_query(request)

    with transaction.atomic():
        order.trang_thai_thanh_toan = status
        order.save(update_fields=["trang_thai_thanh_toan"])
        if status == "unpaid" and order.trang_thai == "pending":
            order.trang_thai = "cancelled"
            order.save(update_fields=["trang_thai"])
            _release_order_inventory_if_needed(order, reason="thanh toán bị trả về chưa thanh toán")
    _create_admin_notification(
        f"Cập nhật thanh toán đơn #{order.pk}",
        (
            f"Trạng thái thanh toán của đơn #{order.pk} "
            f"đã chuyển sang {order.get_trang_thai_thanh_toan_display().lower()}."
        ),
        level="info",
        path=reverse("store:admin_list", kwargs={"model_slug": "don-hang"}),
        method="PATCH",
        status_code=200,
    )
    messages.success(request, "Đã cập nhật trạng thái thanh toán.")

    return _admin_redirect_with_preserved_query(request)


@require_POST
def admin_order_receipt_review_action(request, pk, action):
    unauthorized = _require_module_permission(request, "don-hang", "payment_status")
    if unauthorized:
        return unauthorized

    if action not in {"approve", "reject"}:
        return _admin_redirect_with_preserved_query(request)

    order = get_object_or_404(DonHang, pk=pk)
    if order.phuong_thuc_thanh_toan != "bank_transfer" or not order.anh_bien_lai:
        return _admin_redirect_with_preserved_query(request)

    rejection_note = (request.POST.get("rejection_note") or "").strip()
    if action == "reject" and not rejection_note:
        messages.error(request, "Vui lòng nhập ghi chú từ chối biên lai.")
        return _admin_redirect_with_preserved_query(request)

    if order.trang_thai_thanh_toan not in {"awaiting_confirmation", "unpaid"}:
        return _admin_redirect_with_preserved_query(request)

    with transaction.atomic():
        if action == "approve":
            order.trang_thai_thanh_toan = "paid"
            order.save(update_fields=["trang_thai_thanh_toan"])
            _log_payment_confirmation(
                order,
                "approved",
                performed_by=request.user,
                note="Biên lai chuyển khoản đã được duyệt.",
            )
            messages.success(request, "Đã duyệt biên lai chuyển khoản.")
        else:
            order.trang_thai_thanh_toan = "unpaid"
            order.save(update_fields=["trang_thai_thanh_toan"])
            _log_payment_confirmation(
                order,
                "rejected",
                performed_by=request.user,
                note=rejection_note,
            )
            messages.warning(request, "Đã từ chối biên lai chuyển khoản.")

    return _admin_redirect_with_preserved_query(request)


def admin_user_management(request):
    unauthorized = _require_admin_permission(request, "user_management")
    if unauthorized:
        return unauthorized

    _ensure_role_groups()
    pref = _admin_pref_context(request)
    lang = pref["admin_lang"]
    form = UserCreationForm()
    create_user_email = ""
    create_user_full_name = ""
    create_user_role = ROLE_CUSTOMER
    create_user_is_active = True
    create_user_password_strength = ""
    query = request.GET.get("q", "").strip()
    filter_field = request.GET.get("f", "").strip()

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create_user":
            form = UserCreationForm(request.POST)
            create_user_email = (request.POST.get("email") or "").strip()
            create_user_full_name = (request.POST.get("full_name") or "").strip()
            create_user_role = request.POST.get("role", ROLE_CUSTOMER)
            create_user_is_active = request.POST.get("is_active") == "on"
            create_user_password_strength = _password_strength(request.POST.get("password1") or "")
            email, email_error = _clean_user_email(create_user_email)
            if email_error:
                form.add_error(None, email_error)
            if create_user_password_strength == "weak":
                form.add_error("password1", pref["t"]["password_too_weak"])
            if form.is_valid():
                user = form.save(commit=False)
                if create_user_full_name:
                    user.first_name, user.last_name = _split_full_name(create_user_full_name)
                user.email = email
                user.is_active = create_user_is_active
                user.save()
                _sync_user_role(user, create_user_role)
                messages.success(request, pref["t"]["user_created"])
                return redirect("store:admin_user_management")
        elif action == "update_role":
            user = get_object_or_404(User, pk=request.POST.get("user_id"))
            full_name = (request.POST.get("full_name") or "").strip()
            email_input = (request.POST.get("email") or "").strip()
            email, email_error = _clean_user_email(email_input, exclude_user_id=user.pk)
            if email_error:
                messages.error(request, f"{user.username}: {email_error}")
                redirect_url = reverse("store:admin_user_management")
                query_params = []
                if query:
                    query_params.append(f"q={query}")
                if filter_field:
                    query_params.append(f"f={filter_field}")
                if query_params:
                    redirect_url = f"{redirect_url}?{'&'.join(query_params)}"
                return redirect(redirect_url)

            if full_name:
                user.first_name, user.last_name = _split_full_name(full_name)
            else:
                user.first_name = ""
                user.last_name = ""
            user.email = email
            if not user.is_superuser:
                user.is_active = request.POST.get("is_active") == "on"
                user.save(update_fields=["first_name", "last_name", "email", "is_active"])
            else:
                user.save(update_fields=["first_name", "last_name", "email"])
            _sync_user_role(user, request.POST.get("role", ROLE_CUSTOMER))
            messages.success(request, pref["t"]["user_updated"])
            redirect_url = reverse("store:admin_user_management")
            query_params = []
            if query:
                query_params.append(f"q={query}")
            if filter_field:
                query_params.append(f"f={filter_field}")
            if query_params:
                redirect_url = f"{redirect_url}?{'&'.join(query_params)}"
            return redirect(redirect_url)

    user_qs = User.objects.order_by("username")
    if query:
        filter_field = filter_field or ""
        if filter_field == "username":
            user_qs = user_qs.filter(username__icontains=query)
        elif filter_field == "email":
            user_qs = user_qs.filter(email__icontains=query)
        elif filter_field == "full_name":
            user_qs = user_qs.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
        elif filter_field == "role":
            role_value = query.strip().lower()
            role_aliases = {
                "admin": ROLE_SYSTEM_ADMIN,
                "administrator": ROLE_SYSTEM_ADMIN,
                "quan tri": ROLE_SYSTEM_ADMIN,
                "quản trị": ROLE_SYSTEM_ADMIN,
                "quan ly kho": ROLE_STOCK_MANAGER,
                "quản lý kho": ROLE_STOCK_MANAGER,
                "kho": ROLE_STOCK_MANAGER,
                "quan ly don hang": ROLE_ORDER_MANAGER,
                "quản lý đơn hàng": ROLE_ORDER_MANAGER,
                "don hang": ROLE_ORDER_MANAGER,
                "đơn hàng": ROLE_ORDER_MANAGER,
                "cskh": ROLE_CUSTOMER_SUPPORT,
                "nhan vien cskh": ROLE_CUSTOMER_SUPPORT,
                "nhân viên cskh": ROLE_CUSTOMER_SUPPORT,
                "support": ROLE_CUSTOMER_SUPPORT,
                "customer": ROLE_CUSTOMER,
                "user": ROLE_CUSTOMER,
                "khach": ROLE_CUSTOMER,
                "khách": ROLE_CUSTOMER,
            }
            role_value = role_aliases.get(role_value, role_value)
            user_qs = user_qs.filter(groups__name=role_value)
        elif filter_field == "status":
            q_lower = query.strip().lower()
            truthy = {"1", "true", "yes", "on", "hoat dong", "hoạt động", "active"}
            falsy = {"0", "false", "no", "off", "ngung", "ngừng", "inactive"}
            if q_lower in truthy:
                user_qs = user_qs.filter(is_active=True)
            elif q_lower in falsy:
                user_qs = user_qs.filter(is_active=False)
            else:
                user_qs = user_qs.none()
        else:
            user_qs = user_qs.filter(
                Q(username__icontains=query)
                | Q(email__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
            )

    paginator = Paginator(user_qs, 15)
    page_obj = paginator.get_page(request.GET.get("page"))

    users = []
    for user in page_obj.object_list:
        users.append(
            {
                "object": user,
                "role": _get_user_role(user),
                "role_label": _role_label(_get_user_role(user)),
                "full_name": user.get_full_name().strip() or "-",
            }
        )

    return render(
        request,
        "admin/user_management.html",
        {
            "modules": _menu_context(lang, request.user),
            "create_user_form": form,
            "create_user_email": create_user_email,
            "create_user_full_name": create_user_full_name,
            "create_user_role": create_user_role,
            "create_user_is_active": create_user_is_active,
            "create_user_password_strength": create_user_password_strength,
            "users": users,
            "page_obj": page_obj,
            "paginator": paginator,
            "query": query,
            "filter_field": filter_field,
            "role_choices": ROLE_CHOICES,
            **pref,
        },
    )


def admin_settings(request):
    unauthorized = _require_admin_permission(request, "settings")
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
    return render(request, "admin/settings.html", {"modules": _menu_context(pref["admin_lang"], request.user), **pref})


def _infer_product_ai_category(product) -> str:
    group_name = ""
    try:
        group_name = (product.nhom_san_pham.ten if product.nhom_san_pham else "") or ""
    except Exception:
        group_name = ""
    text = f"{product.ten} {group_name}".lower()
    if any(k in text for k in ["nước", "cà phê", "trà", "sữa", "drink", "sting", "aquafina", "coca", "pepsi"]):
        return "Đồ uống"
    if any(k in text for k in ["mì", "xôi", "bánh mì", "tokbokki", "sandwich", "cơm", "cháo", "lẩu"]):
        return "Đồ ăn nhanh"
    if any(k in text for k in ["snack", "bắp rang", "kẹo", "chip", "ostar"]):
        return "Ăn vặt"
    return "Khác"


def _strip_parenthetical_text(value):
    text = "" if value is None else str(value)
    text = re.sub(r"\s*\([^)]*\)", "", text)
    return re.sub(r"\s{2,}", " ", text).strip()


def _extract_district_from_address(address):
    text = "" if address is None else str(address).strip()
    if not text:
        return ""
    for chunk in [c.strip() for c in text.split(",") if c.strip()]:
        low = chunk.lower()
        if "quận" in low or "huyện" in low or "thủ đức" in low:
            return chunk
    return ""


def _facet_specs_for_model(model_slug):
    return {
        "thuong-hieu": [
            {"param": "brand", "label": "Thương hiệu", "expr": "ten"},
        ],
        "nha-cung-cap": [
            {"param": "supplier", "label": "Nhà cung cấp", "expr": "ten"},
        ],
        "nhom-san-pham": [
            {"param": "group", "label": "Nhóm sản phẩm", "expr": "ten"},
        ],
        "san-pham": [
            {"param": "group", "label": "Nhóm sản phẩm", "expr": "nhom_san_pham__ten"},
            {"param": "supplier", "label": "Nhà cung cấp", "expr": "nha_cung_cap__ten"},
            {"param": "brand", "label": "Thương hiệu", "expr": "thuong_hieu__ten"},
        ],
        "giao-dich-kho": [
            {"param": "product", "label": "Sản phẩm", "expr": "san_pham__ten"},
            {"param": "type", "label": "Loại giao dịch", "expr": "loai"},
            {"param": "staff", "label": "Nhân viên ký", "expr": "nhan_vien__ho_ten"},
        ],
        "chuoi-cua-hang": [
            {"param": "chain", "label": "Chuỗi cửa hàng", "expr": "ten"},
        ],
        "cua-hang": [
            {"param": "chain", "label": "Chuỗi cửa hàng", "expr": "chuoi__ten"},
            {"param": "district", "label": "Quận/Huyện", "expr": "quan_huyen"},
            {"param": "open24", "label": "Hoạt động", "bool_expr": "hoat_dong_24h"},
        ],
        "nhan-vien": [
            {"param": "role", "label": "Chức vụ", "expr": "chuc_vu"},
            {"param": "store", "label": "Cửa hàng", "expr": "cua_hang__ten"},
        ],
        "khuyen-mai": [
            {"param": "promo", "label": "Khuyến mãi", "expr": "ten"},
        ],
        "gop-y-khach-hang": [
            {"param": "topic", "label": "Chủ đề", "expr": "chu_de"},
            {"param": "responded", "label": "Đã phản hồi", "bool_expr": "da_phan_hoi"},
        ],
        "ho-so-khach-hang": [
            {"param": "user", "label": "Tài khoản", "expr": "user__username"},
            {"param": "district", "label": "Quận/Huyện", "custom": "district_from_address", "address_expr": "dia_chi"},
        ],
        "don-hang": [],
        "chi-tiet-don-hang": [
            {"param": "order", "label": "Đơn hàng", "expr": "don_hang__id"},
            {"param": "group", "label": "Nhóm sản phẩm", "expr": "san_pham__nhom_san_pham__ten"},
        ],
    }.get(model_slug, [])


def _build_and_apply_facets(request, model_slug, qs, model):
    facet_filters = []
    specs = _facet_specs_for_model(model_slug)
    if not specs:
        return qs, facet_filters

    for spec in specs:
        param = spec["param"]
        selected = [v for v in request.GET.getlist(param) if str(v).strip()]

        if spec.get("bool_expr"):
            expr = spec["bool_expr"]
            options = [
                {"value": "1", "label": "Có", "selected": "1" in selected},
                {"value": "0", "label": "Không", "selected": "0" in selected},
            ]
            if selected:
                bool_values = []
                if "1" in selected:
                    bool_values.append(True)
                if "0" in selected:
                    bool_values.append(False)
                if bool_values:
                    qs = qs.filter(**{f"{expr}__in": bool_values})
            facet_filters.append(
                {
                    "param": param,
                    "label": spec["label"],
                    "options": options,
                    "selected_count": len([x for x in selected if x in {"1", "0"}]),
                }
            )
            continue

        if spec.get("custom") == "ai_product_category":
            all_products = list(model.objects.select_related("nhom_san_pham").all())
            categories = []
            by_id = {}
            for product in all_products:
                cat = _infer_product_ai_category(product)
                by_id[product.pk] = cat
                categories.append(cat)
            unique_cats = sorted(set(categories))
            options = [{"value": cat, "label": cat, "selected": cat in selected} for cat in unique_cats]
            if selected:
                allowed_ids = [pk for pk, cat in by_id.items() if cat in selected]
                qs = qs.filter(pk__in=allowed_ids)
            facet_filters.append(
                {
                    "param": param,
                    "label": spec["label"],
                    "options": options,
                    "selected_count": len(selected),
                }
            )
            continue

        if spec.get("custom") == "district_from_address":
            address_field = spec.get("address_expr")
            all_rows = list(model.objects.all().only("pk", address_field))
            district_by_id = {}
            districts = []
            for row in all_rows:
                district = _extract_district_from_address(getattr(row, address_field, ""))
                district_by_id[row.pk] = district
                if district:
                    districts.append(district)
            unique_districts = sorted(set(districts))
            options = [{"value": d, "label": d, "selected": d in selected} for d in unique_districts]
            if selected:
                allowed_ids = [pk for pk, district in district_by_id.items() if district in selected]
                qs = qs.filter(pk__in=allowed_ids)
            facet_filters.append(
                {
                    "param": param,
                    "label": spec["label"],
                    "options": options,
                    "selected_count": len(selected),
                }
            )
            continue

        expr = spec["expr"]
        values = list(
            model.objects.order_by(expr).values_list(expr, flat=True).distinct()
        )
        values = [str(v) for v in values if v not in (None, "")]
        options = [{"value": v, "label": _strip_parenthetical_text(v), "selected": v in selected} for v in values[:120]]
        if selected:
            qs = qs.filter(**{f"{expr}__in": selected})
        facet_filters.append(
            {
                "param": param,
                "label": spec["label"],
                "options": options,
                "selected_count": len(selected),
            }
        )

    return qs, facet_filters


def admin_list(request, model_slug):
    unauthorized = _require_module_permission(request, model_slug, "view")
    if unauthorized:
        return unauthorized

    _purge_expired_trash()

    pref = _admin_pref_context(request)
    lang = pref["admin_lang"]

    model = _resolve_model(model_slug)
    query = request.GET.get("q", "").strip()
    filter_field = request.GET.get("f", "").strip()
    status_filters = [
        value
        for value in request.GET.getlist("status")
        if value in {"pending", "confirmed", "shipping", "delivered", "done", "cancelled"}
    ]
    status_filter = status_filters[0] if len(status_filters) == 1 else ""
    qs = model.objects.all().order_by("-pk")
    qs, facet_filters = _build_and_apply_facets(request, model_slug, qs, model)
    if model_slug == "don-hang" and status_filters:
        selected_statuses = set(status_filters)
        final_statuses = set()
        if "done" in selected_statuses:
            final_statuses.update({"done", "delivered"})
        if "delivered" in selected_statuses:
            final_statuses.add("delivered")
        final_statuses.update(selected_statuses - {"done", "delivered"})
        qs = qs.filter(trang_thai__in=sorted(final_statuses))
    if query:
        valid_fields = {
            f.name
            for f in model._meta.fields
            if f.name != "id" and f.get_internal_type() not in {"ImageField", "FileField"}
        }
        if filter_field and filter_field not in valid_fields:
            filter_field = ""
        if filter_field:
            field_obj = model._meta.get_field(filter_field)
            field_type = field_obj.get_internal_type()
            if field_type in {"CharField", "TextField", "EmailField", "SlugField"}:
                qs = qs.filter(**{f"{filter_field}__icontains": query})
            elif field_type in {
                "IntegerField",
                "PositiveIntegerField",
                "BigIntegerField",
                "AutoField",
                "BigAutoField",
                "SmallIntegerField",
                "PositiveSmallIntegerField",
            }:
                try:
                    qs = qs.filter(**{filter_field: int(query)})
                except Exception:
                    qs = qs.none()
            elif field_type in {"DecimalField", "FloatField"}:
                try:
                    qs = qs.filter(**{filter_field: Decimal(query)})
                except Exception:
                    qs = qs.none()
            elif field_type == "BooleanField":
                truthy = {"1", "true", "yes", "on", "có", "co"}
                falsy = {"0", "false", "no", "off", "không", "khong"}
                q_lower = query.lower()
                if q_lower in truthy:
                    qs = qs.filter(**{filter_field: True})
                elif q_lower in falsy:
                    qs = qs.filter(**{filter_field: False})
                else:
                    qs = qs.none()
            elif field_type in {"DateField", "DateTimeField"}:
                dt_value = parse_datetime(query) or parse_date(query)
                if dt_value:
                    qs = qs.filter(**{filter_field: dt_value})
                else:
                    qs = qs.none()
            else:
                qs = qs.none()
        else:
            text_fields = [f.name for f in model._meta.fields if f.get_internal_type() in {"CharField", "TextField"}]
            if text_fields:
                from django.db.models import Q

                conditions = Q()
                for field_name in text_fields:
                    conditions |= Q(**{f"{field_name}__icontains": query})
                qs = qs.filter(conditions)

    fields = [
        {"name": f.name, "verbose_name": _field_label(f, lang), "type": f.get_internal_type()}
        for f in model._meta.fields
        if f.name != "id"
    ]
    filter_fields = [
        {"name": f["name"], "verbose_name": f["verbose_name"]}
        for f in fields
        if f["type"] not in {"ImageField", "FileField"}
    ]
    paginator = Paginator(qs, 15)
    page_obj = paginator.get_page(request.GET.get("page"))
    persisted_params = []
    for key in request.GET.keys():
        if key == "page":
            continue
        for value in request.GET.getlist(key):
            if value != "":
                persisted_params.append((key, value))
    persisted_query = urlencode(persisted_params, doseq=True)

    can_create = _has_module_access(request.user, model_slug, "create")
    can_update = _has_module_access(request.user, model_slug, "update")
    can_delete = _has_module_access(request.user, model_slug, "delete")
    can_change_order_status = _has_module_access(request.user, model_slug, "status")
    can_change_payment_status = _has_module_access(request.user, model_slug, "payment_status")
    can_print_inventory = _has_module_access(request.user, model_slug, "print")

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
                        cell_type = "image"
                        if model_slug == "giao-dich-kho" and field["name"] == "chu_ky":
                            cell_type = "signature"
                        values.append({"type": cell_type, "url": raw_value.url, "text": str(raw_value)})
                    except Exception:
                        values.append({"type": "text", "text": str(raw_value)})
                else:
                    values.append({"type": "text", "text": ""})
            elif field_type == "BooleanField":
                values.append({"type": "bool", "value": bool(raw_value)})
            elif field["name"] in {"trang_thai"}:
                display = str(raw_value)
                try:
                    display = getattr(item, f"get_{field['name']}_display")()
                except Exception:
                    pass
                values.append({"type": "status", "value": str(raw_value), "text": display})
            elif model_slug == "don-hang" and field["name"] == "trang_thai_thanh_toan":
                display = str(raw_value)
                try:
                    display = item.get_trang_thai_thanh_toan_display()
                except Exception:
                    pass
                payment_level = "low"
                if raw_value == "paid":
                    payment_level = "ok"
                elif raw_value == "refunded":
                    payment_level = "out"
                values.append({"type": "stock", "level": payment_level, "text": display})
            elif field["name"] in {"gia_ban", "tong_tien", "don_gia"}:
                values.append({"type": "money", "text": _format_currency(raw_value)})
            elif model_slug == "don-hang" and field["name"] == "giam_gia":
                values.append({"type": "money", "text": _format_currency(raw_value)})
            elif model_slug == "don-hang" and field["name"] == "ma_voucher_ap_dung":
                values.append(
                    {
                        "type": "stock_move",
                        "level": "import" if raw_value else "export",
                        "text": str(raw_value) if raw_value else "Không áp dụng",
                    }
                )
            elif model_slug == "don-hang" and field["name"] == "phuong_thuc_thanh_toan":
                display = str(raw_value)
                try:
                    display = item.get_phuong_thuc_thanh_toan_display()
                except Exception:
                    pass
                level = "info"
                if raw_value == "cod":
                    level = "export"
                elif raw_value == "bank_transfer":
                    level = "import"
                elif raw_value == "momo":
                    level = "low"
                values.append({"type": "stock_move", "level": level, "text": display})
            elif model_slug == "don-hang" and field["name"] in {"vi_do_giao_hang", "kinh_do_giao_hang"}:
                if raw_value is None:
                    values.append({"type": "text", "text": "-"})
                else:
                    values.append({"type": "text", "text": f"{float(raw_value):.6f}"})
            elif model_slug == "san-pham" and field["name"] == "ton_kho":
                stock_value = int(raw_value or 0)
                if stock_value <= 0:
                    values.append({"type": "stock", "level": "out", "text": "Hết hàng"})
                elif stock_value <= SanPham.LOW_STOCK_THRESHOLD:
                    values.append({"type": "stock", "level": "low", "text": f"Sắp hết ({stock_value})"})
                else:
                    values.append({"type": "stock", "level": "ok", "text": f"Còn {stock_value}"})
            elif model_slug == "giao-dich-kho" and field["name"] == "loai":
                values.append(
                    {
                        "type": "stock_move",
                        "level": "import" if raw_value == "import" else "export",
                        "text": "Nhập kho" if raw_value == "import" else "Xuất kho",
                    }
                )
            else:
                values.append({"type": "text", "text": _strip_parenthetical_text(raw_value)})
        row = {
            "object": item,
            "values": values,
            "can_edit": can_update,
            "can_delete": can_delete,
            "can_change_status": can_change_order_status,
            "can_change_payment_status": can_change_payment_status,
            "can_review_receipt": False,
        }
        if model_slug == "don-hang":
            status_actions = []
            payment_actions = []
            receipt_actions = []
            if can_change_order_status and item.trang_thai == "pending":
                status_actions.append({"value": "confirmed", "label": pref["t"]["confirm_order"]})
                status_actions.append({"value": "cancelled", "label": pref["t"]["cancel_order"]})
            elif can_change_order_status and item.trang_thai == "confirmed":
                status_actions.append({"value": "shipping", "label": pref["t"]["ship_order"]})
                status_actions.append({"value": "cancelled", "label": pref["t"]["cancel_order"]})
            elif can_change_order_status and item.trang_thai == "shipping":
                status_actions.append({"value": "delivered", "label": pref["t"]["deliver_order"]})
                status_actions.append({"value": "cancelled", "label": pref["t"]["cancel_order"]})
            elif item.trang_thai == "delivered":
                status_actions.append({"value": "done", "label": pref["t"]["complete_order"]})
            row["status_actions"] = status_actions
            if can_change_payment_status and item.trang_thai_thanh_toan == "unpaid":
                payment_actions.append({"value": "paid", "label": "Đánh dấu đã thanh toán"})
                if item.phuong_thuc_thanh_toan == "bank_transfer":
                    payment_actions.append({"value": "awaiting_confirmation", "label": "Chờ xác nhận CK"})
            elif can_change_payment_status and item.trang_thai_thanh_toan == "awaiting_confirmation":
                payment_actions.append({"value": "paid", "label": "Xác nhận đã nhận tiền"})
                payment_actions.append({"value": "unpaid", "label": "Trả về chưa thanh toán"})
            elif can_change_payment_status and item.trang_thai_thanh_toan == "paid":
                payment_actions.append({"value": "refunded", "label": "Hoàn tiền"})
            row["payment_actions"] = payment_actions
            if (
                can_change_payment_status
                and item.phuong_thuc_thanh_toan == "bank_transfer"
                and bool(item.anh_bien_lai)
                and item.trang_thai_thanh_toan in {"awaiting_confirmation", "unpaid"}
            ):
                receipt_actions = [
                    {"value": "approve", "label": "Duyệt biên lai"},
                    {"value": "reject", "label": "Từ chối biên lai"},
                ]
                row["receipt_preview_url"] = item.anh_bien_lai.url
            row["receipt_actions"] = receipt_actions
            row["can_review_receipt"] = bool(receipt_actions)
        if model_slug == "giao-dich-kho" and can_print_inventory and item.loai == "import":
            row["print_url"] = reverse("store:admin_inventory_print", args=[item.pk])
            row["pdf_url"] = reverse("store:admin_inventory_pdf", args=[item.pk])
        if (
            model_slug == "don-hang"
            and item.vi_do_giao_hang is not None
            and item.kinh_do_giao_hang is not None
        ):
            row["map_url"] = (
                "https://www.google.com/maps/search/?api=1"
                f"&query={float(item.vi_do_giao_hang):.6f},{float(item.kinh_do_giao_hang):.6f}"
            )
        rows.append(row)

    return render(
        request,
        "admin/change_list.html",
        {
            "modules": _menu_context(lang, request.user),
            "model_slug": model_slug,
            "model_name": _model_label(model_slug, lang, plural=True),
            "fields": fields,
            "filter_fields": filter_fields,
            "rows": rows,
            "query": query,
            "filter_field": filter_field,
            "status_filter": status_filter,
            "status_filters": status_filters,
            "page_obj": page_obj,
            "paginator": paginator,
            "facet_filters": facet_filters,
            "persisted_query": persisted_query,
            "show_create": can_create,
            **pref,
        },
    )


def admin_create(request, model_slug):
    unauthorized = _require_module_permission(request, model_slug, "create")
    if unauthorized:
        return unauthorized

    pref = _admin_pref_context(request)
    lang = pref["admin_lang"]

    model = _resolve_model(model_slug)
    form_cls = _admin_form_class_for_model(model_slug, model)
    coord_picker_enabled = model_slug == "cua-hang"
    if request.method == "POST":
        form = _sanitize_admin_form(form_cls(request.POST, request.FILES))
        valid = _validate_coord_from_map(request, form) if coord_picker_enabled else form.is_valid()
        if valid:
            obj = form.save(commit=False) if model_slug == "giao-dich-kho" else form.save()
            if model_slug == "giao-dich-kho":
                obj.created_by = request.user
                obj.save()
            if model_slug == "san-pham":
                _save_product_gallery(obj, request.FILES, request.POST)
            messages.success(request, pref["t"]["saved_successfully"])
            return redirect("store:admin_list", model_slug=model_slug)
    else:
        form = _sanitize_admin_form(form_cls())

    return render(
        request,
        "admin/change_form.html",
        {
            "modules": _menu_context(lang, request.user),
            "form": form,
            "model_slug": model_slug,
            "model_name": _model_label(model_slug, lang, plural=False),
            "mode": "create",
            "file_previews": _build_product_image_preview_context() if model_slug == "san-pham" else _build_file_preview_context(model),
            "coord_picker_enabled": coord_picker_enabled,
            **pref,
        },
    )


def admin_update(request, model_slug, pk):
    unauthorized = _require_module_permission(request, model_slug, "update")
    if unauthorized:
        return unauthorized

    pref = _admin_pref_context(request)
    lang = pref["admin_lang"]

    model = _resolve_model(model_slug)
    obj = get_object_or_404(model, pk=pk)
    form_cls = _admin_form_class_for_model(model_slug, model)
    coord_picker_enabled = model_slug == "cua-hang"

    if request.method == "POST":
        form = _sanitize_admin_form(form_cls(request.POST, request.FILES, instance=obj))
        valid = _validate_coord_from_map(request, form, instance=obj) if coord_picker_enabled else form.is_valid()
        if valid:
            obj = form.save(commit=False) if model_slug == "giao-dich-kho" else form.save()
            if model_slug == "giao-dich-kho":
                if not obj.created_by_id:
                    obj.created_by = request.user
                obj.save()
            if model_slug == "san-pham":
                _save_product_gallery(obj, request.FILES, request.POST)
            messages.success(request, pref["t"]["saved_successfully"])
            return redirect("store:admin_list", model_slug=model_slug)
    else:
        form = _sanitize_admin_form(form_cls(instance=obj))

    return render(
        request,
        "admin/change_form.html",
        {
            "modules": _menu_context(lang, request.user),
            "form": form,
            "model_slug": model_slug,
            "model_name": _model_label(model_slug, lang, plural=False),
            "mode": "update",
            "object": obj,
            "file_previews": _build_product_image_preview_context(obj) if model_slug == "san-pham" else _build_file_preview_context(model, obj),
            "coord_picker_enabled": coord_picker_enabled,
            **pref,
        },
    )


def admin_delete(request, model_slug, pk):
    unauthorized = _require_module_permission(request, model_slug, "delete")
    if unauthorized:
        return unauthorized

    _purge_expired_trash()

    pref = _admin_pref_context(request)
    lang = pref["admin_lang"]

    model = _resolve_model(model_slug)
    obj = get_object_or_404(model, pk=pk)
    if request.method == "POST":
        try:
            trash_data = _serialize_for_trash(obj)
            obj.delete()
            _move_to_trash(obj, data=trash_data)
            messages.success(request, pref["t"]["deleted_successfully"])
        except ValidationError as exc:
            messages.error(request, "; ".join(exc.messages) or "Không thể xóa bản ghi này.")
            return redirect("store:admin_list", model_slug=model_slug)
        return redirect("store:admin_list", model_slug=model_slug)

    return render(
        request,
        "admin/delete_confirmation.html",
        {
            "modules": _menu_context(lang, request.user),
            "model_slug": model_slug,
            "model_name": _model_label(model_slug, lang, plural=False),
            "object": obj,
            **pref,
        },
    )


def admin_trash_list(request):
    unauthorized = _require_admin_permission(request, "trash")
    if unauthorized:
        return unauthorized

    _purge_expired_trash()
    pref = _admin_pref_context(request)
    lang = pref["admin_lang"]
    query = request.GET.get("q", "").strip()
    filter_field = request.GET.get("f", "").strip()

    all_rows = []
    for item in TrashRecord.objects.all():
        model_slug = _model_slug_from_label(item.model_label)
        all_rows.append(
            {
                "id": item.pk,
                "object_id": str(item.object_id),
                "model_name": _model_label(model_slug, lang, plural=False),
                "display_name": _trash_display_name(item.data or {}, item.model_label) or "-",
                "deleted_at": item.deleted_at,
                "expires_at": item.expires_at,
            }
        )

    fields = [
        {"name": "model_name", "verbose_name": "Module"},
        {"name": "display_name", "verbose_name": "Tên"},
        {"name": "deleted_at", "verbose_name": pref["t"]["deleted_at"]},
        {"name": "expires_at", "verbose_name": pref["t"]["expires_at"]},
    ]

    valid_fields = {f["name"] for f in fields}
    if filter_field not in valid_fields:
        filter_field = ""

    if query and filter_field:
        q_lower = query.lower()
        all_rows = [
            row
            for row in all_rows
            if q_lower in str(row.get(filter_field, "")).lower()
        ]
    elif query:
        q_lower = query.lower()
        all_rows = [
            row
            for row in all_rows
            if any(q_lower in str(row.get(name, "")).lower() for name in valid_fields)
        ]

    paginator = Paginator(all_rows, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    rows = []
    for item in page_obj.object_list:
        rows.append(
            {
                "id": item["id"],
                "object_id": item["object_id"],
                "model_name": item["model_name"],
                "display_name": item["display_name"],
                "deleted_at": item["deleted_at"],
                "expires_at": item["expires_at"],
                "restore_url": reverse("store:admin_trash_restore", args=[item["id"]]),
                "delete_url": reverse("store:admin_trash_delete", args=[item["id"]]),
            }
        )

    return render(
        request,
        "admin/trash_list.html",
        {
            "modules": _menu_context(lang, request.user),
            "model_slug": "trash",
            "model_name": pref["t"]["trash"],
            "fields": fields,
            "rows": rows,
            "query": query,
            "filter_field": filter_field,
            "status_filter": "",
            "page_obj": page_obj,
            "paginator": paginator,
            "trash_retention_days": getattr(settings, "TRASH_RETENTION_DAYS", 15),
            "show_create": False,
            **pref,
        },
    )


def admin_trash_restore(request, pk):
    unauthorized = _require_admin_permission(request, "trash", "restore")
    if unauthorized:
        return unauthorized

    _purge_expired_trash()
    pref = _admin_pref_context(request)
    trash = get_object_or_404(TrashRecord, pk=pk)
    try:
        model = apps.get_model(trash.model_label)
        payload = dict(trash.data or {})
        normalized = {}
        for field in model._meta.fields:
            name = field.name
            if name not in payload:
                continue
            value = payload.get(name)
            if isinstance(field, dj_models.ForeignKey):
                if value in ("", None):
                    if field.null:
                        normalized[field.attname] = None
                        continue
                    raise ValueError("missing_fk")
                if not field.remote_field.model.objects.filter(pk=value).exists():
                    if field.null:
                        normalized[field.attname] = None
                        continue
                    raise ValueError("fk_not_found")
                normalized[field.attname] = value
                continue
            field_type = field.get_internal_type()
            if field_type in {"DateTimeField"} and isinstance(value, str):
                normalized[name] = parse_datetime(value) or value
            elif field_type in {"DateField"} and isinstance(value, str):
                normalized[name] = parse_date(value) or value
            elif field_type in {"DecimalField"} and value not in (None, ""):
                normalized[name] = Decimal(str(value))
            elif field_type in {
                "IntegerField",
                "PositiveIntegerField",
                "BigIntegerField",
                "AutoField",
                "BigAutoField",
                "SmallIntegerField",
                "PositiveSmallIntegerField",
            } and value not in (None, ""):
                normalized[name] = int(value)
            elif field_type == "BooleanField":
                if isinstance(value, str):
                    normalized[name] = value.lower() in {"1", "true", "yes", "on", "có", "co"}
                else:
                    normalized[name] = bool(value)
            else:
                normalized[name] = value

        pk_value = trash.object_id
        if pk_value:
            pk_field = model._meta.pk
            if pk_field.get_internal_type() in {"AutoField", "BigAutoField", "IntegerField", "PositiveIntegerField"}:
                try:
                    pk_value = int(pk_value)
                except Exception:
                    pass
        instance = model(**normalized)
        if pk_value and not model.objects.filter(pk=pk_value).exists():
            instance.pk = pk_value
        instance.save()
        trash.delete()
        messages.success(request, pref["t"]["saved_successfully"])
    except Exception:
        messages.error(request, "Không thể khôi phục bản ghi. Vui lòng kiểm tra dữ liệu.")
    return redirect("store:admin_trash")


def admin_trash_delete(request, pk):
    unauthorized = _require_admin_permission(request, "trash", "delete")
    if unauthorized:
        return unauthorized

    _purge_expired_trash()
    pref = _admin_pref_context(request)
    trash = get_object_or_404(TrashRecord, pk=pk)
    trash.delete()
    messages.success(request, pref["t"]["deleted_successfully"])
    return redirect("store:admin_trash")


def admin_notifications(request):
    unauthorized = _require_admin_permission(request, "notifications")
    if unauthorized:
        return unauthorized

    pref = _admin_pref_context(request)
    lang = pref["admin_lang"]
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "delete_selected":
            ids = [int(i) for i in request.POST.getlist("selected_ids") if str(i).isdigit()]
            if ids:
                Notification.objects.filter(pk__in=ids).delete()
                messages.success(request, pref["t"]["deleted_successfully"])
            else:
                messages.warning(request, "Vui lòng chọn ít nhất một thông báo.")
            return redirect("store:admin_notifications")
    # mark all as seen when opening notifications
    Notification.objects.filter(resolved=False).update(resolved=True)
    qs = Notification.objects.all()
    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "admin/notifications.html",
        {
            "modules": _menu_context(lang, request.user),
            "page_obj": page_obj,
            "paginator": paginator,
            **pref,
        },
    )


def admin_inventory_print(request, pk):
    unauthorized = _require_module_permission(request, "giao-dich-kho", "print")
    if unauthorized:
        return unauthorized

    movement = get_object_or_404(
        GiaoDichKho.objects.select_related(
            "san_pham",
            "nhan_vien",
            "nhan_vien__cua_hang",
            "nhan_vien__cua_hang__chuoi",
            "created_by",
        ),
        pk=pk,
        loai="import",
    )
    document_code = f"PNK-{movement.pk}"
    barcode_svg = ""
    qr_svg = ""
    lookup_url = request.build_absolute_uri(reverse("store:admin_inventory_print", args=[movement.pk]))
    try:
        from reportlab.graphics import renderSVG
        from reportlab.graphics.barcode import createBarcodeDrawing
        from reportlab.graphics.shapes import Drawing
        from reportlab.graphics.barcode.qr import QrCodeWidget

        barcode_svg = renderSVG.drawToString(
            createBarcodeDrawing(
                "Code128",
                value=document_code,
                barHeight=42,
                barWidth=1.1,
                humanReadable=True,
            )
        )
        if isinstance(barcode_svg, bytes):
            barcode_svg = barcode_svg.decode("utf-8")
        qr_widget = QrCodeWidget(lookup_url)
        bounds = qr_widget.getBounds()
        qr_width = bounds[2] - bounds[0]
        qr_height = bounds[3] - bounds[1]
        qr_drawing = Drawing(88, 88, transform=[88 / qr_width, 0, 0, 88 / qr_height, 0, 0])
        qr_drawing.add(qr_widget)
        qr_svg = renderSVG.drawToString(qr_drawing)
        if isinstance(qr_svg, bytes):
            qr_svg = qr_svg.decode("utf-8")
    except Exception:
        barcode_svg = ""
        qr_svg = ""

    return render(
        request,
        "admin/inventory_print.html",
        {
            "movement": movement,
            "document_code": document_code,
            "barcode_svg": barcode_svg,
            "qr_svg": qr_svg,
            "lookup_url": lookup_url,
            "generated_at": timezone.now(),
        },
    )


def admin_inventory_pdf(request, pk):
    unauthorized = _require_module_permission(request, "giao-dich-kho", "print")
    if unauthorized:
        return unauthorized

    movement = get_object_or_404(
        GiaoDichKho.objects.select_related(
            "san_pham",
            "nhan_vien",
            "nhan_vien__cua_hang",
            "created_by",
        ),
        pk=pk,
        loai="import",
    )

    try:
        from reportlab.graphics import renderPDF
        from reportlab.graphics.barcode import createBarcodeDrawing
        from reportlab.graphics.barcode.qr import QrCodeWidget
        from reportlab.graphics.shapes import Drawing
        from reportlab.lib.colors import HexColor
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.utils import ImageReader, simpleSplit
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.pdfgen import canvas
    except Exception:
        messages.error(request, "Chưa cài thư viện xuất PDF. Hãy cài reportlab để dùng tính năng này.")
        return redirect("store:admin_inventory_print", pk=movement.pk)

    def resolve_font_names():
        regular_name = "InventoryUnicode"
        bold_name = "InventoryUnicodeBold"
        registered = set(pdfmetrics.getRegisteredFontNames())
        if regular_name in registered and bold_name in registered:
            return regular_name, bold_name

        candidates = [
            ("C:\\Windows\\Fonts\\arial.ttf", "C:\\Windows\\Fonts\\arialbd.ttf"),
            ("C:\\Windows\\Fonts\\tahoma.ttf", "C:\\Windows\\Fonts\\tahomabd.ttf"),
            ("C:\\Windows\\Fonts\\segoeui.ttf", "C:\\Windows\\Fonts\\segoeuib.ttf"),
        ]
        for regular_path, bold_path in candidates:
            if not (os.path.exists(regular_path) and os.path.exists(bold_path)):
                continue
            if regular_name not in registered:
                pdfmetrics.registerFont(TTFont(regular_name, regular_path))
                registered.add(regular_name)
            if bold_name not in registered:
                pdfmetrics.registerFont(TTFont(bold_name, bold_path))
                registered.add(bold_name)
            return regular_name, bold_name
        return "Helvetica", "Helvetica-Bold"

    font_regular, font_bold = resolve_font_names()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="phieu-nhap-kho-{movement.pk}.pdf"'

    pdf = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    margin = 40
    cursor_y = height - margin

    def line(text, x, y, font=None, size=11, color="#102a43"):
        pdf.setFillColor(HexColor(color))
        pdf.setFont(font or font_regular, size)
        pdf.drawString(x, y, text)

    def draw_block(x, y_top, w, h, *, title="", fill="#ffffff", stroke="#d9e2ec", title_color="#0f766e"):
        pdf.setStrokeColor(HexColor(stroke))
        pdf.setFillColor(HexColor(fill))
        pdf.roundRect(x, y_top - h, w, h, 14, stroke=1, fill=1)
        if title:
            line(title, x + 14, y_top - 18, font=font_bold, size=11, color=title_color)

    def draw_label_value(x, y, label, value, *, value_font=None, value_size=11):
        line(label, x, y, font=font_bold, size=10, color="#627d98")
        wrapped = simpleSplit(str(value or "-"), value_font or font_regular, value_size, 210)
        cursor = y - 16
        for item in wrapped[:3]:
            line(item, x, cursor, font=value_font or font_regular, size=value_size, color="#102a43")
            cursor -= 14
        return cursor

    def draw_table_row(x, y_top, col_widths, values, *, fill="#ffffff", stroke="#d9e2ec", bold=False, text_color="#102a43"):
        row_height = 34
        current_x = x
        pdf.setStrokeColor(HexColor(stroke))
        for idx, width_item in enumerate(col_widths):
            pdf.setFillColor(HexColor(fill))
            pdf.rect(current_x, y_top - row_height, width_item, row_height, stroke=1, fill=1)
            cell_text = str(values[idx])
            text_width = width_item - 16
            wrapped = simpleSplit(cell_text, font_bold if bold else font_regular, 10, text_width)
            text_y = y_top - 14
            for part in wrapped[:2]:
                line(part, current_x + 8, text_y, font=font_bold if bold else font_regular, size=10, color=text_color)
                text_y -= 11
            current_x += width_item
        return y_top - row_height

    pdf.setTitle(f"Phiếu nhập kho #{movement.pk}")
    document_code = f"PNK-{movement.pk}"
    lookup_url = request.build_absolute_uri(reverse("store:admin_inventory_print", args=[movement.pk]))

    header_height = 88
    pdf.setFillColor(HexColor("#0f766e"))
    pdf.roundRect(margin, cursor_y - header_height, width - (margin * 2), header_height, 18, stroke=0, fill=1)
    line("SMARTGIS", margin + 18, cursor_y - 28, font=font_bold, size=24, color="#ffffff")
    line("PHIEU NHAP KHO NOI BO", margin + 18, cursor_y - 50, font=font_bold, size=12, color="#d1fae5")
    line(f"So phieu: {document_code}", width - 180, cursor_y - 28, font=font_bold, size=13, color="#ffffff")
    line(f"Ngay in: {timezone.now().strftime('%d/%m/%Y %H:%M')}", width - 180, cursor_y - 48, size=10, color="#d1fae5")
    cursor_y -= header_height + 20

    draw_block(margin, cursor_y, width - (margin * 2), 110, title="Thong tin chung", fill="#f8fbfc")
    left_x = margin + 16
    right_x = margin + 280
    left_cursor = draw_label_value(left_x, cursor_y - 38, "San pham", movement.san_pham.ten, value_font=font_bold, value_size=12)
    left_cursor = draw_label_value(left_x, left_cursor - 4, "Nhan vien ky", movement.nhan_vien.ho_ten if movement.nhan_vien else "-")
    draw_label_value(left_x, left_cursor - 4, "Cua hang", movement.nhan_vien.cua_hang.ten if movement.nhan_vien and movement.nhan_vien.cua_hang else "-")
    right_cursor = draw_label_value(right_x, cursor_y - 38, "Nguoi tao", movement.created_by.username if movement.created_by else "-")
    right_cursor = draw_label_value(right_x, right_cursor - 4, "Thoi gian tao", movement.created_at.strftime("%d/%m/%Y %H:%M"))
    draw_label_value(right_x, right_cursor - 4, "Loai giao dich", "Nhap kho")
    cursor_y -= 130

    draw_block(margin, cursor_y, width - (margin * 2), 92, title="Tong hop so lieu", fill="#fff7ed", stroke="#fdba74", title_color="#c2410c")
    table_x = margin + 16
    table_y = cursor_y - 30
    col_widths = [150, 110, 110, 110]
    table_y = draw_table_row(table_x, table_y, col_widths, ["Chi muc", "So luong", "Ton truoc", "Ton sau"], fill="#ffedd5", stroke="#fdba74", bold=True, text_color="#9a3412")
    draw_table_row(
        table_x,
        table_y,
        col_widths,
        ["Nhap kho", str(movement.so_luong), str(movement.ton_truoc), str(movement.ton_sau)],
        fill="#ffffff",
        stroke="#fed7aa",
    )
    cursor_y -= 112

    barcode_block_height = 94
    draw_block(margin, cursor_y, width - (margin * 2), barcode_block_height, title="Ma tra cuu", fill="#f8fbfc")
    line("Nhap ma nay de tra cuu nhanh phieu trong he thong.", margin + 16, cursor_y - 34, size=10, color="#627d98")
    try:
        barcode = createBarcodeDrawing(
            "Code128",
            value=document_code,
            barHeight=28,
            barWidth=1.05,
            humanReadable=True,
        )
        renderPDF.draw(barcode, pdf, margin + 16, cursor_y - 84)
    except Exception:
        line(document_code, margin + 16, cursor_y - 64, font=font_bold, size=16, color="#0f172a")
    cursor_y -= barcode_block_height + 18

    qr_block_height = 120
    draw_block(margin, cursor_y, width - (margin * 2), qr_block_height, title="QR mo phieu", fill="#f8fbfc")
    line("Quet QR de mo thang phieu in trong he thong.", margin + 16, cursor_y - 34, size=10, color="#627d98")
    try:
        qr_widget = QrCodeWidget(lookup_url)
        bounds = qr_widget.getBounds()
        qr_width = bounds[2] - bounds[0]
        qr_height = bounds[3] - bounds[1]
        qr_drawing = Drawing(78, 78, transform=[78 / qr_width, 0, 0, 78 / qr_height, 0, 0])
        qr_drawing.add(qr_widget)
        renderPDF.draw(qr_drawing, pdf, margin + 18, cursor_y - 104)
    except Exception:
        line("Khong tao duoc QR", margin + 20, cursor_y - 72, size=10, color="#9b1c1c")
    wrapped_lookup = simpleSplit(lookup_url, font_regular, 9, width - (margin * 2) - 130)
    qr_text_y = cursor_y - 54
    for lookup_line in wrapped_lookup[:3]:
        line(lookup_line, margin + 118, qr_text_y, size=9, color="#334e68")
        qr_text_y -= 13
    cursor_y -= qr_block_height + 18

    note_height = 94
    draw_block(margin, cursor_y, width - (margin * 2), note_height, title="Ghi chu", fill="#fbfdff")
    note = (movement.ghi_chu or "Khong co ghi chu.").strip()
    note_lines = simpleSplit(note, font_regular, 11, width - (margin * 2) - 32)
    note_y = cursor_y - 36
    for note_line in note_lines[:4]:
        line(note_line, margin + 16, note_y, size=11)
        note_y -= 15
    cursor_y -= note_height + 18

    signature_top = cursor_y
    draw_block(margin, signature_top, 250, 150, title="Chu ky nhan vien", fill="#fcfdff")
    pdf.roundRect(margin + 16, signature_top - 128, 218, 90, 10, stroke=1, fill=0)
    if movement.chu_ky:
        try:
            signature = ImageReader(movement.chu_ky.path)
            pdf.drawImage(signature, margin + 24, signature_top - 120, width=200, height=74, preserveAspectRatio=True, mask="auto")
        except Exception:
            line("Khong the tai anh chu ky", margin + 28, signature_top - 82, size=10, color="#9b1c1c")
    else:
        line("Chua co chu ky", margin + 28, signature_top - 82, size=10, color="#627d98")

    draw_block(margin + 268, signature_top, width - margin - (margin + 268), 150, title="Xac nhan", fill="#f8fafc")
    line("Nhan vien ky", margin + 286, signature_top - 48, font=font_bold, size=11, color="#334e68")
    line(movement.nhan_vien.ho_ten if movement.nhan_vien else "-", margin + 286, signature_top - 66, size=11)
    line("Nguoi lap phieu", margin + 286, signature_top - 96, font=font_bold, size=11, color="#334e68")
    line(movement.created_by.username if movement.created_by else "-", margin + 286, signature_top - 114, size=11)

    line("Chung tu duoc tao tu he thong SmartGIS.", margin, 32, size=9, color="#627d98")
    line("Vui long doi chieu thong tin hang hoa va luu kem chu ky khi can.", width - 245, 32, size=9, color="#627d98")

    pdf.showPage()
    pdf.save()
    return response


@never_cache
def user_dashboard(request):
    unauthorized = _require_regular_user(request)
    if unauthorized:
        return unauthorized
    _refresh_authenticated_user(request)
    return redirect("store:user_profile")


@never_cache
def user_profile(request):
    unauthorized = _require_regular_user(request)
    if unauthorized:
        return unauthorized

    _refresh_authenticated_user(request)
    pref = _admin_pref_context(request)
    profile = _get_customer_profile(request.user)

    if request.method == "POST":
        email_input = (request.POST.get("email") or "").strip()
        email, email_error = _clean_user_email(email_input, exclude_user_id=request.user.pk)
        avatar_file = request.FILES.get("avatar")
        avatar_error = None

        if avatar_file:
            allowed_types = {"image/jpeg", "image/png"}
            if avatar_file.size > 1024 * 1024:
                avatar_error = "Ảnh đại diện phải nhỏ hơn hoặc bằng 1 MB."
            elif getattr(avatar_file, "content_type", "") not in allowed_types:
                avatar_error = "Ảnh đại diện chỉ hỗ trợ định dạng JPEG hoặc PNG."
            else:
                try:
                    get_image_dimensions(avatar_file)
                    avatar_file.seek(0)
                except Exception:
                    avatar_error = "File tải lên không phải là ảnh hợp lệ."

        if email_error:
            messages.error(request, email_error)
        elif avatar_error:
            messages.error(request, avatar_error)
        else:
            old_avatar = profile.avatar if avatar_file and profile.avatar else None
            request.user.email = email
            request.user.save(update_fields=["email"])
            if avatar_file:
                profile.avatar = avatar_file
                profile.save(update_fields=["avatar"])
                if old_avatar and old_avatar.name != profile.avatar.name:
                    old_avatar.delete(save=False)
            messages.success(request, pref["t"]["profile_saved"])
            return redirect("store:user_profile")

    return render(
        request,
        "user/profile.html",
        {
            "profile": profile,
            "display_name": _user_display_name(request.user),
            "cart_total_quantity": _cart_items(request)[1],
            "user_notifications": _user_header_notifications(request.user),
            **pref,
        },
    )


@never_cache
def user_address(request):
    unauthorized = _require_regular_user(request)
    if unauthorized:
        return unauthorized

    _refresh_authenticated_user(request)
    pref = _admin_pref_context(request)
    profile = _get_customer_profile(request.user)
    addresses = list(_customer_addresses_qs(request.user))
    edit_pk = request.GET.get("edit")
    editing_address = None
    if edit_pk and str(edit_pk).isdigit():
        editing_address = next((item for item in addresses if item.pk == int(edit_pk)), None)

    if request.method == "POST":
        action = (request.POST.get("action") or "create").strip()
        address_id = request.POST.get("address_id")

        if action == "delete" and address_id and str(address_id).isdigit():
            deleting_address = get_object_or_404(DiaChiKhachHang, pk=int(address_id), user=request.user)
            deleting_address.delete()
            _normalize_customer_address_defaults(request.user)
            messages.success(request, "Đã xóa địa chỉ.")
            return redirect("store:user_address")

        if action == "set_default" and address_id and str(address_id).isdigit():
            default_address = get_object_or_404(DiaChiKhachHang, pk=int(address_id), user=request.user)
            DiaChiKhachHang.objects.filter(user=request.user).update(mac_dinh=False)
            default_address.mac_dinh = True
            default_address.save(update_fields=["mac_dinh"])
            _sync_legacy_profile_address(request.user)
            messages.success(request, "Đã đặt địa chỉ mặc định.")
            return redirect("store:user_address")

        ho_ten_nguoi_nhan = (request.POST.get("ho_ten_nguoi_nhan") or "").strip()
        so_dien_thoai = (request.POST.get("so_dien_thoai") or "").strip()
        tinh_thanh = (request.POST.get("tinh_thanh") or "").strip()
        quan_huyen = (request.POST.get("quan_huyen") or "").strip()
        phuong_xa = (request.POST.get("phuong_xa") or "").strip()
        dia_chi_cu_the = (request.POST.get("dia_chi_cu_the") or "").strip()
        loai_dia_chi = (request.POST.get("loai_dia_chi") or "home").strip()
        mac_dinh = request.POST.get("mac_dinh") == "on"

        errors = []
        if not ho_ten_nguoi_nhan:
            errors.append("Vui lòng nhập họ tên người nhận.")
        if not so_dien_thoai:
            errors.append("Vui lòng nhập số điện thoại.")
        if not dia_chi_cu_the:
            errors.append("Vui lòng nhập địa chỉ cụ thể.")
        if loai_dia_chi not in dict(DiaChiKhachHang.LOAI_DIA_CHI_CHOICES):
            loai_dia_chi = "home"

        if errors:
            for error in errors:
                messages.error(request, error)
            editing_address = None
            if address_id and str(address_id).isdigit():
                editing_address = get_object_or_404(DiaChiKhachHang, pk=int(address_id), user=request.user)
            addresses = list(_customer_addresses_qs(request.user))
            form_state = {
                "pk": editing_address.pk if editing_address else "",
                "ho_ten_nguoi_nhan": ho_ten_nguoi_nhan,
                "so_dien_thoai": so_dien_thoai,
                "tinh_thanh": tinh_thanh,
                "quan_huyen": quan_huyen,
                "phuong_xa": phuong_xa,
                "dia_chi_cu_the": dia_chi_cu_the,
                "loai_dia_chi": loai_dia_chi,
                "mac_dinh": mac_dinh,
            }
            return render(
                request,
                "user/address.html",
                {
                    "profile": profile,
                    "display_name": _user_display_name(request.user),
                    "cart_total_quantity": _cart_items(request)[1],
                    "addresses": addresses,
                    "editing_address": editing_address,
                    "show_form": True,
                    "form_state": form_state,
                    "user_notifications": _user_header_notifications(request.user),
                    **pref,
                },
            )

        if action == "update" and address_id and str(address_id).isdigit():
            address_obj = get_object_or_404(DiaChiKhachHang, pk=int(address_id), user=request.user)
            success_message = "Đã cập nhật địa chỉ."
        else:
            address_obj = DiaChiKhachHang(user=request.user)
            success_message = "Đã thêm địa chỉ mới."

        address_obj.ho_ten_nguoi_nhan = ho_ten_nguoi_nhan
        address_obj.so_dien_thoai = so_dien_thoai
        address_obj.tinh_thanh = tinh_thanh
        address_obj.quan_huyen = quan_huyen
        address_obj.phuong_xa = phuong_xa
        address_obj.dia_chi_cu_the = dia_chi_cu_the
        address_obj.loai_dia_chi = loai_dia_chi
        address_obj.mac_dinh = mac_dinh or not addresses
        address_obj.save()

        if address_obj.mac_dinh:
            DiaChiKhachHang.objects.filter(user=request.user).exclude(pk=address_obj.pk).update(mac_dinh=False)
        _normalize_customer_address_defaults(request.user, target=address_obj if address_obj.mac_dinh else None)
        messages.success(request, success_message)
        return redirect("store:user_address")

    default_address = _get_default_customer_address(request.user)
    form_state = {
        "pk": editing_address.pk if editing_address else "",
        "ho_ten_nguoi_nhan": editing_address.ho_ten_nguoi_nhan if editing_address else _user_display_name(request.user),
        "so_dien_thoai": editing_address.so_dien_thoai if editing_address else (profile.so_dien_thoai or ""),
        "tinh_thanh": editing_address.tinh_thanh if editing_address else "",
        "quan_huyen": editing_address.quan_huyen if editing_address else "",
        "phuong_xa": editing_address.phuong_xa if editing_address else "",
        "dia_chi_cu_the": editing_address.dia_chi_cu_the if editing_address else "",
        "loai_dia_chi": editing_address.loai_dia_chi if editing_address else "home",
        "mac_dinh": editing_address.mac_dinh if editing_address else (default_address is None),
    }

    for address in addresses:
        address.loai_dia_chi_hien_thi = _address_type_label(address)

    return render(
        request,
        "user/address.html",
        {
            "profile": profile,
            "addresses": addresses,
            "editing_address": editing_address,
            "show_form": bool(editing_address) or not addresses or request.GET.get("new") == "1",
            "form_state": form_state,
            "display_name": _user_display_name(request.user),
            "cart_total_quantity": _cart_items(request)[1],
            "user_notifications": _user_header_notifications(request.user),
            **pref,
        },
    )


@never_cache
def user_password_change(request):
    unauthorized = _require_regular_user(request)
    if unauthorized:
        return unauthorized

    _refresh_authenticated_user(request)
    pref = _admin_pref_context(request)
    form = PasswordChangeForm(user=request.user)
    password_strength = ""

    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        password_strength = _enforce_password_strength(form, pref)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, pref["t"]["password_updated"])
            return redirect("store:user_dashboard")

    return render(
        request,
        "user/password_form.html",
        {
            "form": form,
            "password_strength_value": password_strength,
            "display_name": _user_display_name(request.user),
            "cart_total_quantity": _cart_items(request)[1],
            "user_notifications": _user_header_notifications(request.user),
            **pref,
        },
    )


def product_catalog(request):
    pref = _admin_pref_context(request)
    qs = SanPham.objects.select_related("nhom_san_pham", "thuong_hieu").prefetch_related("hinh_anh_phu").order_by("ten")
    paginator = Paginator(qs, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    products = list(page_obj.object_list)
    for product in products:
        product.display_price = _format_currency(product.gia_ban)
        product.card_gallery = _build_product_card_gallery(product)
        _attach_stock_ui_fields(product)
    _, cart_total_quantity, _ = _cart_items(request)
    return render(
        request,
        "store/product_catalog.html",
        {
            "products": products,
            "page_obj": page_obj,
            "paginator": paginator,
            "cart_total_quantity": cart_total_quantity,
            **pref,
        },
    )


def product_detail(request, pk):
    pref = _admin_pref_context(request)
    product = get_object_or_404(
        SanPham.objects.select_related("nhom_san_pham", "thuong_hieu", "nha_cung_cap").prefetch_related("hinh_anh_phu"),
        pk=pk,
    )
    product.display_price = _format_currency(product.gia_ban)
    gallery_images = []
    if product.hinh_anh:
        gallery_images.append(
            {
                "url": product.hinh_anh.url,
                "alt": product.ten,
                "caption": product.ten,
            }
        )
    for image in product.hinh_anh_phu.all():
        if not image.hinh_anh:
            continue
        gallery_images.append(
            {
                "url": image.hinh_anh.url,
                "alt": image.chu_thich or product.ten,
                "caption": image.chu_thich,
            }
        )
    product.gallery_images = gallery_images
    _attach_stock_ui_fields(product)
    related_products = list(
        SanPham.objects.select_related("nhom_san_pham", "thuong_hieu")
        .exclude(pk=product.pk)
        .order_by("ten")[:4]
    )
    for item in related_products:
        item.display_price = _format_currency(item.gia_ban)

    _, cart_total_quantity, _ = _cart_items(request)
    return render(
        request,
        "store/product_detail.html",
        {
            "product": product,
            "gallery_images": gallery_images,
            "related_products": related_products,
            "cart_total_quantity": cart_total_quantity,
            **pref,
        },
    )


def cart_add(request, pk):
    if request.method != "POST":
        return redirect("store:product_catalog")
    unauthorized = _require_customer_account(request)
    if unauthorized:
        _remember_post_login_cart_action(request, pk, request.POST.get("next"))
        messages.error(request, _admin_pref_context(request)["t"]["login_to_buy"])
        return unauthorized

    product = get_object_or_404(SanPham, pk=pk)
    next_url = request.POST.get("next")
    if product.ton_kho <= 0:
        messages.error(request, "Sản phẩm này hiện đã hết hàng.")
        return redirect(next_url) if next_url else redirect("store:product_detail", pk=product.pk)
    cart = _cart_session(request)
    key = str(product.pk)
    current_qty = int(cart.get(key, 0))
    if current_qty >= product.ton_kho:
        messages.error(request, f"Bạn chỉ có thể thêm tối đa {product.ton_kho} sản phẩm đang còn trong kho.")
        return redirect(next_url) if next_url else redirect("store:cart")
    cart[key] = current_qty + 1
    request.session.modified = True
    messages.success(request, _admin_pref_context(request)["t"]["product_added"])
    return redirect(next_url) if next_url else redirect("store:cart")


def cart_view(request):
    items, total_quantity, total_amount = _cart_items(request)
    for item in items:
        item["display_unit_price"] = _format_currency(item["unit_price"])
        item["display_line_total"] = _format_currency(item["line_total"])
    return render(
        request,
        "store/cart.html",
        {
            "cart_items": items,
            "cart_total_quantity": total_quantity,
            "cart_total_amount": total_amount,
            "display_cart_total_amount": _format_currency(total_amount),
            **_admin_pref_context(request),
        },
    )


def cart_update(request):
    if request.method != "POST":
        return redirect("store:cart")
    unauthorized = _require_customer_account(request)
    if unauthorized:
        messages.error(request, _admin_pref_context(request)["t"]["login_to_buy"])
        return unauthorized

    cart = _cart_session(request)
    product_ids = [int(key) for key in cart.keys() if str(key).isdigit()]
    products = {p.pk: p for p in SanPham.objects.filter(pk__in=product_ids)}
    for key in list(cart.keys()):
        qty = request.POST.get(f"qty_{key}")
        if qty is None:
            continue
        try:
            qty_int = max(int(qty), 0)
        except ValueError:
            qty_int = 0
        product = products.get(int(key)) if str(key).isdigit() else None
        if product is not None:
            qty_int = min(qty_int, product.ton_kho)
        if qty_int == 0:
            cart.pop(key, None)
        else:
            cart[key] = qty_int
    request.session.modified = True
    messages.success(request, _admin_pref_context(request)["t"]["cart_updated"])
    return redirect("store:cart")


def cart_remove(request, pk):
    if request.method != "POST":
        return redirect("store:cart")
    unauthorized = _require_customer_account(request)
    if unauthorized:
        messages.error(request, _admin_pref_context(request)["t"]["login_to_buy"])
        return unauthorized

    cart = _cart_session(request)
    cart.pop(str(pk), None)
    request.session.modified = True
    messages.success(request, "Đã xóa sản phẩm khỏi giỏ hàng.")
    return redirect("store:cart")


def cart_clear(request):
    if request.method != "POST":
        return redirect("store:cart")
    unauthorized = _require_customer_account(request)
    if unauthorized:
        messages.error(request, _admin_pref_context(request)["t"]["login_to_buy"])
        return unauthorized

    request.session["cart"] = {}
    request.session.modified = True
    messages.success(request, "Đã xóa toàn bộ giỏ hàng.")
    return redirect("store:cart")


def feedback_view(request):
    pref = _admin_pref_context(request)
    initial_name = ""
    initial_email = ""
    initial_phone = ""
    if request.user.is_authenticated and _is_regular_user(request.user):
        profile = _get_customer_profile(request.user)
        initial_name = request.user.get_full_name().strip()
        initial_email = request.user.email or ""
        initial_phone = profile.so_dien_thoai or ""

    form_data = {
        "ho_ten": initial_name,
        "email": initial_email,
        "so_dien_thoai": initial_phone,
        "chu_de": "",
        "noi_dung": "",
    }
    errors = {}

    if request.method == "POST":
        form_data = {
            "ho_ten": (request.POST.get("ho_ten") or "").strip(),
            "email": (request.POST.get("email") or "").strip(),
            "so_dien_thoai": (request.POST.get("so_dien_thoai") or "").strip(),
            "chu_de": (request.POST.get("chu_de") or "").strip(),
            "noi_dung": (request.POST.get("noi_dung") or "").strip(),
        }
        if not form_data["ho_ten"]:
            errors["ho_ten"] = "Vui lòng nhập họ tên."
        if not form_data["email"]:
            errors["email"] = "Vui lòng nhập email."
        else:
            try:
                validate_email(form_data["email"])
            except ValidationError:
                errors["email"] = "Email không đúng định dạng."
        if not form_data["chu_de"]:
            errors["chu_de"] = "Vui lòng nhập chủ đề."
        if not form_data["noi_dung"]:
            errors["noi_dung"] = "Vui lòng nhập nội dung góp ý."

        if not errors:
            feedback = GopYKhachHang.objects.create(**form_data)
            try:
                _send_feedback_emails(feedback)
                messages.success(request, "Đã gửi góp ý thành công. Vui lòng kiểm tra email để xem phản hồi xác nhận.")
            except Exception:
                messages.warning(
                    request,
                    "Hệ thống đã lưu góp ý, nhưng chưa gửi được email. Hãy kiểm tra lại cấu hình Mailtrap trong .env.",
                )
            return redirect("store:feedback")

    return render(
        request,
        "store/feedback.html",
        {
            "feedback_form": form_data,
            "feedback_errors": errors,
            "cart_total_quantity": _cart_items(request)[1],
            **pref,
        },
    )


def checkout_view(request):
    unauthorized = _require_customer_account(request)
    if unauthorized:
        messages.error(request, _admin_pref_context(request)["t"]["login_to_buy"])
        return unauthorized

    items, total_quantity, total_amount = _cart_items(request)
    for item in items:
        item["display_unit_price"] = _format_currency(item["unit_price"])
        item["display_line_total"] = _format_currency(item["line_total"])
    pref = _admin_pref_context(request)
    if not items:
        messages.error(request, pref["t"]["cart_empty"])
        return redirect("store:product_catalog")

    profile = _get_customer_profile(request.user)
    default_address = _get_default_customer_address(request.user)
    saved_addresses = list(_customer_addresses_qs(request.user))
    initial_name = default_address.ho_ten_nguoi_nhan if default_address else request.user.get_full_name().strip()
    initial_email = request.user.email or ""
    initial_phone = default_address.so_dien_thoai if default_address else (profile.so_dien_thoai or "")
    initial_address = _format_customer_address(default_address) if default_address else (profile.dia_chi or "")
    note_value = ""
    subtotal_amount = Decimal(total_amount or 0)
    discount_amount = Decimal("0")
    final_amount = subtotal_amount
    voucher_code = ""
    applied_voucher = None
    available_vouchers = _get_checkout_available_vouchers(items, subtotal_amount)
    delivery_lat = ""
    delivery_lng = ""
    payment_method = "cod"
    transfer_code = ""
    transfer_receipt = None
    payment_method_choices = DonHang.PAYMENT_METHOD_CHOICES
    if request.method == "POST":
        for item in items:
            if item["quantity"] > item["product"].ton_kho:
                messages.error(
                    request,
                    f"{item['product'].ten} chỉ còn {item['product'].ton_kho} sản phẩm trong kho. Vui lòng cập nhật lại giỏ hàng.",
                )
                return redirect("store:cart")
        receiver_name = (request.POST.get("receiver_name") or "").strip()
        phone = (request.POST.get("phone") or "").strip()
        address = (request.POST.get("address") or "").strip()
        note = (request.POST.get("note") or "").strip()
        payment_method = (request.POST.get("payment_method") or "cod").strip()
        transfer_code = (request.POST.get("transfer_code") or "").strip()
        transfer_receipt = request.FILES.get("transfer_receipt")
        initial_name = receiver_name
        initial_phone = phone
        initial_address = address
        note_value = note
        voucher_code = _normalize_voucher_code(request.POST.get("voucher_code"))
        delivery_lat = (request.POST.get("delivery_lat") or "").strip()
        delivery_lng = (request.POST.get("delivery_lng") or "").strip()
        preview_only = request.POST.get("preview_voucher") == "1"

        form_has_error = False
        try:
            lat_value = _parse_latitude(delivery_lat)
            lng_value = _parse_longitude(delivery_lng)
        except ValidationError as exc:
            messages.error(request, "; ".join(exc.messages))
            lat_value = None
            lng_value = None
            form_has_error = True

        if (lat_value is None) ^ (lng_value is None):
            messages.error(request, "Vui lòng chọn đủ cả vĩ độ và kinh độ giao hàng trên bản đồ, hoặc để trống cả hai.")
            form_has_error = True

        if payment_method not in dict(DonHang.PAYMENT_METHOD_CHOICES):
            messages.error(request, "Phương thức thanh toán không hợp lệ.")
            form_has_error = True
        if payment_method == "bank_transfer" and not preview_only and not transfer_receipt:
            messages.error(request, "Vui lòng tải ảnh biên lai chuyển khoản trước khi đặt đơn.")
            form_has_error = True

        if voucher_code and not form_has_error:
            try:
                applied_voucher, discount_amount = _resolve_checkout_voucher(voucher_code, items, subtotal_amount)
            except ValidationError as exc:
                messages.error(request, "; ".join(exc.messages))
                form_has_error = True

        final_amount = max(subtotal_amount - discount_amount, Decimal("0"))
        if preview_only and not form_has_error:
            if applied_voucher is not None:
                messages.success(
                    request,
                    f"Đã áp dụng voucher {applied_voucher.ma_code}. Đơn hàng đang được giảm {_format_currency(discount_amount)}.",
                )
            return render(
                request,
                "store/checkout.html",
                {
                    "cart_items": items,
                    "cart_total_quantity": total_quantity,
                    "cart_total_amount": total_amount,
                    "display_cart_total_amount": _format_currency(total_amount),
                    "subtotal_amount": subtotal_amount,
                    "display_subtotal_amount": _format_currency(subtotal_amount),
                    "discount_amount": discount_amount,
                    "display_discount_amount": _format_currency(discount_amount),
                    "final_amount": final_amount,
                    "display_final_amount": _format_currency(final_amount),
                    "initial_name": initial_name,
                    "initial_email": initial_email,
                    "initial_phone": initial_phone,
                    "initial_address": initial_address,
                    "note_value": note_value,
                    "saved_addresses": saved_addresses,
                    "voucher_code": voucher_code,
                    "applied_voucher": applied_voucher,
                    "available_vouchers": available_vouchers,
                    "delivery_lat": delivery_lat,
                    "delivery_lng": delivery_lng,
                    "payment_method": payment_method,
                    "transfer_code": transfer_code,
                    "has_transfer_receipt": bool(transfer_receipt),
                    "payment_method_choices": payment_method_choices,
                    **pref,
                },
            )
        if receiver_name and phone and address and not form_has_error:
            with transaction.atomic():
                product_ids = sorted({item["product"].pk for item in items})
                locked_products = {
                    product.pk: product
                    for product in SanPham.objects.select_for_update().filter(pk__in=product_ids).order_by("pk")
                }
                for item in items:
                    locked_product = locked_products.get(item["product"].pk)
                    if locked_product is None:
                        messages.error(request, "Một sản phẩm trong giỏ hàng không còn tồn tại. Vui lòng kiểm tra lại giỏ hàng.")
                        return redirect("store:cart")
                    if item["quantity"] > locked_product.ton_kho:
                        messages.error(
                            request,
                            f"{locked_product.ten} chỉ còn {locked_product.ton_kho} sản phẩm trong kho. Vui lòng cập nhật lại giỏ hàng.",
                        )
                        return redirect("store:cart")
                fulfillment_store = _select_fulfillment_store(items)
                if fulfillment_store is None:
                    messages.error(
                        request,
                        "Hiện chưa có cửa hàng nào đủ tồn kho để xử lý trọn bộ đơn hàng này. Vui lòng giảm số lượng hoặc liên hệ quản trị kho.",
                    )
                    return redirect("store:cart")
                order = DonHang.objects.create(
                    khach_hang=request.user,
                    ho_ten_nguoi_nhan=receiver_name,
                    so_dien_thoai=phone,
                    dia_chi_giao_hang=address,
                    vi_do_giao_hang=lat_value,
                    kinh_do_giao_hang=lng_value,
                    ghi_chu=note,
                    tong_so_luong=total_quantity,
                    phuong_thuc_thanh_toan=payment_method,
                    trang_thai_thanh_toan=_default_payment_status_for_method(payment_method),
                    tong_tien_truoc_giam=subtotal_amount,
                    giam_gia=discount_amount,
                    tong_tien=final_amount,
                    cua_hang_xu_ly=fulfillment_store,
                    khuyen_mai=applied_voucher,
                    ma_voucher_ap_dung=applied_voucher.ma_code if applied_voucher else "",
                    anh_bien_lai=transfer_receipt,
                    ma_giao_dich_thanh_toan=transfer_code,
                    thoi_gian_gui_bien_lai=timezone.now() if transfer_receipt else None,
                )
                _create_admin_notification(
                    f"Đơn hàng mới #{order.pk}",
                    (
                        f"Khách hàng {request.user.username} vừa đặt đơn #{order.pk} "
                        f"gồm {total_quantity} sản phẩm, tổng tiền {_format_currency(final_amount)}. "
                        f"Cửa hàng xử lý: {fulfillment_store.ten}."
                    ),
                    level="info",
                    path=f"{reverse('store:admin_list', kwargs={'model_slug': 'don-hang'})}?status=pending",
                    method="ORDER",
                    status_code=201,
                )
                if payment_method == "bank_transfer" and transfer_receipt:
                    _log_payment_confirmation(
                        order,
                        "submitted",
                        performed_by=request.user,
                        note=f"Khách đã tải biên lai chuyển khoản. Mã giao dịch: {transfer_code or '-'}",
                    )
                for item in items:
                    locked_product = locked_products[item["product"].pk]
                    ChiTietDonHang.objects.create(
                        don_hang=order,
                        san_pham=locked_product,
                        so_luong=item["quantity"],
                        don_gia=item["unit_price"],
                    )
                    GiaoDichKho.objects.create(
                        san_pham=locked_product,
                        cua_hang=fulfillment_store,
                        loai="export",
                        so_luong=item["quantity"],
                        don_hang=order,
                        ghi_chu=f"Xuất kho cho đơn hàng #{order.pk} từ {fulfillment_store.ten}",
                    )
            profile.so_dien_thoai = phone
            profile.save(update_fields=["so_dien_thoai"])
            if not saved_addresses:
                auto_address = DiaChiKhachHang.objects.create(
                    user=request.user,
                    ho_ten_nguoi_nhan=receiver_name,
                    so_dien_thoai=phone,
                    dia_chi_cu_the=address,
                    mac_dinh=True,
                )
                _normalize_customer_address_defaults(request.user, target=auto_address)
            request.session["cart"] = {}
            request.session.modified = True
            messages.success(request, pref["t"]["order_success"])
            try:
                if not _send_order_confirmation(order, items):
                    messages.warning(
                        request,
                        "Đã tạo đơn hàng nhưng khách hàng chưa có email để gửi xác nhận.",
                    )
            except Exception:
                messages.warning(
                    request,
                    "Đã tạo đơn hàng nhưng chưa gửi được email. Hãy kiểm tra lại cấu hình Mailtrap trong .env.",
                )
            if payment_method == "momo":
                messages.info(request, "Đơn hàng đã tạo. Hãy hoàn tất bước thanh toán MoMo demo.")
                return redirect("store:momo_demo_payment", pk=order.pk)
            return redirect("store:my_orders")
        if not form_has_error:
            messages.error(request, "Vui lòng điền đầy đủ thông tin nhận hàng.")
    return render(
        request,
        "store/checkout.html",
        {
            "cart_items": items,
            "cart_total_quantity": total_quantity,
            "cart_total_amount": total_amount,
            "display_cart_total_amount": _format_currency(total_amount),
            "subtotal_amount": subtotal_amount,
            "display_subtotal_amount": _format_currency(subtotal_amount),
            "discount_amount": discount_amount,
            "display_discount_amount": _format_currency(discount_amount),
            "final_amount": final_amount,
            "display_final_amount": _format_currency(final_amount),
            "initial_name": initial_name,
            "initial_email": initial_email,
            "initial_phone": initial_phone,
            "initial_address": initial_address,
            "note_value": note_value,
            "saved_addresses": saved_addresses,
            "voucher_code": voucher_code,
            "applied_voucher": applied_voucher,
            "available_vouchers": available_vouchers,
            "delivery_lat": delivery_lat,
            "delivery_lng": delivery_lng,
            "payment_method": payment_method,
            "transfer_code": transfer_code,
            "has_transfer_receipt": bool(transfer_receipt),
            "payment_method_choices": payment_method_choices,
            **pref,
        },
    )


def my_orders(request):
    unauthorized = _require_customer_account(request)
    if unauthorized:
        return unauthorized
    qs = DonHang.objects.filter(khach_hang=request.user).select_related("cua_hang_xu_ly").prefetch_related("items__san_pham")
    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    orders = list(page_obj.object_list)
    for order in orders:
        order.display_total_amount = _format_currency(order.tong_tien)
        order.display_payment_method = order.get_phuong_thuc_thanh_toan_display()
        order.display_payment_status = order.get_trang_thai_thanh_toan_display()
        order.display_store_name = order.cua_hang_xu_ly.ten if order.cua_hang_xu_ly_id else "-"
        for item in order.items.all():
            item.display_unit_price = _format_currency(item.don_gia)
    _, cart_total_quantity, _ = _cart_items(request)
    return render(
        request,
        "store/my_orders.html",
        {
            "orders": orders,
            "page_obj": page_obj,
            "paginator": paginator,
            "cart_total_quantity": cart_total_quantity,
            "user_notifications": _user_header_notifications(request.user),
            **_admin_pref_context(request),
        },
    )


def momo_demo_payment(request, pk):
    unauthorized = _require_customer_account(request)
    if unauthorized:
        return unauthorized

    order = get_object_or_404(DonHang, pk=pk, khach_hang=request.user)
    if order.phuong_thuc_thanh_toan != "momo":
        return redirect("store:order_detail", pk=order.pk)

    pref = _admin_pref_context(request)
    if request.method == "POST":
        action = (request.POST.get("action") or "").strip()
        if action == "success":
            if order.trang_thai_thanh_toan != "paid":
                order.trang_thai_thanh_toan = "paid"
                order.save(update_fields=["trang_thai_thanh_toan"])
            messages.success(request, "Thanh toán MoMo demo thành công.")
            return redirect("store:order_detail", pk=order.pk)
        if action == "fail":
            with transaction.atomic():
                if order.trang_thai_thanh_toan != "unpaid":
                    order.trang_thai_thanh_toan = "unpaid"
                    order.save(update_fields=["trang_thai_thanh_toan"])
                if order.trang_thai != "cancelled":
                    order.trang_thai = "cancelled"
                    order.save(update_fields=["trang_thai"])
                _release_order_inventory_if_needed(order, reason="thanh toán MoMo demo thất bại")
            messages.error(request, "Thanh toán MoMo demo thất bại hoặc đã bị hủy.")
            return redirect("store:order_detail", pk=order.pk)

    _, cart_total_quantity, _ = _cart_items(request)
    return render(
        request,
        "store/momo_demo.html",
        {
            **_momo_demo_context(order),
            "cart_total_quantity": cart_total_quantity,
            "user_notifications": _user_header_notifications(request.user),
            **pref,
        },
    )


def user_notifications(request):
    unauthorized = _require_customer_account(request)
    if unauthorized:
        return unauthorized

    all_notifications = _user_all_notifications(request.user)
    paginator = Paginator(all_notifications, 8)
    page_obj = paginator.get_page(request.GET.get("page"))
    notifications = list(page_obj.object_list)
    _, cart_total_quantity, _ = _cart_items(request)

    return render(
        request,
        "store/notifications.html",
        {
            "notifications": notifications,
            "page_obj": page_obj,
            "paginator": paginator,
            "cart_total_quantity": cart_total_quantity,
            "user_notifications": _user_header_notifications(request.user),
            **_admin_pref_context(request),
        },
    )


def order_detail(request, pk):
    unauthorized = _require_customer_account(request)
    if unauthorized:
        return unauthorized

    order = get_object_or_404(
        DonHang.objects.filter(khach_hang=request.user)
        .select_related("cua_hang_xu_ly")
        .prefetch_related("items__san_pham", "lich_su_xac_nhan_thanh_toan__performed_by"),
        pk=pk,
    )
    for item in order.items.all():
        item.display_unit_price = _format_currency(item.don_gia)
        item.display_line_total = _format_currency((item.don_gia or Decimal("0")) * item.so_luong)

    timeline = _order_status_timeline(order)
    order.display_subtotal_amount = _format_currency(order.tong_tien_truoc_giam or order.tong_tien)
    order.display_discount_amount = _format_currency(order.giam_gia)
    order.display_total_amount = _format_currency(order.tong_tien)
    order.display_payment_method = order.get_phuong_thuc_thanh_toan_display()
    order.display_payment_status = order.get_trang_thai_thanh_toan_display()
    order.display_store_name = order.cua_hang_xu_ly.ten if order.cua_hang_xu_ly_id else "-"
    order.created_text = timezone.localtime(order.created_at).strftime("%d/%m/%Y %H:%M")
    payment_review_logs = list(order.lich_su_xac_nhan_thanh_toan.all())

    _, cart_total_quantity, _ = _cart_items(request)
    return render(
        request,
        "store/order_detail.html",
        {
            "order": order,
            "timeline": timeline,
            "payment_review_logs": payment_review_logs,
            "cart_total_quantity": cart_total_quantity,
            "user_notifications": _user_header_notifications(request.user),
            **_admin_pref_context(request),
        },
    )


def report_404_action(request, action):
    # log user intent from 404 page
    if action not in {"retry", "support"}:
        return redirect("store:home")
    title = "Retry Request" if action == "retry" else "Support Request"
    Notification.objects.create(
        level="info",
        title=title,
        message="User clicked from 404 page",
        path=(request.GET.get("path") or request.path)[:255],
        method=request.method[:10],
        status_code=404,
    )
    # redirect back or home
    return redirect(request.GET.get("back") or "store:home")
