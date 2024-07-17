from django.urls import path
from . import views

from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro', views.registro, name='registro'),
    path('cerrarsesion', views.cerrarsesion, name='cerrarsesion'),
    path('iniciarsesion', views.iniciarsesion, name='iniciarsesion'),
    path('nosotros', views.nosotros, name='nosotros'),
    path('queeselfilmnoir', views.queeselfilmnoir, name='queeselfilmnoir'),
    path('buscador', views.buscador, name='buscador'),
    path('peliculas', views.peliculas, name='peliculas'),
    path('notas', views.notas, name='notas'),
    path('peliculascajitas', views.peliculascajitas, name='peliculascajitas'),
    path('peliculasxgenero/<str:genero>', views.peliculasxgenero, name='peliculasxgenero'),
    path('peliculasxsubgenero/<str:subgenero>', views.peliculasxsubgenero, name='peliculasxsubgenero'),
    path('peliculasxpais/<str:pais>', views.peliculasxpais, name='peliculasxpais'),
    path('peliculasxordenresenia', views.peliculasxordenresenia, name='peliculasxordenresenia'),
    path('peliculasxordenanio', views.peliculasxordenanio, name='peliculasxordenanio'),
    path('peliculasxanioygenero', views.peliculasxanioygenero, name='peliculasxanioygenero'),
    path('abmpeliculas', views.abmpeliculas, name='abmpeliculas'),
    path('actores', views.actores, name='actores'),
    path('directores', views.directores, name='directores'),
    path('top10', views.top10, name='top10'),
    path('listado', views.listado, name='listado'),
    path('peliculas/crear', views.crear, name='crear'),
    path('peliculas/editar', views.editar, name='editar'),
    path('eliminar/<int:id>', views.eliminar, name='eliminar'),
    path('editar/<int:id>', views.editar, name='editar'),
    path('buscar/<str:aBuscar>', views.buscar, name='buscar'),
    path('resenia/<int:id>/',views.reseniaPelicula, name = 'resenia_Pelicula'),
    path('buscaractor/<str:actor>/',views.buscarActor, name = 'buscar_actor'),
    path('buscardirector/<str:director>/',views.buscarDirector, name = 'buscar_director')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)