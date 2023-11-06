'''
# Instalar librerías python
pip3 install -U scipy pandas requests numpy scikit-learn
# Instalar localización de es
sudo apt-get install language-pack-es
# Para que la funcion de generar el pickle pueda insertar un archivo .sav generado
Ejecutar chmod 777 /opt/addons_opens/licibot_module/Inputs 
'''

'''
TODO "Limpiar código basura y comentarios innecesarios."
'''

# Importando librerías Odoo (?)
from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError
import logging

# Importando librerías externas
import requests 
import time
import datetime
import pandas as pd
import locale
import re
from dateutil.parser import parse

# Importando librerías externas ML
import pickle
import numpy as np

# Generate pickle
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import warnings
import sys
if not sys.warnoptions:
    warnings.simplefilter("ignore")
np.random.seed(42)

_logger = logging.getLogger(__name__)

# Configura moneda local CLP
locale.setlocale(locale.LC_MONETARY, 'es_CL.utf8')

class Organismo(models.Model):
    _name = 'licibot.organismo'

    nombre_organismo = fields.Char(string='Nombre organismo') 

class UnidadCompra(models.Model):
    _name = 'licibot.unidad.compra'

    rut_unidad = fields.Char(string='Rut unidad') 
    nombre_unidad = fields.Char(string='Nombre unidad')
    direccion_unidad = fields.Char(string='Dirección unidad')
    comuna_unidad = fields.Char(string='Comuna unidad')
    region_unidad = fields.Char(string='Región unidad')
    sii_anio_comercial = fields.Integer(string='SII Año comercial')
    sii_razon_social = fields.Char(string='SII razón social')
    sii_tramo_segun_ventas = fields.Integer(string='SII Tramo según venta')
    sii_num_trab_dep = fields.Integer(string='SII Num. Trab. Depen.')
    sii_fecha_ini_acta = fields.Datetime(string='SII Fecha inicio Act.')
    sii_fecha_prim_ins = fields.Datetime(string='SII Fecha Primera Inscripción')
    sii_fecha_term_giro = fields.Datetime(string='SII Fecha Termino Giro')
    sii_tipo_term_giro = fields.Char(string='SII Tipo termino giro')
    sii_tipo_contrib = fields.Char(string='SII Tipo contribución')
    sii_subtipo_contrib = fields.Char(string='SII Subtipo contribución')
    sii_tramo_cap_prop_positivo = fields.Integer(string='SII Tramo Cap. Prop. Positivo')
    sii_tramo_cap_prop_negativo = fields.Integer(string='SII Tramo Cap. Prop. Negativo')
    sii_rubro_eco = fields.Char(string='SII Rubro Económico')
    sii_subrubro_eco = fields.Char(string='SII Subrubro Económico')
    sii_region = fields.Char(string='SII Región')
    sii_comuna = fields.Char(string='SII Comuna')
    sii_act_eco = fields.Char(string='SII Actividad económica')
    ranking = fields.Integer(string='Ranking')
    organismo_id = fields.Many2one('licibot.organismo', string = 'Organismo_id')

class TipoCompetidor (models.Model):
    _name = 'licibot.tipo.competidor'

    nom_tipo_comp = fields.Char(string = 'Nombre Tipo Competidor')

class Proveedor (models.Model):
    _name = 'licibot.proveedor'

    rut_proveedor = fields.Char(string = 'Rut Proveedor')
    nombre_proveedor = fields.Char(string = 'Nombre Proveedor')
    tipo_competidor_id = fields.Many2one('licibot.tipo.competidor', string = 'tipoCompetidor_id')

class Categoria (models.Model):
    _name = 'licibot.categoria'

    nom_categoria = fields.Char(string = 'Nombre Categoria')

class TipoLicitacion (models.Model):
    _name = 'licibot.tipo.licitacion'

    id_tipo_licitacion = fields.Char(string = 'ID Tipo Licitación')
    nom_tipo_licitacion = fields.Char(string = 'Nombre Tipo Licitación')

class UnidadMonetaria (models.Model):
    _name = 'licibot.unidad.monetaria'

    id_unidad_monetaria = fields.Char(string = 'ID Unidad Monetaria')
    nom_unidad_monetaria = fields.Char(string = 'Nombre Unidad Monetaria')

class MontoEstimado (models.Model):
    _name = 'licibot.monto.estimado'

    nom_monto_estimado = fields.Char(string = 'Nombre Monto Estimado')

class ModalidadPago (models.Model):
    _name = 'licibot.modalidad.pago'

    nom_modalidad_pago = fields.Char(string = 'Nombre Modalidad Pago')

class UnidadTiempoContrato (models.Model):
    _name = 'licibot.unidad.tiempo.contrato'

    nom_uni_tiempo_con = fields.Char(string = 'Nombre Unidad Tiempo Contrato')

class UnidadTiempoEvaluacion (models.Model):
    _name = 'licibot.unidad.tiempo.evaluacion'

    nom_uni_tiempo_ev = fields.Char(string = 'Nombre Unidad Tiempo Evaluacion')

class TipoActoAdministrativo (models.Model):
    _name = 'licibot.tipo.acto.administrativo'

    nom_acto_admin = fields.Char(string = 'Nombre Tipo Acto Administrativo')

class Adjudicacion (models.Model):
    _name = 'licibot.adjudicacion'

    num_admin_adjudicacion = fields.Char(string = 'Número Administrativo Adjudicación')
    fecha_admin_adjudicacion = fields.Datetime(string = 'Fecha Administrativa Adjudicación')
    num_oferentes = fields.Char(string = 'Fecha Administrativa Adjudicación')
    url_acta = fields.Char(string = 'Fecha Administrativa Adjudicación')
    tipo_acto_admin_id = fields.Many2one('licibot.tipo.acto.administrativo', string = 'TipoActoAdmin_id ')

