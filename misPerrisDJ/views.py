from django.conf import settings
from django.shortcuts import redirect, render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.db.models import Q
from .models import Mascota, Busqueda, Persona, Adopcion
from .forms import IniciarSesionForm, nuevoRescatadoForm, filtrarGaleriaForm, RegistrarPersonaForm, registrarExperienciaForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.mail import send_mail

#from django.views.generic.edit import CreateView, UpdateView, DeleteView
#from django.urls import reverse_lazy


# index: Vista que muestra la galeria en la pagina inicial del sitio.
def index(request):
    if request.method == 'POST':
        form = filtrarGaleriaForm(request.POST)
    else:
        form = filtrarGaleriaForm()
    plantilla = loader.get_template("index.html")
    contexto = {'form': form, 'mascotas': __aplicarFiltro(request, form)}
    return HttpResponse(plantilla.render(contexto, request))


# __aplicarFiltro: funcion para buscar las mascotas segun el filtro de la galeria.
# rquest: Objeto que contiene la informacion del formulario.
# form: Formulario que procesa el filtro de la galeria.
# Retorna: Lista con los resultados del filtro paginados.
def __aplicarFiltro(request, form):
    if form.is_valid():
        filtro = Busqueda()
        filtro.estado = request.POST['estado']
        misMascotas = Mascota.objects.filter(estado=filtro)
    else:
        misMascotas = Mascota.objects.filter(estado='r')
    return __paginarResultados(request, misMascotas, 6)


# __paginarResultados: Funcion para paginar listas de resultados.
# request: Objeto que contiene los elementos del formulario.
# lista: lista que se desea paginar.
# elemPorPagina: Cantidad de elementos que se desea paginar.
# Retorna: Lista paginada.
def __paginarResultados(request, lista, elemPorPagina):
    miPaginador = Paginator(lista, elemPorPagina)
    page = request.GET.get('page')
    return miPaginador.get_page(page)


# iniciarSesion: Vista para iniciar sesion.
def iniciarSesion(request):
    form = IniciarSesionForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(
            username=data.get("username"), password=data.get("password"))
        if user is not None:
            login(request, user)
            return redirect('inicio')
    return render(request, "iniciarSesion.html", {'form': form})


#cerrarSesion:  Vista para cerrar la sesion.
# Retorna: Redirecciona a la pagina de inicio.
@login_required(login_url='iniciarSesion')
def cerrarSesion(request):
    logout(request)
    return redirect('/')


# mantenedorRescatados: Vista para el mantenimiento de los perritos rescatados y disponibles.
@login_required(login_url='iniciarSesion')
def mantenedorRescatados(request):
    if not request.user.is_superuser:
        return redirect('sinAcceso')
    lista = Mascota.objects.filter(
        Q(estado='r') | Q(estado='d') | Q(estado=''))
    mascotasPaginadas = __paginarResultados(request, lista, 10)
    plantilla = loader.get_template("administrador.html")
    contexto = {'mascotas': mascotasPaginadas}
    return HttpResponse(plantilla.render(contexto, request))


# nuevoRescatado: Vista para agregar una nueva mascota a la lista de rescatados.
@login_required(login_url='iniciarSesion')
def nuevoRescatado(request):
    if not request.user.is_superuser:
        return redirect('sinAcceso')
    #form = rescatadoForm(request.POST, request.FILES)
    if request.method == "POST":
        form = nuevoRescatadoForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            miMascota = Mascota(
                nombre=data.get('nombre'),
                raza=data.get('raza'),
                imagen=data.get('imagen'),
                descripcion=data.get('descripcion'))
            miMascota.save()
            return redirect('mantenedorRescatados')
    else:
        form = nuevoRescatadoForm()
    return render(request, "formularioRescatado.html", {'form': form})


# modificarRescatado: Vista para modificar el registro de la mascota.
@login_required(login_url='iniciarSesion')
def modificarRescatado(request, pk):
    if not request.user.is_superuser:
        return redirect('sinAcceso')
    if request.method == "POST":
        form = nuevoRescatadoForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            miMascota = Mascota.objects.get(id=pk)
            miMascota.nombre = data.get('nombre')
            miMascota.raza = data.get('raza')
            miMascota.imagen = data.get('imagen')
            miMascota.descripcion = data.get('descripcion')
            miMascota.save()
            return redirect('mantenedorRescatados')
    else:
        miMascota = Mascota.objects.get(id=pk)
        form = nuevoRescatadoForm(instance=miMascota)
    return render(request, "formularioRescatado.html", {'form': form})


