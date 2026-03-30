from django.shortcuts import render


def home(request):
    featured_products = list(SanPham.objects.order_by("ten")[:8])
    for product in featured_products:
        product.display_price = _format_currency(product.gia_ban)
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
import os
import re
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm, UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import modelform_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import (
    ChiTietDonHang,
    DonHang,
    GopYKhachHang,
    HoSoKhachHang,
    Notification,
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
    "gop-y-khach-hang": GopYKhachHang,
    "ho-so-khach-hang": HoSoKhachHang,
    "don-hang": DonHang,
    "chi-tiet-don-hang": ChiTietDonHang,
}

User = get_user_model()
ROLE_ADMIN = "Admin"
ROLE_USER = "User"
ROLE_CHOICES = (
    (ROLE_ADMIN, "Admin"),
    (ROLE_USER, "User"),
)

MODULE_LABELS = {
    "thuong-hieu": {"vi_singular": "Thương hiệu", "vi_plural": "Thương hiệu", "en_singular": "Brand", "en_plural": "Brands"},
    "nha-cung-cap": {"vi_singular": "Nhà cung cấp", "vi_plural": "Nhà cung cấp", "en_singular": "Supplier", "en_plural": "Suppliers"},
    "nhom-san-pham": {"vi_singular": "Nhóm sản phẩm", "vi_plural": "Nhóm sản phẩm", "en_singular": "Product Group", "en_plural": "Product Groups"},
    "san-pham": {"vi_singular": "Sản phẩm", "vi_plural": "Sản phẩm", "en_singular": "Product", "en_plural": "Products"},
    "chuoi-cua-hang": {"vi_singular": "Chuỗi cửa hàng", "vi_plural": "Chuỗi cửa hàng", "en_singular": "Store Chain", "en_plural": "Store Chains"},
    "cua-hang": {"vi_singular": "Cửa hàng", "vi_plural": "Cửa hàng", "en_singular": "Store", "en_plural": "Stores"},
    "nhan-vien": {"vi_singular": "Nhân viên", "vi_plural": "Nhân viên", "en_singular": "Employee", "en_plural": "Employees"},
    "khuyen-mai": {"vi_singular": "Khuyến mãi", "vi_plural": "Khuyến mãi", "en_singular": "Promotion", "en_plural": "Promotions"},
    "gop-y-khach-hang": {"vi_singular": "Góp ý khách hàng", "vi_plural": "Góp ý khách hàng", "en_singular": "Customer Feedback", "en_plural": "Customer Feedback"},
    "ho-so-khach-hang": {"vi_singular": "Hồ sơ khách hàng", "vi_plural": "Hồ sơ khách hàng", "en_singular": "Customer Profile", "en_plural": "Customer Profiles"},
    "don-hang": {"vi_singular": "Đơn hàng", "vi_plural": "Đơn hàng", "en_singular": "Order", "en_plural": "Orders"},
    "chi-tiet-don-hang": {"vi_singular": "Chi tiết đơn hàng", "vi_plural": "Chi tiết đơn hàng", "en_singular": "Order Item", "en_plural": "Order Items"},
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
        "internal_cms": "CMS nội bộ",
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
        "no_access": "Tài khoản không có quyền truy cập CMS.",
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
        "user_login_title": "Đăng nhập người dùng",
        "user_login_hint": "Tài khoản người dùng sẽ vào trang người dùng. Tài khoản admin sẽ được chuyển sang CMS.",
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
        "login_title": "Đăng nhập CMS",
        "login_only_staff": "Chỉ tài khoản Admin mới được phép truy cập.",
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
        "user_login_hint": "Regular users enter the user area. Admin accounts are redirected to the CMS.",
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
        "chu_de": "Subject",
        "noi_dung": "Feedback Content",
        "da_phan_hoi": "Responded",
        "user": "User",
        "khach_hang": "Customer",
        "ho_ten_nguoi_nhan": "Receiver",
        "dia_chi_giao_hang": "Delivery Address",
        "ghi_chu": "Note",
        "trang_thai": "Status",
        "tong_so_luong": "Total Quantity",
        "tong_tien": "Total Amount",
        "don_hang": "Order",
        "so_luong": "Quantity",
        "don_gia": "Unit Price",
        "created_at": "Created At",
    }
}


def _is_admin_user(user):
    if not user.is_authenticated:
        return False
    return _ensure_user_role(user) == ROLE_ADMIN


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


