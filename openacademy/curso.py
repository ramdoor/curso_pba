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

class openacademy_course(osv.Model):
	_name = 'openacademy.course'
	
	_columns={
		'name': fields.char(string='Titulo', size=256, required=True),
		'description': fields.text(string='Description'),
	}

	_sql_constraints= [('name_unique','UNIQUE (name)','El nombre debe ser unico'),
		('name_description_check','CHECK (name <> description)','El nombre y descripcion deben ser diferentes')]

class openacademy_session(osv.Model):
	_name='openacademy.session'
	
	_columns={
		'name': fields.char(string='Nombre', size=256, required=True),
		'start_date': fields.date(string='Fecha Inicio'),
		'duration': fields.float(string='Duracion', digits=(6,2), help='Duracion en dias'),
		'seats': fields.integer(string='Numero de asientos'),	
		'active': fields.boolean(string='Activo'),
	}

	_defaults={
		'active':True,
		'start_date': fields.date.today,
	}
