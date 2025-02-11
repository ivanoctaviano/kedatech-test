import json
import odoo

from http import HTTPStatus
from odoo.tests.common import tagged, HttpCase
from odoo.addons.kedatech_materials.tests.common import TestKedatechMaterialsCommon

HOST = "http://127.0.0.1:%s" % (odoo.tools.config["http_port"])


@tagged("-at_install", "post_install")
class TestRestAPIMaterials(TestKedatechMaterialsCommon, HttpCase):

    def test_get_material(self):
        """
        Unit Test API Get Material
        """

        response = self.url_open("/material?material_type=jeans", headers=self.headers)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_material(self):
        """
        Unit Test API Create Material
        """

        # positive case
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

        # negative case (required data)
        data = {}
        response = self.opener.post(create_url, headers=self.headers, data=json.dumps(data))
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        material_data = json.loads(response.content)["data"]
        negative_response = {
            "name": "Required",
            "code": "Required",
            "type": "Required",
            "buy_price": "Required",
            "supplier_id": "Required",
        }
        self.assertEqual(material_data, negative_response)

        # negative case (invalid data type)
        data = {
            "name": 1,
            "code": 1,
            "type": 1,
            "buy_price": "test",
            "supplier_id": "test"
        }
        response = self.opener.post(create_url, headers=self.headers, data=json.dumps(data))
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        material_data = json.loads(response.content)["data"]
        negative_response = {
            "name": "Is not a string",
            "code": "Is not a string",
            "type": "Is not a string",
            "buy_price": "Is not a number",
            "supplier_id": "Is not an integer",
        }
        self.assertEqual(material_data, negative_response)

        # negative case (invalid data value)
        data = {
            "name": "Test 1",
            "code": "unit_test_1",
            "type": "test",
            "buy_price": 80,
            "supplier_id": -1
        }
        response = self.opener.post(create_url, headers=self.headers, data=json.dumps(data))
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        material_data = json.loads(response.content)["data"]
        negative_response = {
            "type": "Not valid value (fabric, jeans, cotton)",
            "buy_price": "Buy Price must be greater than or equal to 100",
            "supplier_id": "Not found",
        }
        self.assertEqual(material_data, negative_response)

        # negative case (duplicate code)
        data = {
            "name": "Test 1",
            "code": "unit_test_1",
            "type": "cotton",
            "buy_price": 250,
            "supplier_id": 14
        }
        response = self.opener.post(create_url, headers=self.headers, data=json.dumps(data))
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        material_data = json.loads(response.content)["data"]
        negative_response = {
            "code" : "Already exists"
        }
        self.assertEqual(material_data, negative_response)

    def test_update_material(self):
        """
        Unit Test API Update Material
        """
        # positive case
        update_data = {
            "name": "Test 2",
            "code": "unit_test_2",
            "type": "jeans",
            "buy_price": 150,
            "supplier_id": 1,
        }
        update_url = "%s%s/%s" % (HOST, "/material", self.material_id.id)

        response = self.opener.patch(update_url, headers=self.headers, data=json.dumps(update_data))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        material_data = json.loads(response.content)["data"]
        self.assertEqual(material_data["code"], update_data["code"])

        # negative case
        update_data = {
            "code": "unit_test_2"
        }
        update_url = "%s%s/%s" % (HOST, "/material", 0)

        response = self.opener.patch(update_url, headers=self.headers, data=json.dumps(update_data))
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_delete_material(self):
        """
        Unit Test API Delete Material
        """
        # positive case
        delete_url = "%s%s/%s" % (HOST, "/material", self.material_id.id)

        response = self.opener.delete(delete_url, headers=self.headers)

        self.assertEqual(response.status_code, HTTPStatus.OK)

        # negative case
        update_data = {
            "code": "unit_test_2"
        }
        update_url = "%s%s/%s" % (HOST, "/material", 0)

        response = self.opener.delete(update_url, headers=self.headers, data=json.dumps(update_data))
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)