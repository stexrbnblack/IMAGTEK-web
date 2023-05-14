import sqlite3
from sqlite3 import Error
from flask import current_app, g

from werkzeug.security import generate_password_hash, check_password_hash

# generate_password_hash: Para crear hashes resultado de aplicar PBKDF2. 
# check_password_hash: Para verificar una cadena generada por el método anterior.
generate_password_hash('2') # 'pbkdf2:sha256:150000$Kc5ZhZvI$a749008a312f2b0b631b1253f0ba619d28982e874e35927f0315a1f151e72424'
check_password_hash('pbkdf2:sha256:150000$Kc5ZhZvI$a749008a312f2b0b631b1253f0ba619d28982e874e35927f0315a1f151e72424','2')


def get_db():
    try:
        if 'db' not in g:
            g.db = sqlite3.connect("database.db")
            g.db.row_factory = sqlite3.Row
        return g.db
    except Error:
        print( Error )





def close_db():
    db = g.pop( 'db', None )

    if db is not None:
        db.close()




def sql_connection():
    try:
        con = sqlite3.connect('database.db')
        return con;

    except sqlite3.Error as e:
        print(e)




def sql_select_data_user(user):
   str_sql = 'SELECT * FROM tabla_usuarios WHERE (usuario is ?)'
   data = (user)

   con = sql_connection() 
   cursorObj = con.cursor()
   cursorObj.execute(str_sql, [data])
   productos = cursorObj.fetchall()
   con.commit()
   con.close()
   return productos





def sql_select_productos(usuario, contraseña):

    str_sql = 'SELECT * FROM tabla_usuarios WHERE (usuario, contraseña) is (?,?)'
    data = (usuario, contraseña)

    print(str_sql, data)

    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(str_sql, data)
    productos = cursorObj.fetchall()
    con.commit()
    print(productos)
    con.close()
    if productos == None:
        print('no se encuentra en la db')
    else:
        return productos
    




def sql_validar_correo(correo):
    str_sql = 'SELECT correo FROM usuarios WHERE (correo) is (?)'
    data = (correo)

    print(str_sql, data)

    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(str_sql, [data])
    productos = cursorObj.fetchone()
    con.commit()
    print(productos)
    con.close()
    if productos == None:
        print('no se encuentra en la db')
    else:
        return productos





def sql_select_name_productos(usuario):
    str_sql = 'SELECT usuario, contraseña FROM tabla_usuarios WHERE (usuario = ?)' # 'SELECT usuarios, contraseña FROM usuarios WHERE usuarios = (?)'
    data = (usuario)

    print("DATOS SQL: ", str_sql, data)

    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(str_sql, [usuario])

    productos = cursorObj.fetchone() # --> fetchone() captura una cadena con el contenido solicitado.
                                     # --> fetchall() captura una matris con todo el contenido solicitado.
    con.commit()
    print('ESTA: ', productos)
    con.close()
  
    return productos
    




def sql_edit_password(password, referido):
    str_sql = 'UPDATE usuario SET contraseña = ? WHERE correo = ?'# --> "UPDATE usuarios SET contraseña = '{referido}', WHERE correo = '{valor a cambiar}';"
    data = (password, referido)

    print(data)

    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(str_sql, data)
    con.commit()
    con.close()





def sql_delete_producto(id):
    str_sql = "DELETE FROM productos WHERE id = " + id + ";"

    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(str_sql)
    con.commit()
    con.close()





def sql_validar_existencia_emal(_email):

    print('sql: ', _email)

    # VALIDAMOS QUE NO EXISTA YA ESE _email PARA UN REGISTRO EXITOSO
    str_sql = 'SELECT correo FROM tabla_usuarios WHERE correo = ?'
    data = (_email)  

    con = sql_connection()
    cursor_obj = con.cursor()
    print('antes: ', _email)
    cursor_obj.execute(str_sql, [data])
    email = cursor_obj.fetchone()
    con.commit()
    print('despues: ', email)
    con.close()

    return (email)





def sql_validar_existencia_user(_user):

    # VALIDAMOS QUE NO EXISTA YA UN _user CON ESE NOMBRE PARA UN REGISTRO EXITOSO
    str_sql__user = 'SELECT usuario FROM tabla_usuarios WHERE usuario = ?'
    data_user = (_user)

    con = sql_connection()
    cursor_obj = con.cursor()
    print('antes', user)
    cursor_obj.execute(str_sql__user, [data_user])
    user = cursor_obj.fetchone()
    con.commit()
    print('despues', user)
    con.close()

    return (user)