# eliminarRescatado: Vista para eliminar una mascota en la lista de administrador.
@login_required(login_url='iniciarSesion')
def eliminarRescatado(request, pk):
    if not request.user.is_superuser:
        return redirect('sinAcceso')
    miMascota = Mascota.objects.get(id=pk).delete()
    return redirect('mantenedorRescatados')


# cambiarRescatado: Vista para cambiar el estado de la mascota a disponible.
@login_required(login_url='iniciarSesion')
def cambiarRescatado(request, pk):
    if not request.user.is_superuser:
        return redirect('sinAcceso')
    miMascota = Mascota.objects.get(id=pk)
    miMascota.estado = 'd'
    miMascota.save()
    return redirect('mantenedorRescatados')


# cambiarDisponible: Vista para cambiar el estado de disponible a rescatado.
@login_required(login_url='iniciarSesion')
def cambiarDisponible(request, pk):
    if not request.user.is_superuser:
        return redirect('sinAcceso')
    miMascota = Mascota.objects.get(id=pk)
    miMascota.estado = 'r'
    miMascota.save()
    return redirect('mantenedorRescatados')


# verRescatado: Vista para mostrar la informacion de una mascota.
@login_required(login_url='iniciarSesion')
def verRescatado(request, pk):
    miMascota = Mascota.objects.get(id=pk)
    plantilla = loader.get_template("verRescatado.html")
    contexto = {'mascota': miMascota}
    return HttpResponse(plantilla.render(contexto, request))


# listaRescatados: Vista para los perritos quepueden ser adoptados.
@login_required(login_url='iniciarSesion')
def listaRescatados(request):
    if request.user.is_superuser:
        return redirect('sinAcceso')
    # obteniendo el objeto persona del usuario.
    rut = request.user.username
    miPersona = Persona.objects.get(rut=rut)
    if miPersona:
        print(miPersona.id)
    lista = Mascota.objects.filter(Q(estado='d'))
    mascotasPaginadas = __paginarResultados(request, lista, 10)
    plantilla = loader.get_template("usuarioHome.html")
    contexto = {'mascotas': mascotasPaginadas, 'persona': miPersona}
    return HttpResponse(plantilla.render(contexto, request))


# registrarPersona: Vista del registro de personas al sitio.
# Retorna: Almacena los cambios y renderiza aa la pagina de inicio del sitio.
def registrarPersona(request):
    if request.method == "POST":
        form = RegistrarPersonaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Creando el usuario en el sistema.
            miUsuario = __crearUsuario(data)
            # Creando la persona.
            miPersona = Persona()
            __datosPersona(miPersona, data)
            miPersona.usuario = miUsuario
            miPersona.save()
            # enviando el correo deinformacion de registro.
            __enviarCorreo(miPersona)
            # Devolviendo al usuario a la pagina agradecimiento.
            return redirect('iniciarSesion')
    else:
        form = RegistrarPersonaForm()
    return render(request, "registroPostulante.html", {'form': form})


# __crearUsuario: Funcion para crear un usuario en el sistema para la persona registrada.
# data: Datos provenientes del formulario.
# Retorna: Objeto User creado.
def __crearUsuario(data):
    nomUsuario = data.get('rut')
    pwdUsuario = data.get('rut').replace('-', '')[:5]
    emlUsuario = data.get('email')
    frtUsuario = data.get('nombre')
    lstUsuario = data.get('apellido')
    miUsuario = User.objects.create_user(
        username=nomUsuario,
        email=emlUsuario,
        password=pwdUsuario,
        first_name=frtUsuario,
        last_name=lstUsuario)
    miUsuario.is_staff = False
    miUsuario.is_superuser = False
    miUsuario.save()
    return miUsuario


