from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Pelicula
from .models import Actor
from .models import Director
from .models import Nota
from .forms import PeliculaForm
import random

# Create your views here.
def inicio(request):
    peliculaportada = Pelicula.objects.exclude(resenia__isnull=True).all()
    cantidad = len(peliculaportada)
    portada = random.randrange(1, cantidad+1)
    peliculaportada = Pelicula.objects.get(id=portada)
    peliculaportadatexto = peliculaportada.resenia[0:200]+'...'

    nota = Nota.objects.all()
    cantidad = len(nota)
    notarandom = random.randrange(1, cantidad+1)
    nota = Nota.objects.get(id=notarandom)

    peliculas = Pelicula.objects.exclude(resenia__isnull=True).all().order_by('-id')[1:4]

    peliculaultima = Pelicula.objects.exclude(resenia__isnull=True).all()
    cantidad = len(peliculaultima)
    portada = cantidad
    peliculaultima = Pelicula.objects.get(id=portada)
    peliculaultimatexto = peliculaultima.resenia[0:400]+'...'

    peliculassinresenia = Pelicula.objects.filter(vista=True).exclude(resenia__isnull=False).all()
    peliculasproximamente = Pelicula.objects.filter(vista=False).exclude(resenia__isnull=False).all()

    return render(request, 'paginas/inicio.html', {'peliculas': peliculas, 
        'peliculassinresenia': peliculassinresenia, 
        'peliculasproximamente': peliculasproximamente, 
        'peliculaultima': peliculaultima,
        'peliculaultimatexto': peliculaultimatexto, 
        'peliculaportada': peliculaportada,
        'peliculaportadatexto': peliculaportadatexto, 'notaportada': nota})

def registro(request):

    if request.method == 'GET':
        return render(request, 'paginas/registro.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('inicio')
            except:
                return render(request, 'paginas/registro.html', {
                    'form': UserCreationForm,
                    "error": 'El usuario ya existe'
                })
                
        return render(request, 'paginas/registro.html', {
                    'form': UserCreationForm,
                    "error": 'Las passwords no coinciden'
                })

def iniciarsesion(request):
    if request.method == 'GET':
        return render(request, 'paginas/iniciarsesion.html', {
            'form': AuthenticationForm
    })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'paginas/iniciarsesion.html', {
                'form': AuthenticationForm,
                "error": 'Usuario o password incorrecto'
             })
        else:
            login(request, user)
            return redirect('inicio')

def cerrarsesion(request):
    logout(request)
    return redirect('inicio')

def nosotros(request):
    return render(request, 'paginas/nosotros.html')

def queeselfilmnoir(request):
    return render(request, 'paginas/queeselfilmnoir.html')
    
def buscador(request):
    peliculas = []
    queryset = request.GET.get("buscar")
    if queryset:
        peliculas = (Pelicula.objects.filter(nombre__icontains=queryset).all() | 
            Pelicula.objects.filter(director__icontains=queryset).all() | 
            Pelicula.objects.filter(actor_1__icontains=queryset).all() | 
            Pelicula.objects.filter(actor_2__icontains=queryset).all() | 
            Pelicula.objects.filter(actor_3__icontains=queryset).all() | 
            Pelicula.objects.filter(actor_4__icontains=queryset).all() | 
            Pelicula.objects.filter(actor_5__icontains=queryset).all() | 
            Pelicula.objects.filter(actor_6__icontains=queryset).all()).exclude(resenia__isnull=True).all().order_by('anio', 'nombre')    
    
    return render(request, 'paginas/buscador.html', {'peliculas': peliculas, 'buscador': queryset})

@login_required
def abmpeliculas(request):
    peliculas = Pelicula.objects.all().order_by('id')
    return render(request, 'peliculas/index.html', {'peliculas': peliculas})

def peliculas(request):
    peliculas = Pelicula.objects.exclude(resenia__isnull=True).all().order_by('nombre')
    cantidad = len(peliculas)
    return render(request, 'paginas/peliculas.html', {'peliculas': peliculas, 'cantidad': cantidad})

def notas(request):
    notas = Nota.objects.all().order_by('titulo')
    cantidad = len(notas)
    return render(request, 'paginas/notas.html', {'notas': notas, 'cantidad': cantidad})

def peliculascajitas(request):
    peliculas = Pelicula.objects.exclude(resenia__isnull=True).all().order_by('anio', 'nombre')
    cantidad = len(peliculas)
    return render(request, 'paginas/peliculas-cajitas.html', {'peliculas': peliculas, 'cantidad': cantidad})

