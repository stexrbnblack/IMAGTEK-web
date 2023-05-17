import functools
# --> jsonify convierte un objeto a un json típico del navegador
from flask import Flask, jsonify, render_template, redirect, flash, request, url_for, g, session, make_response
from db import sql_select_name_productos, cargar_data_perfil, guardar_comentario_sql, up_load_edit_perfil, close_db, get_db, up_load_foto, sql_validar_existencia_user,sql_validar_existencia_emal , sql_validar_correo, sql_edit_password, sql_insert_msj, sql_insert_new_user, sql_select_data_user, sql_select_data_user_file
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import send_from_directory           # --> Permite acceder a directorios de las carpetas
import os


app=Flask(__name__)
app.secret_key = os.urandom(24)


CARPETA = os.path.join('upLoads')               # --> Haciendo uso del modulo de sistema 'os' direccionando la localidad de la carpeta
app.config['CARPETA'] = CARPETA                 # --> Almacenar la rideccion de la carpeta 

@app.route('/upLoads/<nombreFoto>')             # --> Direccion donde se guardan y muestran las fotos para aceder a ellas usando nombre de la foto
def upLoads(nombreFoto):
    # --> Acede a la direccion "app.config['CARPETA']" de la carpeta y busca el nombreFoto
    return send_from_directory(app.config['CARPETA'],nombreFoto)  
    # --> NO OLVIDES - importar la libreria send_from_directory [ from flask import send_from ]






# VENTANA DE INICIO (LOCAL HOST), Que redirecciona a login inmediatamente
@app.route('/')
def index():
    # validando si se deja una session abierta para inmediatamente iniciar con el perfil del usuario, sino returna a login
    if g.user:
        return redirect(url_for('/perfil'))
    return redirect ('login')






# --> PAGINA DE INICIO DE SESSION 'LOGEO DEL USUARIO'
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        # si hay una secion ya abierta la redirege al perfil
        if g.user:
            return redirect(url_for('/perfil'))
        
        # --> toma los datos  del formulario usando libreria de Flask, validando si hay un pedido o request del metodo POST
        if request.method == 'POST':
            db = get_db()                           # --> objeto que se le asigna la coneccion con la Base de Datos

            # --> captura la variable dentro del input con el id con el nombre del [''], valida si hay una solicitud, pedido o request del metodo POST capturando la variable del input con el id establesido entre ['']
            _usuario = request.form['txtUsuario']
            _password = request.form['txtPassword']

            print(_usuario)
            print(_password)

            user = db.execute('SELECT * FROM tabla_usuarios WHERE usuario = ?',
                              ([_usuario])).fetchone() # db.sql_select_name_productos(_usuario) # sql_select_productos(_usuario, _password)
        
            if user is None:
                error = 'Usuario inválido. Intenta nuevamente '
                flash( error )    
                return redirect ('login', error=error)
            
            else:       
                #--> check_password_hash():compara las 2 (variables) constraseña cifradas con hash retorna un true oh false si no son iguales
                verificacionContraseña = check_password_hash(f'{user[4]}', f'{_password}') 
                if verificacionContraseña == False:
                    error = 'Contraseña inválida... Intenta nuevamente '
                    
                    
                
                if user[2]==_usuario and verificacionContraseña:
                    print("validando contraseña: ", user[2] ==_usuario and verificacionContraseña)

                    
                    session.clear()                             # --> borrea alguna session anterior en la variable session     
                    session['user_id'] = user[0]                # --> le asigna una session al usuario con esta variable 'user[0]'
                    resp = make_response(redirect(url_for('perfil'))) 
                    resp.set_cookie('username', _usuario)

                    return resp                   
                
                flash( error )   
        else:
            session.clear()
            session['user_id'] = user[0]
            print("render a perfil")

            return redirect(url_for('perfil', error=error))
            return render_template ('login.html')

        return render_template ('login.html', error=error)
    except Exception as e:
        print(e)
        return render_template ('login.html', e=e)