def _get_customer_profile(user):
    profile, _ = HoSoKhachHang.objects.get_or_create(user=user)
    return profile


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
        qty = max(int(quantity), 0)
        if qty <= 0:
            continue
        unit_price = product.gia_ban or Decimal("0")
        line_total = unit_price * qty
        total_quantity += qty
        total_amount += line_total
        items.append({"product": product, "quantity": qty, "unit_price": unit_price, "line_total": line_total})
    return items, total_quantity, total_amount


def _ensure_role_groups():
    admin_group, _ = Group.objects.get_or_create(name=ROLE_ADMIN)
    user_group, _ = Group.objects.get_or_create(name=ROLE_USER)
    return {ROLE_ADMIN: admin_group, ROLE_USER: user_group}


def _ensure_user_role(user):
    groups = _ensure_role_groups()
    if not user or not user.is_authenticated:
        return None

    target_role = None
    if user.groups.filter(name=ROLE_ADMIN).exists():
        target_role = ROLE_ADMIN
    elif user.groups.filter(name=ROLE_USER).exists():
        target_role = ROLE_USER
    elif user.is_superuser or user.is_staff:
        target_role = ROLE_ADMIN
    else:
        target_role = ROLE_USER

    target_group = groups[target_role]
    needs_group_sync = not user.groups.filter(pk=target_group.pk).exists() or user.groups.exclude(pk=target_group.pk).exists()
    expected_is_staff = target_role == ROLE_ADMIN
    needs_staff_sync = user.is_staff != expected_is_staff

    if needs_group_sync:
        user.groups.set([target_group])
    if needs_staff_sync:
        user.is_staff = expected_is_staff
        user.save(update_fields=["is_staff"])

    return target_role


def _get_user_role(user):
    return _ensure_user_role(user) or ROLE_USER


def _sync_user_role(user, role: str):
    groups = _ensure_role_groups()
    role = ROLE_ADMIN if role == ROLE_ADMIN else ROLE_USER
    user.groups.set([groups[role]])
    user.is_staff = role == ROLE_ADMIN
    user.save(update_fields=["is_staff"])


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
                parts = full_name_value.split(" ", 1)
                user.first_name = parts[0]
                user.last_name = parts[1] if len(parts) > 1 else ""
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


def admin_user_password(request, pk):
    unauthorized = _require_admin_user(request)
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
            "modules": _menu_context(pref["admin_lang"]),
            "form": form,
            "page_heading": f'{pref["t"]["reset_password"]}: {user_obj.username}',
            "password_strength_value": password_strength,
            **pref,
        },
    )


def admin_order_status_action(request, pk, status):
    unauthorized = _require_admin_user(request)
    if unauthorized:
        return unauthorized

    if status not in {"confirmed", "shipping", "delivered", "done", "cancelled"}:
        return redirect("store:admin_list", model_slug="don-hang")

    order = get_object_or_404(DonHang, pk=pk)
    allowed_transitions = {
        "pending": {"confirmed", "cancelled"},
        "confirmed": {"shipping", "cancelled"},
        "shipping": {"delivered", "cancelled"},
        "delivered": set(),
        "done": set(),
        "cancelled": set(),
    }
    if status not in allowed_transitions.get(order.trang_thai, set()):
        redirect_url = reverse("store:admin_list", kwargs={"model_slug": "don-hang"})
        query = request.GET.urlencode()
        if query:
            redirect_url = f"{redirect_url}?{query}"
        return redirect(redirect_url)

    order.trang_thai = status
    order.save(update_fields=["trang_thai"])
    messages.success(request, _admin_pref_context(request)["t"]["order_status_updated"])

    redirect_url = reverse("store:admin_list", kwargs={"model_slug": "don-hang"})
    query = request.GET.urlencode()
    if query:
        redirect_url = f"{redirect_url}?{query}"
    return redirect(redirect_url)


