# -*- coding: utf-8 -*-
import uuid

from odoo import api, fields, tools, models, _
from odoo import http
from odoo.exceptions import UserError, ValidationError
from odoo.http import Response
from odoo.http import request
from werkzeug.exceptions import NotFound, Unauthorized, Forbidden, BadRequest
import json
from datetime import datetime, timedelta
import requests
import time
from dateutil.parser import parse
import hmac
import hashlib
import base64

from uuid import uuid4


class CrmLeadBiddingRestService(http.Controller):

    @http.route('/licitaciones', type='json', auth='none')
    def get_biddings(self):
        data = json.loads(request.httprequest.data)
        lead = request.env['crm.lead']
        bidding_type = request.env['crm.lead.bidding.type']
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
                    'contact_name': d['NombreUsuario'],
                    'contact_position': d['CargoUsuario'],
                    'timeline_date': d['FechaCierre']
                }
                lead.sudo().create(vals)
                return {'message': 'Licitación creada'}
        else:
            return {'message': 'No Autorizado'}


    @http.route('/token', type='http', auth='public')
    def get_token(self):
        hours = request.env['ir.config_parameter'].sudo().get_param('crm.horas_token')
        token = uuid4()
        model = request.env['crm.api.token']
        data = {"token": token, 'active': True}
        rec = model.sudo().create(data)
        rec.sudo().write({'due': rec.create_date+timedelta(hours=int(hours))}) # crear parametro sistema
        return Response(str(token))