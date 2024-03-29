# Copyright 2016 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2018 Dinar Gabbasov <https://it-projects.info/team/GabbasovDinar>
# Copyright 2021 Denis Mudarisov <https://github.com/trojikman>
# License MIT (https://opensource.org/licenses/MIT).
{
    "name": """Brand kit""",
    "summary": """Brand your odoo instance in few clicks""",
    "category": "Debranding",
    "images": ["images/brandkit.png"],
    "version": "12.0.2.0.0",
    "application": False,
    "author": "IT-Projects LLC, Ivan Yelizariev",
    "website": "https://itpp.dev",
    "license": "Other OSI approved licence",  # MIT
    "price": 50.00,
    "currency": "EUR",
    "depends": ["web_debranding", "web_login_background", "web_widget_colorpicker"],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "security/ir.model.access.csv",
        "views/ir_attachment.xml",
        "views/templates.xml",
        "views/res_config.xml",
        "views/theme.xml",
        "data/theme_data.xml",
    ],
    "qweb": [],
    "demo": [],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "auto_install": False,
    "installable": True,
    "demo_title": "Brand kit",
    "demo_addons": ["web_debranding", "web_login_background"],
    "demo_addons_hidden": [],
    "demo_url": "theme-kit",
    "demo_summary": "Brand your odoo instance in few clicks.",
    "demo_images": ["images/brandkit.png"],
}