# --> PAGINA DE REGISTRO A USUARIO NUEVO, guarda el usuario nuevo en la Base de Datos
@app.route('/register', methods=['GET', 'POST'])
def register():
    
    if g.user:
        return redirect(url_for('perfil'))
    try:
        # --> toma los datos  del formulario usando libreria de Flask, validando si hay un pedido o request del metodo POST
        if request.method == 'POST':

            # --> captura la variable dentro del input con el id con el nombre del [''], valida si hay una solicitud, pedido o request del metodo POST capturando la variable del input con el id establesido entre ['']
            _nombre = request.form[('txtNombreRegister')]
            _usuario = request.form[('txtUsuarioRegister')]
            _correo = request.form[('txtEmailRegister')]
            _contraseña = request.form[('txtPasswordRegister')]


            print(_nombre)
            print(_usuario)
            print(_correo) 
            print(_contraseña)


            _passwordCifrado = generate_password_hash(f'{_contraseña}')             #--> generate_password_hash():genea un hash a la variable _nuevaContraseña

            error = None

            if not _nombre:
                error = "campo de nombre incompleto"
                flash(error)
                return render_template ('register.html')
            if not _usuario:
                error = "campo de apellido incompleto"
                flash(error)
                return render_template ('register.html')
            if not _correo:
                error = "campo de email incompleto"
                flash(error)
                return render_template ('register.html')
            if not _contraseña:
                error = "campo de password incompleto"
                flash(error)
                return render_template ('register.html')
            
            validacion_usuario = sql_validar_existencia_user(_usuario)
            validacion_correo = sql_validar_existencia_emal(_correo)

            print('usuario', validacion_usuario)
            print('correo', validacion_correo)
            
            if validacion_usuario != None:
                error= 'ya existe ese nombre de usuario'
                flash(error)
                print('ya existe ese nombre de usuario')
                return render_template('register.html') 
            
            if validacion_correo != None: 
                error = f'ya existe un usuario con ese Correo: {_correo}'
                flash(f'ya existe un usuario con ese Correo: {_correo}')                                 
                print(f'ya existe un usuario con ese Correo: {_correo}') 
                return render_template('register.html')    
            
            if validacion_correo == None and validacion_usuario == None:
                print('ingresar el nuevo usuario')
                sql_insert_new_user(_nombre, _usuario, _correo, _passwordCifrado)
                
                print('INSERT INTO tabla_usuarios (nombre, usuario, correo, contraseña) VALUES (?,?,?,?)',
                    (_nombre, _usuario, _correo, _contraseña))
                
                error= 'Registro exitoso Gracias'
                flash(error)


                return render_template( 'login.html', error = error )

        return render_template( 'register.html', error = error )
    except Exception as e:
        print(e)
        return render_template ('register.html', e=e )    
    





#--> @login_required para validar si esta logeado y necesitas importar la libreria functools "impor functools" 
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view






@app.route('/perfil', methods = ['GET', 'POST'])
@login_required                                     # --> Para ingresar a la pagina requiere tener una session activa 
def perfil():
    # --> Captura el ID de usuario que inicio de session con g.user[0] - g.user[0]: g.user contiene toda la info del usuario almacenada en una vecto     
    user_id = g.user[0] 

    #--> obtener toda la info de la base de datos para mostrar lo en el perfil del usuario
    print('dentro del paerfil', g.user)
    datos_perfil_usuario = sql_select_data_user(g.user[2])

    #--> obtener toda los archivos de la tabla tabla_up_fotos usando el Id del Usuario de la base de datos para mostrar las imagenes en el perfil del usuario
    datos_filel_usuario = sql_select_data_user_file(user_id)
    print('datos_filel_usuario', datos_filel_usuario)

    return render_template("perfil.html", imagenes = datos_filel_usuario )





    