class Licitacion(models.Model):
    _name = 'licibot.licitacion'

    codigo_externo = fields.Char(string = 'Código Externo')
    nombre = fields.Char(string = 'Nombre')
    codigo_estado = fields.Integer(string = 'Código Estado')
    descripcion = fields.Char(string = 'Descripción')
    fecha_cierre_1 = fields.Datetime(string = 'Fecha Cierre (1)')
    estado = fields.Char(string = 'Estado')
    dias_cierre_licitacion = fields.Integer(string = 'Días Cierre Licitación')
    informada = fields.Integer(string = 'Informada')
    codigo_tipo = fields.Integer(string = 'Código Tipo')
    tipo_convocatoria = fields.Integer(string = 'Tipo Convocatoria')
    etapas = fields.Integer(string = 'Etapas')
    estado_etapas = fields.Integer(string = 'Estado Etapas')
    toma_razon = fields.Integer(string = 'Toma Razón')
    estado_pub_ofertas = fields.Integer(string = 'Estado Publicidad Ofertas')
    justificacion_pub = fields.Char(string = 'Justiciación Publicidad')
    estado_cs = fields.Integer(string = 'Estado CS')
    contrato = fields.Integer(string = 'Contrato')
    obras = fields.Integer(string = 'Obras')
    cant_reclamos = fields.Integer(string = 'Cantidad de Reclamos')
    fecha_creacion = fields.Datetime(string = 'Fecha Creación')
    fecha_cierre_2 = fields.Datetime(string = 'Fecha Cierre (2)')
    fecha_inicio = fields.Datetime(string = 'Fecha Inicio')
    fecha_final = fields.Datetime(string = 'Fecha Final')
    fecha_pub_respuestas = fields.Datetime(string = 'Fecha Publicación Respuestas')
    fecha_act_aper_tec = fields.Datetime(string = 'Fecha Acto Apertura Técnica')
    fecha_act_aper_eco = fields.Datetime(string = 'Fecha Acto Apertura Económica')
    fecha_publicacion = fields.Datetime(string = 'Fecha Publicación')
    fecha_adjudicacion = fields.Datetime(string = 'Fecha Adjudicación')
    fecha_est_adjudicacion = fields.Datetime(string = 'Fecha Estimada Adjudicación')
    fecha_soporte_fisico = fields.Datetime(string = 'Fecha Soporte Fisico')
    fecha_tiempo_eval = fields.Datetime(string = 'Fecha Tiempo Evaluación')
    fecha_estimada_firma = fields.Datetime(string = 'Fecha Estimada Firma')
    fecha_usuario = fields.Datetime(string = 'Fecha Usuario')
    fecha_visita_terreno = fields.Datetime(string = 'Fecha Visita Tereno')
    fecha_entrega_antecedentes = fields.Datetime(string = 'Fecha Entrega Antecedentes')
    uni_tiempo_eval = fields.Integer(string = 'Unidad de Tiempo de Evaluación')
    direccion_visita = fields.Char(string = 'Dirección de Visita')
    direccion_entrega = fields.Char(string = 'Dirección de Entrega')
    estimacion = fields.Integer(string = 'Estimación')
    fuente_financiamiento = fields.Char(string = 'Fuente Financiamiento')
    visibilidad_monto = fields.Integer(string = 'Visibilidad Monto')
    monto_estimado = fields.Float(string = 'Monto Estimado')
    tiempo = fields.Integer(string = 'Tiempo')
    tipo_pago = fields.Integer(string = 'Tipo de Pago')
    nom_resp_pago = fields.Char(string = 'Nombre del Responsable de Pago')
    email_resp_pago = fields.Char(string = 'Email del Responsable de Pago')
    nom_resp_contrato = fields.Char(string = 'Nombre del Responsable de Contrato')
    email_resp_contrato = fields.Char(string = 'Email del Responsable de Contrato')
    fono_resp_contrato = fields.Char(string = 'Fono del Responsable de Contrato')
    prohibicion_cont = fields.Char(string = 'Prohibición Contratación')
    subcontratacion = fields.Integer(string = 'Subcontratación')
    tiempo_duracion_con = fields.Integer(string = 'Tiempo Duración Contrato')
    just_monto_estimado = fields.Char(string = 'Justificación Monto Estimado')
    obs_contractual = fields.Char(string = 'Observación Contract')
    ext_plazo = fields.Integer(string = 'Extensión de Plazo')
    es_base_tipo = fields.Integer(string = 'Es Base Tipo')
    uni_tiempo_cont_lic = fields.Integer(string = 'Unidad de Tiempo de Contrato')
    valor_tiempo_renov = fields.Integer(string = 'Valor Tiempo Renovación')
    periodo_tiempo_renov = fields.Char(string = 'Periodo Tiempo Renovación')
    es_renovable = fields.Integer(string = 'Es Renovable')
    cantidad_total = fields.Integer(string = 'Cantidad Total')
    codigo_contacto = fields.Integer(string = 'Código Contacto')
    rut_contacto = fields.Char(string = 'Rut Contacto')
    nom_contacto = fields.Char(string = 'Nombre Contacto')
    cargo_contacto = fields.Char(string = 'Cargo Contacto')
    adjudicacion_id = fields.Many2one('licibot.adjudicacion', string = 'Adjudicacion_id')
    tipo_licitacion_id = fields.Many2one('licibot.tipo.licitacion', string = 'tipoLicitacion_id')
    uni_tiempo_ev_id = fields.Many2one('licibot.unidad.tiempo.evaluacion', string = 'UniTiempoEv_id')
    unidad_monetaria_id = fields.Many2one('licibot.unidad.monetaria', string = 'UnidadMonetaria_id')
    monto_estimado_id = fields.Many2one('licibot.monto.estimado', string = 'MontoEstimado_id')
    uni_tiempo_con_id = fields.Many2one('licibot.unidad.tiempo.contrato', string = 'UniTiempoCon_id')
    modalidad_pago_id = fields.Many2one('licibot.modalidad.pago', string = 'ModalidadPago_id')
    unidad_compra_id = fields.Many2one('licibot.unidad.compra', string = 'UnidadCompra_id')

    """
    =================================================================
                        FUNCIONES DE INSERCIÓN
    =================================================================
    """
    # Falta testing.
    def insertar_organismo (self, codigo_organismo, nombre_organismo):
 
        if codigo_organismo:

            cod_org_clean = codigo_organismo.strip()

            organismo_exists = self.env['licibot.organismo'].sudo().search([('id', '=', cod_org_clean)])
            
            if organismo_exists:
                _logger.info(f"El organismo {cod_org_clean}: {nombre_organismo}, ya existe en la base de datos")
            else:
                # self.env['licibot.organismo'].sudo().create({'id': cod_org_clean, 'nombre_organismo': nombre_organismo})
                query_insertar_organismo = f'''insert into licibot_organismo (id, nombre_organismo) values ('{cod_org_clean}','{nombre_organismo}');'''
                self.env.cr.execute(query_insertar_organismo)

        else:
            _logger.info(f"!!! Código organismo nulo. Omitiendo inserción de datos en tabla organismo...")
   
    # Falta testing
    def insertar_unidadCompra (self, codigo_unidad, rut_unidad, nombre_unidad, direccion_unidad, comuna_unidad, region_unidad, organismo_id): # Info SII cargada posteriormente con queries (momentaneo)
        
        if codigo_unidad:

            uc_clean = codigo_unidad.strip()
            cod_org_clean = int(organismo_id.strip())

            unidadCompra_exists = self.env['licibot.unidad.compra'].sudo().search([('id', '=', uc_clean)])
            ### Intención de traer la ID de organismo
            # cod_org_clean = self.env['licibot.organismo'].sudo().search([('id','=', organismo_id)])

            if unidadCompra_exists:
                _logger.info(f"La unidad de compra {uc_clean}: {nombre_unidad}, ya existe en la base de datos.")
            else:
                # self.env['licibot.unidad.compra'].sudo().create({
                #     'id' : uc_clean, 
                #     'rut_unidad' : rut_unidad.strip(), 
                #     'nombre_unidad' : nombre_unidad.strip(), 
                #     'direccion_unidad' : direccion_unidad.strip(), 
                #     'comuna_unidad' : comuna_unidad.strip(), 
                #     'region_unidad' : region_unidad.strip(), 
                #     'organismo_id' : self.is_null_int(cod_org_clean.id) ## FK NULA EN BD
                # })    
                query_insertar_uc = f'''
                insert into licibot_unidad_compra (id, rut_unidad, nombre_unidad, direccion_unidad, comuna_unidad, region_unidad, organismo_id) 
                values ('{uc_clean}','{rut_unidad.strip()}', '{nombre_unidad.strip()}', '{direccion_unidad.strip()}', '{comuna_unidad.strip()}', '{region_unidad.strip()}', {cod_org_clean});'''
                self.env.cr.execute(query_insertar_uc)
        else:
            _logger.info(f"!!! código unidad nulo. Omitiendo inserción de datos en tabla unidad...")
   
    # Falta testing. ID AUTOMATICA POR ODOO
    def insertar_proveedor(self, rut_proveedor, nombre_proveedor):
        
        if rut_proveedor:

            rut_prov_clean = rut_proveedor.strip()
            proveedor_exists = self.env['licibot.proveedor'].sudo().search([('rut_proveedor', '=', rut_prov_clean)])

            if proveedor_exists:
                _logger.info(f"El proveedor {rut_prov_clean} {nombre_proveedor} ya existe en la base de datos.")
            else:
                self.env['licibot.proveedor'].sudo().create({
                    'rut_proveedor': rut_prov_clean,
                    'nombre_proveedor': nombre_proveedor.strip(),
                    'tipo_competidor_id': self.identificar_tipo_competidor(nombre_proveedor),
                })
        else:
            _logger.info("¡RUT de proveedor nulo. Omitiendo inserción de datos en la tabla proveedor...")
  
    # Falta testing
    def insertar_categoria(self, codigo_categoria, nom_categoria):

        if codigo_categoria:
            
            cod_cat_clean = int(codigo_categoria.strip())
            categoria_exists = self.env['licibot.categoria'].sudo().search([('id', '=', cod_cat_clean)])

            if categoria_exists:
                _logger.info(f"La categoría {cod_cat_clean}: {nom_categoria} ya existe en la base de datos.")
            else:
                # self.env['licibot.categoria'].sudo().create({
                #     'id': cod_cat_clean,
                #     'nom_categoria': nom_categoria.strip(),
                # })
                query_insertar_categoria = f'''
                insert into licibot_categoria (id, nom_categoria) 
                values ('{cod_cat_clean}','{nom_categoria.strip()}');'''
                self.env.cr.execute(query_insertar_categoria)
        else:
            _logger.info("¡Código de categoría nulo. Omitiendo inserción de datos en la tabla categoría...")
   
    # Falta testing
    def insertar_productoServicio(self, codigo_producto, nom_prod_servicio, categoria_id):
        if codigo_producto:
            cod_cat_clean = int(categoria_id.strip())
            producto_servicio_exists = self.env['licibot.producto.servicio'].sudo().search([('id', '=', codigo_producto)])
            ### Intención de traer la ID de categoria
            # cod_cat_clean = self.env['licibot.organismo'].sudo().search([('id','=', categoria_id)])

            if producto_servicio_exists:
                _logger.info(f"El producto/servicio {codigo_producto} {nom_prod_servicio} ya existe en la base de datos.")
            else:
                # self.env['licibot.producto.servicio'].sudo().create({
                #     'id': codigo_producto,
                #     'nom_prod_servicio': nom_prod_servicio.strip(),
                #     'categoria_id': self.is_null_int(cod_cat_clean),  
                # })
                query_insertar_ps = f'''
                insert into licibot_producto_servicio (id, nom_prod_servicio, categoria_id) 
                values ({codigo_producto},'{nom_prod_servicio.strip()}', {cod_cat_clean});'''
                self.env.cr.execute(query_insertar_ps)
        else:
            _logger.info("¡ID de producto/servicio nulo. Omitiendo inserción de datos en la tabla producto/servicio...")
   
    # Falta testing. ID AUTOMATICA POR ODOO
    def insertar_adjudicacion(self, num_admin_adjudicacion, fecha_admin_adjudicacion, num_oferentes, url_acta, tipo_acto_admn_id):
        
        if num_admin_adjudicacion:

            num_admin_adj_clean = num_admin_adjudicacion.strip()
            num_adj_exists = self.env['licibot.adjudicacion'].sudo().search([('num_admin_adjudicacion', '=', num_admin_adj_clean)])
            
            if num_adj_exists:
                _logger.info(f"La adjudicación {num_admin_adj_clean} ya existe en la base de datos.")
            else:
                self.env['licibot.adjudicacion'].sudo().create({
                    'num_admin_adjudicacion': num_admin_adj_clean,
                    'fecha_admin_adjudicacion': self.convertir_fecha(fecha_admin_adjudicacion),
                    'num_oferentes': self.is_null_int(num_oferentes),
                    'url_acta': self.is_null_str(url_acta),
                    'tipo_acto_admin_id': self.normalize_tipo_acto_admin(tipo_acto_admn_id),
                })
        else:
            _logger.info("¡Adjudicacion Nula. Omitiendo inserción de datos en la tabla de Adjudicaciones...")
     
    # Falta testing. ID AUTOMATICA POR ODOO
    def insertar_licitacion (
        self,
        codigo_externo, 
        nombre, 
        codigo_estado, 
        descripcion, 
        fecha_cierre_1, 
        estado, 
        dias_cierre_licitacion, 
        informada, 
        codigo_tipo, 
        tipo_convocatoria, 
        etapas, 
        estado_etapas, 
        toma_razon, 
        estado_pub_ofertas, 
        justificacion_pub, 
        contrato, 
        obras, 
        cant_reclamos, 
        fecha_creacion, 
        fecha_cierre_2, 
        fecha_inicio, 
        fecha_final, 
        fecha_pub_respuestas, 
        fecha_act_aper_tec, 
        fecha_act_aper_eco, 
        fecha_publicacion, 
        fecha_adjudicacion, 
        fecha_est_adjudicacion, 
        fecha_soporte_fisico, 
        fecha_tiempo_eval, 
        fecha_estimada_firma, 
        fecha_usuario, 
        fecha_visita_terreno, 
        fecha_entrega_antecedentes, 
        uni_tiempo_eval, 
        direccion_visita, 
        direccion_entrega, 
        estimacion, 
        fuente_financiamiento, 
        visibilidad_monto, 
        monto_estimado, 
        tiempo, 
        tipo_pago, 
        nom_resp_pago,
        email_resp_pago, 
        nom_resp_contrato, 
        email_resp_contrato, 
        fono_resp_contrato, 
        prohibicion_cont, 
        subcontratacion, 
        tiempo_duracion_con, 
        just_monto_estimado, 
        obs_contractual, 
        ext_plazo, 
        es_base_tipo, 
        uni_tiempo_cont_lic, 
        valor_tiempo_renov, 
        periodo_tiempo_renov, 
        es_renovable, 
        cantidad_total, 
        codigo_contacto, 
        rut_contacto, 
        nom_contacto, 
        cargo_contacto, 
        adjudicacion_id, # ID ODOO
        tipo_licitacion_id, 
        uni_tiempo_ev_id,
        unidad_monetaria_id,
        monto_estimado_id,
        uni_tiempo_con_id,
        modalidad_pago_id,
        unidad_compra_id # ID MP
        ):
        num_adj = self.env['licibot.adjudicacion'].sudo().search([('num_admin_adjudicacion','=', adjudicacion_id)])
        clean_uc = int(unidad_compra_id.strip())
        # tipo_licitacion_select = self.env['licibot.tipo.licitacion'].sudo().search([('id_tipo_licitacion','=', tipo_licitacion_id)])
        # tipo_id_monetaria = self.env['licibot.unidad.monetaria'].sudo().search([('id_unidad_monetaria','=', unidad_monetaria_id)])
        # select_uni_comp = self.env['licibot.unidad.compra'].sudo().search([('id', '=', unidad_compra_id)])
        # select_monto_est = self.env['licibot.monto.unitario'].sudo().search([('')])
        
        if codigo_externo:
            licitacion_existe = self.env['licibot.licitacion'].sudo().search([('codigo_externo', '=', codigo_externo)])
            if licitacion_existe:
                _logger.info(f"La licitacion {codigo_externo}:{nombre}, ya existe en la base de datos.")
            else:
                self.env['licibot.licitacion'].sudo().create({
                    'codigo_externo' : codigo_externo, 
                    'nombre' : nombre, 
                    'codigo_estado' : codigo_estado, 
                    'descripcion' : descripcion, 
                    'fecha_cierre_1' : fecha_cierre_1, 
                    'estado' : estado, 
                    'dias_cierre_licitacion' : dias_cierre_licitacion, 
                    'informada' : informada, 
                    'codigo_tipo' : codigo_tipo, 
                    'tipo_convocatoria' : tipo_convocatoria, 
                    'etapas' : etapas, 
                    'estado_etapas' : estado_etapas, 
                    'toma_razon' : toma_razon, 
                    'estado_pub_ofertas' : estado_pub_ofertas, 
                    'justificacion_pub' : justificacion_pub, 
                    'contrato' : contrato, 
                    'obras' : obras, 
                    'cant_reclamos' : cant_reclamos, 
                    'fecha_creacion' : self.convertir_fecha(fecha_creacion), 
                    'fecha_cierre_2' : self.convertir_fecha(fecha_cierre_2), 
                    'fecha_inicio' : self.convertir_fecha(fecha_inicio), 
                    'fecha_final' : self.convertir_fecha(fecha_final), 
                    'fecha_pub_respuestas' : self.convertir_fecha(fecha_pub_respuestas), 
                    'fecha_act_aper_tec' : self.convertir_fecha(fecha_act_aper_tec), 
                    'fecha_act_aper_eco' : self.convertir_fecha(fecha_act_aper_eco), 
                    'fecha_publicacion' : self.convertir_fecha(fecha_publicacion), 
                    'fecha_adjudicacion' : self.convertir_fecha(fecha_adjudicacion), 
                    'fecha_est_adjudicacion' : self.convertir_fecha(fecha_est_adjudicacion), 
                    'fecha_soporte_fisico' : self.convertir_fecha(fecha_soporte_fisico), 
                    'fecha_tiempo_eval' : self.convertir_fecha(fecha_tiempo_eval), 
                    'fecha_estimada_firma' : self.convertir_fecha(fecha_estimada_firma), 
                    'fecha_usuario' : self.convertir_fecha(fecha_usuario), 
                    'fecha_visita_terreno' : self.convertir_fecha(fecha_visita_terreno), 
                    'fecha_entrega_antecedentes' : self.convertir_fecha(fecha_entrega_antecedentes), 
                    'uni_tiempo_eval' : uni_tiempo_eval, 
                    'direccion_visita' : direccion_visita, 
                    'direccion_entrega' : direccion_entrega, 
                    'estimacion' : estimacion, 
                    'fuente_financiamiento' : fuente_financiamiento, 
                    'visibilidad_monto' : visibilidad_monto, 
                    'monto_estimado' : monto_estimado, 
                    'tiempo' : tiempo, 
                    'tipo_pago' : tipo_pago, 
                    'nom_resp_pago' : nom_resp_pago,
                    'email_resp_pago' : email_resp_pago, 
                    'nom_resp_contrato' : nom_resp_contrato, 
                    'email_resp_contrato' : email_resp_contrato, 
                    'fono_resp_contrato' : fono_resp_contrato, 
                    'prohibicion_cont' : prohibicion_cont, 
                    'subcontratacion' : subcontratacion, 
                    'tiempo_duracion_con' : tiempo_duracion_con, 
                    'just_monto_estimado' : just_monto_estimado, 
                    'obs_contractual' : obs_contractual, 
                    'ext_plazo' : ext_plazo, 
                    'es_base_tipo' : es_base_tipo, 
                    'uni_tiempo_cont_lic' : uni_tiempo_cont_lic, 
                    'valor_tiempo_renov' : valor_tiempo_renov, 
                    'periodo_tiempo_renov' : periodo_tiempo_renov, 
                    'es_renovable' : es_renovable, 
                    'cantidad_total' : cantidad_total, 
                    'codigo_contacto' : codigo_contacto, 
                    'rut_contacto' : self.is_null_str(rut_contacto), 
                    'nom_contacto' : nom_contacto, 
                    'cargo_contacto' : cargo_contacto, 
                    'adjudicacion_id' : num_adj.id,  
                    'tipo_licitacion_id' : self.normalize_tipo_licitacion(tipo_licitacion_id),           
                    'uni_tiempo_ev_id' : self.normalize_uni_tiempo_ev(uni_tiempo_ev_id),        
                    'unidad_monetaria_id' : self.normalize_unidad_monetaria(unidad_monetaria_id), 
                    'monto_estimado_id' : self.normalize_monto_estimado(monto_estimado_id), 
                    'uni_tiempo_con_id' : self.normalize_uni_tiempo_con(uni_tiempo_con_id), 
                    'modalidad_pago_id' : self.normalize_modalidad_pago(modalidad_pago_id), 
                    'unidad_compra_id' : clean_uc})

        else:
            _logger.info("¡ID de producto/servicio nulo. Omitiendo inserción de datos en la tabla producto/servicio...")

    # Falta testing. ID AUTOMATICA POR ODOO
    def insertar_item (
        self,
        correlativo, 
        uni_medida_prod, 
        cant_unitaria_prod, 
        monto_unitario, 
        desc_producto, 
        licitacion_id, 
        producto_servicio_id, 
        proveedor_id):

        licitacion_select = self.env['licibot.licitacion'].sudo().search([('codigo_externo','=', licitacion_id.strip())])
        proveedor_select = self.env['licibot.proveedor'].sudo().search([('rut_proveedor','=', proveedor_id.strip())])
        ### Intención de traer la ID de producto
        # producto_select = self.env['licibot.producto.servicio'].sudo().search([('id','=', producto_servicio_id)])

        self.env['licibot.item.licitacion'].sudo().create({
            'correlativo' : correlativo, 
            'uni_medida_prod' : uni_medida_prod, 
            'cant_unitaria_prod' : cant_unitaria_prod, 
            'monto_unitario' : monto_unitario, 
            'desc_producto' : desc_producto, 
            'licitacion_id' : licitacion_select.id, 
            'producto_servicio_id' : producto_servicio_id,
            'proveedor_id' : proveedor_select.id
            })

    """
    =================================================================
                        FUNCIONES DE EXTRACCIÓN
    =================================================================
    """
            
    # Entrega lista de licitaciones adjudicadas (lista grande)
    def listar_licitaciones_diarias(self):
        
        # Esta función realiza una petición a la api de mercadopublico y retorna una lista con todos los codigos externos
        # de las licitaciones encontradas para la fecha del día anterior (se consulta el día anterior ya que de esta forma
        # se asegura que se dispone de la lista de licitaciones completa de un día).
        
        token_mp = self.env['ir.config_parameter'].sudo().get_param('licibot_module.token_mp')
        url = "https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json"
        params = {'estado' : 'adjudicada', 'fecha': self.fecha_dia_anterior(), 'ticket': token_mp}

        # Sólo para printear la fecha en el formato clásico
        fecha_print = datetime.date.today()
        fecha_print_anterior = fecha_print - datetime.timedelta(days=1)

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if 'Listado' in data:
                codigos_externos = [item['CodigoExterno'] for item in data['Listado']]
                _logger.info(f"Para el día {fecha_print_anterior} hay {len(codigos_externos)} licitaciones adjudicadas.)")
                return codigos_externos
            else:
                return {'error': f'No se encontraron licitaciones adjudicadas para la fecha {fecha_print_anterior}'}

        except requests.exceptions.RequestException as e:
            return {'error': f"Error en la solicitud a la API: {e}"}

    def extraccion_licitaciones_diarias(self):
        '''Función que recibe por parámetro una lista de licitaciones y, para cada una de las ID de licitaciones, 
        envía una petición a la API de mercadopublico.cl para recopilar información más detallada sobre esa ID. 
        Repite este proceso tantas veces como licitaciones haya en la lista y luego inserta la información en la base de datos.'''
        
        # Contador ID's licitaciones
        count = 1

        # Traer token mp desde configuración
        token_mp = self.env['ir.config_parameter'].sudo().get_param('licibot_module.token_mp')

        # Definición de palabras clave para traer licitaciones relacionadas al negocio del gas
        keywords = ['Gas', 'Gas Licuado', 'Gas ciudad', 'Gas de petróleo licuefactado', 'Suministro de gas natural', 'Granel', 'VALES DE GAS', 'Vales', 'Centrales de gas', 
        'Calderas de gas natural', 'Servicios de descontaminacion medioambiental', 'Servicios de asesoría de ciencias medioambientales', 'Generadores de gas', 
        'Servicios de gasoductos', 'Construcción de sistema de fontanería o gasfiteria', 'Recarga de tanques de gas', 'Tanques o botellas de aire o gas', 
        'Servicios de elevación por presión de gas de tubería adujada (en espiral)', 'Servicios de producción de gas natural', 
        'Supervisión de instalación, ajuste o mantenimiento de calderas', 'Instalación estanque de abastecimiento de gas licuado y certificación sello verde', 
        'Instalación, reparación o mantenimiento de sistemas de calefacción', 'Servicio de gasfiteria y alcantarillado', 'Combustibles, lubricantes y anticorrosivos', 
        'Combustibles gaseosos y aditivos', 'Combustibles gaseosos', 'Servicios de elevación por presión de gas de tubería adujada (en espiral)', 
        'Servicios de producción de gas natural', 'Tubería de cobre']

        # Definición de palabras que pueden involucrar gas o categorias relacionadas a gas pero no son de interés para el negocio (agua con gas, recarga de tanques, etc.)
        omitir_productos = ['agua', 'oxígeno', 'oxigeno', 'helio', 'medicos', 'medico', 'médico', 'médicos', 'xenón', 'xenon', 'nitrógeno', 'nitrogeno', 'argón', 'argon', 'anestesia',
        'kriptón', 'neón', 'neon', 'radón', 'co2', 'dióxido', 'dioxido', 'soplete', 'motor', 'aceite']

        # Listado de entrada 
        # listado = ['1080095-17-L123','1091-17-LE23','5196-91-L123','848-51-LE23','3073-83-L123']

        # Listado original (comentado para hacer pruebas)
        listado = self.listar_licitaciones_diarias()
        # listado = lista

        try:
            # Recorrer los elementos almacenados en la lista de ids de licitaciones
            for id in listado:
                # Realizar petición de datos para la ID de licitación
                url = 'https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json'
                args = {'codigo': id, 'ticket': token_mp}
                response = self.make_request_with_retries(url, args)
                _logger.info(f"\nProceso licitaciones diarias : En ejecución ... ({count} de {len(listado)})")

                if response and response.status_code == 200:
                    
                    payload = response.json()
                    datos_licitacion = payload.get('Listado', [])

                    for dato in datos_licitacion:
                        codigo_externo = dato['CodigoExterno']
                        nombre = dato['Nombre']
                        codigo_estado = dato['CodigoEstado']
                        descripcion = dato['Descripcion']
                        fecha_cierre_1 = dato['FechaCierre']
                        estado = dato['Estado']
                        comprador = dato.get('Comprador', {})
                        codigo_organismo = comprador['CodigoOrganismo']
                        nombre_organismo = comprador['NombreOrganismo']
                        rut_unidad = comprador['RutUnidad']
                        codigo_unidad = comprador['CodigoUnidad']
                        nombre_unidad = comprador['NombreUnidad']
                        direccion_unidad = comprador['DireccionUnidad']
                        comuna_unidad = comprador['ComunaUnidad']
                        region_unidad = comprador['RegionUnidad']
                        rut_comprador = comprador['RutUsuario']
                        codigo_comprador = comprador['CodigoUsuario']
                        nombre_comprador = comprador['NombreUsuario']
                        cargo_comprador = comprador['CargoUsuario']
                        dias_cierre_licitacion = dato['DiasCierreLicitacion']
                        informada = dato['Informada']
                        codigo_tipo = dato['CodigoTipo']
                        tipo = dato['Tipo']
                        tipo_convocatoria = dato['TipoConvocatoria']
                        moneda = dato['Moneda']
                        etapas = dato['Etapas']
                        estado_etapas = dato['EstadoEtapas']
                        toma_razon = dato['TomaRazon']
                        estado_publicidad_ofertas = dato['EstadoPublicidadOfertas']
                        justificacion_publicidad = dato['JustificacionPublicidad']
                        contrato = dato['Contrato']
                        obras = dato['Obras']
                        cantidad_reclamos = dato['CantidadReclamos']
                        fechas = dato.get('Fechas', {})
                        fecha_creacion = fechas['FechaCreacion']
                        fecha_cierre_2 = fechas['FechaCierre']
                        fecha_inicio = fechas['FechaInicio']
                        fecha_final = fechas['FechaFinal']
                        fecha_pub_respuestas = fechas['FechaPubRespuestas']
                        fecha_apertura_tecnica = fechas['FechaActoAperturaTecnica']
                        fecha_apertura_economica = fechas['FechaActoAperturaEconomica']
                        fecha_publicacion = fechas['FechaPublicacion']
                        fecha_adjudicacion = fechas['FechaAdjudicacion']
                        fecha_estimada_adjudicacion = fechas['FechaEstimadaAdjudicacion']
                        fecha_soporte_fisico = fechas['FechaSoporteFisico']
                        fecha_tiempo_evaluacion = fechas['FechaTiempoEvaluacion']
                        fecha_estimada_firma = fechas['FechaEstimadaFirma']
                        fecha_usuario = fechas['FechasUsuario']
                        fecha_visita_terreno = fechas['FechaVisitaTerreno']
                        fecha_entrega_antecedentes = fechas['FechaEntregaAntecedentes']
                        unidad_tiempo_evaluacion = dato['UnidadTiempoEvaluacion']
                        direccion_visitas = dato['DireccionVisita']
                        direccion_entrega = dato['DireccionEntrega']
                        estimacion = dato['Estimacion']
                        fuente_financiamiento = dato['FuenteFinanciamiento']
                        visibilidad_monto = dato['VisibilidadMonto']
                        monto_estimado = dato['MontoEstimado']
                        tiempo = dato['Tiempo']
                        unidad_tiempo = dato['UnidadTiempo']
                        modalidad = dato['Modalidad']
                        tipo_pago = dato['TipoPago']
                        nombre_reponsable_pago = dato['NombreResponsablePago']
                        email_responsable_pago = dato['EmailResponsablePago']
                        nombre_responsable_contrato = dato['NombreResponsableContrato']
                        email_responsable_contrato = dato['EmailResponsableContrato']
                        fono_responsable_contrato = dato['FonoResponsableContrato']
                        prohibicion_contratacion = dato['ProhibicionContratacion']
                        subcontratacion = dato['SubContratacion']
                        unidad_tiempo_duracion_contrato = dato['UnidadTiempoDuracionContrato']
                        tiempo_duracion_contrato = dato['TiempoDuracionContrato']
                        tipo_duracion_contrato = dato['TipoDuracionContrato']
                        justificacion_monto_estimado = dato['JustificacionMontoEstimado']
                        observacion_contract = dato['ObservacionContract']
                        extension_plazo = dato['ExtensionPlazo']
                        es_base_tipo = dato['EsBaseTipo']
                        unidad_tiempo_contrato_licitacion = dato['UnidadTiempoContratoLicitacion']
                        valor_tiempo_renovacion = dato['ValorTiempoRenovacion']
                        periodo_tiempo_renovacion = dato['PeriodoTiempoRenovacion']
                        es_renovable = dato['EsRenovable']
                        cantidad_items = dato.get('Items', {}).get('Cantidad')

                        adjudicacion = dato.get('Adjudicacion')
                        if adjudicacion:
                            adj_tipo = adjudicacion.get('Tipo')
                            adj_fecha = adjudicacion.get('Fecha')
                            adj_numero = adjudicacion.get('Numero')
                            adj_num_oferentes = adjudicacion.get('NumeroOferentes')
                            adj_url_acta = adjudicacion.get('UrlActa')
                        else:
                            adj_tipo = 0
                            adj_fecha = '1900-01-01'
                            adj_numero = 0
                            adj_num_oferentes = 0
                            adj_url_acta = 'Sin Información'
                        
                        licitacion_insertada = False
                        listado_items = dato.get('Items', {}).get('Listado', [])
                        for index, item_data in enumerate(listado_items):
                            item_correlativo = item_data['Correlativo']
                            item_codigo_producto = item_data['CodigoProducto']
                            item_codigo_categoria = item_data['CodigoCategoria']
                            item_categoria = item_data['Categoria']
                            item_nombre_producto = item_data['NombreProducto']
                            item_descripcion = item_data['Descripcion']
                            item_unidad_medida = item_data['UnidadMedida']
                            item_cantidad = item_data['Cantidad']

                            item_adjudicacion = item_data['Adjudicacion']
                            if item_adjudicacion:
                                rut_proveedor = item_adjudicacion['RutProveedor']
                                nombre_proveedor = item_adjudicacion['NombreProveedor']
                                cantidad_adjudicada = item_adjudicacion['Cantidad']
                                monto_unitario = item_adjudicacion['MontoUnitario']
                            else:
                                rut_proveedor = 'Sin Información'
                                nombre_proveedor = 'Sin Información'
                                cantidad_adjudicada = 0
                                monto_unitario = 0
                            
                            related = False
                            # Buscar palabras clave en los datos de la licitación y los productos
                            for keyword in keywords:
                                pattern = r'\b' + re.escape(keyword) + r'\b'
                                if re.search(pattern, nombre, re.IGNORECASE) or \
                                    re.search(pattern, descripcion, re.IGNORECASE) or \
                                    re.search(pattern, item_descripcion, re.IGNORECASE) or \
                                    re.search(pattern, item_categoria, re.IGNORECASE) or \
                                    re.search(pattern, item_nombre_producto, re.IGNORECASE):
                                    related = True
                                    _logger.info(f"Se ha encontrado en ítem: {item_correlativo} relacionado a {keyword}")
                                    break

                            # Verificar si se debe omitir el producto por falso positivo
                            for exclude_keyword in omitir_productos:
                                if exclude_keyword.lower() in item_nombre_producto.lower():
                                    related = False
                                    _logger.info(f"Se ha detectado al item correlativo: {item_correlativo} como falso positivo: {exclude_keyword}. Omitiendo item...")

                            if related:
                                if not licitacion_insertada: 
                                    _logger.info(f"INSERTANDO A ORGANISMO {codigo_organismo}: {nombre_organismo}")
                                    self.insertar_organismo (codigo_organismo, nombre_organismo)

                                    _logger.info(f"INSERTANDO A UNIDAD DE COMPRA {codigo_unidad}: {nombre_unidad}")
                                    self.insertar_unidadCompra (
                                        codigo_unidad,
                                        rut_unidad.upper(),
                                        nombre_unidad,
                                        direccion_unidad,
                                        comuna_unidad,
                                        region_unidad,
                                        codigo_organismo # organismo_id
                                    )

                                    _logger.info(f"INSERTANDO A ADJUDICACION {adj_numero}: {adj_fecha}")
                                    self.insertar_adjudicacion (
                                        adj_numero,
                                        adj_fecha,
                                        adj_num_oferentes,
                                        adj_url_acta,
                                        adj_tipo    # tipo_acto_adm_id
                                    )

                                    _logger.info(f"INSERTANDO A LICITACION {codigo_externo}: {nombre}")
                                    self.insertar_licitacion (
                                        codigo_externo, 
                                        nombre, 
                                        codigo_estado, 
                                        descripcion,
                                        fecha_cierre_1, 
                                        estado,
                                        dias_cierre_licitacion,
                                        informada,
                                        codigo_tipo,
                                        tipo_convocatoria,
                                        etapas, 
                                        estado_etapas,
                                        toma_razon,
                                        estado_publicidad_ofertas,
                                        justificacion_publicidad,
                                        contrato,
                                        obras,
                                        cantidad_reclamos,
                                        fecha_creacion,
                                        fecha_cierre_2,
                                        fecha_inicio,
                                        fecha_final,
                                        fecha_pub_respuestas,
                                        fecha_apertura_tecnica,
                                        fecha_apertura_economica,
                                        fecha_publicacion,
                                        fecha_adjudicacion,
                                        fecha_estimada_adjudicacion,
                                        fecha_soporte_fisico,
                                        fecha_tiempo_evaluacion,
                                        fecha_estimada_firma,
                                        fecha_usuario,
                                        fecha_visita_terreno,
                                        fecha_entrega_antecedentes,
                                        unidad_tiempo_evaluacion,
                                        direccion_visitas,
                                        direccion_entrega,
                                        estimacion,
                                        fuente_financiamiento,
                                        visibilidad_monto,
                                        monto_estimado,
                                        tiempo,
                                        tipo_pago,
                                        nombre_reponsable_pago,
                                        email_responsable_pago,
                                        nombre_responsable_contrato,
                                        email_responsable_contrato,
                                        fono_responsable_contrato,
                                        prohibicion_contratacion,
                                        subcontratacion,
                                        tiempo_duracion_contrato,
                                        justificacion_monto_estimado,
                                        observacion_contract,
                                        extension_plazo,
                                        es_base_tipo,
                                        unidad_tiempo_contrato_licitacion,
                                        valor_tiempo_renovacion,
                                        periodo_tiempo_renovacion,
                                        es_renovable,
                                        cantidad_items,
                                        codigo_comprador,
                                        rut_comprador,
                                        nombre_comprador,
                                        cargo_comprador,
                                        adj_numero,                         # adjudicacion_id
                                        tipo,                               # tipo_licitacion_id
                                        unidad_tiempo_evaluacion,           # uni_tiempo_ev_id
                                        moneda,                             # unidad_monetaria_id
                                        visibilidad_monto,                  # monto_estimado_id
                                        unidad_tiempo_contrato_licitacion,  # uni_tiempo_con_id
                                        modalidad,                          # modalidad_pago_id
                                        codigo_unidad                       # UnidadCompra_codigoUnidad
                                    )
                                    licitacion_insertada = True
                                    # <<< FIN if not licitacion_insertada: 

                                _logger.info(f"INSERTANDO A PROVEEDOR {rut_proveedor}: {nombre_proveedor}")
                                self.insertar_proveedor (rut_proveedor, nombre_proveedor)

                                _logger.info(f"INSERTANDO A CATEGORIA {item_codigo_categoria}: {item_categoria}")
                                self.insertar_categoria (item_codigo_categoria, item_categoria)

                                _logger.info(f"INSERTANDO A CODIGO PRODUCTO {item_codigo_producto}: {item_nombre_producto}")
                                self.insertar_productoServicio (item_codigo_producto, item_nombre_producto, item_codigo_categoria)

                                _logger.info(f"INSERTANDO A ITEM CORRELATIVO {item_correlativo}: {item_descripcion}")
                                self.insertar_item (
                                    item_correlativo, 
                                    item_unidad_medida,
                                    cantidad_adjudicada,
                                    monto_unitario,
                                    item_descripcion,
                                    codigo_externo,         # licitacion_id
                                    item_codigo_producto,   # producto_servicio_id
                                    rut_proveedor           # proveedor_id
                                )

                                _logger.info(f"Los datos del item correlativo: {item_correlativo} se han insertado exitosamente.")

                                # <<< FIN if related
                            # <<< FIN index, item_data in enumerate(listado_items):
                        # <<< FIN for dato in datos_licitacion:

                    
                    # <<< FIN if response and response.status_code == 200:

                else:
                    _logger.info(f"No se pudo extraer la licitación {id}. Código de Estado: {response.status_code} - {response.reason}")
                count += 1
                # Esperar 2 segundos entre cada solicitud para evitar errores (ANTES ERA 5)
                time.sleep(2)
                # <<< FIN for id in listado:
        except KeyboardInterrupt:
            # Capturar la señal de "Ctrl + C" para detener la ejecución
            _logger.info("Se ha detenido la ejecución. Guardando los datos recopilados hasta ahora en la base de datos.")
        # <<< FIN def extraccion_licitaciones_diarias(self):

    """
    =================================================================
                        FUNCIONES PARA EL RANKING
    =================================================================
    """
    def calculo_rankingv1(self):
        '''
        Función que calcula el ranking para los primeros 20 codigos de unidad de compra de la vista licibot_ranking_v1.
        Primero, limpia todos los registros para el campo ranking en la tabla UnidadCompra.
        Segundo, crea una lista con los codigos de unidad de compra en la vista licibot_ranking_v1.
        Tercero, recorre esa lista y para los primeros 20 elementos asigna de forma secuencial el ranking.
        '''
        _logger.info('''\n\n\n>>> Ejecutando CRON Licibot: Calculo Ranking v1 <<<\n\n\n''')

        # Limpiar todos los valores del campo "ranking" en el modelo UnidadCompra
        self.env.cr.execute("UPDATE licibot_unidad_compra SET ranking = NULL;")

        # Recuperar la lista de rut_unidad de la vista licibot_ranking_v1
        ranking_length = int(self.env['ir.config_parameter'].sudo().get_param('licibot_module.ranking_length'))
        self.env.cr.execute(f'SELECT "ID Unidad de Compra" FROM licibot_ranking_v1 LIMIT {ranking_length};')
        id_unidad_list = list(line[0] for line in self.env.cr.fetchall())

        # Inicializar el contador de ranking
        pos_ranking = 1

        # Recorrer los primeros 20 elementos de la lista
        for id_unidad in id_unidad_list: 

            # Buscar y actualizar el campo "ranking" en el modelo UnidadCompra
            unidad_compra = self.env['licibot.unidad.compra'].sudo().search([('id', '=', id_unidad)])
            unidad_compra.sudo().write({'ranking': pos_ranking})
            
            # Incrementar el contador de ranking para el siguiente valor
            pos_ranking += 1

        _logger.info('''\n\n\n>>> Finalizando CRON Licibot: Calculo Ranking v1<<<\n\n\n''')        

    """ 
    TODO Falta por mejorar acorde a lo conversado en la última reunion
    """
    def calcular_ranking_ml(self):
        _logger.info('''\n\n\n>>> Ejecutando CRON Licibot: Calcular Ranking ML <<<\n\n\n''')

        # Cargar el archivo que contiene el modelo de ML
        kmeans_model = pickle.load(open('opt/addons_opens/licibot_module/Inputs/kmeans_pca2.sav', 'rb'))

        # Generar un PCA a partir de la información de la base de datos.
        self.env.cr.execute("""
            SELECT 
                idunidad,
                licitacionestotales,
                totalgastado,
                gasto2022,
                diferenciaanterior2023,
                proveedores2022,
                proveedores2023,
                competenciaotros,
                valorpromediocompra,
                cantidadtrabajadores,
                clientenuevo
            FROM licibot_variables_kmeans;
            """)

        query_result = self.env.cr.fetchall()

        # Convierte los resultados en un DataFrame
        df = pd.DataFrame(query_result, columns=["idunidad", 
        "licitacionestotales", 
        "totalgastado", 
        "gasto2022", 
        "diferenciaanterior2023", 
        "proveedores2022", 
        "proveedores2023", 
        "competenciaotros", 
        "valorpromediocompra", 
        "cantidadtrabajadores", 
        "clientenuevo"])

        _logger.info('''\n\n\n
        Imprime DF head 10:
        %s
        \n\n\n
        ''', df.head(10))

        # Replicando el Componente Principal de Análisis (PCA) 
        scaler = StandardScaler()
        scaler.fit(df)
        scaled_df = pd.DataFrame(scaler.transform(df),columns= df.columns)
        pca = PCA(n_components=3)
        pca.fit(scaled_df)
        PCA_df = pd.DataFrame(pca.transform(scaled_df), columns=(["col1","col2", "col3"]))
        _logger.info('''\n\n\n
        Describing PCA:
        %s
        \n\n\n
        ''', PCA_df.describe().T)

        # Generar una predicción utilizando el modelo desde el archivo .sav.
        pred = kmeans_model.predict(PCA_df)

        # Sobreescribir la información de la predicción en la base de datos.
        df['Segment K-means PCA'] = pred
        _logger.info(f'''\n\n\n
        Showing DataFrame ... :
        {df.head(100)}
        \n\n\n
        ''')

        # df_cluster_0 = df[(df["Segment K-means PCA"] == 0)]
        # _logger.info(f'''\n\n\n
        # Showing DF Cluster 0 ...:
        # Total: {len(df_cluster_0)}
        # {df_cluster_0.head(50)}
        # \n\n\n
        # ''')

        # df_cluster_2 = df[(df["Segment K-means PCA"] == 2)]
        # _logger.info(f'''\n\n\n
        # Showing DF Cluster 2 ...:
        # Total: {len(df_cluster_2)}
        # {df_cluster_2.head(50)}
        # \n\n\n
        # ''')

        filtro_1 = df[(df["competenciaotros"] == 0)]
        _logger.info(f'''\n\n\n
        Showing DF filtro 1 ...:
        Total: {len(filtro_1)}
        {filtro_1[["idunidad", "competenciaotros", "Segment K-means PCA"]].head(50)}
        \n\n\n
        ''')
        f1_list = filtro_1['idunidad'].tolist()
        f1_list_str = ', '.join(map(str, f1_list))

        filtro_2 = df[(df["Segment K-means PCA"] == 2) & (df["competenciaotros"] == 1)]
        _logger.info(f'''\n\n\n
        Showing DF filtro 2 ...:
        Total: {len(filtro_2)}
        {filtro_2[["idunidad", "competenciaotros", "Segment K-means PCA"]].head(50)}
        \n\n\n
        ''')
        f2_list = filtro_2['idunidad'].tolist()
        f2_list_str = ', '.join(map(str, f2_list))

        filtro_3 = df[(df["Segment K-means PCA"] == 0) & (df["competenciaotros"] == 1)]
        _logger.info(f'''\n\n\n
        Showing DF filtro 3 ...:
        Total: {len(filtro_3)}
        {filtro_3[["idunidad", "competenciaotros", "Segment K-means PCA"]].head(50)}
        \n\n\n
        ''')
        f3_list = filtro_3['idunidad'].tolist()
        f3_list_str = ', '.join(map(str, f3_list))

        # Generar lista con los  clusters de interes.
        filtro = (
            (df['competenciaotros'] == 0) | 
            ((df['Segment K-means PCA'] == 2) & (df["competenciaotros"] == 1)) | 
            ((df['Segment K-means PCA'] == 0) & (df["competenciaotros"] == 1) )
        )
        df_filtrado = df[filtro]

        # Crea una lista con las unidades de compra a rankear
        uc_list = df_filtrado['idunidad'].tolist()
        _logger.info(f'''El filtro contiene {len(uc_list)} unidades de compra... ''')
        uc_list_str = ', '.join(map(str, uc_list))

        # Crear vista ranking_ml
        query_ranking_ml_view = f"""
        CREATE OR REPLACE VIEW licibot_ranking_ml AS
        SELECT 
            licibot_unidad_compra.id AS "ID Unidad de Compra",
            licibot_unidad_compra.nombre_unidad as "Nombre de Unidad de Compra",
            SUM(CASE WHEN licibot_licitacion.fecha_adjudicacion >= DATE '2022-01-01' AND licibot_licitacion.fecha_adjudicacion <= DATE '2022-12-31' THEN licibot_item_licitacion.cant_unitaria_prod * licibot_item_licitacion.monto_unitario ELSE 0 END) AS "Monto Total Año Anterior",
            SUM(CASE WHEN licibot_licitacion.fecha_adjudicacion >= DATE '2023-01-01' AND licibot_licitacion.fecha_adjudicacion <= DATE '2023-12-31' THEN licibot_item_licitacion.cant_unitaria_prod * licibot_item_licitacion.monto_unitario ELSE 0 END) AS "Monto Total Año Actual",
            SUM(CASE WHEN licibot_licitacion.fecha_adjudicacion >= DATE '2022-01-01' AND licibot_licitacion.fecha_adjudicacion <= DATE '2022-12-31' THEN licibot_item_licitacion.cant_unitaria_prod * licibot_item_licitacion.monto_unitario ELSE 0 END) -
            SUM(CASE WHEN licibot_licitacion.fecha_adjudicacion >= DATE '2023-01-01' AND licibot_licitacion.fecha_adjudicacion <= DATE '2023-12-31' THEN licibot_item_licitacion.cant_unitaria_prod * licibot_item_licitacion.monto_unitario ELSE 0 END) AS "Monto Diferencial"
        FROM 
            licibot_unidad_compra 
            JOIN licibot_licitacion ON licibot_unidad_compra.id = licibot_licitacion.unidad_compra_id
            JOIN licibot_item_licitacion ON licibot_licitacion.id = licibot_item_licitacion.licitacion_id
        WHERE
            licibot_unidad_compra.id IN ({uc_list_str})
        GROUP BY 
            licibot_unidad_compra.id
        ORDER BY
            "Monto Diferencial" DESC;
        """
        tools.drop_view_if_exists(self._cr, 'licibot_ranking_ml')
        self.env.cr.execute(query_ranking_ml_view)

        # Limpiar todos los valores del campo "ranking" en el modelo UnidadCompra
        self.env.cr.execute("UPDATE licibot_unidad_compra SET ranking = NULL;")

        # Recuperar la lista de rut_unidad de la vista licibot_ranking_ml
        ranking_ml_length = int(self.env['ir.config_parameter'].sudo().get_param('licibot_module.ranking_ml_length'))
        _logger.info(f"""\n\n
            ranking_ml_length = {ranking_ml_length} 
            f1_list = {len(f1_list)}
            f2_list = {len(f2_list)}
            f3_list = {len(f3_list)}
            Espacio disponible para f3_list = {ranking_ml_length - (len(f1_list) + len(f2_list))}
        \n\n""")
        if len(f1_list) + len(f2_list) < ranking_ml_length:
            ranking_ml_length =  ranking_ml_length - (len(f1_list) + len(f2_list))

        if len(f1_list) > 0:
            self.env.cr.execute(f'SELECT "ID Unidad de Compra" FROM licibot_ranking_ml WHERE "ID Unidad de Compra" IN ({f1_list_str});')
            prior_f1_list = list(line[0] for line in self.env.cr.fetchall())
        if len(f2_list) > 0:
            self.env.cr.execute(f'SELECT "ID Unidad de Compra" FROM licibot_ranking_ml WHERE "ID Unidad de Compra" IN ({f2_list_str});')
            prior_f2_list = list(line[0] for line in self.env.cr.fetchall())
        if len(f3_list) > 0:
            self.env.cr.execute(f'SELECT "ID Unidad de Compra" FROM licibot_ranking_ml WHERE "ID Unidad de Compra" IN ({f3_list_str}) LIMIT {ranking_ml_length};')
            prior_f3_list = list(line[0] for line in self.env.cr.fetchall())

        # Inicializar el contador de ranking
        pos_ranking = 1

        # Asignando las posiciones del ranking
        # >>> Filtro 1
        if len(f1_list) > 0:
            for uc in prior_f1_list: 
                # Buscar y actualizar el campo "ranking" en el modelo UnidadCompra
                unidad_compra = self.env['licibot.unidad.compra'].sudo().search([('id', '=', uc)])
                unidad_compra.sudo().write({'ranking': pos_ranking})
                # Incrementar el contador de ranking para el siguiente valor
                pos_ranking += 1
        
        # >>> Filtro 2
        if len(f2_list) > 0:
            for uc in prior_f2_list: 
                # Buscar y actualizar el campo "ranking" en el modelo UnidadCompra
                unidad_compra = self.env['licibot.unidad.compra'].sudo().search([('id', '=', uc)])
                unidad_compra.sudo().write({'ranking': pos_ranking})
                # Incrementar el contador de ranking para el siguiente valor
                pos_ranking += 1

        # >>> Filtro 3
        if len(f3_list) > 0:
            for uc in prior_f3_list: 
                # Buscar y actualizar el campo "ranking" en el modelo UnidadCompra
                unidad_compra = self.env['licibot.unidad.compra'].sudo().search([('id', '=', uc)])
                unidad_compra.sudo().write({'ranking': pos_ranking})
                # Incrementar el contador de ranking para el siguiente valor
                pos_ranking += 1

        _logger.info('''\n\n\n>>> Finalizando CRON Licibot: Calcular Ranking ML <<<\n\n\n''')

    """
    =================================================================
                        FUNCIONES AUXILIARES
    =================================================================
    """

    def is_null_int (self, variable):
    
        if variable:
            return variable
        else:
            return 0
    
    def is_null_str (self, variable):
        
        if variable:
            return variable
        else:
            return "NaN"

    def is_null_date (self, variable):

        if variable:
            return variable
        else:
            return "1900-01-01"

    def normalize_tipo_licitacion (self, tipo_licitacion):
        # Limpia el string utilizando strip
        clean_string = tipo_licitacion.strip()
    
        # Lista de valores permitidos
        valores_permitidos = [
            "L1", "LE", "LP", "LQ", "LR", "LS", "A1", "B1", "E1", "F1",
            "J1", "CO", "B2", "A2", "D1", "E2", "C2", "C1", "F2", "F3",
            "G2", "G1", "R1", "CA", "SE", "R2", "COT"
        ]

        # Comprueba si el string limpio está en la lista de valores permitidos
        if clean_string in valores_permitidos:
            select_tipo_lic = self.env['licibot.tipo.licitacion'].sudo().search([('id_tipo_licitacion','=', clean_string)])
            return int(select_tipo_lic.id)
        else:
            return 0

    def normalize_unidad_monetaria (self, unidad_monetaria):
        # Limpia el string utilizando strip
        clean_string = unidad_monetaria.strip()
    
        # Lista de valores permitidos
        valores_permitidos = ["CLP", "CLF", "USD", "UTM", "EUR"]

        # Comprueba si el string limpio está en la lista de valores permitidos
        if clean_string in valores_permitidos:
            select_uni_mon = self.env['licibot.unidad.monetaria'].sudo().search([('id_unidad_monetaria','=', clean_string)])
            return int(select_uni_mon.id)
        else:
            return 0

    def normalize_uni_tiempo_ev (self, uni_tiempo_ev):
        # Lista de valores permitidos
        valores_permitidos = [1, 2, 3, 4, 5]

        # Comprueba si el string limpio está en la lista de valores permitidos
        if uni_tiempo_ev in valores_permitidos:
            return uni_tiempo_ev
        else:
            return 0

    def normalize_tipo_acto_admin (self, tipo_acto_admin):
        # Lista de valores permitidos
        valores_permitidos = [1, 2, 3, 4, 5]

        # Comprueba si el string limpio está en la lista de valores permitidos
        if tipo_acto_admin in valores_permitidos:
            return tipo_acto_admin
        else:
            return 0

    def normalize_uni_tiempo_con (self, uni_tiempo_con):

        clean_uni_tiempo_con = int(uni_tiempo_con.strip())
        # Lista de valores permitidos
        valores_permitidos = [1, 2, 3, 4, 5]

        # Comprueba si el string limpio está en la lista de valores permitidos
        if clean_uni_tiempo_con in valores_permitidos:
            return clean_uni_tiempo_con
        else:
            return 0

    def normalize_monto_estimado (self, monto_estimado):
        # Lista de valores permitidos
        valores_permitidos = [1, 2]

        # Comprueba si el string limpio está en la lista de valores permitidos
        if monto_estimado in valores_permitidos:
            return monto_estimado
        else:
            return 0

    def normalize_modalidad_pago (self, modalidad_pago):
        # Lista de valores permitidos
        valores_permitidos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        # Comprueba si el string limpio está en la lista de valores permitidos
        if modalidad_pago in valores_permitidos:
            return modalidad_pago
        else:
            return 0

    # Al ejecutarla a las 23 hrs me entregaba la fecha actual, pasado las 00 funcionó
    def fecha_dia_anterior(self):
        fecha_actual = datetime.date.today()
        fecha_anterior = fecha_actual - datetime.timedelta(days=1)
        fecha_anterior_str = fecha_anterior.strftime("%d%m%Y")
        return fecha_anterior_str

    def convertir_fecha(self, fecha_str):
        if fecha_str in ("null", "Null", "NULL", None):
            return None
        else:
            try:
                # Convierte la fecha en un objeto datetime
                fecha_obj = parse(fecha_str)

                # Formatea la fecha en el formato deseado
                fecha_formateada = fecha_obj.strftime("%Y-%m-%d %H:%M:%S")
                
                return fecha_formateada

            except ValueError:
                # Si no se puede analizar el formato
                return None

    def identificar_tipo_competidor(self, nombre_proveedor):
        """
        ## Descripción
        Función que recibe por parametro una variable string con el nombre del proveedor y comprueba si pertenece a 'gasco' o 'lipigas', retornando la id correspondiente (1) para competidor directo y (2) para competidor indirecto.
        ## Parámetros
        - nombre_proveedor: str que contiene el nombre del proveedor
        ## Retorna
        - (número entero) que referencia a una id de tipo competidor.
        """
        if 'gasco' in nombre_proveedor.lower() or 'lipigas' in nombre_proveedor.lower():
            return 1
        else:
            return 2

    def make_request_with_retries (self, url, params, max_retries=3):
        """
        ## Descripción
        Función para realizar una solicitud con reintentos en caso de error de tiempo de espera.
        """
        for retry in range(max_retries):
            try:
                response = requests.get(url, params)
                return response
            except requests.exceptions.ReadTimeout as e:
                _logger.info(f"Intento {retry+1} de {max_retries}. Error de tiempo de espera: {e}")
                time.sleep(5)  # Esperar 5 segundos antes de reintentar

    # Funcion innecesaria actualmente (?)
    def generate_pickle (self):
        #Loading the dataset
        data = pd.read_csv("opt/addons_opens/licibot_module/Inputs/training.csv", sep="," , encoding='iso-8859-1')
        data = data.dropna()
        data["ultima_licitacion"] = pd.to_datetime(data["ultima_licitacion"])
        data["primera_licitacion"] = pd.to_datetime(data["primera_licitacion"])
        data2 = data.drop("nombre_organismo", axis=1)
        data2 = data2.drop("nombre_unidad", axis=1)
        ds = data2.copy()
        cols_del = ['ultima_licitacion', 'primera_licitacion']
        ds = ds.drop(cols_del, axis=1)
        scaler = StandardScaler()
        scaler.fit(ds)
        scaled_ds = pd.DataFrame(scaler.transform(ds),columns= ds.columns )
        print("All features are now scaled")
        pca = PCA(n_components=3)
        pca.fit(scaled_ds)
        PCA_ds = pd.DataFrame(pca.transform(scaled_ds), columns=(["col1","col2", "col3"]))
        PCA_ds.describe().T
        kmeans_pca = KMeans(n_clusters = 4, init = 'k-means++', random_state = 42)
        kmeans_pca.fit(PCA_ds)
        df_segm_pca_kmeans = pd.concat([data.reset_index(drop = True), pd.DataFrame(PCA_ds)], axis = 1)
        df_segm_pca_kmeans.columns.values[-3: ] = ['col1', 'col2', 'col3']

        df_segm_pca_kmeans['Segment K-means PCA'] = kmeans_pca.labels_
        df_segm_pca_kmeans.head(100)

        pred = kmeans_pca.predict(PCA_ds)

        ds['Segment K-means PCA'] = pred

        pickle_K = 'opt/addons_opens/licibot_module/Inputs/kmeans_pca_odoo.sav'
        pickle.dump(kmeans_pca, open(pickle_K, 'wb'))

    def easter_egg(self):
        """
        Para ver esta funcion ejecutar en consola el comando 'tail -f /var/log/odoo/odoo-server.log'
        """
    _logger.info('''


                ===++***#***###**##**###########%%%%%%#%%%%%%%%%%%%%%%%%%%%%%%%#*%%%@###%%%@%%@%%%%%%%%%%%%%
                =============++*+**++***+**++======++*%%%%%%%%%%%%%%%%%%@%%%%@#*@@@%%%%%%@@@@%@@%@%%%%%%%%%%
                ==========------------------=:...::..:-====++%%##%##%#%%@%#%@**%%%*###%@%%%%#%%%%%%@%%%%%%@%
                =============----=-----::::..                .. .:.-:+#%%%%@#*%%#####%%%%@@%%%%%%%%%%%%%%%%%
                ===============---:::..                               .-+#%#*%%*%%#%@#%@@@%@%@@@%%%%@@@@@%%%
                +==============---.                                   ...:+=*%*%%#%%%@%%%%@@%@%%@%%@@@@%%@%%
                ++======-==----:.....                   ...... ... .     ...=*#%#%%@@%%%%%%%%%%%@@@@@@@%@%%%
                +++====------:.......       .. ..  ...........................=*#%@@@%%%%@@@@@@%@@@@@@@%@%@@
                ======---::... .   . ..... .  .................................=+#%%##%%%###*%%@%%@@@@@@%%%#
                ==-----::....   ......:::..............................:.::::... .=+*%#%###**#%%%@@@@@%%#**+
                +==--::............:-----::::::::.::...........:::...::::----:..   .:--+*##**##%@@@@%@%#****
                ==-:::......:.....:::==---------::::::..........:..:::-------:........:-+*+++#%%@@@%@@%%#***
                --::....:::::::-:::...:---====---::::::........:::::-------:::..........:-=***#%%%%%%%%%#***
                =:...:-=+++++*+=+=-::::---=====--::::::.... ...::::-------::::-:::::-::::::--*###%%%%%%%****
                :...:-+***########*+===-========------::::.....:::::--------==++**####*+-::...-=++*#%%%%****
                ...::-=+*##**#%%%%%#*+++++===---------:::.....:::::::---===+**#%%%%%%###*=-...:::-+**#%%#***
                :::::--=++*#%%%%%%%%%#**+++=====-==-----:..::::::-:::--=+++*#%%%%%%######*=....:--+*##%%****
                ---------==+*#%%%%%%%%#****+=--=====--=-:::.::::::::::-=**#%%%%%%%%%%%###+-:.....:-=+#%%****
                -=============++*#%%%%%%#*#+==---==--=---:::::::::::::-=*#%%%%@@%%%%@%%#*=-:::...  .-=*#*+**
                ======+++++++======++*###++++=-=====-------::--:::::::-=+#%%%@%@%%%%%*=-::--:-::.....:+#*+*#
                ======++++===++==---=++=++++==+==---------::::::::::-:-==+*+++==--------------=-:.:::.:+****
                ============+++++++++++++++++===---::----::::::::::::--===-------==-======+=+==--:::::.=**##
                ===============-=====++========------::::::::::::::::---::=======++======+=====------::-*#%%
                ====----------:::::::::::::-------:::::.::::::::..::::--:::::-====-====--------==---=-::+#%%
                =====---=-----:..........:.:::----::::::::-::::::.::::-::::..:..:::.::::::::------=--:::-*%%
                +++=====--:-:.... ........::::----:-----:----:::::::-----::::..........:::::-----=====---+*#
                +++======--:::..........:::::-------------=----:::-----=--:-::.:.......:-=====--=+=======+*#
                +=++======--::.....::::-:----------===---===-=-------=---:::::::::::.:::--++===-==+==+====+*
                ======+===-::..:::::::::::--======++===========-----------::----::::...::--+++=-==-=+=+*%%%%
                ++======---:::::::::-----==+***++++=========+===----------:---=--::::::::-===--===+++++***#%
                **+++++==---::::-:-----=+********++++++==+++++=+=====-=-----====++=------:-===-===+*#%@@@@@@
                ********+==---========+****+++****++++++***+*+*+++===++++=-=---==+***++=====+++++++++=+=+=++
                *******+=======+++++*##*++++++*###***************++++++++=----===+++***+=+++=+===+***###****
                ******++++++*++++*#%%#**++++++**######******************+==-====+*****##+=+**##%%%%%%%%%%%%#
                #*+++++==+++**#####*####*#***+**##%%##################*+====+++*******##+==+*******#*#######
                %##*+++++++********###***********###################**+++++++**+++*****++++++**##%%%%%%%%%%%
                #%##****++++++++==+##*#*******+****#################******+++++*#***++++++****#%%%#*****####
                %%%##*+++++++****++*##%%###*************##########***********##%#**++++++#*+*##%%##%%%%%%%%#
                #**####*#*++++*#*++***#%%%%%#####*##*****#########****#******####**+==+++*+==+++*#####%%%%%%
                ###%%##***+*++++**+**########**+***********######**+**++=*++##*#*+++++*****+=+*#*##########%
                ####**####**+++++****##########++#+=+***=-+++*#*+=-=+*+-:+*###********####*=+=-+########%%%#
                ##*####%#####*********####*####*++===-*-::----*+:...:=:.:####*******####***++++-=*%%#######%
                #%%%%%%###%###*********#*#########+=--+-..::-:-=....-**#%###******#######**++++=::-=+*######
                #%%%###%%%##%###**#****##*#*#####%%%%%%*-::.::=*+=+*######******##########***++*=...:-=+**##
                %%####%#%#%#%######********####%%%%%##%%%%%%%%%%%#######******######%%#%##***++*+:....:-++**
                %%%%##%%%%%%##%%%%##*******#***######%%%%%#%%#########*****+*#####%#%%%%%#*******-......:-+*
                %%%###%%%%#%###%%%%%##*****#*##****################*****+**#####%%#%%%%%%##**###*-::......:=
                %%#%%%########%##%%%%%#*****###****************************##%##%%#%%%%%%########-:::::::.::
                %#%%%%%#######%%%%%%%%%##*****#****#******************++**##%%%%%%%%%%%%%########-::::..:..:
                #%%%%%%##%###%#%%%%%%%%%%#*********#***##************++**####%%%%%%%%%%%###%###%#--::::::::.

                        "Cuando los tiempos fueron difíciles... 
                    Y los errores de código y estres abundaban... 
                        Este sujeto siempre estubo allí... 
                            para sacarnos una sonrisa...
                        ...Te recordaremos michi sonriente..."
                
                ''')

    """
    =================================================================
                        FUNCIONES PARA EL CRM
    =================================================================
    """

    def ol_crm_get_token (self):
        '''Función que retorna el token de acceso necesario para utilizar la api del crm'''

        server_ip = self.env['ir.config_parameter'].sudo().get_param('licibot_module.ip')
        url = f'http://{server_ip}:8069/token'
        response = requests.get(url)
        _logger.info(f'api crm status: {response.status_code}')

        if response.status_code == 200:
            data = response.json() 
            token = data["token"]
            return token
        else:
            _logger.info(f"\n Error al obtener el token. Código de estado: {response.status_code}")
            return None

    def ol_crm_craft_json (self, codigo_externo, nombre_licitacion, tipo_licitacion, descripcion_licitacion, nombre_contacto, cargo_contacto, fecha_cierre):
        '''Función que arma un json con los parametros que recibe'''

        json = {'licitaciones': [{
            'CodigoExterno': codigo_externo, 
            'Tipo': tipo_licitacion, 
            'Nombre': nombre_licitacion, 
            'Descripcion': descripcion_licitacion, 
            'NombreUsuario': nombre_contacto, 
            'CargoUsuario': cargo_contacto, 
            'FechaCierre': fecha_cierre }]}

        return json

    def ol_crm_send_info (self):
        '''Función que envía al CRM la lista de unidades de compra rankeadas. La cantidad enviada depende del parametro configurado en odoo'''

        server_ip = self.env['ir.config_parameter'].sudo().get_param('licibot_module.ip')
        _logger.info('''\n\n\n>>> Ejecutando CRON Licibot: Envío al CRM <<<\n\n\n''')

        # Listar las id de unidades de compra rankeadas
        ranking_length = int(self.env['ir.config_parameter'].sudo().get_param('licibot_module.ranking_length'))
        self.env.cr.execute(f'SELECT id FROM licibot_unidad_compra ORDER BY ranking ASC LIMIT {ranking_length};')
        id_unidad_list = list(line[0] for line in self.env.cr.fetchall())

        # Obtener token de la api crm
        token = self.ol_crm_get_token()

        # Recorrer la lista de ids de unidades de compra rankeadas
        for id_unidad in id_unidad_list: 
            
            query_ultima_oportunidad = f'''
            SELECT CAST(create_date AS DATE) FROM crm_lead WHERE bidding_number LIKE '%{id_unidad}%';
            '''
            self.env.cr.execute(query_ultima_oportunidad)
            fecha_ultima_oportunidad = self.env.cr.fetchone()

            fecha_actual = datetime.date.today()
            diff_dias_permitidos = int(self.env['ir.config_parameter'].sudo().get_param('licibot_module.days_gone'))

            # Cuando exista la fecha de ultima oportunidad la calcula, caso contrario asigna un valor a la diff_real para entender que no existen registros de esa unidad de compra
            if fecha_ultima_oportunidad:
                fecha_ultima_oportunidad = datetime.date(fecha_ultima_oportunidad[0].year, fecha_ultima_oportunidad[0].month, fecha_ultima_oportunidad[0].day)
                diff_real = int((fecha_actual - fecha_ultima_oportunidad).total_seconds() / 60 / 60 / 24)
            else:
                diff_real = 9999999

            # Si han pasado "diff_dias_permitidos" desde la última oportunidad ingresada para la unidad de compra... Caso contrario la ignora
            if (diff_real > diff_dias_permitidos):

                # Query para obtener los datos de la unidad de compra
                query_datos = f'''
                SELECT  
                    DISTINCT(licibot_unidad_compra.id), 
                    licibot_unidad_compra.nombre_unidad,
                    licibot_licitacion.nom_contacto,
                    licibot_licitacion.cargo_contacto,
                    licibot_unidad_compra.ranking
                FROM licibot_unidad_compra 
                JOIN licibot_licitacion ON licibot_unidad_compra.id = licibot_licitacion.unidad_compra_id 
                JOIN licibot_item_licitacion ON licibot_item_licitacion.licitacion_id = licibot_licitacion.id
                WHERE licibot_unidad_compra.id = {id_unidad}
                AND licibot_licitacion.fecha_creacion = (
                    SELECT MAX(fecha_creacion) FROM licibot_unidad_compra 
                    JOIN licibot_licitacion ON licibot_unidad_compra.id = licibot_licitacion.unidad_compra_id 
                    WHERE licibot_unidad_compra.id = {id_unidad}
                    );
                '''
                self.env.cr.execute(query_datos)
                resultado = self.env.cr.fetchone()

                # Query para calcular el monto diferencial de la unidad de compra
                query_monto_diferencial = f'''
                SELECT 
                    SUM(CASE WHEN licibot_licitacion.fecha_adjudicacion >= DATE '2022-01-01' AND licibot_licitacion.fecha_adjudicacion <= DATE '2022-12-31' THEN licibot_item_licitacion.cant_unitaria_prod * licibot_item_licitacion.monto_unitario ELSE 0 END) -
                    SUM(CASE WHEN licibot_licitacion.fecha_adjudicacion >= DATE '2023-01-01' AND licibot_licitacion.fecha_adjudicacion <= DATE '2023-12-31' THEN licibot_item_licitacion.cant_unitaria_prod * licibot_item_licitacion.monto_unitario ELSE 0 END) AS "Monto Diferencial"
                FROM 
                    licibot_unidad_compra 
                    JOIN licibot_licitacion ON licibot_unidad_compra.id = licibot_licitacion.unidad_compra_id
                    JOIN licibot_item_licitacion ON licibot_licitacion.id = licibot_item_licitacion.licitacion_id
                WHERE 
                    licibot_unidad_compra.id = {id_unidad}
                GROUP BY 
                    licibot_unidad_compra.id
                ORDER BY
                    "Monto Diferencial" DESC;
                '''
                self.env.cr.execute(query_monto_diferencial)
                resultado2 = self.env.cr.fetchone()

                # Pre-armado de datos a enviar
                fecha_actual = datetime.date.today()
                id_unidad = resultado[0]
                nombre_unidad = resultado[1]
                monto_por_licitar = resultado2[0]
                nombre_contacto = resultado[2]
                cargo_contacto = resultado[3]
                margen_días = 5                         # Será parámetro

                # Armado de json con datos a enviar
                json = self.ol_crm_craft_json (
                    f"{id_unidad} - {fecha_actual}",                                                                                             # CodigoExterno: Id Unidad de Compra + Fecha Actual.
                    " ",                                                                                                                         # Tipo: Dejar en blanco o crear un valor para un "Sin Tipo".
                    f"{nombre_unidad} + Monto de gas por licitar {locale.currency(monto_por_licitar, grouping=True)} al {fecha_actual}",         # Nombre: "Nombre Cliente" + "Monto Gas por Licitar $ al " + Fecha Actual.
                    f"{nombre_unidad} + Monto de gas por licitar {locale.currency(monto_por_licitar, grouping=True)} al {fecha_actual}",         # Descripción: Repetir lo de campo nombre.
                    nombre_contacto,                                                                                                             # Nombre Usuario: Tomar el nombre desde la última licitación.
                    cargo_contacto,                                                                                                              # Cargo Usuario: Tomar el cargo desde la última licitación.
                    (fecha_actual + datetime.timedelta(days = margen_días)).strftime('%Y-%m-%d'))                                                # Fecha Cierre: Tomar fecha de hoy + X días (parámetro).
                
                # Envio de información al CRM acorde a las instrucciones de Fco.
                url = f'http://{server_ip}:8069/licitaciones'
                headers = {'Authorization': token}
                response = requests.post(url, headers=headers, json=json)
                
        _logger.info('''\n\n\n>>> Finalizando CRON Licibot: Envío al CRM <<<\n\n\n''')

