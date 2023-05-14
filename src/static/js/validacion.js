function validarFormulario(){
    var txtNombre = document.getElementById("txtNombre");
    if (txtNombre.value.length <= 5){
        alert("Debe incluir un txtNombre con mas de 5 caracteres");
        obtenerFoco(txtNombre);
    }

    var txtApellido = document.getElementById("txtApellido");
    if (txtApellido.value.length <= 5){
        alert("Debe incluir un txtApellido con mas de 5 caracteres"); 
        obtenerFoco(txtApellido);
    }

// NO SE LOGRA CAPTURAR Y VALIDAR SI ESTA SEECCIONADA O NO "Emitir un Alert porque es requerido el capmpo"
    // var sexoH = document.getElementById("hombre");
    // var sexoM= document.getElementById("mujer");
    // if (sexoH.value !== "hombre" && sexoM.value !== "mujer"){
    //     alert("sexo");
    // }

    var txtEmail = document.getElementById("txtEmail");
    if (!txtEmail.value.includes("@")){
        alert("El txtEmail debe contener @ ");
        obtenerFoco(txtEmail);
    }

    var txtPassword = document.getElementById("txtPassword");
    if (txtPassword.value.length <= 3){
        alert("La txtPassword debe contener mas de 3 caracteres");
        obtenerFoco(txtPassword);
    }

// NO SE LOGRA CAPTURAR Y VALIDAR SI ESTA SEECCIONADA O NO "Emitir un Alert porque es requerido el capmpo"
    // var checkbox = document.getElementById("checkbox");
    // (checkbox.value) === "acepto"? alert("ok"):alert("no")
    // if ((checkbox.value) !== ""){
    //     alert("Debes Aceptar los Terminos")
    // }
}


// MOSATRAR oh COCULTAR CONTRASEÑA AL HACER ( CLICK ) SOBRE LA IMAGEN O ELEMENTO, en la paginas de login
function mostrarPasswordOnClick(){
    var txtPassword = document.getElementById("txtPassword");

    // resumido en pocas lineas...  (con ? o if funciona igual)
    txtPassword.type === "password"? txtPassword.type = "text": txtPassword.type = "password";

// ejecucion con IF de forma normal.... (con '?' o 'IF' funciona igual)
    // if (txtPassword.type == "password"){
    //     txtPassword.type = "text";
    // }else{
    //     txtPassword.type = "password"
    // }
}

// MOSATRAR CONTRASEÑA AL TENER EL ( MOUSE SOBRE ) LA IMAGEN O ELEMENTO, en la paginas de login
function mostrarPasswordOnMouseOver(){
    var txtPassword = document.getElementById("txtPassword");
    // un IF pero ejecuta uno o otro, variable === 'x'? : si lo es ejecuta esto : sino ejecuta esto;
    txtPassword.type === "password"? txtPassword.type = "text": txtPassword.type = "password";

     
    // setTimeout(txtPassword.type = "text", 1000):
    // setTimeout(txtPassword.type = "password",1000);
}

// OCULTAR CONTRASEÑA AL ( TENER EL MOUSE FUERA ) DE LA IMAGEN O ELEMENTO, en la paginas de login
function mostrarPasswordOnMouseOut(){
    var txtPassword = document.getElementById("txtPassword");
    txtPassword.type = "password";
    // txtPassword.type === "password"? txtPassword.type = "text": txtPassword.type = "password";
}




// MOSTRAR CONTRASEÑA EN EL MODAL DE FORGOT PASSWORD o OLVIDE CONTRASEÑA.............................................
let imgNuevaContraseña = document.getElementById('imgNuevaContraseña') // captura el elemento con el id:imgNuevaContraseña y la almacena en la variable let
let txtNuevaContraseña = document.getElementById('txtNuevaContraseña') // captura el elemento con el id:imgNuevaContraseña y la almacena en la variable let
imgNuevaContraseña.addEventListener('click', ()=>{
    // un IF pero ejecuta uno o otro, variable === 'x'? : si lo es ejecuta esto : sino ejecuta esto;
    txtNuevaContraseña.type === 'password'? txtNuevaContraseña.type = 'text': txtNuevaContraseña.type = 'password';
});

let imgConfirmarContraseña = document.getElementById('imgConfirmarContraseña') // captura el elemento con el id:imgNuevaContraseña y la almacena en la variable let
let txtConfirmarContraseña = document.getElementById('txtConfirmarContraseña') // captura el elemento con el id:imgNuevaContraseña y la almacena en la variable let
imgConfirmarContraseña.addEventListener('click', ()=>{
    // un IF pero ejecuta uno o otro, variable === 'x'? : si lo es ejecuta esto : sino ejecuta esto;
    txtConfirmarContraseña.type === 'password'? txtConfirmarContraseña.type = 'text': txtConfirmarContraseña.type = 'password';
});




