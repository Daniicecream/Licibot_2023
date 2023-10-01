# -*- coding: utf-8 -*-
{
    'name': 'Licibot',
    'summary': 'Recolector de licitaciones',
    'description': '''
        Módulo que envía peticiones a la api de mercadopublico.cl he ingresa la información recopilada de las licitaciones en la base de datos.
        
        Adicionalmente, permite 'rankear' a las unidades de compra según ciertos criterios.
    ''',
    'author': 'Daniel V., Ricardo A., Esteban S.',
    'version': '1.0',
    'website': '',
    'depends': ['crm', 'opens_licitacion_crm'],
    'external_dependencies': {'python': ['pandas', 'requests']},
    'license': 'OPL-1',
    'data': [
        'data/crones_licibot.xml'
    ],
    'active': True,
    'installable': True,
    'application': False,
    'auto_install': False,
}