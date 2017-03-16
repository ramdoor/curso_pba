import openerplib

HOST='127.0.0.1'
PORT=8069
DB='curso_amiganet'
USER='admin'
PASS='admin'

connection=openerplib.get_connection(hostname=HOST, port=PORT, database=DB,
login=USER, password=PASS)

connection.check_login()
print "Logged in as %s (uid:%d)" % (connection.login, connection.user_id)

session_model = connection.get_model('openacademy.session')
session_ids = session_model.search([])
print session_ids
sessions = session_model.read(session_ids, ['name', 'seats'])
print sessions


course_model=connection.get_model('openacademy.course')
course_id=course_model.create({'name':'nuevo curso'})
