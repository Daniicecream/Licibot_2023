from odoo import fields, models, api
from ast import literal_eval


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    bidding = fields.Boolean(default=False, string='Licitación')

    # Datos Licitación
    portal = fields.Many2one('crm.lead.bidding.portal', string='Portal')
    bidding_number = fields.Char('Nro Licitación')
    bidding_link = fields.Char('Link Licitación')
    bidding_type = fields.Many2one('crm.lead.bidding.type', string='Tipo Licitación')
    bidding_name = fields.Text(string='Nombre Licitación')
    services_description = fields.Text(string='Descripción Servicios')
    bases_file = fields.Binary(string='Archivos Base')
    other_files = fields.Binary(string='Otros Archivos')

    bidding_contact = fields.One2many('crm.lead.contact', 'lead_id', string='Contactos Licitación')
    bidding_timeline = fields.One2many('crm.lead.timeline', 'lead_id', string='Cronograma Licitación')
    bidding_anexxes = fields.One2many('crm.lead.anexxes', 'lead_id', string='Anexos Licitación')

class CrmLeadContact(models.Model):
    _name = 'crm.lead.contact'

    lead_id = fields.Many2one('crm.lead')
    contact_name = fields.Char(string='Nombre contacto')
    contact_position = fields.Char(string='Cargo')
    contact_info = fields.Char(string='Información')

class CrmLeadTimeline(models.Model):
    _name = 'crm.lead.timeline'
    
    lead_id = fields.Many2one('crm.lead')
    portal = fields.Many2one('crm.lead.bidding.portal', string='Portal', related='lead_id.portal')
    bidding_number = fields.Char('Nro Licitación', related='lead_id.bidding_number')
    bidding_name = fields.Text('Nombre Licitación', related='lead_id.bidding_name')
    timeline_activity = fields.Many2one('crm.lead.bidding.activity', string='Actividad/Evento')
    timeline_date = fields.Datetime(string='Fecha Licitación')
    timeline_status = fields.Many2one('crm.lead.bidding.status', string='Estado')

class CrmLeadAnexxes(models.Model):
    _name = 'crm.lead.anexxes'
    
    lead_id = fields.Many2one('crm.lead')
    portal = fields.Many2one('crm.lead.bidding.portal', string='Portal', related='lead_id.portal')
    bidding_number = fields.Char('Nro Licitación', related='lead_id.bidding_number')
    bidding_name = fields.Text('Nombre Licitación', related='lead_id.bidding_name')
    anex_name = fields.Char(string='Nombre Anexo')
    anex_title = fields.Char(string='Título Anexo')
    anex_deadline = fields.Datetime(string='Fecha Vencimiento Anexo')
    anex_format = fields.Many2one('crm.lead.bidding.format', string='Formato')
    anex_details = fields.Char(string='Detalles Anexo')
    anex_status = fields.Many2one('crm.lead.bidding.status', string='Estado')


class CrmLeadBiddingPortal(models.Model):
    _name = 'crm.lead.bidding.portal'

    name = fields.Char(string='Nombre')

class CrmLeadBiddingType(models.Model):
    _name = 'crm.lead.bidding.type'

    code = fields.Char(string='Código')
    name = fields.Char(string='Nombre')

class CrmLeadBiddingActivity(models.Model):
    _name = 'crm.lead.bidding.activity'

    code = fields.Char(string='Código')
    name = fields.Char(string='Nombre')

class CrmLeadBiddingStatus(models.Model):
    _name = 'crm.lead.bidding.status'

    name = fields.Char(string='Nombre')


class CrmLeadBiddingFormat(models.Model):
    _name = 'crm.lead.bidding.format'

    name = fields.Char(string='Nombre')