# -*- coding: utf-8 -*-
{
    'name': 'Licibot',
    'summary': 'Recolector de licitaciones',
    'description': '''
        Módulo que envía peticiones a la api de mercadopublico.cl he ingresa la información recopilada de las licitaciones en la base de datos.
        
        Adicionalmente, permite 'rankear' a las unidades de compra según ciertos criterios.
    ''',
    'author': 'Daniel V., Ricardo A., Esteban S., Nicolas P.',
    'version': '0.1.0',
    'website': '',
    'depends': ['crm', 'opens_licitacion_crm'],
    'external_dependencies': {'python': ['pandas', 'requests', 'numpy', 'scipy']},
    'license': 'OPL-1',
    'data': [
        'data/crones_licibot.xml',
        'data/config_parameters.xml'
    ],
    'active': True,
    'installable': True,
    'application': False,
    'auto_install': False,
}