def peliculasxgenero(request, genero):
    peliculas = Pelicula.objects.filter(genero=genero).exclude(resenia__isnull=True).all().order_by('anio', 'nombre')
    cantidad = len(peliculas)
    return render(request, 'paginas/peliculas.html', {'peliculas': peliculas, 'genero': genero, 'cantidad': cantidad })

def peliculasxsubgenero(request, subgenero):
    peliculas = []
    peliculas = (Pelicula.objects.filter(subgenero1=subgenero).all() | 
        Pelicula.objects.filter(subgenero2=subgenero).all() | 
        Pelicula.objects.filter(subgenero3=subgenero)).all().exclude(resenia__isnull=True).order_by('anio', 'nombre')

    cantidad = len(peliculas)
    return render(request, 'paginas/peliculas.html', {'peliculas': peliculas, 'subgenero': subgenero, 'cantidad': cantidad })

def peliculasxpais(request, pais):
    peliculas = Pelicula.objects.filter(pais=pais).exclude(resenia__isnull=True).all().order_by('anio', 'nombre')
    cantidad = len(peliculas)
    return render(request, 'paginas/peliculas.html', {'peliculas': peliculas, 'pais': pais, 'cantidad': cantidad })

def peliculasxordenresenia(request):
    peliculas = Pelicula.objects.exclude(resenia__isnull=True).all().order_by('id')
    cantidad = len(peliculas)
    return render(request, 'paginas/peliculasxordenresenia.html', {'peliculas': peliculas, 'cantidad': cantidad})

def peliculasxanioygenero(request):
    genero = 'NO NOIR'
    peliculas_nonoir = Pelicula.objects.filter(genero=genero).exclude(resenia__isnull=True).all().order_by('anio')
    cantidad_nonoir = len(peliculas_nonoir)

    genero = 'PRE NOIR'
    peliculas_prenoir = Pelicula.objects.filter(genero=genero).exclude(resenia__isnull=True).all().order_by('anio')
    cantidad_prenoir = len(peliculas_prenoir)

    genero = 'NOIR'
    peliculas_noir = Pelicula.objects.filter(genero=genero).exclude(resenia__isnull=True).all().order_by('anio')
    cantidad_noir = len(peliculas_noir)

    genero = 'POST NOIR'
    peliculas_postnoir = Pelicula.objects.filter(genero=genero).exclude(resenia__isnull=True).all().order_by('anio')
    cantidad_postnoir = len(peliculas_postnoir)

    genero = 'POLAR'
    peliculas_polar = Pelicula.objects.filter(genero=genero).exclude(resenia__isnull=True).all().order_by('anio')
    cantidad_polar = len(peliculas_polar)

    genero = 'NEO NOIR'
    peliculas_neonoir = Pelicula.objects.filter(genero=genero).exclude(resenia__isnull=True).all().order_by('anio')
    cantidad_neonoir = len(peliculas_neonoir)

    cantidad_total = cantidad_nonoir + cantidad_prenoir + cantidad_noir + cantidad_postnoir + cantidad_polar + cantidad_neonoir

    return render(request, 'paginas/peliculasxanioygenero.html', {
            'peliculas_nonoir': peliculas_nonoir, 'cantidad_nonoir': cantidad_nonoir,
            'peliculas_prenoir': peliculas_prenoir, 'cantidad_prenoir': cantidad_prenoir,
            'peliculas_noir': peliculas_noir, 'cantidad_noir': cantidad_noir,
            'peliculas_postnoir': peliculas_postnoir, 'cantidad_postnoir': cantidad_postnoir,
            'peliculas_polar': peliculas_polar, 'cantidad_polar': cantidad_polar,
            'peliculas_neonoir': peliculas_neonoir, 'cantidad_neonoir': cantidad_neonoir,
            'cantidad_total': cantidad_total })


def peliculasxordenanio(request):
    peliculas = Pelicula.objects.exclude(resenia__isnull=True).all().order_by('anio')
    cantidad = len(peliculas)
    return render(request, 'paginas/peliculasxordenanio.html', {'peliculas': peliculas, 'cantidad': cantidad})

def top10(request):
    peliculas = Pelicula.objects.filter(top10=True).exclude(resenia__isnull=True).all()
    return render(request, 'paginas/top10.html', {'peliculas': peliculas})

def listado(request):
    return render(request, 'paginas/lista-filmnoirboard.html')

