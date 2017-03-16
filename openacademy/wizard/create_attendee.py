# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
##############################################################################


from openerp.osv import osv, fields

class CreateAttendeeWizard(osv.TransientModel):
    _name='openacademy.create.attendee.wizard'
    
    _columns={
        'session_ids': fields.many2many('openacademy.session','wizard_session_rel','wizard_id', 'session_id', string='Sessions'),
        'attendee_ids': fields.one2many('openacademy.attendee.wizard', 'wizard_id', 'Attendees')
    }
    
    def action_add_attendee(self, cr, uid, ids, context=None):
        attendee_model=self.pool.get('openacademy.attendee')
        wizard=self.browse(cr, uid, ids[0], context=context)
        for session in wizard.session_ids:
            for attendee in wizard.attendee_ids:
                attendee_model.create(cr, uid, {'partner_id':attendee.partner_id.id, 'session_id':session.id},context)
        return {}
        
    
    def _get_active_session(self, cr, uid, context):
        print context,"esto manda"
        if context.get('active_model')=='openacademy.session':
            return context.get('active_ids', False)
        return False
    
    _defaults={
        'session_ids':_get_active_session,
    }

class AttendeeWizard(osv.TransientModel):
    _name = 'openacademy.attendee.wizard'
    _columns = {
        'partner_id': fields.many2one('res.partner', 'Partner', required=True),
        'wizard_id':fields.many2one('openacademy.create.attendee.wizard'),
    }
