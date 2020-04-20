# -*- coding: utf-8 -*-
{
    'name': 'Partner Tweaks. Limit Restrict Configure Partner Contact Access Easily',
    'version': '12.0.1.0',
    'author': 'Cetmix, Ivan Sokolov',
    'category': 'Discuss',
    'license': 'LGPL-3',
    'website': 'https://demo.cetmix.com',
    'live_test_url': 'https://demo.cetmix.com',
    'summary': """Limit Restrict Configure Partner Contact Access""",
    'description': """
    Configurable access rules for Partners / Contacts 
""",
    'depends': ['base'],
    'images': ['static/description/banner.png'],
    'data': [
        'security/rules.xml',
        'views/prt_users.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'uninstall_hook': "restore_access_rules",
}
