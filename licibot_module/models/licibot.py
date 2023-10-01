# Importando librerías Odoo (?)
from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError
import logging

# Importando librerías externas
import requests 
import time
import datetime
import pandas as pd

_logger = logging.getLogger(__name__)

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
    
    def insertar_organismo (self, codigo_organismo, nombre_organismo):
 
        if codigo_organismo is not None:
            organismo_exists = self.env['licibot.organismo'].sudo().search([('codigo_organismo', '=', codigo_organismo)])
            
            if organismo_exists:
                _logger.info(f"El organismo {codigo_organismo}:{nombre_organismo}, ya existe en la base de datos")
            else:
                self.env['licibot.organismo'].sudo().create({'id': codigo_organismo, 'nombre_organismo': nombre_organismo})

        else:
            _logger.info(f"!!! Código organismo nulo. Omitiendo inserción de datos en tabla organismo...")

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

    def insertar_adjudicacion(self, num_admin_adjudicacion, fecha_admin_adjudicacion, num_oferentes, url_acta, tipo_acto_admn_id):

        self.env['licibot.adjudicacion'].sudo().create({
            'num_admin_adjudicacion': numeroAdmAdjudicacion,
            'fecha_admin_adjudicacion': fechaAdmAdjudicacion,
            'num_oferentes': numeroOferentes,
            'url_acta': urlActa,
            'tipo_acto_admin_id': self.is_null_int(tipo_acto_admn_id),
        })

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

        # Llamada del objeto res_config_settings que almacena el token de mp
        res_config_settings = self.env['res.config.settings'].sudo()

        try:
            # Recorrer los elementos almacenados en la lista de ids de licitaciones
            for id in ids:

                # Realizar petición de datos para la ID de licitación
                url = 'https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json'
                args = {'codigo': id, 'ticket': res_config_settings.get_param('token_api_mp')}
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
                            data['Adjudicacion_Tipo'] # tipo_acto_admn_id
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

    def licitaciones_semana_anterior (self):
        ''' Esta función debe buscar todos los códigos externos o id's de licitaciones que se hayan agregado la semana pasada (en el contexto de que el calculo del ranking
        se haga de forma semanal, por ejemplo cada lunes.)
        Retornara la lista de aquellas licitaciones'''
        # Obtener la fecha de hoy
        fecha_actual = datetime.date.today()
        print(f"fecha_actual: {fecha_actual}")

        # Calcular la fecha del lunes de la semana anterior
        delta_dias = (fecha_actual.weekday()) % 7  # 0 para lunes, 1 para martes, ..., 6 para domingo
        print(f"delta_dias: {delta_dias}")
        fecha_lunes_semana_anterior = fecha_actual - datetime.timedelta(days=delta_dias, weeks=1)
        print(f"fecha_lunes_semana_anterior: {fecha_lunes_semana_anterior}")

        # Calcular la fecha del domingo de la semana anterior
        fecha_domingo_semana_anterior = fecha_lunes_semana_anterior + datetime.timedelta(days=6)
        print(f"fecha_domingo_semana_anterior: {fecha_domingo_semana_anterior}")

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

        # Limpiar todos los valores del campo "ranking" en el modelo UnidadCompra
        self.env.cr.execute("UPDATE licibot_unidad_compra SET ranking = NULL;")

        # Recuperar la lista de rut_unidad de la vista RANKING_V1
        self.env.cr.execute('SELECT "ID Unidad de Compra" FROM RANKING_V1;')
        id_unidad_list = list(line[0] for line in self.env.cr.fetchall())

        # Inicializar el contador de ranking
        pos_ranking = 1

        # Recorrer los primeros 20 elementos de la lista
        for id_unidad in id_unidad_list[:20]:

            # Buscar y actualizar el campo "ranking" en el modelo UnidadCompra
            unidad_compra = self.env['licibot.unidad.compra'].sudo().search([('id', '=', id_unidad)])
            unidad_compra.sudo().write({'ranking': pos_ranking})
            
            # Incrementar el contador de ranking para el siguiente valor
            pos_ranking += 1

    """
    =================================================================
                        FUNCIONES PARA EL CRM
    =================================================================
    """

    def ol_crm_get_token (self):
        '''Función que retorna el token de acceso necesario para utilizar la api del crm'''

        url = 'http://173.255.243.74:8069/token'
        response = requests.get(url)

        if response.status_code == 200:
            token = response.text 
            _logger.info(f"\n TOKEN {token}")
            return token
        else:
            _logger.error(f"\n Error al obtener el token. Código de estado: {response.status_code}")
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

        _logger.info("-" * 50)
        _logger.info("CRON CRM")
        _logger.info("-" * 50)
        # Listar las id de unidades de compra de la vista RANKING_V1
        self.env.cr.execute('SELECT "ID Unidad de Compra" FROM RANKING_V1;')
        id_unidad_list = list(line[0] for line in self.env.cr.fetchall())

        n = 1

        token = self.ol_crm_get_token()
        _logger.info(f"\n TOKEN {token}")

        for id_unidad in id_unidad_list[:20]:
            query = f'''
            SELECT  
                licibot_unidad_compra.id, 
                licibot_licitacion.codigo_externo,
                licibot_licitacion.nombre,
                licibot_tipo_licitacion.id,
                licibot_tipo_licitacion.id_tipo_licitacion,
                licibot_licitacion.descripcion,
                licibot_licitacion.nom_contacto,
                licibot_licitacion.cargo_contacto,
                CASE 
                    WHEN licibot_licitacion.fecha_cierre_1 IS NULL THEN TO_CHAR(licibot_licitacion.fecha_cierre_2,'YYYY-MM-DD')
                    ELSE TO_CHAR(licibot_licitacion.fecha_cierre_1,'YYYY-MM-DD') 
                END AS fecha_cierre,
                licibot_unidad_compra.ranking
            FROM licibot_unidad_compra 
            JOIN licibot_licitacion ON licibot_unidad_compra.id = licibot_licitacion.unidad_compra_id 
            JOIN licibot_tipo_licitacion ON licibot_licitacion.tipo_licitacion_id = licibot_tipo_licitacion.id
            WHERE licibot_unidad_compra.id = {id_unidad} 
            AND licibot_licitacion.fecha_creacion = (
                SELECT MAX(fecha_creacion) FROM licibot_unidad_compra 
                JOIN licibot_licitacion ON licibot_unidad_compra.id = licibot_licitacion.unidad_compra_id 
                WHERE licibot_unidad_compra.id = {id_unidad}
            );
            '''
            _logger.info(f"\n Licitación {n}")

            self.env.cr.execute(query)
            resultado = self.env.cr.fetchone()
            _logger.info(f"""\n Resultado = (Codigo Externo = {resultado[1]}, 
            Nombre Licitacion = {resultado[2]}, 
            Tipo Licitacion = {resultado[4]}, 
            Descripcion = {resultado[5]}, 
            Nombre Contacto = {resultado[6]}, 
            Cargo Contacto = {resultado[7]}, 
            Fecha Cierre = {resultado[8]})""")
            
            json = self.ol_crm_craft_json(resultado[1], resultado[2], resultado[4], resultado[5], resultado[6], resultado[7], resultado[8])
            '''
            BUG Campo Descripción demaciado extenso
            ERROR: index row size 3168 exceeds maximum 2712 for index "crm_lead_name_index"
            HINT:  Values larger than 1/3 of a buffer page cannot be indexed.
            Consider a function index of an MD5 hash of the value, or use full text indexing.
            '''
            
            url = 'http://173.255.243.74:8069/licitaciones'
            headers = {'Authorization': token}
            response = requests.post(url, headers=headers, json=json)
            
            _logger.info(f"Respuesta de API CRM: Código {response.status_code}")
            n += 1

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

    @api.model_cr
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
