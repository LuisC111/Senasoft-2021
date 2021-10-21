/*
nombreUsuario
apellidoUsuario
emailUsuario
contraseñaUsuario
fechaNacimiento --
documentoUsuario
estadoUsuario --
direccionUsuario
imgUsuario --
idTipoDoc --
idPerfilUsuario --
*/
//idNegocio
//precioProducto
//cantidadProducto
//estadoProductoNegocio

const formulario = document.getElementById('pro-form');
const inputs = document.querySelectorAll('#pro-form input');

const expresiones = {
    nombreUsuario: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras, numeros, guion y guion_bajo
    apellidoUsuario: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
    correoUsuario: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/, // Letras, numeros, guion y guion_bajo
    contraseñaUsuario: /^.{4,12}$/, // Letras y espacios, pueden llevar acentos.
    documentoUsuario: /^\d{8,10}$/, // 4 a 12 digitos.
    direccionUsuario: /^[a-zA-ZÀ-ÿ\s0-9\_\-\#]{4,40}$/
}

const campos = {
    nombreUsuario: false,
    apellidoUsuario: false,
    correoUsuario: false,
    contraseñaUsuario: false,
    documentoUsuario: false,
    direccionUsuario: false
}

const validarFormulario = (e) => {
    switch (e.target.name) {
        case "nombreUsuario":
            validarCampo(expresiones.nombreUsuario, e.target, 'nombreUsuario');
            break;
        case "apellidoUsuario":
            validarCampo(expresiones.apellidoUsuario, e.target, 'apellidoUsuario');
            break;
        case "correoUsuario":
            validarCampo(expresiones.correoUsuario, e.target, 'correoUsuario');
            break;
        case "contraseñaUsuario":
            validarCampo(expresiones.contraseñaUsuario, e.target, 'contraseñaUsuario');
            break;
        case "documentoUsuario":
            validarCampo(expresiones.documentoUsuario, e.target, 'documentoUsuario');
            break;
        case "direccionUsuario":
            validarCampo(expresiones.direccionUsuario, e.target, 'direccionUsuario');
            break;

    }
}

const validarCampo = (expresion, input, campo) => {
    if (expresion.test(input.value)) {
        document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-incorrecto');
        document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-correcto');
        document.querySelector(`#grupo__${campo} i`).classList.add('fa-check-circle');
        document.querySelector(`#grupo__${campo} i`).classList.remove('fa-times-circle');
        document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.remove('formulario__input-error-activo');
        campos[campo] = true;
    } else {
        document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-incorrecto');
        document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-correcto');
        document.querySelector(`#grupo__${campo} i`).classList.add('fa-times-circle');
        document.querySelector(`#grupo__${campo} i`).classList.remove('fa-check-circle');
        document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.add('formulario__input-error-activo');
        campos[campo] = false;
    }
}

inputs.forEach((input) => {
    input.addEventListener('keyup', validarFormulario);
    input.addEventListener('blur', validarFormulario);
});

function mensaje() {
    window.location('../PerfilAdmin')
    alertify.success('Negocio agregado');
}