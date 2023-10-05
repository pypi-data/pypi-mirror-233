# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StockProductionLot(models.Model):
    _name = "stock.production.lot"
    _inherit = ["stock.production.lot", "mixin.qr_code"]

    _qr_code_create_page = True
