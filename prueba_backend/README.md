# API Rest full de modulo de usuarios en Django con los siguientes endpoints

## Instalar modulos requeridos (entorno activado) 
```
pip install -r requeriments.txt
```
## Crear migraciones (haber creado antes una db en postgresql 'db_prueba' y estar ubicado en directorio del proyecto 'prueba_backend')
```
python manage.py makemigrations
```
```
python manage.py migrate
```
## Crear un superusuario
```
python manage.py createsuperuser
```

## Correr el servidor de django
```
python manage.py runserver
```

# Enpoints de CRUD de usuarios
### Crear un usuario correctamente
```
POST/api/user/ {"name":"Bunker","last_name":"Develores","username":"BunkerDevelopers","email":"BunkerDeveloers@gmail.com","password":"bunkerdevelopers"}
201 {
        "message": "user created successfully",
        "user": {
            "username": "BunkerDevelopers",
            "email": "BunkerDevelopers@hotmail.com",
            "name": Bunker,
            "last_name": Develores,
            "tokens": {
                "refresh": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "access": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
            }
        }
    }
```

### Crear usuario incorrectamente ( con algún campo requerido("username","email" o "password") faltante)
```
POST/api/user/ {"name":"Bunker_new","last_name":"Develores_new","email":"BunkerDeveloers_new@gmail.com","password":"bunkerdevelopers_new"}
400 {   "message": "error during user creation",
        "error": {
            "username": [
                "This field is required."
            ]
        }
    }
```

### Listar usuarios
```
GET/api/user
200 { "users":
        ...
        [ 
            {  
            "id": 2,
            "username": "BunkerDevelopers",
            "email": "BunkerDeveloers@gmail.com",
            "name": "Bunker",
            "last_name": "Develores"
            }
        ] 
    }
```

### Obtener usuario existente
```
GET/api/user/2
200 {
    "user": {
        "id": 2,
        "username": "BunkerDevelopers",
        "name": "Bunker",
        "last_name": "Develores",
        "email": "BunkerDeveloers@gmail.com",
        "password": "pbkdf2_sha256$260000$evDyH77xzgKJkJmuojSmgV$+HuNKoPKVII3kJv9mEv9bl6IzMfLF8kphgnkVaLlbEM="
    }
}
```

### Obtener usuario inexistente

```
GET/api/user/100
400 {"error:":"User not found, wrong request"}
```

### Actualizar usuario existente
```
PUT/api/user/2/  {"username": "BunkerDevelopers_up","email": "BunkerDevelopers_up@gmail.com","password":"bunkerdevelopers_up"}
200 {
    "message": "successful update",
    "user": {
        "id": 2,
        "username": "BunkerDevelopers_up",
        "name": "Bunker",
        "last_name": "Develores",
        "email": "BunkerDeveloers_up@gmail.com",
        "password": "pbkdf2_sha256$260000$evDyH77xzgKJkJmuojSmgV$+HuNKoPKVII3kJv9mEv9bl6IzMfLF8kphgnkVaLlbEM="
    }
}
```
### Actualizar usuario inexistente
```
PUT/api/user/100/  {"username":"BunkerDevelopers_update","email":"BunkerDevelopers_update@gmail.com"}
400 { "error:": "User not found, wrong request." }
```

### Eliminar usuario existente
```
DELETE/api/user/2/
200 {"message":"removed BunkerDevelopers_update successfully"}
```

## Endpoints de CRUD de roles de usuarios

### Crear un nuevo rol
```
POST/api/rol {"rol":"USER_CLIENT"}
201 { 
        "Message": "successfully created role",
        "Rol": {
        "id": 1,
        "rol": "USER_CLIENT"
    }
}
```

### Listar los roles de usuarios
```
GET/api/rol
200 {
        ...
        {
            id": 2,
            "rol": "USER_CLIENT"
        }
    }
```

### Actualizar un rol de usuario exitosa
```
PUT/api/rol/1 { "rol": "USER_CLIENT_UPDATE"}
200 {
        "message": "successful role upgrade.",
        "rol": {
            "id": 1,
            "rol": "USER_CLIENT_UPDATE"
        }
    }
```

### Actualizar un rol de usuario inexistente
```
PUT/api/rol/100
400 {
        "message:": "Role not found, check entered value"
    } 
```

### Obtener un Rol existente
```
GET/api/rol/1
200 {
        "id": 1,
        "rol": "USER_CLIENT_UPDATE"
    }
```

### Obtener un rol inexistente
```
GET/api/rol/100
400 {
        "message:": "Role not found, check entered value"
    }
```

### Eliminar un rol
```
DELETE/api/rol/1
200 {
        "message": "USER_CLIENT_UPDATE role removed successfully."
    }
```

## CRUD de permisos

### Listar los permisos del modelo "Permission" de Django
```
GET/api/permission
200 [ 
        {
            "id": 1,
            "name": "Can add log entry",
            "codename": "add_logentry",
            "content_type": 1 
        },
        ...
    ]
```
### Nota:  Para consideración los "content_type" a considerar son: User y Rol (usuarios y roles), y los "permission" basicos (parametro "action") son: add, view, change, delete, (agregar, ver, cambiar, eliminar), sin embargo puede usarse nuevas acciones por permitir

### Crear un permiso con exito
```
POST/api/permission/ {"content":"user","action":"add"} 
201 {
        "message": "Permission created successfully."
    }
```
### Crear un permiso sin exito
```
POST/api/permission/ {"content":"user"} 
400 {
        "error": "missing 'action' value."
    }
```
### Obtener un permiso existente
```
GET/api/permission/1
200 {
        "id": 1,
        "name": "Can add log entry",
        "codename": "add_logentry",
        "content_type": 1
    }
```