def admin_user_management(request):
    unauthorized = _require_admin_user(request)
    if unauthorized:
        return unauthorized

    _ensure_role_groups()
    pref = _admin_pref_context(request)
    lang = pref["admin_lang"]
    form = UserCreationForm()
    create_user_email = ""
    create_user_full_name = ""
    create_user_role = ROLE_USER
    create_user_is_active = True
    create_user_password_strength = ""
    query = request.GET.get("q", "").strip()

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "create_user":
            form = UserCreationForm(request.POST)
            create_user_email = (request.POST.get("email") or "").strip()
            create_user_full_name = (request.POST.get("full_name") or "").strip()
            create_user_role = request.POST.get("role", ROLE_USER)
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
                    parts = create_user_full_name.split(" ", 1)
                    user.first_name = parts[0]
                    user.last_name = parts[1] if len(parts) > 1 else ""
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
                if query:
                    redirect_url = f"{redirect_url}?q={query}"
                return redirect(redirect_url)

            if full_name:
                parts = full_name.split(" ", 1)
                user.first_name = parts[0]
                user.last_name = parts[1] if len(parts) > 1 else ""
            else:
                user.first_name = ""
                user.last_name = ""
            user.email = email
            if not user.is_superuser:
                user.is_active = request.POST.get("is_active") == "on"
                user.save(update_fields=["first_name", "last_name", "email", "is_active"])
            else:
                user.save(update_fields=["first_name", "last_name", "email"])
            _sync_user_role(user, request.POST.get("role", ROLE_USER))
            messages.success(request, pref["t"]["user_updated"])
            redirect_url = reverse("store:admin_user_management")
            if query:
                redirect_url = f"{redirect_url}?q={query}"
            return redirect(redirect_url)

    user_qs = User.objects.order_by("username")
    if query:
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
                "full_name": user.get_full_name().strip() or "-",
            }
        )

    return render(
        request,
        "admin/user_management.html",
        {
            "modules": _menu_context(lang),
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
            "role_choices": ROLE_CHOICES,
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
    status_filter = request.GET.get("status", "").strip()
    qs = model.objects.all().order_by("-pk")
    if model_slug == "don-hang" and status_filter in {"pending", "confirmed", "shipping", "delivered", "done", "cancelled"}:
        if status_filter == "done":
            qs = qs.filter(trang_thai__in=["done", "delivered"])
        else:
            qs = qs.filter(trang_thai=status_filter)
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
            elif field["name"] in {"trang_thai"}:
                display = str(raw_value)
                try:
                    display = getattr(item, f"get_{field['name']}_display")()
                except Exception:
                    pass
                values.append({"type": "status", "value": str(raw_value), "text": display})
            elif field["name"] in {"gia_ban", "tong_tien", "don_gia"}:
                values.append({"type": "money", "text": _format_currency(raw_value)})
            else:
                values.append({"type": "text", "text": "" if raw_value is None else str(raw_value)})
        row = {"object": item, "values": values}
        if model_slug == "don-hang":
            status_actions = []
            if item.trang_thai == "pending":
                status_actions.append({"value": "confirmed", "label": pref["t"]["confirm_order"]})
                status_actions.append({"value": "cancelled", "label": pref["t"]["cancel_order"]})
            elif item.trang_thai == "confirmed":
                status_actions.append({"value": "shipping", "label": pref["t"]["ship_order"]})
                status_actions.append({"value": "cancelled", "label": pref["t"]["cancel_order"]})
            elif item.trang_thai == "shipping":
                status_actions.append({"value": "delivered", "label": pref["t"]["deliver_order"]})
                status_actions.append({"value": "cancelled", "label": pref["t"]["cancel_order"]})
            row["status_actions"] = status_actions
        rows.append(row)

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
            "status_filter": status_filter,
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


def admin_notifications(request):
    unauthorized = _require_admin_user(request)
    if unauthorized:
        return unauthorized

    pref = _admin_pref_context(request)
    lang = pref["admin_lang"]
    # mark all as seen when opening notifications
    Notification.objects.filter(resolved=False).update(resolved=True)
    qs = Notification.objects.all()
    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "admin/notifications.html",
        {
            "modules": _menu_context(lang),
            "page_obj": page_obj,
            "paginator": paginator,
            **pref,
        },
    )


def user_dashboard(request):
    unauthorized = _require_regular_user(request)
    if unauthorized:
        return unauthorized

    pref = _admin_pref_context(request)
    profile = _get_customer_profile(request.user)
    return render(
        request,
        "user/dashboard.html",
        {
            "role_label": pref["t"]["user_role"],
            "profile": profile,
            **pref,
        },
    )


def user_profile(request):
    unauthorized = _require_regular_user(request)
    if unauthorized:
        return unauthorized

    pref = _admin_pref_context(request)
    profile = _get_customer_profile(request.user)

    if request.method == "POST":
        full_name = (request.POST.get("full_name") or "").strip()
        email_input = (request.POST.get("email") or "").strip()
        phone = (request.POST.get("phone") or "").strip()
        address = (request.POST.get("address") or "").strip()
        email, email_error = _clean_user_email(email_input, exclude_user_id=request.user.pk)
        if email_error:
            messages.error(request, email_error)
        else:
            if full_name:
                parts = full_name.split(" ", 1)
                request.user.first_name = parts[0]
                request.user.last_name = parts[1] if len(parts) > 1 else ""
            else:
                request.user.first_name = ""
                request.user.last_name = ""
            request.user.email = email
            request.user.save(update_fields=["first_name", "last_name", "email"])
            profile.so_dien_thoai = phone
            profile.dia_chi = address
            profile.save(update_fields=["so_dien_thoai", "dia_chi"])
            messages.success(request, pref["t"]["profile_saved"])
            return redirect("store:user_profile")

    return render(
        request,
        "user/profile.html",
        {
            "profile": profile,
            **pref,
        },
    )


def user_password_change(request):
    unauthorized = _require_regular_user(request)
    if unauthorized:
        return unauthorized

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
            **pref,
        },
    )


