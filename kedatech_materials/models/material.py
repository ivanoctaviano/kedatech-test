from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class Material(models.Model):
    _name = "material"
    _description = "Master Data Material"

    code = fields.Char(string="Material Code", required=True)
    name = fields.Char(string="Material Name", required=True)
    type = fields.Selection(string="Material Type", required=True, selection=[
        ("fabric", "Fabric"),
        ("jeans", "Jeans"),
        ("cotton", "Cotton"),
    ])
    buy_price = fields.Float(string="Material Buy Price", required=True)
    related_supplier_id = fields.Many2one("res.partner", required=True)

    _sql_constraints = [
        ("code_uniq", "unique(code)", "Material Code must be unique !"),
    ]

    @api.constrains("buy_price")
    def _check_buy_price(self):
        for rec in self:
            if rec.buy_price < 100:
                raise ValidationError(_("Buy Price must be greater than or equal to 100"))