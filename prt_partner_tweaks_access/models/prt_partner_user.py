from odoo import models, fields, api, SUPERUSER_ID

# -- List of predefined rules that must be managed
PREDEFINED_RULES = ['res.partner.rule.private.employee', 'res.partner.rule.private.group']


#############
# Res Users #
#############
class PRTUsers(models.Model):
    _name = "res.users"
    _inherit = "res.users"

    allowed_partner_category_ids = fields.Many2many(string="Allowed Partner Categories",
                                                    comodel_name='res.partner.category',
                                                    relation='prt_user_partner_category_rel',
                                                    column1='user_id',
                                                    column2='category_id')

    allowed_country_ids = fields.Many2many(string="Allowed Countries",
                                           comodel_name='res.country',
                                           relation='prt_user_country_rel',
                                           column1='user_id',
                                           column2='country_id')

    allowed_country_state_ids = fields.Many2many(string="Allowed States",
                                                 comodel_name='res.country.state',
                                                 relation='prt_user_country_state_rel',
                                                 column1='user_id',
                                                 column2='state_id')

# -- Tweak access rules
    """
    Need to shut down some non-updatable rules to ensure tweak is applied correctly
    """
    @api.model
    def tweak_access_rules(self):
        rules = self.env['ir.rule'].sudo().search([('name', 'in', PREDEFINED_RULES)])
        if rules:
            rules.sudo().write({'active': False})

# -- Write. Clear caches if related vals changed
    @api.multi
    def write(self, vals):
        super(PRTUsers, self).write(vals)
        if 'allowed_partner_category_ids' in vals or 'allowed_country_ids' in vals or 'allowed_country_state_ids' in vals:
            self.clear_caches()