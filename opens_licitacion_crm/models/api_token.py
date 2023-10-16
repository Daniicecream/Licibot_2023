from odoo import fields, models, api
from ast import literal_eval
from datetime import datetime, timedelta


class CrmApiToken(models.Model):
    _name = 'crm.api.token'

    token = fields.Char('Token')
    active = fields.Boolean(default=False)
    due = fields.Datetime()