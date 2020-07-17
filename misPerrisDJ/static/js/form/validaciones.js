/****
 * Archivo: validaciones.js
 * Caso de uso: Validaciones del formulario de postulacion.
 * Alumno: Daniel Garcia.
 * ---------------------------------------------------------------------------------
 ****/


/****
 * Preparando el formulario al cargar la pagina de postulacion.
 ****/
$(document).ready(function() {
    limpiarCiudades();
});




/****
 * Controlar el cambio de items en las regiones y asignarles el contenido a las ciudades.
 ****/
$("#id_region").change(function() {
    if ($("#id_region").val() == '') return;
    limpiarCiudades();
    if ($("#id_region").val() == 'santiago') ciudadesSantiago();
    if ($("#id_region").val() == 'valparaiso') ciudadesValparaiso();
    if ($("#id_region").val() == 'rancagua') ciudadesRancagua();
    if ($("#id_region").val() == 'maule') ciudadesMaule();
});