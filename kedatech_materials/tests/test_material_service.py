import json
import odoo

from http import HTTPStatus
from odoo.tests.common import tagged, HttpCase
from odoo.addons.kedatech_materials.tests.common import TestKedatechMaterialsCommon

HOST = "http://127.0.0.1:%s" % (odoo.tools.config["http_port"])


@tagged("-at_install", "post_install")
class TestRestAPIMaterials(TestKedatechMaterialsCommon, HttpCase):

    def test_get_material(self):
        response = self.url_open("/material?material_type=jeans", headers=self.headers)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_material(self):
        data = {
            "name": "Test 1",
            "code": "unit_test_1",
            "type": "cotton",
            "buy_price": 250,
            "supplier_id": 14
        }

        create_url = "%s%s" % (HOST, "/material")

        response = self.opener.post(create_url, headers=self.headers, data=json.dumps(data))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        material_data = json.loads(response.content)["data"]
        self.assertEqual(material_data["code"], data["code"])

    def test_update_material(self):
        update_data = {
            "code": "unit_test_2"
        }
        update_url = "%s%s/%s" % (HOST, "/material", self.material_id.id)

        response = self.opener.patch(update_url, headers=self.headers, data=json.dumps(update_data))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        material_data = json.loads(response.content)["data"]
        self.assertEqual(material_data["code"], update_data["code"])

    def test_delete_material(self):
        delete_url = "%s%s/%s" % (HOST, "/material", self.material_id.id)

        response = self.opener.delete(delete_url, headers=self.headers)

        self.assertEqual(response.status_code, HTTPStatus.OK)