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
