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

    # codigo_organismo = fields.Integer(string='Código organismo')
    nombre_organismo = fields.Char(string='Nombre organismo') 

class UnidadCompra(models.Model):
    _name = 'licibot.unidad.compra'

    # codigo_unidad = fields.Integer(string='Código unidad')
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

    # id_tipo_comp = fields.Integer(string = 'ID Tipo Competidor')
    nom_tipo_comp = fields.Char(string = 'Nombre Tipo Competidor')

class Proveedor (models.Model):
    _name = 'licibot.proveedor'

    rut_proveedor = fields.Char(string = 'Rut Proveedor')
    nombre_proveedor = fields.Char(string = 'Nombre Proveedor')
    tipo_competidor_id = fields.Many2one('licibot.tipo.competidor', string = 'tipoCompetidor_id')

class Categoria (models.Model):
    _name = 'licibot.categoria'

    # codigo_categoria = fields.Integer(string = 'Código Categoria')
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

    # id_monto_estimado = fields.Integer(string = 'ID Monto Estimado')
    nom_monto_estimado = fields.Char(string = 'Nombre Monto Estimado')

class ModalidadPago (models.Model):
    _name = 'licibot.modalidad.pago'

    # id_modalidad_pago = fields.Integer(string = 'ID Modalidad Pago')
    nom_modalidad_pago = fields.Char(string = 'Nombre Modalidad Pago')

class UnidadTiempoContrato (models.Model):
    _name = 'licibot.unidad.tiempo.contrato'

    # id_uni_tiempo_con = fields.Integer(string = 'ID Unidad Tiempo Contrato')
    nom_uni_tiempo_con = fields.Char(string = 'Nombre Unidad Tiempo Contrato')

class UnidadTiempoEvaluacion (models.Model):
    _name = 'licibot.unidad.tiempo.evaluacion'

    # id_uni_tiempo_ev = fields.Integer(string = 'ID Unidad Tiempo Evaluacion')
    nom_uni_tiempo_ev = fields.Char(string = 'Nombre Unidad Tiempo Evaluacion')