@app.route('/send', methods = ['GET', 'POST'])
@login_required                                     # --> Para ingresar a la pagina requiere tener una session activa 
def send():

    if request.method == 'POST':
        _de = request.form['txtMensajeDE']
        _para = request.form['txtMensajePara']
        _mensaje = request.form['txtAreaMensaje']

        db = get_db()

        De = db.execute('SELECT * FROM tabla_usuarios WHERE usuario = ?',
                              ([_de])).fetchone() # db.sql_select_name_productos(_usuario) # sql_select_productos(_usuario, _password)

        print('mensaje de: ', De[3])

        if (De[3] == _de) or (De[2] == _de): #--> valida si el usuario a quien va dirigido el mensaje existe en la bd

            if (De[3] == _para) or (De[2] == _para):

                sql_insert_msj(_de, _para, _mensaje)
                print('Mensaje enviado')
                flash('Mensaje enviado') 
            else:
                error='Usuario ah quien va dirijido el mjs no esta en la base de datos'
                return render_template ('send.html', error=error)
        else:
            error='No estar registrado para enviar mensaje ah otro usuario'
            return render_template ('send.html', error=error)

    return render_template ('send.html')  






@app.route('/mensajes', methods = ['GET', 'POST'])
def mensaje():

    if request.method == 'POST':
        a =0
    return render_template("mensajes.html")






# RECUPERER LA CONTRASEÑA DEL USUARIO
@app.route('/forgetPassword', methods = ['GET', 'POST'])
def forgetPassword():
    # --> toma los datos  del formulario usando libreria de Flask, validando si hay un pedido o request del metodo POST
    if request.method == 'POST':
        # --> captura la variable dentro del input con el id con el nombre del [''], valida si hay una solicitud, pedido o request del metodo POST capturando la variable del input con el id establesido entre [''] 
        _confirmarCorreo = request.form['txtConfirmarCorreo']
        _nuevaContraseña = request.form['txtNuevaContraseña']

        # --> if valida si el correo existe o no dentro de la Base de datos. 
        if sql_validar_correo(_confirmarCorreo) is None:
            print('correo no exite en bd')
            flash('Correo no existe')
            return forgetPassword()
        # --> si el if no es None osea que si existe el correo, encripta el password con hash y actualiza el password biejo por el nuevo
        else:
            _passwordCifrado = generate_password_hash(f'{_nuevaContraseña}')  #--> generate_password_hash():genea un hash a la variable _nuevaContraseña
            sql_edit_password(_nuevaContraseña, _passwordCifrado)
            print('contraseña cambiada  ')
            flash('Contraseña Modificada')
            return render_template ('login.html')

    return forgetPassword()






@app.route('/cargarImagen', methods=['GET', 'POST'])
@login_required                                     # --> Para ingresar a la pagina requiere tener una session activa 
def cargarImagen():
    # --> toma los datos  del formulario usando libreria de Flask, validando si hay un pedido o request del metodo POST
    if request.method == 'POST':
        # --> captura la variable dentro del input con el id con el nombre del [''], valida si hay una solicitud, pedido o request del metodo POST capturando la variable del input con el id establesido entre ['']
        _foto = request.files['txtFoto']
        _descripcion = request.form['txtAreaDescripcion']

        print(_foto)
        print(_descripcion)

        timeNow = datetime.now()                    # --> datetime.now(): obtiene la fecha actual.
        time = timeNow.strftime("%Y%H%M%S")         # --> strftime("%Y%H%M%S": establese el formato del la fecha ("%Y%H%M%S") Y:year H:hour M:mes S:segundos
        
        # --> valida si el archivo capturado del form esta basio si no lo esta se ejecuta
        if _foto.filename != '':                    
            nuevoNombreFoto = time+_foto.filename   # --> Genera nuevo nombre a _foto agregando la fecha actual
            _foto.save("upLoads/"+nuevoNombreFoto)  # --> save: guarda el file obtenido en _foto en la direcion uploads+el nuevo nombre ("uploads/"+nuevoNombreFoto)

        up_load_foto(g.user[0], _descripcion, nuevoNombreFoto)

    return redirect('perfil')