// MOSTRAS CONTRASEÑA EN LA PAGINA DE REGISTER.....................................
let imgRegister = document.getElementById('imgRegister')  // captura el elemento con el id:imgNuevaContraseña y la almacena en la variable let
let txtPasswordRegister = document.getElementById('txtPasswordRegister') // captura el elemento con el id:imgNuevaContraseña y la almacena en la variable let
imgRegister.addEventListener('click', ()=>{
    // un IF pero ejecuta uno o otro, variable === 'x'? : si lo es ejecuta esto : sino ejecuta esto;
    txtPasswordRegister.type === 'password'? txtPasswordRegister.type ='text': txtPasswordRegister.type = 'password'; 
})










// PREVISUALIZAR UNA IMAGEN CON UN DIV QUE ES EL CONTENEDOR ( div id:'preview ) DONDE SE PRE-VISUALISARA Y EL INPUT:FILE id:'txtFotoPerfil'
document.getElementById('txtFotoPerfil').onchange() = function(e){
    let reader = new FileReader();
    reader.readAsDataURL(e.target.files[0]);
    reader.onload = function(){
        let preview = document.getElementById('preview');
        imagen = document.createElement('img');
        imagen.src = reader.result;
        imagen.style.width = '200px';
        preview.append(imagen);
    }
}

// PREVISUALIZAR UNA IMAGEN CON UN img QUE ES EL CONTENEDOR ( img id:'seleccionFotoPerfil' ) DONDE SE PRE-VISUALISARA Y EL INPUT:FILE id:'txtFotoPerfil'
const defaultFile="{{url_for( 'static', filename='images/imagPerfil/imagen_Perfil.webp' )}}"
const file = document.getElementById('txtFotoPerfil');
const img = document.getElementById('seleccionFotoPerfil');
file.addEventListener('change', e => {
    if (e.target.files[0]){
        const reader = new FileReader();
        reader.onload = function(){
            img.src = e.target.result;
        }
        reader.readAsDataURL(e.target.files[0])
    }else{
        img.src = defaultFile;
    }
});





function contador_remueve_class(){
// CONSTADOR DE LIKES ...................
var btnElm = document.getElementById('btnLike');
var contadorLike = document.getElementById('contadorLike');
var contador = 1;
contadorLike.textContent = 1;

btnElm.onclick = function(){                        // cuando hagas click en el btnElem entra en la funcion
    contador ++;                                    // Aumenta el contador '++' en 1

    // contadorLike.textContent = contador;            // muestra el html el contenido de contador en la variable contadorLike
    contadorLike.innerHTML = contador;              // muestra el html el contenido de contador en la variable contadorLike
    console.log(contador)
}

// REMOVEDOR DE CLASS DE UN ELEMENTRO ........................
var removerClassSpan = document.getElementById('span');

btnElm.addEventListener('click', function(){        // esta atento al hacer click sobre el elemento 'btnElm' entra en la funcion
    removerClassSpan.classList.remove('collapse');  // .classList.remove: remueve la clase collapse de la var removerClassSpan con id-"span"
});}


// function alertaWeb (){
//     var name = document.formRegistro.txtNombre;
//     var txtApellido = document.formRegistro.txtApellido;
//     var sexo = document.formRegistro.sexo;
//     var txtEmail = document.formRegistro.txtEmail;
//     var password = document.formRegistro.txtPassword;
//     var checkbox = document.formRegistro.checkbox;
//     var checkbox_2 = document.getElementById("checkbox");

//    // var name = document.getElementById("txtNombre");
//    // var password = document.getElementById("txtPassword");

//     var len_name = name.value.length;
//     if (len_name <= 0){
//         alert("Tiene que llenar el campo txtNombre")
//         name.focus();
//     }

//     var len_txtApellido = txtApellido.value.length;
//     if (len_txtApellido <= 0){
//         alert("Tiene que llenar el campo txtApellido ")
//         name.focus();
//     }


//     if (sexo.value == onselectionchange){
//         alert("Tiene que llenar el campo Sexo")
//         name.focus();
//     }

//     var len_txtEmail = txtEmail.value.length;
//     if (len_txtEmail <= 0){
//         alert("Tiene que llenar el campo txtEmail")
//         name.focus();
//     }

//     var len_password = document.getElementById("txtPassword");
//     if (len_password.value.length <= 0){
//         alert("Tiene que llenar el campo txtPassword")
//         name.focus();
//     }

//     if (checkbox == onselectionchange){
//         alert("Tiene que llenar el campo checkbox")
//         name.focus();
//     }

//     if (checkbox_2 == fail){
//         alert("Tiene que llenar el campo checkbox_2")
//         name.focus();
//     }


//     if (name.value == "steven" || password.value == 123456789){
//         alert("hola " + name.value + " eres Bienvenido")
//     }else{alert("no posees acceso")}
//     name.focus();
// }