def sql_insert_new_user(nombre, usuarios, correo, contraseña):

    # El objeto con obtiene la conexión con la base de datos llamando al método creado anteriormente
    con = sql_connection()

    str_sql = "INSERT INTO usuarios (nombre, usuarios, correo, contraseña) VALUES (?,?,?,?)"
    data = (nombre, usuarios, correo, contraseña)

    print(str_sql, data)
    print('dentro: INSERT INTO usuarios (nombre, usuarios, correo, contraseña) VALUES (?,?,?,?)',
    (nombre, usuarios, correo, contraseña))
    # 'INSERT INTO usuarios (nombre, usuarios, correo, contraseña) VALUES('f'{nombre}, {usuarios}, {correo}, {contraseña});'

    # Es necesario un objeto cursor, el cual se obtiene de la variable de conexión, para ejecutar las sentencias SQL
    cursorObj = con.cursor()

    # Ejecutar la sentencia SQL enviada por parámetro
    # con.execute('INSERT INTO usuarios (nombre, usuarios, correo, contraseña) VALUES (?,?,?,?)',
    # (nombre, usuarios, correo, contraseña))
    cursorObj.execute(str_sql, data)

    # Actualizar los cambios realizados a la base de datos
    con.commit()
    
    # Cerrar la conexión
    con.close()






def sql_insert_msj(para, asunto, mensaje):

    str_sql = 'INSERT INTO tabla_mensajes (from_id, to_id as nombre from usuarios, asunto, msj) VALUES (?,?,?)'
    data = (para, asunto, mensaje)

    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(str_sql, [data])
    con.commit()
    con.close()





def up_load_foto(id_usuario, descripcion, foto):
    str_sql = 'INSERT INTO tabla_up_fotos (id_usuario, descripcion_foto, file_foto) VALUES (?,?,?)'
    data = (id_usuario, descripcion, foto)

    con= sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(str_sql, data)
    con.commit()
    con.close()





def sql_select_data_user_file(id_user):
    str_sql = 'SELECT * FROM tabla_up_fotos WHERE id_usuario = ?' #'SELECT * FROM upFoto WHERE id = ? '
    data = (id_user)

    con= sql_connection()
    cursorObj= con.cursor()
    cursorObj.execute(str_sql, [data])
    
    files = cursorObj.fetchall()    # --> fetchone() captura una cadena con el contenido solicitado.
                                    # --> fetchall() captura una matris con todo el contenido solicitado.
    con.commit()
    con.close()

    return files





def cargar_data_perfil():

    return 





def up_load_edit_perfil(nombre_perfil, descripcion_perfil, foto_perfil, id_user):
    # El objeto con obtiene la conexión con la base de datos llamando al método creado anteriormente
    con = sql_connection()

    # 'UPDATE tabla SET nombre_perfil = ?, descripcion_perfil = ?, foto_perfil = ? WHERE id = id_user;'
    str_sql = "UPDATE tabla_usuarios SET nombre_perfil = ?, descripcion_perfil = ?, foto_perfil = ? WHERE id = ?"
    data = (nombre_perfil, descripcion_perfil, foto_perfil, id_user)

    # Es necesario un objeto cursor, el cual se obtiene de la variable de conexión, para ejecutar las sentencias SQL
    cursorObj = con.cursor()

    # Ejecuta la sentencia SQL enviada por parámetro
    # con.execute('INSERT INTO usuarios (nombre, usuarios, correo, contraseña) VALUES (?,?,?,?)',
    # (nombre, usuarios, correo, contraseña))
    cursorObj.execute(str_sql, data)

    # Actualizar los cambios realizados a la base de datos
    con.commit()
    
    # Cerrar la conexión
    con.close()





def guardar_comentario_sql(nombre, correo, comentario):
    sql = 'INSERT INTO tabla_comentarios (Nombre, Correo, Comentario) VALUES (?, ?, ?) '
    data = (nombre, correo, comentario)

    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(sql, data)
    con.commit()
    con.close()





def close_db():
    db = g.pop( 'db', None )

    if db is not None:
        db.close()
