# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'ownerp Backend UI',
    'license': 'AGPL-3',
    'version': '1.0.41',
    'description': "Easy configurable Backend Theme",
    'author': 'Equitania Software GmbH',
    'website': 'https://www.ownerp.com',
    'depends': ['base_setup','web'],
    'images': [
        'images/main_1.png',
	    'images/main_screenshot.png',
	],
    'category': 'Theme/Backend',
    'summary': 'Choose your colors for Backend',

    'data': [
        "data/default_parameters.xml",
        "views/assets.xml",
        "views/templates.xml",
        "views/eq_res_users.xml",
        "views/eq_template_colors.xml",
        'views/sidebar.xml'
    ],
    'qweb': [
        'static/src/xml/navigation.xml',
        'static/src/xml/form_view.xml',
        'static/src/xml/navbar.xml'
    ],
    'demo': [],
    'css': ['base.css'],
    'installable': True,
    'auto_install': False,
}