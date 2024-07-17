from django.contrib import admin
from .models import Pelicula
from .models import Actor
from .models import Director
from .models import Nota

# Register your models here.
admin.site.register(Pelicula)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Nota)