class ProductoServicio (models.Model):
    _name = 'licibot.producto.servicio'

    nom_prod_servicio = fields.Char(string = 'Nombre Producto Servicio')
    categoria_id = fields.Many2one('licibot.categoria', string='categoria_id')

class ItemLicitacion (models.Model):
    _name = 'licibot.item.licitacion'

    correlativo = fields.Integer(string = 'Correlativo')
    uni_medida_prod = fields.Char(string = 'Unidad Medida Producto')
    cant_unitaria_prod = fields.Integer(string = 'Cantidad Unitaria Producto')
    monto_unitario = fields.Float(string = 'Monto Unitario')
    desc_producto = fields.Char(string = 'Descripción Producto')
    licitacion_id = fields.Many2one('licibot.licitacion', string = 'Licitacion_id')
    producto_servicio_id = fields.Many2one('licibot.producto.servicio', string = 'ProductoServicio_id')
    proveedor_id = fields.Many2one('licibot.proveedor', string = 'Proveedor_id')

    def init(self):
        '''Método que se ejecutara en la inicialización de bd, al instalar o actualizar este u otro
        modulo que contenga el modelo por herencia, es importante el decorador @api.model_cr'''

        query = '''
        CREATE OR REPLACE VIEW licibot_ranking_v1 AS
        SELECT 
            licibot_unidad_compra.id AS "ID Unidad de Compra",
            licibot_unidad_compra.nombre_unidad as "Nombre de Unidad de Compra",
            SUM(CASE WHEN licibot_licitacion.fecha_adjudicacion >= DATE '2022-01-01' AND licibot_licitacion.fecha_adjudicacion <= DATE '2022-12-31' THEN licibot_item_licitacion.cant_unitaria_prod * licibot_item_licitacion.monto_unitario ELSE 0 END) AS "Monto Total Año Anterior",
            SUM(CASE WHEN licibot_licitacion.fecha_adjudicacion >= DATE '2023-01-01' AND licibot_licitacion.fecha_adjudicacion <= DATE '2023-12-31' THEN licibot_item_licitacion.cant_unitaria_prod * licibot_item_licitacion.monto_unitario ELSE 0 END) AS "Monto Total Año Actual",
            SUM(CASE WHEN licibot_licitacion.fecha_adjudicacion >= DATE '2022-01-01' AND licibot_licitacion.fecha_adjudicacion <= DATE '2022-12-31' THEN licibot_item_licitacion.cant_unitaria_prod * licibot_item_licitacion.monto_unitario ELSE 0 END) -
            SUM(CASE WHEN licibot_licitacion.fecha_adjudicacion >= DATE '2023-01-01' AND licibot_licitacion.fecha_adjudicacion <= DATE '2023-12-31' THEN licibot_item_licitacion.cant_unitaria_prod * licibot_item_licitacion.monto_unitario ELSE 0 END) AS "Monto Diferencial"
        FROM 
            licibot_unidad_compra 
            JOIN licibot_licitacion ON licibot_unidad_compra.id = licibot_licitacion.unidad_compra_id
            JOIN licibot_item_licitacion ON licibot_licitacion.id = licibot_item_licitacion.licitacion_id
        GROUP BY 
            licibot_unidad_compra.id
        ORDER BY
            "Monto Diferencial" DESC;
        '''

        tools.drop_view_if_exists(self._cr, 'licibot_ranking_v1')
        self.env.cr.execute(query)

        vista_variables = '''
        CREATE OR REPLACE VIEW licibot_variables_kmeans AS
        SELECT
            licibot_unidad_compra.id as IDUnidad,
            licibot_unidad_compra.nombre_unidad as NombreUnidad,
            licibot_organismo.nombre_organismo NombreOrganismo,
            COUNT(DISTINCT licibot_licitacion.codigo_externo) as LicitacionesTotales ,
            CAST(SUM(licibot_item_licitacion.cant_unitaria_prod * licibot_item_licitacion.monto_unitario) AS FLOAT) as TotalGastado,
            TO_CHAR(MIN(licibot_licitacion.fecha_adjudicacion), 'YYYY-MM-DD') AS PrimeraLicitacion,
            TO_CHAR(MAX(licibot_licitacion.fecha_adjudicacion), 'YYYY-MM-DD') AS UltimaLicitacion,
            SUM(CASE WHEN licibot_licitacion.fecha_adjudicacion BETWEEN '2022-01-01' AND '2022-12-31' THEN licibot_item_licitacion.cant_unitaria_prod * licibot_item_licitacion.monto_unitario ELSE 0 END) as Gasto2022,
            (CAST((
            SUM(CASE WHEN licibot_licitacion.fecha_adjudicacion BETWEEN '2018-01-01' AND '2022-12-31' THEN licibot_item_licitacion.cant_unitaria_prod * licibot_item_licitacion.monto_unitario ELSE 0 END) / 
            NULLIF(
                (SELECT COUNT(DISTINCT EXTRACT(year FROM (licibot_licitacion.fecha_adjudicacion)))
                FROM licibot_licitacion
                WHERE licibot_licitacion.fecha_adjudicacion BETWEEN '2018-01-01' AND '2022-12-31'
                ), 
                0
                )
            - SUM(CASE WHEN licibot_licitacion.fecha_adjudicacion BETWEEN '2023-01-01' AND '2023-12-31' THEN licibot_item_licitacion.cant_unitaria_prod * licibot_item_licitacion.monto_unitario ELSE 0 END)
            ) AS FLOAT)) as DiferenciaAnterior2023,
            (SELECT COUNT(DISTINCT licibot_item_licitacion.proveedor_id)
            FROM licibot_licitacion
            JOIN licibot_item_licitacion ON licibot_licitacion.id = licibot_item_licitacion.licitacion_id
            WHERE EXTRACT(year FROM (licibot_licitacion.fecha_adjudicacion)) = '2022' AND licibot_licitacion.unidad_compra_id = licibot_unidad_compra.id) as Proveedores2022,
            (SELECT COUNT(DISTINCT licibot_item_licitacion.proveedor_id)
            FROM licibot_licitacion
            JOIN licibot_item_licitacion ON licibot_licitacion.id = licibot_item_licitacion.licitacion_id
            WHERE EXTRACT(year FROM (licibot_licitacion.fecha_adjudicacion)) = '2023' AND licibot_licitacion.unidad_compra_id = licibot_unidad_compra.id) as Proveedores2023,
            CASE 
                WHEN EXISTS (
                    SELECT 1
                    FROM licibot_licitacion
                    JOIN licibot_item_licitacion ON licibot_licitacion.id = licibot_item_licitacion.licitacion_id
                    JOIN licibot_proveedor ON licibot_item_licitacion.proveedor_id = licibot_proveedor.id
                    WHERE licibot_licitacion.unidad_compra_id = licibot_unidad_compra.id
                    AND licibot_proveedor.nombre_proveedor = 'ABASTIBLE S.A.'
                ) THEN 0
                WHEN EXISTS (
                    SELECT 1
                    FROM licibot_licitacion
                    JOIN licibot_item_licitacion ON licibot_licitacion.id = licibot_item_licitacion.licitacion_id
                    JOIN licibot_proveedor ON licibot_item_licitacion.proveedor_id = licibot_proveedor.id
                    WHERE licibot_licitacion.unidad_compra_id = licibot_unidad_compra.id
                    AND licibot_proveedor.nombre_proveedor IN (
                        'EMPRESAS LIPIGAS S A',
                        'EMPRESAS GASCO S.A.',
                        'GASCO GLP S A'
                    )
                ) THEN 1
                ELSE 2
            end as CompetenciaOtros,
            CAST(SUM(licibot_item_licitacion.cant_unitaria_prod * licibot_item_licitacion.monto_unitario) / COUNT(DISTINCT licibot_licitacion.codigo_externo) AS FLOAT) as ValorPromedioCompra,
            COALESCE(licibot_unidad_compra.sii_num_trab_dep, 0) as CantidadTrabajadores,
            CASE 
                WHEN EXISTS (
                    SELECT 1
                    FROM licibot_licitacion
                    JOIN licibot_item_licitacion ON licibot_licitacion.id = licibot_item_licitacion.licitacion_id
                    JOIN licibot_proveedor ON licibot_item_licitacion.proveedor_id = licibot_proveedor.id
                    WHERE licibot_licitacion.unidad_compra_id = licibot_unidad_compra.id
                    AND licibot_proveedor.nombre_proveedor = 'ABASTIBLE S.A.'
                ) THEN 1
                ELSE 0
            end as ClienteNuevo
        FROM licibot_licitacion
        JOIN licibot_unidad_compra ON licibot_licitacion.unidad_compra_id = licibot_unidad_compra.id
        JOIN licibot_item_licitacion ON licibot_licitacion.id = licibot_item_licitacion.licitacion_id
        JOIN licibot_organismo ON licibot_unidad_compra.organismo_id = licibot_organismo.id
        GROUP BY licibot_unidad_compra.nombre_unidad, licibot_unidad_compra.id, licibot_organismo.nombre_organismo
        ORDER BY TotalGastado desc 
        '''

        tools.drop_view_if_exists(self._cr, 'licibot_variables_kmeans')
        self.env.cr.execute(vista_variables)