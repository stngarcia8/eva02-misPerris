/****
 * Archivo: funciones.js
 * Caso de uso: Funciones variadas para el funcionamiento del validador.
 * Alumno: Daniel Garcia.
 * ---------------------------------------------------------------------------------
 ****/


/****
 *  Devuelve la fecha actual para asignarlas a la fecha de nacimiento.
 ****/
function asignarFechaActual() {
    var d = new Date();
    var dia = d.getDate();
    if (dia < 10) dia = "0" + dia;
    var mes = (d.getMonth() + 1);
    if (mes < 10) mes = "0" + mes;
    var anio = 2001;
    var fechatotal = anio + "-" + mes + "-" + dia;
    var dateControl = document.querySelector('input[type="date"]');
    dateControl.value = fechatotal;
};


/****
 *  Funcion para validar si un campo esta vacio.
 ****/
function campoVacio(elemento, elementoError, mensajeError) {
    if ($(elemento).val().length == 0) {
        escribirMensajeError(elementoError, mensajeError);
        return true;
    }
    ocultarMensajeError(elementoError);
    return false;
};


/****
 *  Verificar el formato del campo
 ****/
function formatoCorrecto(elemento, patronAplicado, elementoError, mensajeError) {
    var patron = new RegExp(patronAplicado);
    if (!patron.test($(elemento).val())) {
        escribirMensajeError(elementoError, mensajeError);
        return true;
    }
    ocultarMensajeError(elementoError);
    return false;
};


/****
 *  Funcion para validar el año de la fecha.
 ****/
function esAnioValido(elemento, anioTope, elementoError, mensajeError) {
    var fecha = new Date($(elemento).val());
    if (fecha.getFullYear() > anioTope) {
        escribirMensajeError(elementoError, mensajeError);
        return true;
    }
    ocultarMensajeError(elementoError);
    return false;
};


/****
 * * Funcion para limpiar el contenido de los inputs.
 * ****/
function limpiarCampos() {
    $("input").val("");
    asignarFechaActual();
    $("#region").val("");
    limpiarCiudades();
    $("#ciudad").val("");
    $("#postular").val("Postular");
    $("#vivienda").val("");
};


/****
 * * Funcion para limpiar los textos de errores del formulario.
 * ****/
function limpiarSpan() {
    $("span").text("");
    $("span").hide();
};


/****
 * Funcion para limpiar las ciudades.
 ****/
function limpiarCiudades() {
    $("#id_ciudad").empty();
    agregarCiudad("", "Seleccione una ciudad");
}


/****
 *  Asigna las ciudades de Santiago.
 ****/
function ciudadesSantiago() {
    agregarCiudad("santiago", "Santiago");
    agregarCiudad("maipo", "Isla de Maipo");
};


/****
 *  Asigna las ciudades de Valparaiso.
 ****/
function ciudadesValparaiso() {
    agregarCiudad("valparaiso", "Valparaiso");
    agregarCiudad("vina", "Viña del Mar");
    agregarCiudad("calera", "Calera")
};


/****
 *  Asigna las ciudades de Rancagua.
 ****/
function ciudadesRancagua() {
    agregarCiudad("rancagua", "Rancagua");
    agregarCiudad("san-fernando", "San Fernando");
    agregarCiudad("pichilemu", "Pichilemu");
};


/****
 * Asigna las ciudades a Maule.
 ****/
function ciudadesMaule() {
    agregarCiudad("talca", "Talca");
    agregarCiudad("linares", "Linares");
    agregarCiudad("parral", "Parral");
};


/****
 *  Funcion para agregar una ciudad.
 * valor: corresponde al valor del opcion que sera agregado.
 * texto: corresponde al texto que aparecera en el option.
 ****/
function agregarCiudad(valor, texto) {
    var miCombo = document.getElementById("id_ciudad");
    var miOption = document.createElement("option");
    miOption.text = texto;
    miOption.value = valor;
    miCombo.add(miOption);
};


/****
 * * Funcion para escribir el mensaje de error en un elemento.
 * elemento: corresponde al elemento que se aplicara el mensaje
 * mensaje: corresponde al mensaje que sera asignado al elemento
 ****
 */
function escribirMensajeError(elemento, mensaje) {
    $(elemento).text(mensaje);
    $(elemento).show();
};


/****
 *  Funcion para esconderel elemento de mensaje de error.
 * elemento: corresponde al elemento que sera ocultado.
 ****/
function ocultarMensajeError(elemento, ) {
    $(elemento).text("");
    $(elemento).hide();
};