###################################################################################
# 
#    Copyright (C) 2017 MuK IT GmbH
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)

class Read(models.Model):
    
    _name = "muk_quality_docs.read"
    _description = "QMS Reading Information"
    
    #===========================================================================
    # Variables
    #===========================================================================
    
    user_id = fields.Many2one(
        "res.users",
        required=True,
        ondelete="cascade"
    )
    
    document_id = fields.Many2one(
        "muk_quality_docs.document",
        required=True,
        ondelete="cascade"
    )