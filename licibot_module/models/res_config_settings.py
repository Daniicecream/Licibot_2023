from odoo import fields, models, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    token_api_mp = fields.Char(string = 'Token de API Mercado Público')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('token_api_mp', self.token_api_mp)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        token_api_mp = params.get_param('token_api_mp')
        res.update(
            token_api_mp = token_api_mp
        )
        return res