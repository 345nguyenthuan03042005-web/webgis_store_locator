from datetime import time
from unittest.mock import patch

from django.test import TestCase

from modules.spatial.controllers import _store_dict
from modules.store.models import ChuoiCuaHang, CuaHang


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