def product_catalog(request):
    pref = _admin_pref_context(request)
    qs = SanPham.objects.select_related("nhom_san_pham", "thuong_hieu").order_by("ten")
    paginator = Paginator(qs, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    products = list(page_obj.object_list)
    for product in products:
        product.display_price = _format_currency(product.gia_ban)
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


def cart_add(request, pk):
    if request.method != "POST":
        return redirect("store:product_catalog")
    unauthorized = _require_customer_account(request)
    if unauthorized:
        _remember_post_login_cart_action(request, pk, request.POST.get("next"))
        messages.error(request, _admin_pref_context(request)["t"]["login_to_buy"])
        return unauthorized

    product = get_object_or_404(SanPham, pk=pk)
    cart = _cart_session(request)
    key = str(product.pk)
    cart[key] = int(cart.get(key, 0)) + 1
    request.session.modified = True
    messages.success(request, _admin_pref_context(request)["t"]["product_added"])
    return redirect(request.POST.get("next") or "store:cart")


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
    for key in list(cart.keys()):
        qty = request.POST.get(f"qty_{key}")
        if qty is None:
            continue
        try:
            qty_int = max(int(qty), 0)
        except ValueError:
            qty_int = 0
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
    initial_name = request.user.get_full_name().strip()
    initial_email = request.user.email or ""
    initial_phone = profile.so_dien_thoai or ""
    initial_address = profile.dia_chi or ""
    if request.method == "POST":
        receiver_name = (request.POST.get("receiver_name") or "").strip()
        phone = (request.POST.get("phone") or "").strip()
        address = (request.POST.get("address") or "").strip()
        note = (request.POST.get("note") or "").strip()
        if receiver_name and phone and address:
            order = DonHang.objects.create(
                khach_hang=request.user,
                ho_ten_nguoi_nhan=receiver_name,
                so_dien_thoai=phone,
                dia_chi_giao_hang=address,
                ghi_chu=note,
                tong_so_luong=total_quantity,
                tong_tien=total_amount,
            )
            for item in items:
                ChiTietDonHang.objects.create(
                    don_hang=order,
                    san_pham=item["product"],
                    so_luong=item["quantity"],
                    don_gia=item["unit_price"],
                )
            profile.so_dien_thoai = phone
            profile.dia_chi = address
            profile.save(update_fields=["so_dien_thoai", "dia_chi"])
            request.session["cart"] = {}
            request.session.modified = True
            messages.success(request, pref["t"]["order_success"])
            return redirect("store:my_orders")
        messages.error(request, "Vui lòng điền đầy đủ thông tin nhận hàng.")
    return render(
        request,
        "store/checkout.html",
        {
            "cart_items": items,
            "cart_total_quantity": total_quantity,
            "cart_total_amount": total_amount,
            "display_cart_total_amount": _format_currency(total_amount),
            "initial_name": initial_name,
            "initial_email": initial_email,
            "initial_phone": initial_phone,
            "initial_address": initial_address,
            **pref,
        },
    )


def my_orders(request):
    unauthorized = _require_customer_account(request)
    if unauthorized:
        return unauthorized
    qs = DonHang.objects.filter(khach_hang=request.user).prefetch_related("items__san_pham")
    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    orders = list(page_obj.object_list)
    for order in orders:
        order.display_total_amount = _format_currency(order.tong_tien)
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







