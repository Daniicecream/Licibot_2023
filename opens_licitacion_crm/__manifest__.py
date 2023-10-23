# -*- coding: utf-8 -*-
{
    'name': 'Licitaciones en Iniciativas y Oportunidades',
    'version': '1.0.0',
    'author': 'Open Solutions',
    'description': """
    """,
    'website': 'https://www.opens.cl',
    'depends': ['crm'],
    'license': 'OPL-1',
    'data': [
        'security/ir.model.access.csv',
        'views/crm.xml',
        'views/portal.xml',
        'views/type.xml',
        'views/activity.xml',
        'views/status.xml',
        'views/format.xml',
        'views/bidding.xml',
        'views/timeline.xml',
        'views/anexxes.xml',
        'views/menuitems.xml',
        'data/parameters.xml',
        ],
    'active': True,
    'installable': True,
    'application': False,
    'auto_install': False,
}