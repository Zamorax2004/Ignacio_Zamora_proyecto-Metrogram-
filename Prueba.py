import requests
from Usuarios import Profesor,Estudiante,Usuario
from Publicaciones import Publicacion
api_usuarios = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/08d4d2ce028692d71e9f8c32ea8c29ae24efe5b1/users.json"
api_Post = "https://raw.githubusercontent.com/Algoritmos-y-Programacion-2223-3/api-proyecto/main/posts.json"

response_usuarios = requests.get(api_usuarios)
response_Post = requests.get(api_Post)

datos_usuarios = response_usuarios.json()
datos_post = response_Post.json()

usuarios = []

for data in datos_usuarios:
    if data['type'] == 'professor':
        usuario = Profesor(data['id'], data['firstName'], data['lastName'], data['email'], data['username'], data['department'], data['following'])
    elif data['type'] == 'student':
        usuario = Estudiante(data['id'], data['firstName'], data['lastName'], data['email'], data['username'], data['major'], data['following'])
    usuarios.append(usuario)
publicaciones = []

for datos in datos_post:
     publicacion = Publicacion(datos['publisher'],datos['type'],datos['caption'],datos['date'],datos['tags'],datos['multimedia'])
     publicaciones.append(publicacion)

class Usuario:
    def __init__(self, username):
        self.username = username
        self.following = []

    def seguir(self, otro_usuario):
        self.following.append(otro_usuario)

class Publicacion:
    def __init__(self, usuario, tipo, caption, fecha, hashtags):
        self.usuario = usuario
        self.tipo = tipo
        self.caption = caption
        self.fecha = fecha
        self.likes = []
        self.comentarios = []
        self.hashtags = hashtags

    def agregar_like(self, usuario):
        self.likes.append(usuario)

    def agregar_comentario(self, comentario):
        self.comentarios.append(comentario)

class Multimedia:
    def __init__(self, tipo, url):
        self.tipo = tipo
        self.url = url

# Crear usuarios
usuario1 = Usuario("usuario1")
usuario2 = Usuario("usuario2")

# Usuario 1 sigue a Usuario 2
usuario1.seguir(usuario2)

# Crear una publicación
publicacion1 = Publicacion(usuario1, "foto", "¡Mi primera foto!", "2023-01-14T16:22:47.951Z", ["#fotodeldia"])
multimedia1 = Multimedia("foto", "https://example.com/foto1.jpg")
publicacion1.multimedia = multimedia1

# Usuario 2 agrega un like y un comentario a la publicación
publicacion1.agregar_like(usuario2)
publicacion1.agregar_comentario("Hermosa foto")

# Búsqueda de publicaciones por usuario
def buscar_publicaciones_por_usuario(usuario, publicaciones):
    return [p for p in publicaciones if p.usuario == usuario]

# Búsqueda de publicaciones por hashtag
def buscar_publicaciones_por_hashtag(hashtag, publicaciones):
    return [p for p in publicaciones if hashtag in p.hashtags]

# Mostrar las publicaciones del usuario 1
publicaciones_usuario1 = buscar_publicaciones_por_usuario(usuario1, [publicacion1])
for publicacion in publicaciones_usuario1:
    print(f"Publicación de {publicacion.usuario.username}:")
    print(f"Tipo: {publicacion.tipo}")
    print(f"Caption: {publicacion.caption}")
    print(f"Fecha: {publicacion.fecha}")
    print(f"Likes: {len(publicacion.likes)}")
    print(f"Comentarios: {', '.join(publicacion.comentarios)}")
    print(f"Hashtags: {', '.join(publicacion.hashtags)}")


def ver_comentarios(self, usuarios):
        print("Comentarios en la publicación:")
        for i, comentario in enumerate(self.comentarios):
            print(f"{i + 1}: {comentario}")

        opcion_comentario = input("Ingrese el número del comentario para ver el perfil del usuario (o '0' para volver al menú anterior): ")
        if opcion_comentario.isdigit():
            opcion_comentario = int(opcion_comentario) - 1
            if 0 <= opcion_comentario < len(self.comentarios):
                comentario_seleccionado = self.comentarios[opcion_comentario]

                # Extraer el nombre de usuario del comentario
                username_comentario = comentario_seleccionado.split(":")[0].strip()

                # Buscar el usuario correspondiente (Cambiar de usuario a Usuario)
                usuario_comentario = usuario.buscar_por_username(username_comentario, usuarios)

                if usuario_comentario:
                    # Mostrar el perfil del usuario
                    print(f"Perfil del usuario que comentó:")
                    print(f"Nombre: {usuario_comentario.firstname} {usuario_comentario.lastname}")
                    print(f"Email: {usuario_comentario.email}")
                    # Puedes agregar más información del perfil según tus necesidades
                else:
                    print("Usuario no encontrado.")
            elif opcion_comentario == "0":
                print("Volviendo al menú anterior.")
            else:
                print("Opción de comentario no válida.")
        else:
            print("Opción de comentario no válida.")