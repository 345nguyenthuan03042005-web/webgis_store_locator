from datetime import time
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from modules.store.controllers import ROLE_ADMIN, ROLE_USER, _ensure_role_groups
from modules.spatial.controllers import _store_dict
from modules.store.models import ChiTietDonHang, ChuoiCuaHang, CuaHang, DonHang, SanPham


class SmokeTests(TestCase):
    def test_home_page_ok(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_map_page_ok(self):
        response = self.client.get("/map/")
        self.assertEqual(response.status_code, 200)

    def test_ping_api_ok(self):
        response = self.client.get("/tools/ping/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"ok": True, "message": "pong", "pong": True})


class StorePayloadTests(TestCase):
    def setUp(self):
        self.chain = ChuoiCuaHang.objects.create(ten="CIRCLEK")

    def test_store_payload_includes_business_fields(self):
        store = CuaHang.objects.create(
            chuoi=self.chain,
            ten="CK Test",
            dia_chi="1 Test",
            quan_huyen="Quan 1",
            vi_do=10.77,
            kinh_do=106.70,
            mo_cua=time(7, 0),
            dong_cua=time(22, 0),
            hoat_dong_24h=False,
        )
        payload = _store_dict(store)
        self.assertEqual(payload["open_time"], "07:00")
        self.assertEqual(payload["close_time"], "22:00")
        self.assertEqual(payload["is_24h"], False)
        self.assertIn("is_open_now", payload)
        self.assertIn("business_hours", payload)
        self.assertEqual(payload["coord_source"], "db")

    def test_store_payload_24h(self):
        store = CuaHang.objects.create(
            chuoi=self.chain,
            ten="CK 24h",
            dia_chi="2 Test",
            quan_huyen="Quan 1",
            vi_do=10.78,
            kinh_do=106.71,
            hoat_dong_24h=True,
        )
        payload = _store_dict(store)
        self.assertEqual(payload["is_24h"], True)
        self.assertEqual(payload["business_hours"], "24/7")
        self.assertEqual(payload["is_open_now"], True)


class SmartSearchTests(TestCase):
    def setUp(self):
        self.chain = ChuoiCuaHang.objects.create(ten="CIRCLEK")
        CuaHang.objects.create(
            chuoi=self.chain,
            ten="Circle K Test",
            dia_chi="236 Le Van Sy, Tan Binh, TP.HCM",
            quan_huyen="Tan Binh",
            vi_do=10.7934,
            kinh_do=106.6789,
            hoat_dong_24h=True,
        )

    @patch("modules.spatial.controllers._call_photon_search_safe")
    @patch("modules.spatial.controllers._call_nominatim_search_safe")
    def test_smart_search_geocode_address_mode(self, mock_nominatim, mock_photon):
        mock_photon.return_value = ([], None)
        mock_nominatim.return_value = (
            [
                {
                    "display_name": "236 Le Van Sy, Tan Binh, Thanh pho Ho Chi Minh, Viet Nam",
                    "lat": "10.7934",
                    "lon": "106.6789",
                }
            ],
            None,
        )

        response = self.client.post(
            "/tools/smart-search/",
            data='{"ten":"CIRCLEK","dia_chi":"236 Le Van Sy, Tan Binh, Thanh pho Ho Chi Minh, Viet Nam","max_km":1}',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["mode"], "geocode_address")
        self.assertTrue(data["ok"])
        self.assertEqual(data["count"], 1)


class AdminOrderManagementTests(TestCase):
    def setUp(self):
        groups = _ensure_role_groups()
        self.admin = User.objects.create_user(
            username="admin_orders",
            password="Abc12345!",
            is_staff=True,
        )
        self.admin.groups.add(groups[ROLE_ADMIN])

        self.customer = User.objects.create_user(
            username="customer_orders",
            password="Abc12345!",
        )
        self.customer.groups.add(groups[ROLE_USER])

        self.product = SanPham.objects.create(
            ten="San pham test",
            gia_ban=25000,
        )
        self.order = DonHang.objects.create(
            khach_hang=self.customer,
            ho_ten_nguoi_nhan="Khach Test",
            so_dien_thoai="0123456789",
            dia_chi_giao_hang="Dia chi test",
            trang_thai="pending",
            tong_so_luong=1,
            tong_tien=25000,
        )

    def test_admin_order_list_can_filter_by_status(self):
        self.client.force_login(self.admin)

        response = self.client.get("/admin/don-hang/", {"status": "pending"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["status_filter"], "pending")
        rows = response.context["rows"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["object"].pk, self.order.pk)
        self.assertEqual(rows[0]["status_actions"][0]["value"], "confirmed")

    def test_admin_can_confirm_ship_and_deliver_order(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            f"/admin/orders/{self.order.pk}/confirmed/",
            {"status": "pending", "page": 1},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.trang_thai, "confirmed")

        response = self.client.get(
            f"/admin/orders/{self.order.pk}/shipping/",
            {"status": "confirmed", "page": 1},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.trang_thai, "shipping")

        response = self.client.get(
            f"/admin/orders/{self.order.pk}/delivered/",
            {"status": "shipping", "page": 1},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.trang_thai, "delivered")

    def test_admin_cannot_cancel_delivered_order(self):
        self.client.force_login(self.admin)
        self.order.trang_thai = "delivered"
        self.order.save(update_fields=["trang_thai"])

        response = self.client.get(
            f"/admin/orders/{self.order.pk}/cancelled/",
            {"status": "delivered", "page": 1},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.trang_thai, "delivered")

    def test_done_filter_includes_delivered_orders(self):
        self.client.force_login(self.admin)
        self.order.trang_thai = "delivered"
        self.order.save(update_fields=["trang_thai"])

        response = self.client.get("/admin/don-hang/", {"status": "done"})

        self.assertEqual(response.status_code, 200)
        rows = response.context["rows"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["object"].pk, self.order.pk)


class CustomerPurchaseFlowTests(TestCase):
    def setUp(self):
        groups = _ensure_role_groups()
        self.admin = User.objects.create_user(
            username="admin_flow",
            password="Abc12345!",
            is_staff=True,
        )
        self.admin.groups.add(groups[ROLE_ADMIN])

        self.customer = User.objects.create_user(
            username="customer_flow",
            password="Abc12345!",
        )
        self.customer.groups.add(groups[ROLE_USER])

        self.product = SanPham.objects.create(
            ten="San pham mua ngay",
            gia_ban=30000,
        )

    def test_buy_now_redirects_guest_to_login_then_checkout(self):
        response = self.client.post(
            f"/cart/add/{self.product.pk}/",
            {"next": "/checkout/"},
        )

        self.assertRedirects(response, "/user/login/?next=/checkout/")

        response = self.client.post(
            "/user/login/?next=/checkout/",
            {"username": "customer_flow", "password": "Abc12345!", "next": "/checkout/"},
        )

        self.assertRedirects(response, "/checkout/")

    def test_add_to_cart_redirects_guest_to_login_then_cart(self):
        response = self.client.post(
            f"/cart/add/{self.product.pk}/",
            {"next": "/cart/"},
        )

        self.assertRedirects(response, "/user/login/?next=/cart/")

        response = self.client.post(
            "/user/login/?next=/cart/",
            {"username": "customer_flow", "password": "Abc12345!", "next": "/cart/"},
        )

        self.assertRedirects(response, "/cart/")

    def test_admin_is_redirected_to_customer_login_when_buying(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            f"/cart/add/{self.product.pk}/",
            {"next": "/checkout/"},
        )

        self.assertRedirects(response, "/user/login/?next=/checkout/")

    def test_regular_user_cannot_access_admin_dashboard(self):
        self.client.force_login(self.customer)

        response = self.client.get("/admin/")

        self.assertRedirects(response, "/admin/login/")

    def test_admin_cannot_access_user_dashboard(self):
        self.client.force_login(self.admin)

        response = self.client.get("/user/")

        self.assertRedirects(response, "/admin/")

    def test_checkout_creates_order_and_item(self):
        self.client.force_login(self.customer)
        session = self.client.session
        session["cart"] = {str(self.product.pk): 2}
        session.save()

        response = self.client.post(
            "/checkout/",
            {
                "receiver_name": "Nguyen Van A",
                "phone": "0900000000",
                "address": "123 Duong Test",
                "note": "Giao gio hanh chinh",
            },
        )

        self.assertRedirects(response, "/orders/")
        order = DonHang.objects.get(khach_hang=self.customer)
        self.assertEqual(order.tong_so_luong, 2)
        self.assertEqual(order.tong_tien, 60000)
        self.assertTrue(ChiTietDonHang.objects.filter(don_hang=order, san_pham=self.product, so_luong=2).exists())
