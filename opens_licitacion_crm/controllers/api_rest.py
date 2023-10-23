# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import Response
from odoo.http import request
import json
from datetime import datetime, timedelta
from uuid import uuid4


class CrmLeadBiddingRestService(http.Controller):

    @http.route('/licitaciones', type='json', auth='public')
    def get_biddings(self):
        data = json.loads(request.httprequest.data)
        lead = request.env['crm.lead']
        bidding_type = request.env['crm.lead.bidding.type']
        contact = request.env['crm.lead.contact']
        timeline = request.env['crm.lead.timeline']
        token_model = request.env['crm.api.token']

        auth = request.httprequest.headers.get('Authorization')
        token = token_model.search([('token', '=', auth)])
        
        if token.due <= datetime.now():
            token.sudo().update({'active': False})
            return {'message': 'Token vencido. Genere otro.'}
        
        if token:
            for d in data['licitaciones']:
                bt = bidding_type.sudo().search([('code', '=', d['Tipo'])])

                vals = {
                    'name': d['Descripcion'],
                    'bidding': True,
                    'bidding_number': d['CodigoExterno'],
                    'bidding_type': bt.id if bt else None,
                    'bidding_name': d['Nombre'],
                    'services_description': d['Descripcion'],
                }
                new_lead = lead.sudo().create(vals)
                if new_lead:
                    contact.sudo().create({
                        'lead_id': new_lead.id,
                        'contact_name': d['NombreUsuario'],
                        'contact_position': d['CargoUsuario'],
                    })
                    timeline.sudo().create({
                        'lead_id': new_lead.id,
                        'timeline_date': d['FechaCierre']
                    })
                    return {'message': 'Licitación creada'}
        else:
            return {'message': 'No Autorizado'}

    @http.route('/token', type='http', auth='public')
    def get_token(self):
        ''' Genera un token para ser utilizado en creación de licitaciones
            - retorna json con token y fecha de vencimiento.'''
        hours = request.env['ir.config_parameter'].sudo().get_param('crm.horas_token')
        token = uuid4()
        model = request.env['crm.api.token'].sudo().create({
            "token": token,
            "active": True,
            "due": datetime.now() + timedelta(hours=int(hours))
        })
        response_data = {'token': model.token, 'due': model.due.strftime('%Y-%m-%d %H:%M:%S')}
        return Response(json.dumps(response_data), content_type='application/json')
