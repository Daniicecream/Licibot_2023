from odoo import fields, models, api, _

class LicibotConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    token_api_mp = fields.Char(
        string = 'Token de API Mercado Público',
        help = 'Token obtenido desde la api de mercado público, necesario para el correcto funcionamiento del módulo.\n'
                'Solicita el tuyo en https://api.mercadopublico.cl/modules/Participa.aspx',
        config_parameter = 'licibot.token_api_mp',
        default = 'Ingresa aquí tu token obtenido en mercado público'
    )

    def set_values(self):
        print('Licibot: Set Values Executed')
        super(LicibotConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('token_api_mp', self.token_api_mp)

    @api.model
    def get_values(self):
        print('Licibot: Get Values Executed')
        res = super(LicibotConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        token_api_mp = params.get_param('token_api_mp')
        res.update(
            token_api_mp = token_api_mp
        )
        return res