# __datosPersona: Funcion para agregar los datos de una persona a la base de datos.
# miPersona: Objeto de tipo persona a quien se asignaran los datos.
# data: Objeto de datos provenientes del formulario de registro.
# Retorna: Objeto persona con los datos agregados o actualizados.
def __datosPersona(miPersona, data):
    miPersona.nombre = data.get('nombre')
    miPersona.apellido = data.get('apellido')
    miPersona.rut = data.get('rut')
    miPersona.nacimiento = data.get('nacimiento')
    miPersona.email = data.get('email')
    miPersona.telefono = data.get('telefono')
    miPersona.region = data.get('region')
    miPersona.ciudad = data.get('ciudad')
    miPersona.vivienda = data.get('vivienda')
    return miPersona


# __enviarCorreo: Funcion que permite enviar correos electronicos de informacion a los usuarios cuando se registran.
# miUusuario: Parametro de tipo Persona el cual contien los datos del postulante registrado.
def __enviarCorreo(miUsuario):
    nomUsuario = miUsuario.rut
    pwdUsuario = miUsuario.rut.replace('-', '')[:5]
    salto = '\n'
    cuerpo = "Bienvenido " + miUsuario.nombre + "!" + salto + salto
    cuerpo = "Se ha registrado correctamente en nuestro sitio, esperamos que pueda encontrar una mascota para adoptar." + salto
    cuerpo = cuerpo + "Sus credenciales para entrar al sitio son las siguientes:" + salto
    cuerpo = cuerpo + "Nombre de usuario: " + nomUsuario + salto
    cuerpo = cuerpo + "Contraseña: " + pwdUsuario + salto + salto
    cuerpo = cuerpo + "Esperamos que disfrute su estadía con nosotros y logre encontrar a su mascota deseada." + salto + salto
    cuerpo = cuerpo + "Atentamente," + salto
    cuerpo = cuerpo + "Fundación Mis Perris"
    send_mail(
        'Fundación Mis Perris: Registro.',
        cuerpo,
        'stngarcia8@gmail.com',
        [miUsuario.email],
    )


# adoptarDisponible: Vista para realizar la adopcion por parte del usuario.
# request: Objeto que realiza la peticion.
# pkPersona: Corresponde al id de la persona que adopta.
# pkMascota: Corresponde al id de la mascota que sera adoptada.
@login_required(login_url='iniciarSesion')
def adoptarDisponible(request, pkPersona, pkMascota):
    if request.user.is_superuser:
        return redirect('sinAcceso')
    # buscar las instancias de la persona y de la mascota.
    miPersona = Persona.objects.get(id=pkPersona)
    miMascota = Mascota.objects.get(id=pkMascota)
    # Agregar la adopcion al modelo de adopcion.
    miAdopcion = Adopcion()
    miAdopcion.idPersona = miPersona
    miAdopcion.idMascota = miMascota
    miAdopcion.save()
    # marcar la mascota como adoptada.
    miMascota.estado = 'a'
    miMascota.save()
    # por ultimo volver a la lista de disponibles.
    return redirect('listaRescatados')


# dejarAdopcion: Vista para deshacer una adopcion.
# request: Objeto que realiza la peticion.
# pkPersona: Corresponde al id de la persona que adopto.
# pkMascota: Corresponde al id de la mascota que fue adoptada.
@login_required(login_url='iniciarSesion')
def dejarAdopcion(request, pkPersona, pkMascota):
    if request.user.is_superuser:
        return redirect('sinAcceso')
    # buscar las instancias de la persona y de la mascota.
    miPersona = Persona.objects.get(id=pkPersona)
    miMascota = Mascota.objects.get(id=pkMascota)
    # buscar la adopcion y quitarla de la base de datos.
    miAdopcion = Adopcion.objects.filter(
        Q(idPersona=miPersona) & Q(idMascota=miMascota))
    miAdopcion.delete()
    # Dejar la mascota disponible.
    miMascota.estado = 'd'
    miMascota.save()
    # Volver a la pantalla de informacion de la persona.
    return redirect('infoPersona', nomUsuario=miPersona.rut)


