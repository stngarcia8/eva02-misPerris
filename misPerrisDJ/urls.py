from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [

    # rutas para el control de sesion.
    url(r'^iniciarSesion/$', views.iniciarSesion, name="iniciarSesion"),
    url(r'^cerrarSesion/$', views.cerrarSesion, name="cerrarSesion"),
    url(
        r'^restaurarContrasena/$',
        auth_views.PasswordResetView.as_view(
            template_name='restaurarContrasena.html',
            email_template_name='restaurarContrasenaEmail.html',
        ),
        name='password_reset',
    ),
    url(
        r'^restaurarContrasenaEnviada/done/$',
        auth_views.PasswordResetDoneView.as_view(
            template_name='restaurarContrasenaEnviada.html', ),
        name='password_reset_done',
    ),
    url(
        r'^restaurarContrasenaEnviada/done/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('password_reset_complete'),
            post_reset_login=True,
            template_name='restaurarContrasenaConfirmar.html',
            post_reset_login_backend=(
                'django,contrib.auth.backend.AllowAllUsersModelBackend'),
        ),
        name='password_reset_confirm',
    ),
    url(
        r'^restaurarContrasenaCompleta',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='restaurarContrasenaCompleta.html', ),
        name='password_reset_complete',
    ),

    # rutas para el mantenedor de mascotas rescatadas.
    url(r'^mantenedorRescatados/$',
        views.mantenedorRescatados,
        name="mantenedorRescatados"),
    url(r'^nuevoRescatado/$', views.nuevoRescatado, name="nuevoRescatado"),
    url(r'^modificarRescatado/(?P<pk>\d+)/$',
        views.modificarRescatado,
        name="modificarRescatado"),
    url(r'^eliminarRescatado/(?P<pk>\d+)/$',
        views.eliminarRescatado,
        name="eliminarRescatado"),
    url(r'^verRescatado/(?P<pk>\d+)/$',
        views.verRescatado,
        name="verRescatado"),
    url(r'^cambiarRescatado/(?P<pk>\d+)/$',
        views.cambiarRescatado,
        name="cambiarRescatado"),
    url(r'^cambiarDisponible/(?P<pk>\d+)/$',
        views.cambiarDisponible,
        name="cambiarDisponible"),

    # Rutas para las opciones de los usuarios.
    url(r'^listaRescatados/$', views.listaRescatados, name="listaRescatados"),
    url(r'^registrarPersona/$',
        views.registrarPersona,
        name="registrarPersona"),
    url(r'^adoptarDisponible/(?P<pkPersona>\d+)/(?P<pkMascota>\d+)/$',
        views.adoptarDisponible,
        name="adoptarDisponible"),
    url(r'^experienciaAdopcion/(?P<pkPersona>\d+)/(?P<pkMascota>\d+)/$',
        views.experienciaAdopcion,
        name="experienciaAdopcion"),
    url(r'^dejarAdopcion/(?P<pkPersona>\d+)/(?P<pkMascota>\d+)/$',
        views.dejarAdopcion,
        name="dejarAdopcion"),
    url(r'^infoPersona/(?P<nomUsuario>([0-9]{6,8}-[0-9Kk]))/$',
        views.infoPersona,
        name="infoPersona"),
    url(r'^solicitarBajaPersona/(?P<pk>\d+)/$',
        views.solicitarBajaPersona,
        name="solicitarBajaPersona"),
    url(r'^eliminarPersona/(?P<pk>\d+)/$',
        views.eliminarPersona,
        name="eliminarPersona"),

    # Ruta para la pagina de inicio.
    url(r'^$', views.index, name="inicio"),

    # Ruta para denegar acceso.
    url(r'^sinAcceso$', views.sinAcceso, name="sinAcceso"),
]
