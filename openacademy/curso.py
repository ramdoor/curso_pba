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
from datetime import datetime, timedelta

class openacademy_course(osv.Model):
    _name = 'openacademy.course'
    
    def copy(self, cr, uid, id, default, context=None):
        print default,"default"
        course=self.browse(cr, uid, id, context=context)
        new_name="copy of %s" % course.name
        cours_dup=self.search(cr, uid, [('name','=like', new_name+'%')], count=True, limit=80, context=context)
        if cours_dup > 0:
            new_name="%s (%s)" %(new_name,cours_dup +1)
        default['name']=new_name
        return super(openacademy_course, self).copy(cr, uid, id, default, context=context)
        
    def _get_attendee_count(self, cr, uid, ids, name, args, context=None):
        res = {}
        for course in self.browse(cr, uid, ids, context=context):
            res[course.id] = 0
            for session in course.session_ids:
                res[course.id] += len(session.attendee_ids)
        return res
        
    def _get_courses_from_sessions(self, cr, uid, ids, context=None):
        sessions = self.browse(cr, uid, ids, context=context)
        return list(set(sess.course_id.id for sess in sessions))
        
    _columns={
        'name': fields.char(string='Titulo', size=256, required=True),
        'description': fields.text(string='Description'),
        'responsible_id': fields.many2one('res.users',string='Responsable', select=True, ondelete='set null'),
        'session_ids': fields.one2many('openacademy.session', 'course_id',string='Sesiones'),
        'attendee_count': fields.function(_get_attendee_count, type='integer', string='Attendee Count',
        store={'openacademy.session':(_get_courses_from_sessions,['attendee_ids'],0)})
    }

    _sql_constraints= [('name_unique','UNIQUE (name)','El nombre debe ser unico'),
        ('name_description_check','CHECK (name <> description)','El nombre y descripcion deben ser diferentes')]

class openacademy_session(osv.Model):
    _name='openacademy.session'
    
    def _check_instructor_not_in_attendees(self, cr, uid, ids, context=None): # cuando la fucnion empieza con guion bajo es que es privada, no puedeser usada fuera de open academy
        if not context:
            contex={}
            print ids,"imprimo ids"
        for session in self.browse(cr, uid, ids, context):
            lista_attendee=[]
            for attendee in session.attendee_ids:
                lista_attendee.append(attendee.partner_id.id)
            print lista_attendee, " imprimo lista de attendees"
            if session.instructor_id and session.instructor_id.id in lista_attendee:
                return False
            return True
                        
    def _get_percent(self, seats, attendee_ids):
        try:
            return (100 * len(attendee_ids)) / seats
        except ZeroDivisionError:
            return 0.0
            
            
    def _take_seats_percent(self, cr, uid,ids, field, args, context=None):
        print field, "field"
        print args,"args"
        resultado={}
        for session in self.browse(cr, uid, ids, context):
            resultado[session.id]=self._get_percent(session.seats, session.attendee_ids)
        print resultado,"resultado"
        return resultado            
            
    def onchange_taken_seats(self, cr,uid,ids,seats,attendee_ids):
        print attendee_ids,"recibe"
        num_attendees=self.resolve_2many_commands(cr, uid, 'attendee_ids', attendee_ids, ['id'])
        print num_attendees,"despues"
        resultado={'value':{'taken_seats_percent':self._get_percent(seats,attendee_ids)}}
        print resultado
        if seats < len(num_attendees):
            resultado['warning']={'title':"Atencion asientos",'message':"No puedes tener menos asientos que asistentes"}
        print resultado
        return resultado
              
    def _determin_end_date(self, cr, uid, ids, field, arg, context=None):
        res={}
        for session in self.browse(cr, uid, ids, context):
            if session.start_date and session.duration:
                start_date=datetime.strptime(session.start_date, "%Y-%m-%d")
                duration=timedelta(days=session.duration-1)
                end_date=start_date+duration
                res[session.id]=end_date.strftime("%Y-%m-%d")
            else:
                res[session.id]=session.start_date
        print res
        return res 
        
    def _set_end_date(self, cr, uid, id, field, value, arg, context=None):
        session=self.browse(cr, uid, id, context)
        if session.start_date and value:
            start_date=datetime.strptime(session.start_date, "%Y-%m-%d")
            end_date=datetime.strptime(value, "%Y-%m-%d")
            duration=end_date-start_date
            self.write(cr, uid, id, {'duration':duration.days+1}, context)
    
    def _determin_hours_from_duration(self, cr, uid, ids, field, arg, context=None):
        result = {}
        sessions = self.browse(cr, uid, ids, context=context)
        for session in sessions:
            result[session.id] = (session.duration * 8 if session.duration else 0)
        return result
        
    def _set_hours(self, cr, uid, id, field, value, arg, context=None):
        if value:
            self.write(cr, uid, id,{'duration' : (value / 8)},context=context)
        
    def _get_attendee_count(self, cr, uid, ids, name, args, context=None):
        res={}
        for session in self.browse(cr, uid, ids, context):
            res[session.id]=len(session.attendee_ids)
        return res
        
    def action_confirm(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'confirm'}, context=context)
        
    def action_draft(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'draft'}, context=context)
        
    def action_done(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'done'}, context=context)
        
               
    _columns={
        'name': fields.char(string='Nombre', size=256, required=True),
        'start_date': fields.date(string='Fecha Inicio'),
        'duration': fields.float(string='Duracion', digits=(6,2), help='Duracion en dias'),
        'seats': fields.integer(string='Numero de asientos'),	
        'active': fields.boolean(string='Activo'),
#       'instructor_id': fields.many2one('res.partner', string='Instructor', domain= ['|',('instructor','=',True),('name','ilike','%axel%')] ),
        'instructor_id': fields.many2one('res.partner', string='Instructor', domain= [('instructor','=',True) ], required=True),
        'course_id': fields.many2one('openacademy.course', string='Curso', ondelete='cascade'),
        'attendee_ids':fields.one2many('openacademy.attendee', 'session_id',string='Asistentes'),
        'taken_seats_percent': fields.function(_take_seats_percent, type='float', string='Taken Seats'),
        'end_date': fields.function(_determin_end_date,type='date', string="End Date", fnct_inv=_set_end_date), 
        'hours': fields.function(_determin_hours_from_duration, type='float', string='Hours', fnct_inv=_set_hours),
        'attendee_count':fields.function(_get_attendee_count,type='integer', string='Attendee Count',store=True),
        'color': fields.integer('Color'), 
        'state': fields.selection([('draft','Draft'),('confirm','Confirmed'),('done','Done')], string='State'),
        
    }

    _defaults={
        'active':True,
        'start_date': fields.date.today,
        'state': 'draft',
    }
    
    _constraints=[(_check_instructor_not_in_attendees,"El instructor no puede ser asistente",['instructor_id','attendee_ids'])]
    
class openacademy_attendee(osv.Model):
    _name='openacademy.attendee'
    
    _rec_name='partner_id'
    
    _columns={
        'partner_id':fields.many2one('res.partner',string='Attendee',required=True, ondelete='cascade'),
        'session_id':fields.many2one('openacademy.session', string='Session', ondelete='cascade'),
        }
    
    