# infoPersona: Vista para visualizar la informacion de la persona.
# nomUsuario: Nombre del usuario a mostrar informacion.
@login_required(login_url='iniciarSesion')
def infoPersona(request, nomUsuario):
    if request.user.is_superuser:
        return redirect('sinAcceso')
    # Obtener la instancia de la persona.
    miPersona = Persona.objects.get(rut=nomUsuario)
    # Obtener la lista de mascotas adoptadas.
    misAdoptados = Adopcion.objects.filter(idPersona=miPersona)
    plantilla = loader.get_template("infoPersona.html")
    contexto = {
        'persona': miPersona,
        'mascotas': __paginarResultados(request, misAdoptados, 10)
    }
    return HttpResponse(plantilla.render(contexto, request))


# solicitarBajaPersona: Vista para confirmar la baja de la persona del sitio.
# request: Objeto que realiza la peticion.
# pk: id de la persona que dara de baja el servicio.
@login_required(login_url='iniciarSesion')
def solicitarBajaPersona(request, pk):
    if request.user.is_superuser:
        return redirect('sinAcceso')
    miPersona = Persona.objects.get(id=pk)
    plantilla = loader.get_template("confirmarBaja.html")
    contexto = {'persona': miPersona}
    return HttpResponse(plantilla.render(contexto, request))


# eliminarPersona: Vista que elimina el registro de la persona en la base de datos.
# request: Objeto que realiza la peticion.
# pk: Identificador de la persona.
@login_required(login_url='iniciarSesion')
def eliminarPersona(request, pk):
    if request.user.is_superuser:
        return redirect('sinAcceso')
    # Cerrar la sesion antes de eliminar.
    logout(request)
    # Obtener a la persona y el usuario relacionado.
    miPersona = Persona.objects.get(id=pk)
    miUsuario = Persona.usuario
    # eliminando objetos.
    miUsuario = User.objects.get(username=miPersona.rut).delete()
    miPersona.delete()
    # Despedirse.
    plantilla = loader.get_template("adios.html")
    return HttpResponse(plantilla.render({}, request))


# experienciaAdopcion: Vista para agregar una experiencia de adopcion.
# pkPersona: Identificador de la persona
# pkMascota: Identificador de la mascota que  agregaran experiencia
@login_required(login_url='iniciarSesion')
def experienciaAdopcion(request, pkPersona, pkMascota):
    if request.user.is_superuser:
        return redirect('sinAcceso')
    if request.method == "POST":
        form = registrarExperienciaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # buscar las instancias de la persona y de la mascota.
            miPersona = Persona.objects.get(id=pkPersona)
            miMascota = Mascota.objects.get(id=pkMascota)
            # buscar la adopcion para agregar la experiencia.
            miAdopcion = Adopcion.objects.get(
                Q(idPersona=miPersona) & Q(idMascota=miMascota))
            miAdopcion.descripcion = data.get('descripcion')
            miAdopcion.save()
            return redirect('infoPersona', nomUsuario=miPersona.rut)
    else:
        # buscar las instancias de la persona y de la mascota.
        miPersona = Persona.objects.get(id=pkPersona)
        miMascota = Mascota.objects.get(id=pkMascota)
        # buscar la adopcion para agregar la experiencia.
        miAdopcion = Adopcion.objects.get(
            Q(idPersona=miPersona) & Q(idMascota=miMascota))
        form = registrarExperienciaForm(instance=miAdopcion)
    return render(request, "registrarExperiencia.html", {
        'form': form,
        'mascota': miMascota
    })


# restaurarContrasena: Vista para iniciar el proceso de restauracion de la contraseña
# request: Objeto que realiza la peticion.
def restaurarContrasena(request):
    return render(request, "restaurarContrasena.html")


# restaurarContrasenaEnviada: Vista que indica que se restauro la contrasena.
# request: Objeto que realiza la peticion.
def restaurarContrasenaEnviada(request):
    return render(request, "restaurarContrasenaEnviada.html")


# sinAcceso: Vista utilizada para mostrar mensaje de restriccion de acceso.
# Retorna: Redirige a una pagina que indica que el usuario no tiene acceso.
@login_required(login_url='iniciarSesion')
def sinAcceso(request):
    plantilla = loader.get_template("sinAcceso.html")
    return HttpResponse(plantilla.render({}, request))
