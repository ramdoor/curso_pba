import xmlrpclib

HOST='127.0.0.1'
PORT=8069
DB='curso_amiganet'
USER='admin'
PASS='admin'

url='http://%s:%d/xmlrpc/' %(HOST,PORT)
common_proxy = xmlrpclib.ServerProxy(url+'common')
object_proxy = xmlrpclib.ServerProxy(url+'object')

def execute(*args):
    return object_proxy.execute(DB, uid, PASS, *args)
    
uid=common_proxy.login(DB, USER, PASS)
print "uid de admin es %d" %uid

session_ids= execute ('openacademy.session', 'search', [])
print session_ids

sessions= execute('openacademy.session', 'read', session_ids, ['name','seats'])
print sessions


#~ id_session=execute('openacademy.session','create', {'name':'Si se crea'})
#~ 
#~ id_course=execute('openacademy.course', 'create',{'name':'curso ejemplo'})

course_id=execute('openacademy.course', 'search', [('name','=','Curso de prueba')])
if course_id:
    execute('openacademy.course', 'write', course_id[0],{'name':'Modificado'})
