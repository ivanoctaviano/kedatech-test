# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name" : "KeDATech Material",
    "version" : "1.0",
    "author": "Ivan Octaviano",
    "description": """
        Manage Materials
    """,
    "depends" : ["base"],
    "data": [
        "data/config_data.xml",
        "security/ir.model.access.csv",
        "views/material.xml"
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}
