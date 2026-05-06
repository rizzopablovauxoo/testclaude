{
    'name': 'ICQ Partner Field',
    'version': '19.0.1.0.0',
    'summary': 'Add ICQ field to res.partner',
    'description': 'Adds an optional ICQ field to res.partner with validation.',
    'author': 'Test Writer',
    'depends': ['base'],
    'data': [
        'views/res_partner_views.xml',
    ],
    'test': True,
    'installable': True,
}