def actores(request):
    actores = []
    peliculas = Pelicula.objects.all()
    for pelicula in peliculas:
        actor = pelicula.actor_1
        if actor:
            if actor not in actores:
                actores.append(actor)

        actor = pelicula.actor_2
        if actor:
            if actor not in actores:
                actores.append(actor)

        actor = pelicula.actor_3
        if actor:
            if actor not in actores:
                actores.append(actor)

        actor = pelicula.actor_4
        if actor:
            if actor not in actores:
                actores.append(actor)

        actor = pelicula.actor_5
        if actor:
            if actor not in actores:
                actores.append(actor)

        actor = pelicula.actor_6
        if actor:
            if actor not in actores:
                actores.append(actor)

    actores.sort()

    tipo = 'crack masculino'
    cracks_m_imgs = Actor.objects.filter(tipo=tipo).all().order_by('nombreactor') 

    tipo = 'crack femenina'
    cracks_f_imgs = Actor.objects.filter(tipo=tipo).all().order_by('nombreactor') 

    tipo = 'una pelicula'
    una_pelicula_imgs = Actor.objects.filter(tipo=tipo).all().order_by('nombreactor') 

    tipo = 'primera linea femenina'
    primeralinea_f_imgs = Actor.objects.filter(tipo=tipo).all().order_by('nombreactor') 

    tipo = 'primera linea masculina'
    primeralinea_m_imgs = Actor.objects.filter(tipo=tipo).all().order_by('nombreactor') 

    tipo = 'secundario'
    secundario_m_imgs = Actor.objects.filter(tipo=tipo).all().order_by('nombreactor') 

    return render(request, 'paginas/actores.html', {'actores': actores,
        'cracks_f_imgs': cracks_f_imgs,
        'cracks_m_imgs': cracks_m_imgs,
        'una_pelicula_imgs': una_pelicula_imgs,
        'primeralinea_f_imgs': primeralinea_f_imgs,
        'primeralinea_m_imgs': primeralinea_m_imgs,
        'secundario_m_imgs': secundario_m_imgs
                                                        })

def directores(request):
    directores = []
    peliculas = Pelicula.objects.all()
    for pelicula in peliculas:
        director = pelicula.director
        if director not in directores:
            directores.append(director)
    directores.sort()

    directores_imgs = Director.objects.all().order_by('nombredirector') 

    tipo = 'esencial'
    directores_e_imgs = Director.objects.filter(tipo=tipo).all().order_by('nombredirector') 

    tipo = 'destacado'
    directores_d_imgs = Director.objects.filter(tipo=tipo).all().order_by('nombredirector') 

    return render(request, 'paginas/directores.html', {'directores': directores,
        'directores_imgs': directores_imgs,
        'directores_e_imgs': directores_e_imgs,
        'directores_d_imgs': directores_d_imgs
        })

def crear(request):
    formulario = PeliculaForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('peliculas')
    return render(request, 'peliculas/crear.html', {'formulario': formulario})

def editar(request, id):
    pelicula = Pelicula.objects.get(id=id)
    formulario = PeliculaForm(request.POST or None, request.FILES or None, instance=pelicula)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('peliculas')
    return render(request, 'peliculas/editar.html', {'formulario': formulario})

def buscar(request, aBuscar):
    peliculas = Pelicula.objects.filter(nombre__icontains=aBuscar).exclude(resenia__isnull=True).all().order_by('anio', 'nombre')
    return render(request, 'peliculas/mostrar.html', {'peliculas': peliculas})

def buscarDirector(request, director):
    peliculas = []
    peliculas = Pelicula.objects.filter(director=director).exclude(resenia__isnull=True).all().order_by('anio', 'nombre')

    directores = []
    directores = Director.objects.filter(nombredirector=director).all() 
    return render(request, 'paginas/buscador.html', {'peliculas': peliculas, 'director': director, 'directores': directores})

def buscarActor(request, actor):
    peliculas = []
    peliculas = (Pelicula.objects.filter(actor_1=actor).all() | 
    Pelicula.objects.filter(actor_2=actor).all() | 
    Pelicula.objects.filter(actor_3=actor).all() | 
    Pelicula.objects.filter(actor_4=actor).all() | 
    Pelicula.objects.filter(actor_5=actor).all() | 
    Pelicula.objects.filter(actor_6=actor).all()).exclude(resenia__isnull=True).order_by('anio', 'nombre')

    actores = []
    actores = Actor.objects.filter(nombreactor=actor).all() 
    return render(request, 'paginas/buscador.html', {'peliculas': peliculas, 'actor': actor, 'actores': actores})

def eliminar(request, id):
    pelicula = Pelicula.objects.get(id=id)
    pelicula.delete()
    return redirect('peliculas')

def reseniaPelicula(request, id):
    peliculas = Pelicula.objects.get(id=id)
    return render(request, 'paginas/reseniaPelicula.html', {'peliculas': peliculas})
