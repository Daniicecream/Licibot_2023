# Licitaciones en Iniciativas y Oportunidades


* Este módulo añade nuevo campo booleando a modelo de Iniciativas (crm.lead) el cual permite marca una iniciativa como Licitación.
* Si el check está activado, se desplegarán 5 nuevas pestañas: **Datos licitación**, **Contacto licitación**, **Cronograma licitación**, **Anexos licitación**. Los cuales permiten registrar nuevos datos al modelo.
* Al realizar la conversión a Oportunidad, estos datos también son trapasados al nuevo registro.
* Se añaden nuevos menús:
* **CRM** -> **Ventas** -> [*Licitaciones*, *Cronograma Licitaciones*, *Anexos Licitaciones*].
* **CRM** -> **Configuración** -> **Licitación** -> [*Portal Licitación*, *Tipo Licitación*, *Actividad Licitación*, *Status Licitación*, *Formato Licitación*]

# Uso de API

## Generar Token

* Realizar petición GET a la ruta *http://<ip_servidor>:8069/token*

## Envío Licitaciones

* El módulo está diseñado también para recibir datos JSON y cargarlos al modelo **crm.lead**.
* Se realiza petición POST a la ruta *http://<ip_servidor>:8069/licitaciones*
* El formato a recibir es el siguiente:

`` 
{
  "licitaciones": [{
    "CodigoExterno": "1509-5-L114",
    "Tipo": "L1",
    "Nombre": "Insumos Medicos y Medicamentos ",
    "Descripcion": "se requiere la compra de insumos y medicamentos para la unidad de urgencia y unidad de Hospitalizados del establecimiento de salud.",
    "NombreUsuario": "Joycie   Valle Chacon",
    "CargoUsuario": "Contabilidad",
    "FechaCierre": null,
  }]
}
``

* En los headers de la petición, se debe incluir **Authorization: <token>**

# Configuración

#. En **Parámetros del sistema** se debe declarar las horas de duración de los token a generar. Por defecto viene en 1 hora. (valor del parámetro debe ser número entero)


# Creditos

* Opens Solutions

# Dependencias

* crm