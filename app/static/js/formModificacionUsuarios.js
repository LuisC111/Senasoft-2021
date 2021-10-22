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
    nombreUsuario: /^[a-zA-ZÀ-ÿ\s]{1,40}$/,
    nombrePaciente: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras, numeros, guion y guion_bajo
    apellidoUsuario: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
    correoUsuario: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/, // Letras, numeros, guion y guion_bajo
    contraseñaUsuario: /^.{4,12}$/, // Letras y espacios, pueden llevar acentos.
    documentoPaciente: /^\d{6,15}$/, // 4 a 12 digitos.
    direccionUsuario: /^[a-zA-ZÀ-ÿ\s0-9\_\-\#]{4,40}$/,
    telefonoPaciente: /^\d{7,12}$/,
    edadPaciente: /^\d{1,3}$/,
    telefonoUsuario: /^\d{7,12}$/,
    documentoUsuario: /^\d{6,15}$/
}

const campos = {
    nombreUsuario: false,
    nombrePaciente: false,
    apellidoUsuario: false,
    correoUsuario: false,
    contraseñaUsuario: false,
    documentoPaciente: false,
    direccionUsuario: false,
    telefonoPaciente: false,
    edadPaciente: false,
    telefonoUsuario: false,
    documentoUsuario: false
}

const validarFormulario = (e) => {
    switch (e.target.name) {
        case "nombreUsuario":
            validarCampo(expresiones.nombrePaciente, e.target, 'nombreUsuario');
            break;
        case "nombrePaciente":
            validarCampo(expresiones.nombrePaciente, e.target, 'nombreUsuario');
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
        case "documentoPaciente":
            validarCampo(expresiones.documentoPaciente, e.target, 'documentoUsuario');
            break;
        case "documentoUsuario":
            validarCampo(expresiones.documentoPaciente, e.target, 'documentoUsuario');
            break;
        case "direccionUsuario":
            validarCampo(expresiones.direccionUsuario, e.target, 'direccionUsuario');
            break;
        case "telefonoPaciente":
            validarCampo(expresiones.telefonoPaciente, e.target, 'telefonoPaciente');
            break;
        case "telefonoUsuario":
            validarCampo(expresiones.telefonoUsuario, e.target, 'telefonoUsuario');
            break;
        case "edadPaciente":
            validarCampo(expresiones.edadPaciente, e.target, 'edadPaciente');
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