@app.route('/comentarios', methods=['GET', 'POST'])
def comentarios():
    if request.method == 'POST':
        _nombre = request.form['txtNombreComentario']
        _correo = request.form['txtCorreoComentario']
        _comentario =request.form['txtAreaComentario']

        guardar_comentario_sql(_nombre, _correo, _comentario)


    return render_template('login.html')






@app.route('/edita_Perfil', methods=['GET', 'POST'])

def edita_Perfil():

    # --> Captura el ID de usuario que inicio de session con g.user[0] - g.user[0]: g.user contiene toda la info del usuario almacenada en una vecto     
    user_id = g.user[0] 

    # --> toma los datos  del formulario usando libreria de Flask, validando si hay un pedido o request del metodo POST
    if request.method == 'POST':
        # --> captura la variable dentro del input con el id con el nombre del [''], valida si hay una solicitud, pedido o request del metodo POST capturando la variable del input con el id establesido entre ['']
        _nombrePerfil = request.form['txtEditNombreUsuario']
        _descripcionPerfil = request.form['txtAreaEditDescripcionPerfil']
        _fotoPerfil = request.files['txtFotoEditPerfil']

        timeNow = datetime.now()                    # --> datetime.now(): obtiene la fecha actual.
        time = timeNow.strftime("%Y%H%M%S")         # --> strftime("%Y%H%M%S": establese el formato del la fecha ("%Y%H%M%S") Y:year H:hour M:mes S:segundos

        if _fotoPerfil.filename != '':                    # --> valida si el archivo capturado del form esta basio si no lo esta se ejecuta
            nuevoNombreFoto = time+_fotoPerfil.filename   # --> Genera nuevo nombre a _foto agregando la fecha actual
            _fotoPerfil.save("upLoads/"+nuevoNombreFoto)  # --> save: guarda el file obtenido en _foto en la direcion uploads+el nuevo nombre ("uploads/"+nuevoNombreFoto)

        up_load_edit_perfil(_nombrePerfil, _descripcionPerfil, nuevoNombreFoto, user_id)

    return redirect('perfil')






@app.route('/btn_likes', methods= ['GET', 'POST'])
def btnlikes():
    if request.method == 'POST':
        _likes_fotos = request.submit['btnLike']
        print('este es el btn like ->', _likes_fotos)

    return





# @app.route('/mensajes/<string:_usuario>')
# def getmensaje(_usuario):
# # --> variable = [valor iten for iten in vector oh map if:si iten[nombre oh posicion ah obtener] == sea igual a  _variable ]
#     encontrado = [mensaje for mensaje in mensajes if mensaje['usuario'] == _usuario] 

#     if (len(encontrado) > 0):
#         return jsonify({"mensaje": encontrado[0]})
    
#     return jsonify({"message":"mensaje no encontrado"})





# --> SE EJECUTA ANTES DE CADA SOLICITUD O REQUEST VALIDANDO SI HAY UNA SESIION ALMACENADA EN SESSION  
@app.before_request
def load_logged_in_user():
    # --> le asigna una session al 'user_id' dentro de la variable
    user_id = session.get('user_id')

    # --> valida si existe era un valor para user si hay secion, sino le otorga a user = none.
    if user_id is None:
        g.user = None
    else:
        # --> valida si existe dentro de la Base de Datos un usuarioi con user_id y almacena toda la informacion del user en g.user
        g.user = get_db().execute(
            'SELECT * FROM tabla_usuarios WHERE id = ?', (user_id,)
        ).fetchone()
        close_db()

        


# --> CEIERRE DE SESSION
@app.route('/logout')
def logout():
    # --> limpia la variable session, la que valida si existe un usuario
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