class TipoActoAdministrativo (models.Model):
    _name = 'licibot.tipo.acto.administrativo'

    # id_tipo_acto_admin = fields.Integer(string = 'ID Tipo Acto Administrativo')
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
                        FUNCIONES BASE DE DATOS
    =================================================================
    """
    # REVISAR CÓDIGO CONSIDERANDO ERRORES DE NORM. CONOCIDOS Y ID ASIGNADA POR ODOO.
    def insertar_organismo (self, codigo_organismo, nombre_organismo):
 
        if codigo_organismo is not None:
            organismo_exists = self.env['licibot.organismo'].sudo().search([('codigo_organismo', '=', codigo_organismo)])
            
            if organismo_exists:
                _logger.info(f"El organismo {codigo_organismo}:{nombre_organismo}, ya existe en la base de datos")
            else:
                self.env['licibot.organismo'].sudo().create({'id': codigo_organismo, 'nombre_organismo': nombre_organismo})

        else:
            _logger.info(f"!!! Código organismo nulo. Omitiendo inserción de datos en tabla organismo...")
   
    # REVISAR CÓDIGO CONSIDERANDO ERRORES DE NORM. CONOCIDOS Y ID ASIGNADA POR ODOO.
    def insertar_unidadCompra (self, codigo_unidad, rut_unidad, nombre_unidad, direccion_unidad, comuna_unidad, region_unidad, organismo_id): # Info SII cargada posteriormente con queries (momentaneo)
        
        if codigo_unidad is not None:
            unidadCompra_exists = self.env['licibot.unidad.compra'].sudo().search([('id', '=', codigo_unidad)])

            if unidadCompra_exists:
                _logger.info(f"La unidad de compra {codigo_unidad}:{nombre_unidad}, ya existe en la base de datos.")
            else:
                self.env['licibot.unidad.compra'].sudo().create({
                    'id' : codigo_unidad, 
                    'rut_unidad' : rut_unidad, 
                    'nombre_unidad' : nombre_unidad, 
                    'direccion_unidad' : direccion_unidad, 
                    'comuna_unidad' : comuna_unidad, 
                    'region_unidad' : region_unidad, 
                    'organismo_id' : self.is_null_int(organismo_id)
                })    
        else:
            _logger.info(f"!!! código unidad nulo. Omitiendo inserción de datos en tabla unidad...")
   
    # REVISAR CÓDIGO CONSIDERANDO ERRORES DE NORM. CONOCIDOS Y ID ASIGNADA POR ODOO.
    def insertar_proveedor(self, rut_proveedor, nombre_proveedor):
        
        if rut_proveedor:
            proveedor_existente = self.env['licibot.proveedor'].sudo().search([('rut_proveedor', '=', rut_proveedor)])

            if proveedor_existente:
                _logger.info(f"El proveedor {rut_proveedor} {nombre_proveedor} ya existe en la base de datos.")
            else:
                self.env['licibot.proveedor'].sudo().create({
                    'rut_proveedor': rut_proveedor,
                    'nombre_proveedor': nombre_proveedor,
                    'tipo_competidor_id': self.identificar_tipo_competidor(nombre_proveedor),
                })
        else:
            _logger.info("¡RUT de proveedor nulo. Omitiendo inserción de datos en la tabla proveedor...")
  
    # REVISAR CÓDIGO CONSIDERANDO ERRORES DE NORM. CONOCIDOS Y ID ASIGNADA POR ODOO.
    def insertar_categoria(self, codigo_categoria, nom_categoria):

        if codigo_categoria:
            categoria_existente = self.env['licibot.categoria'].sudo().search([('id', '=', codigo_categoria)])

            if categoria_existente:
                _logger.info(f"La categoría {codigo_categoria}:{nom_categoria} ya existe en la base de datos.")
            else:
                self.env['licibot.categoria'].sudo().create({
                    'id': codigo_categoria,
                    'nom_categoria': nom_categoria,
                })
        else:
            _logger.info("¡Código de categoría nulo. Omitiendo inserción de datos en la tabla categoría...")
   
    # REVISAR CÓDIGO CONSIDERANDO ERRORES DE NORM. CONOCIDOS Y ID ASIGNADA POR ODOO.
    def insertar_productoServicio(self, id_producto_servicio, nom_prod_servicio, categoria_id):

        if id_producto_servicio:
            producto_servicio_existente = self.env['licibot.producto.servicio'].sudo().search([('id', '=', id_producto_servicio)])

            if producto_servicio_existente:
                _logger.info(f"El producto/servicio {id_producto_servicio} {nom_prod_servicio} ya existe en la base de datos.")
            else:
                self.env['licibot.producto.servicio'].sudo().create({
                    'id': id_producto_servicio,
                    'nom_prod_servicio': nom_prod_servicio,
                    'categoria_id': self.is_null_int(categoria_id),
                })
        else:
            _logger.info("¡ID de producto/servicio nulo. Omitiendo inserción de datos en la tabla producto/servicio...")
   
    # REVISAR CÓDIGO CONSIDERANDO ERRORES DE NORM. CONOCIDOS Y ID ASIGNADA POR ODOO.
    def insertar_adjudicacion(self, num_admin_adjudicacion, fecha_admin_adjudicacion, num_oferentes, url_acta, tipo_acto_admn_id):

        self.env['licibot.adjudicacion'].sudo().create({
            'num_admin_adjudicacion': numeroAdmAdjudicacion,
            'fecha_admin_adjudicacion': fechaAdmAdjudicacion,
            'num_oferentes': numeroOferentes,
            'url_acta': urlActa,
            'tipo_acto_admin_id': self.is_null_int(tipo_acto_admn_id),
        })
   
    # REVISAR CÓDIGO CONSIDERANDO ERRORES DE NORM. CONOCIDOS Y ID ASIGNADA POR ODOO.
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
        adjudicacion_id, 
        tipo_licitacion_id, 
        uni_tiempo_ev_id, 
        unidad_monetaria_id, 
        monto_estimado_id, 
        uni_tiempo_con_id, 
        modalidad_pago_id, 
        unidad_compra_id 
        ):

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
                    'fecha_creacion' : fecha_creacion, 
                    'fecha_cierre_2' : fecha_cierre_2, 
                    'fecha_inicio' : fecha_inicio, 
                    'fecha_final' : fecha_final, 
                    'fecha_pub_respuestas' : fecha_pub_respuestas, 
                    'fecha_act_aper_tec' : fecha_act_aper_tec, 
                    'fecha_act_aper_eco' : fecha_act_aper_eco, 
                    'fecha_publicacion' : fecha_publicacion, 
                    'fecha_adjudicacion' : fecha_adjudicacion, 
                    'fecha_est_adjudicacion' : fecha_est_adjudicacion, 
                    'fecha_soporte_fisico' : fecha_soporte_fisico, 
                    'fecha_tiempo_eval' : fecha_tiempo_eval, 
                    'fecha_estimada_firma' : fecha_estimada_firma, 
                    'fecha_usuario' : fecha_usuario, 
                    'fecha_visita_terreno' : fecha_visita_terreno, 
                    'fecha_entrega_antecedentes' : fecha_entrega_antecedentes, 
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
                    'adjudicacion_id' : self.is_null_str(adjudicacion_id), 
                    'tipo_licitacion_id' : self.is_null_str(tipo_licitacion_id), 
                    'uni_tiempo_ev_id' : self.is_null_int(uni_tiempo_ev_id), 
                    'unidad_monetaria_id' : self.is_null_int(unidad_monetaria_id), 
                    'monto_estimado_id' : self.is_null_int(monto_estimado_id), 
                    'uni_tiempo_con_id' : self.is_null_int(uni_tiempo_con_id), 
                    'modalidad_pago_id' : self.is_null_int(modalidad_pago_id), 
                    'unidad_compra_id' : self.is_null_str(unidad_compra_id) 
                })
        else:
            _logger.info("¡ID de producto/servicio nulo. Omitiendo inserción de datos en la tabla producto/servicio...")
   
    # REVISAR CÓDIGO CONSIDERANDO ERRORES DE NORM. CONOCIDOS Y ID ASIGNADA POR ODOO.
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

        proveedor_select = self.env['licibot.proveedor'].sudo().search([('rut_proveedor','=', proveedor_id)])
        licitacion_select = self.env['licibot.licitacion'].sudo().search([('codigo_Externo','=', licitacion_id)])

        self.env['licibot.item.licitacion'].sudo().create({
            'correlativo' : correlativo, 
            'uni_medida_prod' : uni_medida_prod, 
            'cant_unitaria_prod' : cant_unitaria_prod, 
            'monto_unitario' : monto_unitario, 
            'desc_producto' : desc_producto, 
            'licitacion_id' : self.is_null_str(licitacion_select.id), 
            'producto_servicio_id' : self.is_null_int(producto_servicio_id), 
            'proveedor_id' : self.is_null_int(proveedor_select.id)
            })
  
    # VERIFICAR FUNCIONAMIENTO...
    def obtener_licitaciones_hoy(self, ticket):
        fecha = self.get_fecha_actual()
        url = "http://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json"
        params = {"fecha": fecha, "ticket": ticket}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Genera una excepción si la solicitud no fue exitosa

            data = response.json()

            if "Listado" in data:
                licitaciones = data["Listado"]
                codigo_externo_list = [licitacion["CodigoExterno"] for licitacion in licitaciones]
                return codigo_externo_list
            else:
                _logger.warning("No se encontraron licitaciones.")
                return []
        except requests.exceptions.RequestException as e:
            _logger.error("Error en la solicitud HTTP: %s", e)
            return []
  
    # VERIFICAR FUNCIONAMIENTO...
    def obtener_licitaciones_gas(self, codigos_externos, ticket, keywords):
        licitaciones_filtradas = []

        for codigo in codigos_externos:
            url = "http://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json"
            params = {"codigo": codigo, "ticket": ticket}

            try:
                response = requests.get(url, params=params)
                response.raise_for_status()  # Genera una excepción si la solicitud no fue exitosa

                data = response.json()

                if "Listado" in data:
                    licitacion = data["Listado"][0]  # El código externo es único.
                    if "Nombre" in licitacion and "Descripcion" in licitacion and "Categoria" in licitacion:
                        texto_licitacion = f"{licitacion['Nombre'].lower()} {licitacion['Descripcion'].lower()} {licitacion['Categoria'].lower()}"
                        if any(keyword.strip().lower() in texto_licitacion for keyword in keywords.split(',')):
                            licitaciones_filtradas.append(codigo)
                else:
                    _logger.warning(f"No se encontró licitación para el CodigoExterno {codigo}.")
            except requests.exceptions.RequestException as e:
                _logger.error("Error en la solicitud HTTP para el CodigoExterno %s: %s", codigo, e)

        licitaciones_model = self.env['your.licitaciones.model']
        licitaciones = licitaciones_model.search([('codigo_externo', 'in', licitaciones_filtradas)])
        self.licitaciones_ids = [(6, 0, licitaciones.ids)]
  
    # VERIFICAR FUNCIONAMIENTO...
    def obtener_licitaciones_y_actualizar(self):
        ticket = self.env['ir.config_parameter'].sudo().get_param('your.ticket.parameter')
        codigos_externos = self.obtener_licitaciones_hoy(ticket)
        keywords = self.keywords
        self.obtener_licitaciones_gas(codigos_externos, ticket, keywords)

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
                response = requests.get(url, params=params)
                return response
            except requests.exceptions.ReadTimeout as e:
                _logger.info(f"Intento {retry+1} de {max_retries}. Error de tiempo de espera: {e}")
                time.sleep(5)  # Esperar 5 segundos antes de reintentar
    
    # VERIFICAR UTILIDAD (?)
    def poblamiento_inicial (self):
        """
        ## Descripción
        Función que recibe por parámetro una lista de licitaciones y, para cada una de las ID de licitaciones, envía una petición a la API de mercadopublico.cl para recopilar información más detallada sobre esa ID. Repite este proceso tantas veces como licitaciones haya en la lista y luego exporta los datos a un archivo CSV.
        ## Parámetros
        - rutaArchivo: str con formato ruta\\archivo.csv, ej: 'Inputs\MuestraLicitacionesAdjudicadasGas.csv'.
        - ticket: Ticket de la API Mercado Público (similar a un token de acceso, sin él no es posible interactuar con la API).
        ## Retorna
        - None
        """
        # Contador ID's licitaciones
        count = 1
        
        ruta_archivo = 'Inputs/MuestraLicitacionesAdjudicadasGas.csv'

        # Leer lista de licitaciones recibida por parámetro.
        listado = pd.read_csv(rutaArchivo, sep=";")

        # Crear lista que almacene únicamente la columna de ids de licitaciones
        ids = listado['IDLicitacion']

        # Restringir la columna de ids solo a la ID antes del primer ";"
        ids = ids.apply(lambda x: x.split(';')[0])

        # Traer token mp desde configuración
        token_mp = self.env['ir.config_parameter'].sudo().get_param('licibot_module.token_mp')

        try:
            # Recorrer los elementos almacenados en la lista de ids de licitaciones
            for id in ids:

                # Realizar petición de datos para la ID de licitación
                url = 'https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json'
                args = {'codigo': id, 'ticket': token_mp}
                response = self.make_request_with_retries(url, args)
                _logger.info(f"\nID: {id} Status Code: {response} \n")
                _logger.info(f"\nProcesando ({count}/{len(ids)})")

                if response is not None and response.status_code == 200:
                    payload = response.json()

                    for item in payload['Listado']:
                        data = {
                            'CodigoExterno': item.get('CodigoExterno'),
                            'Nombre': item.get('Nombre'),
                            'CodigoEstado': item.get('CodigoEstado'),
                            'Descripcion': item.get('Descripcion'),
                            'FechaCierre1': item.get('FechaCierre'),
                            'Estado': item.get('Estado'),
                            'Comprador_CodigoOrganismo': item.get('Comprador', {}).get('CodigoOrganismo'),
                            'Comprador_NombreOrganismo': item.get('Comprador', {}).get('NombreOrganismo'),
                            'Comprador_RutUnidad': item.get('Comprador', {}).get('RutUnidad'),
                            'Comprador_CodigoUnidad': item.get('Comprador', {}).get('CodigoUnidad'),
                            'Comprador_NombreUnidad': item.get('Comprador', {}).get('NombreUnidad'),
                            'Comprador_DireccionUnidad': item.get('Comprador', {}).get('DireccionUnidad'),
                            'Comprador_ComunaUnidad': item.get('Comprador', {}).get('ComunaUnidad'),
                            'Comprador_RegionUnidad': item.get('Comprador', {}).get('RegionUnidad'),
                            'Comprador_RutUsuario': item.get('Comprador', {}).get('RutUsuario'),
                            'Comprador_CodigoUsuario': item.get('Comprador', {}).get('CodigoUsuario'),
                            'Comprador_NombreUsuario': item.get('Comprador', {}).get('NombreUsuario'),
                            'Comprador_CargoUsuario': item.get('Comprador', {}).get('CargoUsuario'),
                            'DiasCierreLicitacion': item.get('DiasCierreLicitacion'),
                            'Informada': item.get('Informada'),
                            'CodigoTipo': item.get('CodigoTipo'),
                            'Tipo': item.get('Tipo'),
                            'TipoConvocatoria': item.get('TipoConvocatoria'),
                            'Moneda': item.get('Moneda'),
                            'Etapas': item.get('Etapas'),
                            'EstadoEtapas': item.get('EstadoEtapas'),
                            'TomaRazon': item.get('TomaRazon'),
                            'EstadoPublicidadOfertas': item.get('EstadoPublicidadOfertas'),
                            'JustificacionPublicidad': item.get('JustificacionPublicidad'),
                            'Contrato': item.get('Contrato'),
                            'Obras': item.get('Obras'),
                            'CantidadReclamos': item.get('CantidadReclamos'),
                            'FechaCreacion': item.get('Fechas', {}).get('FechaCreacion'),
                            'FechaCierre2': item.get('Fechas', {}).get('FechaCierre'),
                            'FechaInicio': item.get('Fechas', {}).get('FechaInicio'),
                            'FechaFinal': item.get('Fechas', {}).get('FechaFinal'),
                            'FechaPubRespuestas': item.get('Fechas', {}).get('FechaPubRespuestas'),
                            'FechaActoAperturaTecnica': item.get('Fechas', {}).get('FechaActoAperturaTecnica'),
                            'FechaActoAperturaEconomica': item.get('Fechas', {}).get('FechaActoAperturaEconomica'),
                            'FechaPublicacion': item.get('Fechas', {}).get('FechaPublicacion'),
                            'FechaAdjudicacion': item.get('Fechas', {}).get('FechaAdjudicacion'),
                            'FechaEstimadaAdjudicacion': item.get('Fechas', {}).get('FechaEstimadaAdjudicacion'),
                            'FechaSoporteFisico': item.get('Fechas', {}).get('FechaSoporteFisico'),
                            'FechaTiempoEvaluacion': item.get('Fechas', {}).get('FechaTiempoEvaluacion'),
                            'FechaEstimadaFirma': item.get('Fechas', {}).get('FechaEstimadaFirma'),
                            'FechaUsuario': item.get('Fechas', {}).get('FechaUsuario'),
                            'FechaVisitaTerreno': item.get('Fechas', {}).get('FechaVisitaTerreno'),
                            'FechaEntregaAntecedentes': item.get('Fechas', {}).get('FechaEntregaAntecedentes'),
                            'UnidadTiempoEvaluacion': item.get('UnidadTiempoEvaluacion'),
                            'DireccionVisita': item.get('DireccionVisita'),
                            'DireccionEntrega': item.get('DireccionEntrega'),
                            'Estimacion': item.get('Estimacion'),
                            'FuenteFinanciamiento': item.get('FuenteFinanciamiento'),
                            'VisibilidadMonto': item.get('VisibilidadMonto'),
                            'MontoEstimado': item.get('MontoEstimado'),
                            'Tiempo': item.get('Tiempo'),
                            'UnidadTiempo': item.get('UnidadTiempo'),
                            'Modalidad': item.get('Modalidad'),
                            'TipoPago': item.get('TipoPago'),
                            'NombreResponsablePago': item.get('NombreResponsablePago'),
                            'EmailResponsablePago': item.get('EmailResponsablePago'),
                            'NombreResponsableContrato': item.get('NombreResponsableContrato'),
                            'EmailResponsableContrato': item.get('EmailResponsableContrato'),
                            'FonoResponsableContrato': item.get('FonoResponsableContrato'),
                            'ProhibicionContratacion': item.get('ProhibicionContratacion'),
                            'SubContratacion': item.get('SubContratacion'),
                            'UnidadTiempoDuracionContrato': item.get('UnidadTiempoDuracionContrato'),
                            'TiempoDuracionContrato': item.get('TiempoDuracionContrato'),
                            'TipoDuracionContrato': item.get('TipoDuracionContrato'),
                            'JustificacionMontoEstimado': item.get('JustificacionMontoEstimado'),
                            'ObservacionContract': item.get('ObservacionContract'),
                            'ExtensionPlazo': item.get('ExtensionPlazo'),
                            'EsBaseTipo': item.get('EsBaseTipo'),
                            'UnidadTiempoContratoLicitacion': item.get('UnidadTiempoContratoLicitacion'),
                            'ValorTiempoRenovacion': item.get('ValorTiempoRenovacion'),
                            'PeriodoTiempoRenovacion': item.get('PeriodoTiempoRenovacion'),
                            'EsRenovable': item.get('EsRenovable'),
                            'Items_Cantidad': item.get('Items', {}).get('Cantidad')
                        }

                        adjudicacion = item.get('Adjudicacion')
                        if adjudicacion is not None:
                            data['Adjudicacion_Tipo'] = adjudicacion.get('Tipo')
                            data['Adjudicacion_Fecha'] = adjudicacion.get('Fecha')
                            data['Adjudicacion_Numero'] = adjudicacion.get('Numero')
                            data['Adjudicacion_NumeroOferentes'] = adjudicacion.get('NumeroOferentes')
                            data['Adjudicacion_UrlActa'] = adjudicacion.get('UrlActa')
                        else:
                            data['Adjudicacion_Tipo'] = None
                            data['Adjudicacion_Fecha'] = None
                            data['Adjudicacion_Numero'] = None
                            data['Adjudicacion_NumeroOferentes'] = None
                            data['Adjudicacion_UrlActa'] = None

                        # Agregar fila para cada item en el DataFrame
                        for i, item_data in enumerate(item.get('Items', {}).get('Listado', [])):
                            item_row = data.copy()

                            item_row.update({
                                'Items_Correlativo': item_data.get('Correlativo'),
                                'Items_CodigoProducto': item_data.get('CodigoProducto'),
                                'Items_codigo_categoria': item_data.get('CodigoCategoria'),
                                'Items_Categoria': item_data.get('Categoria'),
                                'Items_NombreProducto': item_data.get('NombreProducto'),
                                'Items_Descripcion': item_data.get('Descripcion'),
                                'Items_UnidadMedida': item_data.get('UnidadMedida'),
                                'Items_CantidadItem': item_data.get('Cantidad'),
                            })

                            adjudicacion = item_data.get('Adjudicacion')
                            if adjudicacion is not None:
                                item_row['Items_rut_proveedor'] = adjudicacion.get('rut_proveedor')
                                item_row['Items_nombre_proveedor'] = adjudicacion.get('nombre_proveedor')
                                item_row['Items_MontoUnitario'] = adjudicacion.get('MontoUnitario')

                                self.insertar_proveedor (
                                    item_row['Items_rut_proveedor'],
                                    item_row['Items_nombre_proveedor']
                                )

                                self.insertar_categoria (
                                    item_row['Items_codigo_categoria'],
                                    item_row['Items_Categoria']
                                )

                                self.insertar_productoServicio (
                                    item_row['Items_CodigoProducto'],
                                    item_row['Items_NombreProducto'],
                                    item_row['Items_codigo_categoria'] # categoria_id
                                )

                                self.insertar_item (
                                    item_row['Items_Correlativo'], 
                                    item_row['Items_UnidadMedida'],
                                    item_row['Items_CantidadItem'],
                                    item_row['Items_MontoUnitario'],
                                    item_row['Items_Descripcion'],
                                    data['CodigoExterno'], # licitacion_id
                                    item_row['Items_CodigoProducto'], # producto_servicio_id
                                    item_row['Items_rut_proveedor'] # proveedor_id
                                )

                                _logger.info(f"Los datos del item correlativo: {item_row['Items_Correlativo']} se han recopilado exitosamente.")
                                    
                        self.insertar_organismo (
                            data['Comprador_CodigoOrganismo'],
                            data['Comprador_NombreOrganismo']
                        )

                        self.insertar_unidadCompra (
                            data['Comprador_CodigoUnidad'],
                            data['Comprador_RutUnidad'].upper(),
                            data['Comprador_NombreUnidad'],
                            data['Comprador_DireccionUnidad'],
                            data['Comprador_ComunaUnidad'],
                            data['Comprador_RegionUnidad'],
                            data['Comprador_CodigoOrganismo'] # organismo_id
                        )

                        self.insertar_adjudicacion (
                            data['Adjudicacion_Numero'],
                            data['Adjudicacion_Fecha'],
                            data['Adjudicacion_NumeroOferentes'],
                            data['Adjudicacion_UrlActa'],
                            data['Adjudicacion_Tipo'] # tipo_acto_adm_id
                        )

                        self.insertar_licitacion (
                            data['CodigoExterno'], 
                            data['Nombre'], 
                            data['CodigoEstado'], 
                            data['Descripcion'],
                            data['FechaCierre1'], 
                            data['Estado'],
                            data['DiasCierreLicitacion'],
                            data['Informada'],
                            data['CodigoTipo'],
                            data['TipoConvocatoria'],
                            data['Etapas'], 
                            data['EstadoEtapas'],
                            data['TomaRazon'],
                            data['EstadoPublicidadOfertas'],
                            data['JustificacionPublicidad'],
                            data['Contrato'],
                            data['Obras'],
                            data['CantidadReclamos'],
                            data['FechaCreacion'],
                            data['FechaCierre2'],
                            data['FechaInicio'],
                            data['FechaFinal'],
                            data['FechaPubRespuestas'],
                            data['FechaActoAperturaTecnica'],
                            data['FechaActoAperturaEconomica'],
                            data['FechaPublicacion'],
                            data['FechaAdjudicacion'],
                            data['FechaEstimadaAdjudicacion'], 
                            data['FechaSoporteFisico'], 
                            data['FechaTiempoEvaluacion'],
                            data['FechaEstimadaFirma'], 
                            data['FechaUsuario'],
                            data['FechaVisitaTerreno'],
                            data['FechaEntregaAntecedentes'],
                            data['UnidadTiempoEvaluacion'],
                            data['DireccionVisita'],
                            data['DireccionEntrega'],
                            data['Estimacion'],
                            data['FuenteFinanciamiento'],
                            data['VisibilidadMonto'],
                            data['MontoEstimado'],
                            data['Tiempo'],
                            data['TipoPago'],
                            data['NombreResponsablePago'],
                            data['EmailResponsablePago'],
                            data['NombreResponsableContrato'],
                            data['EmailResponsableContrato'],
                            data['FonoResponsableContrato'],
                            data['ProhibicionContratacion'],
                            data['SubContratacion'],
                            data['TiempoDuracionContrato'],
                            data['JustificacionMontoEstimado'],
                            data['ObservacionContract'],
                            data['ExtensionPlazo'],
                            data['EsBaseTipo'],
                            data['UnidadTiempoContratoLicitacion'],
                            data['ValorTiempoRenovacion'],
                            data['PeriodoTiempoRenovacion'],
                            data['EsRenovable'],
                            data['Items_Cantidad'],
                            data['Comprador_CodigoUsuario'],
                            data['Comprador_RutUsuario'],
                            data['Comprador_NombreUsuario'],
                            data['Comprador_CargoUsuario'],
                            data['Adjudicacion_Numero'], # adjudicacion_id
                            data['Tipo'], # tipo_licitacion_id
                            data['UnidadTiempoEvaluacion'], # uni_tiempo_ev_id
                            data['Moneda'], # unidad_monetaria_id
                            data['VisibilidadMonto'], # monto_estimado_id
                            data['UnidadTiempoContratoLicitacion'], # uni_tiempo_con_id
                            data['Modalidad'], # modalidad_pago_id
                            data['Comprador_CodigoUnidad'] # UnidadCompra_codigoUnidad
                        )

                        _logger.info(f"Los datos de la licitacion ID: {id} se han recopilado exitosamente.")

                        count += 1
                else:
                    _logger.info(f"Error al realizar la solicitud a la API para la ID: {id}. Código de Estado: {response.status_code} : {response.reason}")
                    count += 1

                # Esperar 2 segundos entre cada solicitud para evitar errores
                time.sleep(2)

        except KeyboardInterrupt:
            # Capturar la señal de "Ctrl + C" para detener la ejecución
            _logger.info("Se ha detenido la ejecución. Guardando los datos recopilados hasta ahora en la base de datos.")

    # VERIFICAR UTILIDAD (?)
    def licitaciones_semana_anterior (self):
        ''' Esta función debe buscar todos los códigos externos o id's de licitaciones que se hayan agregado la semana pasada (en el contexto de que el calculo del ranking
        se haga de forma semanal, por ejemplo cada lunes.)
        Retornara la lista de aquellas licitaciones'''
        # Obtener la fecha de hoy
        fecha_actual = datetime.date.today()

        # Calcular la fecha del lunes de la semana anterior
        delta_dias = (fecha_actual.weekday()) % 7  # 0 para lunes, 1 para martes, ..., 6 para domingo
        fecha_lunes_semana_anterior = fecha_actual - datetime.timedelta(days=delta_dias, weeks=1)

        # Calcular la fecha del domingo de la semana anterior
        fecha_domingo_semana_anterior = fecha_lunes_semana_anterior + datetime.timedelta(days=6)

        '''
            TODO Falta por agregar la lógica que busque todas aquellas licitaciones que X variable de fecha este dentro de lunes-domingo semana anterior y la agregue a un listado
            luego debera retornar ese listado (ya sea de id's o de codigo_externo) 
        '''

    def calculo_rankingv1(self):
        '''
        Función que calcula el ranking para los 20 primeros rut_unidad de la vista RANKING_V1.
        Primero, limpia todos los registros para el campo ranking en la tabla UnidadCompra.
        Segundo, crea una lista con los rut_unidad en la vista RANKING_V1.
        Tercero, recorre esa lista y para los primeros 20 elementos asigna de forma secuencial el ranking.
        '''
        _logger.info('''\n\n\n>>> Ejecutando CRON Licibot: Calculo Ranking_V1 <<<\n\n\n''')

        # Limpiar todos los valores del campo "ranking" en el modelo UnidadCompra
        self.env.cr.execute("UPDATE licibot_unidad_compra SET ranking = NULL;")

        # Recuperar la lista de rut_unidad de la vista RANKING_V1
        ranking_length = int(self.env['ir.config_parameter'].sudo().get_param('licibot_module.ranking_length'))
        _logger.info(ranking_length)
        _logger.info(type(ranking_length))
        self.env.cr.execute(f'SELECT "ID Unidad de Compra" FROM RANKING_V1 LIMIT {ranking_length};')
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

        _logger.info('''\n\n\n>>> Finalizando CRON Licibot: Calculo Ranking_v1 <<<\n\n\n''')

    def get_fecha_actual(self):
        fecha_actual = fields.Date.today()
        return fecha_actual

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

    def ml_model(self):
        _logger.info('''\n\n\n>>> Ejecutando CRON Licibot: ML Model K-Means <<<\n\n\n''')

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
        df = pd.DataFrame(query_result, columns=["idunidad", "licitacionestotales", "totalgastado", "gasto2022", "diferenciaanterior2023", "proveedores2022", "proveedores2023", "competenciaotros", "valorpromediocompra", "cantidadtrabajadores", "clientenuevo"])

        _logger.info('''\n\n\n
        Imprime DF head 10:
        %s
        \n\n\n
        ''', df.head(10))

        # Replicando el Componente Principal de Análisis (PCA) 
        scaler = StandardScaler()
        scaler.fit(df)
        scaled_df = pd.DataFrame(scaler.transform(df),columns= df.columns)
        _logger.info("All features are now scaled ...")

        pca = PCA(n_components=3)
        pca.fit(scaled_df)
        PCA_df = pd.DataFrame(pca.transform(scaled_df), columns=(["col1","col2", "col3"]))
        _logger.info('''\n\n\n
        Describing PCA:
        %s
        \n\n\n
        ''', PCA_df.describe().T)

        kmeans_pca = KMeans(n_clusters = 4, init = 'k-means++', random_state = 42)
        kmeans_pca.fit(PCA_df)
        _logger.info('PCA kmeans calculated? ... OK')

        df_segm_pca_kmeans = pd.concat([df.reset_index(drop = True), pd.DataFrame(PCA_df)], axis = 1)
        df_segm_pca_kmeans.columns.values[-3: ] = ['col1', 'col2', 'col3']

        df_segm_pca_kmeans['Segment K-means PCA'] = kmeans_pca.labels_
        _logger.info('''\n\n\n
        Showing dataframe segment pca kmeans ...:
        %s
        \n\n\n
        ''', df_segm_pca_kmeans.iloc[:, :5])

        _logger.info('''\n\n\n
        Showing dataframe segment pca kmeans INFO ...:
        %s
        \n\n\n
        ''', df_segm_pca_kmeans.info(verbose=True))

        df_last_3_columns = df_segm_pca_kmeans.iloc[:, -4:]

        _logger.info('''\n\n\n
        Showing dataframe last 4 columns ...:
        %s
        \n\n\n
        ''', df_last_3_columns.head(25))

        # Analisis de clusters
        # _logger.info('''
        # \n\n\n
        # > > > Clusters analisis < < <
        # \n\n\n
        # ''')

        # selected_columns = df_segm_pca_kmeans[['nombre_unidad', 'competencia_otros', 'Segment K-means PCA']]
        # _logger.info('''\n\n\n
        # Showing Selected Columns ...:
        # %s
        # \n\n\n
        # ''', selected_columns.head(25))

        # analisiscluster = df_segm_pca_kmeans[(df_segm_pca_kmeans["Segment K-means PCA"] == 0)]
        # _logger.info('''\n\n\n
        # Showing Clusters 0 Analisis ...:
        # %s
        # \n\n\n
        # ''', analisiscluster.head(50))

        # analisiscluster = df_segm_pca_kmeans[(df_segm_pca_kmeans["Segment K-means PCA"] == 1)]
        # _logger.info('''\n\n\n
        # Showing Clusters 1 Analisis ...:
        # %s
        # \n\n\n
        # ''', analisiscluster.head(50))

        # analisiscluster = df_segm_pca_kmeans[(df_segm_pca_kmeans["Segment K-means PCA"] == 2)]
        # _logger.info('''\n\n\n
        # Showing Clusters 2 Analisis ...:
        # %s
        # \n\n\n
        # ''', analisiscluster.head(50))

        # analisiscluster = df_segm_pca_kmeans[(df_segm_pca_kmeans["Segment K-means PCA"] == 3)]
        # _logger.info('''\n\n\n
        # Showing Clusters 3 Analisis ...:
        # %s
        # \n\n\n
        # ''', analisiscluster.head(50))

        # pickle.dump(kmeans_pca, open('opt/addons_opens/licibot_module/Inputs/kmeans_pca_odoo.sav', 'wb'))
        
        # Generar una predicción utilizando el modelo desde el archivo .sav.
        # pred = kmeans_pca.predict(PCA_df)
        # df['Segment K-means PCA'] = pred

        # Sobreescribir la información de la predicción en la base de datos.

        # Generar los clusters.

        # Rankear los Clusters de interes (0 y 2)

        # Asignar una "marca" a las unidades de compra rankeadas

        _logger.info('''\n\n\n>>> Finalizando CRON Licibot: ML Model K-Means <<<\n\n\n''')

    def easter_egg(self):
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
        _logger.info(f'ol_crm_get_token: {response.status_code}')

        if response.status_code == 200:
            data = response.json() 
            token = data["token"]
            _logger.info(f'ol_crm_get_token: {token}')
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
        '''Función que buscará en la base de datos las licitaciones de la semana anterior. Si algúna de ellas pertenece a una unidad de compra rankeada (20 puestos)
        será enviada su información al CRM de Odoo'''

        # Si el token esta activo realizar proceso, si el token venció pedir nuevo token (?)
        token_crm = self.ol_crm_get_token()

        url = 'http://173.255.243.74:8069/licitaciones'
        headers = {'Authorization': token}
        response = requests.post(url, headers=headers, json=json)

        '''
            ///////////////////////////////////////////////////////////////////////////////////
                 ////     ////       W O R K    I N    P R O G R E S S   ////    ////    ////
            ///////////////////////////////////////////////////////////////////////////////////
        '''

    def ol_crm_send_info_provisoria (self):
        '''De momento dado que la api de mercadopublico sigue caída lo que se quiere es que teniendo en consideración el ranking, se busque y se envie al CRM
        la información de la última licitación registrada en la base de datos para cada una de esas unidades de compra dentro del ranking (20 en total)'''

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
            # _logger.info(f"# # # # Tipo fecha_actual: {type(fecha_actual)} Valor {fecha_actual} # # # # ")
            diff_dias_permitidos = int(self.env['ir.config_parameter'].sudo().get_param('licibot_module.days_gone'))

            # Cuando exista la fecha de ultima oportunidad la calcula, caso contrario asigna un valor a la diff_real para entender que no existen registros de esa unidad de compra
            if fecha_ultima_oportunidad:
                # _logger.info(f"# # # # Tipo fecha ultima oportunidad: {type(fecha_ultima_oportunidad)} Valor {fecha_ultima_oportunidad} # # # # ")
                fecha_ultima_oportunidad = datetime.date(fecha_ultima_oportunidad[0].year, fecha_ultima_oportunidad[0].month, fecha_ultima_oportunidad[0].day)
                # _logger.info(f"# # # # Tipo fecha ultima oportunidad (DESPUES): {type(fecha_ultima_oportunidad)} Valor {fecha_ultima_oportunidad} # # # # ")
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
                
                # _logger.info(f"Respuesta de API CRM: Código {response.status_code}")

        _logger.info('''\n\n\n>>> Finalizando CRON Licibot: Envío al CRM <<<\n\n\n''')

class ProductoServicio (models.Model):
    _name = 'licibot.producto.servicio'

    # id_producto_servicio = fields.Integer(string = 'ID Producto Servicio')
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
        CREATE OR REPLACE VIEW ranking_v1 AS
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

        tools.drop_view_if_exists(self._cr, 'ranking_v1')
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