### Obtener un permiso inexistente
```
GET/api/permission/100
400 {
        "error:": "Permission not found, check the data"
    }
```

### Actualizar un permiso existente
```
PUT/api/permission/1/ {"content":"User","action":"change_up"}
200 {
        "message": "Permission updated successfully."
    }
```

### Actualizar un permiso inexistente
```
PUT/api/permission/100 {"content":"User","action":"add_act"}
400 {
        "error:": "Permission not found, check the data"
    }
```

### Eliminar un permiso existente
```
DELETE/api/permission/1
200 {
        "message": "permission removed successfully.",
        "permission deleted": "Can change_up user"
    }
```

## Autenticación con nombre de usuario (username)
### Registro de usuario exitoso
```
POST/register {"username":"BunkerDevelopers02","name":"Bunker","last_name":"Developers","email","talentohumano@bunkerdevelopers.com","password":"password01"}
201 {
    "message": "check your mailbox, we have sent a verification email",
    "user": {
        "username": "BunkerDevelopers02",
        "email": "talentohumano@bunkerdevelopers.com",
        "name": "Bunker",
        "last_name": "Developers",
        "tokens": {
            "refresh": "XXXXXXXXXXXXXXXXXXX",
            "access":  "XXXXXXXXXXXXXXXXXXX"
        }
    }
}
```
```
Nota: En el buzon deverás encontrar un email de remitente luism con un cuerpo como el siguiente

Hola, Bienvenido BunkerDevelopers02
Usa este link para verificar tu registro.
http://localhost:8000/verify_email/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI5MzE1NDQyLCJqdGkiOiI2YWY2ZDA4ZDg4M2U0MWU1OTcxN2M4ZWNhZGZhMjg3ZSIsInVzZXJfaWQiOjZ9.gQOfuT1n-sOI3jkZhIqttH4cn13bu7DswAFqrBJ6B5E

```

### Logueo con "username", creación de token exitoso
```
Conserva el "access_token" y el "refresh" para el siguiente endpoint
```
```
POST/login {"username": "BunkerDevelopers","password": "bunkerdevelopers"}
201 {
    "message": "inicio de seción exitoso",
    "user": {
        "email": "luism3872@gmail.com",
        "username": "LmiguelUG",
        "tokens": {
            "refresh": "XXXXXXXXXXXXXXXX",
            "access":  "XXXXXXXXXXXXXXXX"
        },
        "auth_provider": "username"
    }
}
```


### Deslogueo de usuario exitoso
``` 
POST/logut -H [Authorization: Bearer <Acess_token de endpoint anterior> ] -d { "refresh": <refresh de endpoint anterior>}
200 {"message":"Sesión finalizada"}
```

## Restablecimiento de contraseña
```
El restablecimietno se cumple en tres pasos:
1) solicitud del restablecimiento
2) confirmación de restablecimiento
3) cumpletado 
```
### Etapa 1
```
POST/reset_password {"email": talentohumano@bunkerdevelopers.com}
200 { 'message': 'check your email, you were sent a link to reset your password.'}
```
```
Nota: En el buzon deverás encontrar un email de remitente luism con un cuerpo como el siguiente, Que lo llevará a la etapa 2 ( enlace de confirmación con retorno)

Hola BunkerDevelopers usa este link para reestablecimiento de su contraseña
http://localhost:8000/password_reset_confirm/MQ/arlj81-45a479e8e2c05b96cc2b727783a1f0f5/
```
### Etapa 2
```
Esta etapa es llevada a cabo al clickear el enlace del correo, recibido en la etapa 1
```
```
GET /password_reset_confirm/MQ/arlj81-45a479e8e2c05b96cc2b727783a1f0f5/
200 {
        "success": true,
        "message": "credenciales validas",
        "uidb64": "MQ",
        "token": "arlj81-45a479e8e2c05b96cc2b727783a1f0f5"
    } 
```

### Etapa 3
```
PATCH/password_reset_complete {"uidb64": "<uidb64 obtenido en la etapa 2>","token":"token obtenido en la etapa 2","password":"<new_password>" }
200 {
    "message": "successful password reset."
    }
```

## Autentificación social (facebook y gmail)

### Facebook
```
Nota: Para acceder con facebook en la app dirigase al siguiente enlace, el cual en dado caso el Fronend redieccionaría para hacer la solicitud de inicio de sesión en la aplicación
```
```
https://www.facebook.com/v7.0/dialog/oauth?client_id=4276744392401466&redirect_uri=http://localhost:8000/accounts/facebook&state={%22{st=state123abc,ds=123456789}%22}&scope=email
```

#### Obtendrá
```
    {
        "message": "Login with facebook successful.",
        "user": {
            "username": "migoro67@hotmail.com",
            "email": "migoro67@hotmail.com",
            "auth_provider": "facebook"
        },
        "tokens": {
            "refresh": "xxxxxxxxxxxxxxxxxxxxxxxxxx",
            "access":  "xxxxxxxxxxxxxxxxxxxxxxxxxx"
        }
    }
```

### Google
```
Nota: Para probar este enpoints de la api, en el patio de ejuegos, https://developers.google.com/oauthplayground/ 
seleccione 'Google OAuth2 API v2' y autorice para obtener un token de acceso
```
```
POST/accounts/google/ {"token":"<token obtenido en la sala de juegos de google>"}
200 {
    {
    "message": "user successfully logged in",
    "name": "Bunker",
    "last_name": "Developers",
    "email": "talentohumano@bunkerdevelopers.com",
    "password": "pbkdf2_sha256$260000$cr3HhUa3ypDz5IXW6WqXm2$utaGRJDHJWYor+VkdYm1VZ+WbQqvHboZ7kn5sQB4EGQ=",
    "tokens": {
        "refresh": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "access": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
}
```