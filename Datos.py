import json
from Usuarios import Profesor,Estudiante
from Publicaciones import Publicacion
from datetime import datetime
import requests

def guardar_usuarios_desde_0(usuarios):
    "Guarda los datos de 'usuarios' en un archivo json."
    with open('usuarios.json', 'w') as file:
        usuarios_data = [
            {
                'id': usuario.identification,
                'firstName': usuario.firstname,
                'lastName': usuario.lastname,
                'email': usuario.email,
                'username': usuario.username,
                'type': 'professor' if isinstance(usuario, Profesor) else 'student',
                'department': getattr(usuario, 'department', None),
                'major': getattr(usuario, 'major', None),
                'following': usuario.following,
                'publicaciones': [publicacion.to_dict() for publicacion in getattr(usuario, 'publicaciones', [])]
            }
            for usuario in usuarios
        ]
        json.dump(usuarios_data, file, indent=4)


def actualizar_datos_usuarios(datos_actualizados):
    "Actualiza los datos de los usuarios en el archivo json."
    with open('usuarios.json', 'w') as file:
        json.dump(datos_actualizados, file, indent=4)

def cargar_datos_usuarios():
    "Carga los datos de los usuarios desde el archivo json."
    try:
        with open('usuarios.json', 'r') as file:
            usuarios_data = json.load(file)
    except FileNotFoundError:
        usuarios_data = []
    return usuarios_data


def cargar_datos():
    "Carga los datos de los usuarios y las publicaciones desde la API."
    api_usuarios = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/08d4d2ce028692d71e9f8c32ea8c29ae24efe5b1/users.json"
    api_post = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/main/posts.json"

    response_usuarios = requests.get(api_usuarios)
    response_post = requests.get(api_post)

    datos_usuarios = response_usuarios.json()
    datos_post = response_post.json()

    usuarios = []

    for data in datos_usuarios:
        publicaciones_usuario = []  # Crear una lista para las publicaciones del usuario actual
        for datos in datos_post:
            if datos['publisher'] == data['id']:  # Comprobar si la publicación pertenece al usuario actual
                publicacion = Publicacion(datos['publisher'], datos['type'], datos['caption'], datos['tags'], datos['date'], datos['multimedia'])
                publicaciones_usuario.append(publicacion)
        print(publicaciones_usuario)

        if data['type'] == 'professor':
            usuario = Profesor(data['id'], data['firstName'], data['lastName'], data['email'], data['username'], data['department'], data['following'], publicaciones_usuario)
        elif data['type'] == 'student':
            usuario = Estudiante(data['id'], data['firstName'], data['lastName'], data['email'], data['username'], data['major'], data['following'], publicaciones_usuario)
        usuarios.append(usuario)

    return usuarios