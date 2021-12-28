# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api, _
import base64

class EqTemplateColors(models.TransientModel):
    _name = "eq.template.colors"
    _description = 'Color Picker'

    SCSS_TEMPLATE = """
    
        .eq_old_icons {{ 
            display: {eq_old_icons};
        }}
        
        .eq_new_icons {{ 
            display: {eq_new_icons};
        }}
        
        #app-sidebar {{
            display: {app_sidebar};
        }}
        
        @if {eq_show_sidebar_names} {{
            .app-sidebar-panel:hover {{
                overflow-y: auto;
                -ms-flex: 0 0 150px;
                -moz-flex: 0 0 150px;
                -webkit-box-flex: 0;
                -webkit-flex: 0 0 150px;
                flex: 0 0 150px;
            }}
            .app-sidebar-panel:hover .eq_sidebar_title {{
                display: inline-block;
                overflow: hidden;
                text-overflow: ellipsis;
                max-width: 90px;
                margin-left: 5px;
                vertical-align: -moz-middle-with-baseline;
                vertical-align: -webkit-baseline-middle;
            }}
            .app-sidebar-panel .eq_new_icons,
            .app-sidebar-panel .eq_old_icons {{
                width: 34px;
                float: left;
            }}
        }}
        
        body {{
             color: {eq_basic_text_color};
           }}
           
        body a,
        .o_form_view .o_form_uri,
        .o_form_view .oe_button_box .oe_stat_button .o_button_icon {{
            color: {eq_link_color};
        }}
        
        .o_list_view .text-info {{
            color: {eq_link_color} !important;
        }}
        
        body a:hover,
        .o_form_view .o_form_uri:hover,
        .o_form_view .oe_button_box .oe_stat_button .o_button_icon:hover {{
            color: darken({eq_link_color},20%);
        }}
    
        .o_main_navbar {{
             background-color: {eq_navi_background} !important;
           }}

        .o_main_navbar > ul > li > a,
        .o_main_navbar > ul > li > label,
        .o_main_navbar > .o_menu_brand {{
            color: {eq_navi_fontcolor} !important;
           }}
            
        .o_main_navbar > ul > li > a:hover,
        .o_main_navbar > ul > li > label:hover,
        .o_main_navbar > a:hover, .o_main_navbar > a:focus,
        .o_main_navbar > button:hover, .o_main_navbar > button:focus,
        .o_main_navbar > ul > li.o_extra_menu_items.show > ul > li > a.dropdown-toggle,
        .o_main_navbar .show .dropdown-toggle,
        .navbar-default .navbar-nav > .active > a,
        .navbar-default .navbar-nav > .active > a:hover,
        .navbar-default .navbar-nav > .active > a:focus,
        .navbar-default .navbar-nav > .open > a,
        .navbar-default .navbar-nav > .open > a:hover,
        .navbar-default .navbar-nav > .open > a:focus {{
            background-color: {eq_navi_hover};
            color: {eq_navi_hover_fontcolor} !important;
        }}
        
        .o_menu_apps .dropdown-menu a.o_app i.o-app-icon,
        #sidebar .eq_new_icons i.o-app-icon {{
            color:{eq_apps_color};
        }}
      
        .text-muted {{
            color: {eq_basic_secondary_color} !important;
        }}
        
        .btn-primary {{
            color: {eq_btn_primary_fontcolor};
            background-color: {eq_btn_primary_background};
        }}
        .btn-primary:hover,
        .btn-primary:focus,
        .btn-primary.focus,
        .btn-primary:not(:disabled):not(.disabled):active,
        .btn-primary:not(:disabled):not(.disabled).active,
        .show > .btn-primary.dropdown-toggle {{
            color: {eq_btn_primary_fontcolor};
              background-color: darken({eq_btn_primary_background},10%);
        }}
        
        .btn-secondary {{
            color: {eq_btn_secondary_fontcolor};
            background-color: {eq_btn_secondary_background};
        }}
        .btn-secondary:hover,
        .btn-secondary:focus,
        .btn-secondary.focus,
        .btn-secondary:not(:disabled):not(.disabled):active,
        .btn-secondary:not(:disabled):not(.disabled).active,
        .show > .btn-secondary.dropdown-toggle {{
            color: {eq_btn_secondary_fontcolor};
            background-color: darken({eq_btn_secondary_background},10%);
        }}
        
        @if {eq_show_notification_right} {{
            .o_form_view .o_form_sheet_bg {{
                position: relative;
            }}
            
            .o_form_view > .oe_chatter {{
                -webkit-box-flex: 0;
                -webkit-flex: 1000 0 auto;
                flex: 1000 0 auto;
                width: 100%;
                min-width: auto;
                padding-right: 16px;
                padding-left: 16px;
                margin-right: auto;
                margin-left: auto;
                padding: 8px 0;
            }}
            
            @media (max-width: 575px) {{ /* fix for small devices at table columns such as contact view */
                .o_form_view .o_group .o_group_col_6 {{
                    width: 100%;
                }}
            }}
            
            @media (min-width: 576px) {{ .o_form_view > .oe_chatter {{ max-width: 540px; }} }}
            @media (min-width: 768px) {{ .o_form_view > .oe_chatter {{ max-width: 720px; }} }}
            @media (min-width: 992px) {{ .o_form_view > .oe_chatter {{ max-width: 960px; }} }}
            @media (min-width: 1200px) {{ .o_form_view > .oe_chatter {{ max-width: 1140px; }} }}
            
            @media (min-width: 768px) {{
                .o_form_view {{
                    display: -webkit-box;
                    display: -webkit-flex;
                    display: flex;
                    -webkit-flex-flow: column nowrap;
                    flex-flow: column nowrap;
                    min-height: 100%;
                }}
            }}
            
            @media (min-width: 1534px) {{
            
                .o_form_view {{
                    -webkit-flex-flow: row nowrap;
                    flex-flow: row nowrap;
                    height: 100%;
                }}
            
                .o_form_view > .o_form_sheet_bg {{
                    -webkit-box-flex: 1;
                    -webkit-flex: 1 1 auto;
                    flex: 1 1 auto;
                    width: 1022px;
                    padding: 0 16px;
                    overflow: auto;
                    border-bottom: none;
                }}
            
                .o_form_view > .oe_chatter {{
                    -webkit-box-flex: 1;
                    -webkit-flex: 1 1 auto;
                    flex: 1 1 auto;
                    width: 530px;
                    padding: 0;
                    overflow: auto;
                    border-left: 1px solid #dee2e6;
                    background-color: white;
                }}
            }}
        }}
        
        @else {{
            
        }}
        
        
        
    """

    URL = '/eq_ownerp_ui/static/src/scss/eq_backend_gen_colors.scss'


    name = fields.Char(string="Name", default="Template Colors")
    eq_navi_background = fields.Char(string="Navigation Background")
    eq_navi_fontcolor = fields.Char(string="Navigation Fontcolor")
    eq_navi_hover = fields.Char(string="Navigation Hover Background")
    eq_navi_hover_fontcolor = fields.Char(string="Navigation Hover Font")
    eq_apps_color = fields.Char(string="App-Icon Color")
    eq_link_color = fields.Char(string="Link Color")
    eq_basic_text_color = fields.Char(string="Basic Text Color")
    eq_basic_secondary_color = fields.Char(string="Basic Secondary Color")
    eq_btn_primary_background = fields.Char(string="Primary Button Backgroundcolor")
    eq_btn_primary_fontcolor = fields.Char(string="Primary Button Fontcolor")
    eq_btn_secondary_background = fields.Char(string="Secondary Button Backgroundcolor")
    eq_btn_secondary_fontcolor = fields.Char(string="Secondary Button Fontcolor")
    eq_original_icons = fields.Boolean(string="Use original Icons")
    eq_show_sidebar = fields.Boolean(string="Show Sidebar")
    eq_show_sidebar_names = fields.Boolean(string="Show Sidebar Names")
    eq_show_notification_right = fields.Boolean(string="Show Notification Right")

    @api.multi
    def execute(self):
        self.env['ir.config_parameter'].set_param("eq_navi_background", self.eq_navi_background)
        self.env['ir.config_parameter'].set_param("eq_navi_fontcolor", self.eq_navi_fontcolor)
        self.env['ir.config_parameter'].set_param("eq_navi_hover", self.eq_navi_hover)
        self.env['ir.config_parameter'].set_param("eq_navi_hover_fontcolor", self.eq_navi_hover_fontcolor)
        self.env['ir.config_parameter'].set_param("eq_apps_color", self.eq_apps_color)
        self.env['ir.config_parameter'].set_param("eq_basic_text_color", self.eq_basic_text_color)
        self.env['ir.config_parameter'].set_param("eq_basic_secondary_color", self.eq_basic_secondary_color)
        self.env['ir.config_parameter'].set_param("eq_link_color", self.eq_link_color)
        self.env['ir.config_parameter'].set_param("eq_btn_primary_background", self.eq_btn_primary_background)
        self.env['ir.config_parameter'].set_param("eq_btn_primary_fontcolor", self.eq_btn_primary_fontcolor)
        self.env['ir.config_parameter'].set_param("eq_btn_secondary_background", self.eq_btn_secondary_background)
        self.env['ir.config_parameter'].set_param("eq_btn_secondary_fontcolor", self.eq_btn_secondary_fontcolor)
        self.env['ir.config_parameter'].set_param("eq_original_icons", self.eq_original_icons)
        self.env['ir.config_parameter'].set_param("eq_show_sidebar", self.eq_show_sidebar)
        self.env['ir.config_parameter'].set_param("eq_show_sidebar_names", self.eq_show_sidebar_names)
        self.env['ir.config_parameter'].set_param("eq_show_notification_right", self.eq_show_notification_right)
        self.scss_create_or_update_attachment()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    @api.multi
    def reset_default(self):
        self.env['ir.config_parameter'].set_param("eq_navi_background", '#374D8B')
        self.eq_navi_background = '#374D8B'
        self.env['ir.config_parameter'].set_param("eq_navi_fontcolor", '#FFFFFF')
        self.eq_navi_fontcolor = '#FFFFFF'
        self.env['ir.config_parameter'].set_param("eq_navi_hover", '#FFFFFF')
        self.eq_navi_hover = '#FFFFFF'
        self.env['ir.config_parameter'].set_param("eq_navi_hover_fontcolor", '#1E2C52')
        self.eq_navi_hover_fontcolor = '#1E2C52'
        self.env['ir.config_parameter'].set_param("eq_apps_color", '#374D8B')
        self.eq_apps_color = '#374D8B'
        self.env['ir.config_parameter'].set_param("eq_basic_text_color", '#141414')
        self.eq_basic_text_color = '#141414'
        self.env['ir.config_parameter'].set_param("eq_basic_secondary_color", '#858585')
        self.eq_basic_secondary_color = '#858585'
        self.env['ir.config_parameter'].set_param("eq_link_color", '#284DA3')
        self.eq_link_color = '#284DA3'
        self.env['ir.config_parameter'].set_param("eq_btn_primary_background", '#374D8B')
        self.eq_btn_primary_background = '#374D8B'
        self.env['ir.config_parameter'].set_param("eq_btn_primary_fontcolor", '#FFFFFF')
        self.eq_btn_primary_fontcolor = '#FFFFFF'
        self.env['ir.config_parameter'].set_param("eq_btn_secondary_background", '#CFCFCF')
        self.eq_btn_secondary_background = '#CFCFCF'
        self.env['ir.config_parameter'].set_param("eq_btn_secondary_fontcolor", '#212529')
        self.eq_btn_secondary_fontcolor = '#212529'
        self.scss_create_or_update_attachment()


    @api.model
    def default_get(self, fields):
        if self.env['ir.config_parameter'].get_param("eq_navi_background"):
            eq_navi_background = self.env['ir.config_parameter'].get_param("eq_navi_background")
        else:
            eq_navi_background = '#374D8B'
        if self.env['ir.config_parameter'].get_param("eq_navi_fontcolor"):
            eq_navi_fontcolor = self.env['ir.config_parameter'].get_param("eq_navi_fontcolor")
        else:
            eq_navi_fontcolor = '#FFFFFF'
        if self.env['ir.config_parameter'].get_param("eq_navi_hover"):
            eq_navi_hover = self.env['ir.config_parameter'].get_param("eq_navi_hover")
        else:
            eq_navi_hover = '#FFFFFF'
        if self.env['ir.config_parameter'].get_param("eq_navi_hover_fontcolor"):
            eq_navi_hover_fontcolor = self.env['ir.config_parameter'].get_param("eq_navi_hover_fontcolor")
        else:
            eq_navi_hover_fontcolor = '#1E2C52'
        if self.env['ir.config_parameter'].get_param("eq_apps_color"):
            eq_apps_color = self.env['ir.config_parameter'].get_param("eq_apps_color")
        else:
            eq_apps_color = '#374D8B'
        if self.env['ir.config_parameter'].get_param("eq_basic_text_color"):
            eq_basic_text_color = self.env['ir.config_parameter'].get_param("eq_basic_text_color")
        else:
            eq_basic_text_color = '#141414'
        if self.env['ir.config_parameter'].get_param("eq_basic_secondary_color"):
            eq_basic_secondary_color = self.env['ir.config_parameter'].get_param("eq_basic_secondary_color")
        else:
            eq_basic_secondary_color = '#858585'
        if self.env['ir.config_parameter'].get_param("eq_link_color"):
            eq_link_color = self.env['ir.config_parameter'].get_param("eq_link_color")
        else:
            eq_link_color = '#284DA3'
        if self.env['ir.config_parameter'].get_param("eq_btn_primary_background"):
            eq_btn_primary_background = self.env['ir.config_parameter'].get_param("eq_btn_primary_background")
        else:
            eq_btn_primary_background = '#374D8B'
        if self.env['ir.config_parameter'].get_param("eq_btn_primary_fontcolor"):
            eq_btn_primary_fontcolor = self.env['ir.config_parameter'].get_param("eq_btn_primary_fontcolor")
        else:
            eq_btn_primary_fontcolor = '#FFFFFF'
        if self.env['ir.config_parameter'].get_param("eq_btn_secondary_background"):
            eq_btn_secondary_background = self.env['ir.config_parameter'].get_param("eq_btn_secondary_background")
        else:
            eq_btn_secondary_background = '#CFCFCF'
        if self.env['ir.config_parameter'].get_param("eq_btn_secondary_fontcolor"):
            eq_btn_secondary_fontcolor = self.env['ir.config_parameter'].get_param("eq_btn_secondary_fontcolor")
        else:
            eq_btn_secondary_fontcolor = '#212529'
        eq_original_icons = self.env['ir.config_parameter'].get_param("eq_original_icons")
        eq_show_sidebar = self.env['ir.config_parameter'].get_param("eq_show_sidebar")
        eq_show_sidebar_names = self.env['ir.config_parameter'].get_param("eq_show_sidebar_names")
        eq_show_notification_right = self.env['ir.config_parameter'].get_param("eq_show_notification_right")
        res = {
            "eq_navi_background": eq_navi_background,
            "eq_navi_fontcolor": eq_navi_fontcolor,
            "eq_navi_hover": eq_navi_hover,
            "eq_navi_hover_fontcolor": eq_navi_hover_fontcolor,
            "eq_apps_color": eq_apps_color,
            "eq_basic_text_color": eq_basic_text_color,
            "eq_basic_secondary_color": eq_basic_secondary_color,
            "eq_link_color": eq_link_color,
            "eq_btn_primary_background": eq_btn_primary_background,
            "eq_btn_primary_fontcolor": eq_btn_primary_fontcolor,
            "eq_btn_secondary_background": eq_btn_secondary_background,
            "eq_btn_secondary_fontcolor": eq_btn_secondary_fontcolor,
            "eq_original_icons": eq_original_icons,
            "eq_show_sidebar": eq_show_sidebar,
            "eq_show_sidebar_names": eq_show_sidebar_names,
            "eq_show_notification_right": eq_show_notification_right
               }
        return res

    @api.multi
    def scss_create_or_update_attachment(self):
        IrAttachmentObj = self.env['ir.attachment']
        parameters = self.sudo().default_get([])
        eq_original_icons = parameters["eq_original_icons"]
        if eq_original_icons:
            eq_new_icons = "none"
            eq_old_icons = "block"
        else:
            eq_new_icons = "block"
            eq_old_icons = "none"
        parameters["eq_new_icons"] = eq_new_icons
        parameters["eq_old_icons"] = eq_old_icons
        eq_show_sidebar = parameters["eq_show_sidebar"]
        if eq_show_sidebar:
            app_sidebar = "block"
        else:
            app_sidebar = "none"
        parameters["app_sidebar"] = app_sidebar
        parameters["eq_show_sidebar_names"] = str(parameters["eq_show_sidebar_names"]).lower()
        parameters["eq_show_notification_right"] = str(parameters["eq_show_notification_right"]).lower()
        #eq_css_min = ''.join(self.SCSS_TEMPLATE.split())
        #eq_css_data = eq_css_min.format(**parameters)
        eq_css_data = self.SCSS_TEMPLATE.format(**parameters)
        datas = base64.b64encode(eq_css_data.encode('utf-8'))
        custom_attachment = IrAttachmentObj.sudo().search([('url', 'like', self.URL)])
        values = {
            'datas': datas,
            'url': self.URL,
            'name': self.URL,
            'datas_fname': self.URL.split("/")[-1],
        }
        if custom_attachment:
            custom_attachment.sudo().write(values)
        else:
            values.update({
                'type': 'binary',
                'mimetype': 'text/scss',
            })
            IrAttachmentObj.sudo().create(values)
        self.env['ir.qweb'].sudo().clear_caches()


    @api.multi
    def get_colors(self):
        self.scss_create_or_update_attachment()
        return self.URL
