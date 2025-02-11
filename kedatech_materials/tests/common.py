# -*- coding: utf-8 -*-
from odoo.tests.common import HttpCase

class TestKedatechMaterialsCommon(HttpCase):

    def setUp(self):
        super().setUp()
        self.static_token = "token_unit_test"
        param_obj = self.env["ir.config_parameter"]
        partner_obj = self.env["res.partner"]
        material_obj = self.env["material"]

        param_obj.set_param("kedatech.static_token", self.static_token)
        self.headers = {
            "Authorization": "Bearer %s" % self.static_token
        }
        self.partner_id = partner_obj.create({
            "name": "Partner Test"
        })
        self.material_id = material_obj.create({
            "name": "Material Test",
            "code": "material_test",
            "type": "jeans",
            "buy_price": 120,
            "related_supplier_id": self.partner_id.id
        })