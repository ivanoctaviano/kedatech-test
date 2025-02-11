import json

from odoo import http
from odoo.http import request
from . import helper
from .helper import JsonControllerMixin

import logging
_logger = logging.getLogger(__name__)


class Material(http.Controller):
    JsonControllerMixin.patch_for_json("/material")

    @http.route("/material", auth="public", csrf=False, methods=["POST"])
    def action_create_material(self):
        """
        API for Create Material
        """
        auth = helper.parse_header()
        token = request.env["ir.config_parameter"].sudo().get_param("kedatech.static_token", "ABC")

        if auth == token:
            body = json.loads(request.httprequest.data.decode("utf-8"))

            vals, invalid_payload = self.check(body)
            if invalid_payload:
                return helper.response(code=400, success=False, data=invalid_payload)

            material_obj = request.env["material"].sudo()
            
            exist_material = material_obj.search([("code","=",body.get("code"))])
            if exist_material:
                return helper.response(code=400, success=False, data={"code": "Already exists"})

            try:
                material_id = material_obj.create(vals)
                data = {
                    "id": material_id.id,
                    "name": material_id.name,
                    "code": material_id.code,
                }
                return helper.response(code=200, success=True, message="Success", data=data)
            except Exception as e:
                _logger.info("Failed to create material : %s", e)
                return helper.response(code=500, success=False, message="Internal Server Error")
        else:
            return helper.response(code=401, success=False, message="Token Not Found")

    @http.route("/material", auth="public", csrf=False, methods=["GET"])
    def action_get_material(self):
        """
        API for Get Material
        """
        auth = helper.parse_header()
        token = request.env["ir.config_parameter"].sudo().get_param("kedatech.static_token")

        if auth == token:
            domain = []
            data = []
            material_obj = request.env["material"].sudo()
            filter_type = request.httprequest.args.get("material_type")
            if filter_type:
                domain += [("type", "=", filter_type)]

            try:
                materials = material_obj.search(domain)
                for rec in materials:
                    material = {
                        "material_id": rec.id,
                        "material_name": rec.name,
                        "material_code": rec.code,
                        "material_type": rec.type,
                        "material_buy_price": rec.buy_price,
                        "related_supplier": {
                            "supplier_id": rec.related_supplier_id.id,
                            "name": rec.related_supplier_id.name,
                            "address": rec.related_supplier_id.street,
                        }
                    }
                    data.append(material)

                return helper.response(code=200, success=True, message="Data found", data=data)
            except Exception as e:
                _logger.info("Failed to get material detail : %s", e)
                return helper.response(code=500, success=False, message="Internal Server Error")
        else:
            return helper.response(code=401, success=False, message="Token Not Found")
    
    @http.route("/material/<int:material_id>", auth="public", csrf=False, methods=["PATCH"])
    def action_update_material(self, material_id):
        """
        API for Update Material
        """
        auth = helper.parse_header()
        token = request.env["ir.config_parameter"].sudo().get_param("kedatech.static_token")

        if auth == token:

            material_obj = request.env["material"].sudo()
            body = json.loads(request.httprequest.data.decode("utf-8"))
            
            exist_material = material_obj.search([("id","=",material_id)])
            if not exist_material:
                return helper.response(code=400, success=False, data={"material": "material id not found"})

            exist_material_code = material_obj.search([("id","!=",material_id),("code","=",body.get("code"))])
            if exist_material_code:
                return helper.response(code=400, success=False, data={"code": "Already exists"})

            vals, invalid_payload = self.check(body, res_id=exist_material.id)
            if invalid_payload:
                return helper.response(code=400, success=False, data=invalid_payload)

            try:
                exist_material.write(vals)
                data = {
                    "id": exist_material.id,
                    "name": exist_material.name,
                    "code": exist_material.code,
                }
                return helper.response(code=200, success=True, message="Success", data=data)
            except Exception as e:
                _logger.info("Failed to update material : %s", e)
                return helper.response(code=500, success=False, message="Internal Server Error")
        else:
            return helper.response(code=401, success=False, message="Token Not Found")

    @http.route("/material/<int:material_id>", auth="public", csrf=False, methods=["DELETE"])
    def action_delete_material(self, material_id):
        """
        API for Delete Material
        """
        auth = helper.parse_header()
        token = request.env["ir.config_parameter"].sudo().get_param("kedatech.static_token")

        if auth == token:

            material_obj = request.env["material"].sudo()
            
            exist_material = material_obj.search([("id","=",material_id)])
            if not exist_material:
                return helper.response(code=400, success=False, data={"material": "material id not found"})

            try:
                exist_material.unlink()
                return helper.response(code=200, success=True, message="Success", data={})
            except Exception as e:
                _logger.info("Failed to delete material : %s", e)
                return helper.response(code=500, success=False, message="Internal Server Error")
        else:
            return helper.response(code=401, success=False, message="Token Not Found")

    def check(self, body, res_id=None):
        """
        Validation Payload for Create and Update Material
        """
        vals = {}
        invalid = {}

        if not res_id:
            if not body.get("name"):
                invalid["name"] = "Required"
            if not body.get("code"):
                invalid["code"] = "Required"
            if not body.get("type"):
                invalid["type"] = "Required"
            if not body.get("buy_price"):
                invalid["buy_price"] = "Required"
            if not body.get("supplier_id"):
                invalid["supplier_id"] = "Required"

        if body.get("name"):
            if not isinstance(body.get("name"), str):
                invalid["name"] = "Is not a string"
            else:
                vals["name"] = body.get("name")

        if body.get("code"):
            if not isinstance(body.get("code"), str):
                invalid["code"] = "Is not a string"
            else:
                vals["code"] = body.get("code")

        if body.get("type"):
            if not isinstance(body.get("type"), str):
                invalid["type"] = "Is not a string"
            elif body.get("type") not in ("fabric", "jeans", "cotton"):
                invalid["type"] = "Not valid value (fabric, jeans, cotton)"
            else:
                vals["type"] = body.get("type")

        if body.get("buy_price"):
            if not isinstance(body.get("buy_price"), (float, int)):
                invalid["buy_price"] = "Is not a number"
            else:
                if body.get("buy_price") < 100:
                    invalid["buy_price"] = "Buy Price must be greater than or equal to 100"
            vals["buy_price"] = body.get("buy_price")

        if body.get("supplier_id"):
            if not isinstance(body.get("supplier_id"), int):
                invalid["supplier_id"] = "Is not an integer"
            else:
                partner_id = request.env["res.partner"].sudo().search([("id","=",body.get("supplier_id"))])
                if not partner_id:
                    invalid["supplier_id"] = "Not found"
            vals["related_supplier_id"] = body.get("supplier_id")

        return vals, invalid