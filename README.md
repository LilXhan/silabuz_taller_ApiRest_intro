# Taller

## Pre requisitos

1.  Crear entorno virtual.
    
2.  Instalar Django > 4.0.
    
3.  Instalar Django Rest Framework.
    

```shell
pip install djangorestframework
```

4.  Creamos nuestra app `todos`.

```shell
python manage.py startapp todos
```

5.  Añadimos la aplicación y el `rest_framework` a nuestro `settings.py`.

```py
INSTALLED_APPS = [
    # ...
    'todos',
    'rest_framework',
]
```

6.  Ejecutamos nuestra aplicación.

Para este tutorial, utilizaremos sqlite por lo que no necesitaremos hacer la conexión a otra base de datos.

## Creando modelo

Creamos nuestro modelo para los TODOS:

```py
class Todo(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    done_at = models.DateField(null=True)
    updated_at = models.DateField(auto_now_add=True)
    deleted_at = models.DateField(null=True)
    status = models.IntegerField(default=0)
```

Realizamos las migraciones

```shell
python manage.py makemigrations todos
python manage.py migrate
```

## ViewSets

Un viewSet es la forma en la que Django va a poder convertir los datos de Python en objetos JSON, que puedes ser consultados por el cliente.

Para poder crear nuestro primer serializador de los datos de Python, creamos el archivo `serializer.py` dentro de nuestra app `todos`.

```py
from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = (
            "id",
            "title",
            "body",
            "created_at",
            "done_at",
            "updated_at",
            "deleted_at",
            "status",
        )
        read_only_fields = ('created_at', 'done_at', 'updated_at', 'deleted_at',)
```

-   `serializers.ModelSerializer`, permite crear la serialización de nuestros datos en base a un modelo que nosotros creemos.
    
-   Dentro de la clase `Meta`, indicamos que campos van a ser extraídos de la base de datos con `fields` y `read_only_fields`, determina cuales campos son únicamente de lectura.
    

> Importante mantener la coma al final en `read_only_fields` para que el framework lo reconozca como una tupla y no como un string.

> Si no queremos hacerlo de esta forma, simplemente podemos omitir los paréntesis y la coma del final, funcionará de la misma forma.

```py
read_only_fields = 'created_at', 'done_at', 'updated_at', 'deleted_at'
```

Otra forma:

```py
read_only_fields = ('created_at', 'done_at', 'updated_at', 'deleted_at', )
```

## API

Ahora crearemos un nuevo archivo dentro de nuestra aplicación `todos`, llamado `api.py`, el cual contendrá lo siguiente:

```py
from .models import Todo
from rest_framework import viewsets, permissions

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    permission_classes = [permissions.AllowAny]
```

-   Con `viewsets`, importamos el modulo que nos permitirá indicar que tipo de consultas se van a poder hacer a nuestros datos, y con `permissions` definir quienes pueden hacer uso de ellos, por ahora admitiremos cualquier cliente, después podremos definirlo para que únicamente puedan acceder usuarios autenticados.
    
-   Con `serializer_class` definimos a partir de que serializer va a estar utilizando estos datos, en otras palabras como van a ser convertidos nuestros datos de Python.
    

Con esto ya tendríamos nuestra API creada, pero todavía falta agregar las rutas.

## Rutas con rest_framework

`rest_framework` nos ofrece la posibilidad de crear las rutas del CRUD de nuestros datos mediante un módulo especial llamado `routers`. Para utilizarlo, creamos el archivo `urls.py` dentro de nuestra aplicación.

```py
from rest_framework import routers
from .api import TodoViewSet

router = routers.DefaultRouter()

router.register('api/todos', TodoViewSet, 'todos')

urlpatterns = router.urls
```

Al momento de utilizar `.DefaultRouter()` creamos nuestra variable que va a contener todo nuestro CRUD. Dentro de cada registro del router, indicamos la ruta, el viewset y el nombre de la ruta.

Por último, añadiremos las nuevas rutas a nuestra carpeta principal, dentro de `drfcrud/urls.py`.

```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todos.urls')),
]
```

Ahora si ejecutamos nuestro servidor, veremos que la ventada principal nos va a mostrar nuestras rutas registradas.

![Nuevas rutas](https://photos.silabuz.com/uploads/big/3c7608b36225bcae9569da6783aea009.PNG)

Django Rest Framework, coloca por defecto una documentación automática de nuestras rutas creadas.

Si ingresamos a `http://127.0.0.1:8000/api/todos/`, deberíamos obtener la siguiente vista, en la que vamos a poder agregar algunos registros a nuestra base de datos.

![Post](https://photos.silabuz.com/uploads/big/cfa8cda5292c36342371f0fc6332af25.PNG)

Si creamos el registro, obtendremos la siguiente vista.

![Post Completo](https://photos.silabuz.com/uploads/big/bd611347406e1bb4ea41cfea0d971a8c.PNG)

De esta forma ya hemos registrado nuestro primer TODO dentro de la base de datos.

Además, con nuestro servidor ejecutándose, podemos hacer las peticiones desde otros API clients.

![Petición desde otro cliente](https://photos.silabuz.com/uploads/big/f9f6c8e00bea9adf76581ce07748e817.PNG)

Por lo cual, podemos hacer POST desde estos clientes a nuestra API.

![Post](https://photos.silabuz.com/uploads/big/7c5c9bb20f9011b051d9cad08aeec120.PNG)

Entonces, con una única ruta creada, podemos realizar todo el CRUD de nuestra aplicación. Esta ruta podemos utilizarla en nuestro frontend para realizar el CRUD completo pero desde el lado del cliente.

### Links
Videos:
[Teoria](https://www.youtube.com/watch?v=t4QZp1TQZp4&list=PLxI5H7lUXWhgHbHF4bNrZdBHDtf0CbEeH&index=1&ab_channel=Silabuz)
[Practica](https://www.youtube.com/watch?v=J-K0oehNI-8&list=PLxI5H7lUXWhgHbHF4bNrZdBHDtf0CbEeH&index=2&ab_channel=Silabuz)
Diapositivas:
[Slide](https://docs.google.com/presentation/d/e/2PACX-1vTOc4XAwHV8cn1hHbwH3lYiCEzzMEUjwGcC7tbVF4z4rpR_nI83b1O987LQnTKt9rg7uUdTE7Z9jGAJ/embed?start=false&loop=false&delayms=3000&slide=id.g143f30675af_0_0)
