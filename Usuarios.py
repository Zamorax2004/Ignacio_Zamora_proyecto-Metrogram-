import uuid
import datetime
from Comentario import Comentario
import json


class Usuario:
    "Clase que representa un usuario."
    def __init__(self, identification, firstname, lastname, email, username, types, departament, following, publicaciones=None):
        self.identification = identification
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = username
        self.type = types
        self.departament = departament
        self.following = following
        self.publicaciones = publicaciones
        self.es_admin = False

    def __str__(self):
        "Devuelve un string del objeto 'Usuario'."
        return (f"ID: {self.identification}\n"
                f"Nombre: {self.firstname} {self.lastname}\n"
                f"Correo electrónico: {self.email}\n"
                f"Nombre de usuario: {self.username}\n"
                f"Tipo: {self.type}\n"
                f"Departamento: {self.departament}\n"
                f"Siguiendo: {self.following}\n"
                f"Publicaciones: {self.publicaciones}\n"
                f"Solicitudes pendientes: {self.solicitudes_pendientes}\n")

    @staticmethod
    def agregar_profesor(usuarios):
        "Agrega un profesor al sistema"
        identification = str(uuid.uuid4())
        firstName = input("Ingrese el nombre: ")
        lastName = input("Ingrese el apellido: ")
        email = input("Ingrese el email: ")
        username = input("Ingrese un username: ")
        department = input("Ingrese el departamento: ")

        nuevo_profesor = {
            'id': identification,
            'firstName': firstName,
            'lastName': lastName,
            'email': email,
            'username': username,
            'type': 'professor',
            'department': department,
            'following': [],
            'publicaciones': []
        }
        usuarios.append(nuevo_profesor)
        return usuarios

    @staticmethod
    def agregar_estudiante(usuarios):
        "Agrega un estudiante al sistema"
        identification = str(uuid.uuid4())
        firstName = input("Ingrese el nombre: ")
        lastName = input("Ingrese el apellido: ")
        email = input("Ingrese el email: ")
        username = input("Ingrese un username: ")
        major = input("Ingresa la carrera que estudias: ")

        nuevo_estudiante = {
            'id': identification,
            'firstName': firstName,
            'lastName': lastName,
            'email': email,
            'username': username,
            'type': 'student',
            'major': major,
            'following': [],
            'publicaciones': []
        }
        usuarios.append(nuevo_estudiante)
        return usuarios

    @classmethod
    def buscar_por_username(cls, username, datos):
        "Busca un usuario por su nombre de usuario."
        for usuario in datos:
            if username == usuario['username']:
                return usuario
        return None  # Retorna None si el usuario no se encuentra

    @staticmethod
    def buscar_por_departamento_o_carrera(tipo, datos):
        "Busca un usuario por su departamento o carrera."
        criterio = ""
        perfiles_encontrados = []

        if tipo == "1":
            criterio = input("Ingrese el departamento: ")
            for usuario in datos:
                if usuario.get('type') == 'professor' and usuario.get('department') == criterio:
                    perfiles_encontrados.append(usuario)
        elif tipo == "2":
            criterio = input("Ingrese la carrera: ")
            for usuario in datos:
                if usuario.get('type') == 'student' and usuario.get('major') == criterio:
                    perfiles_encontrados.append(usuario)

        return perfiles_encontrados

    @staticmethod
    def actualizar_informacion(self, firstname, lastname, email, new_username, department, major):
        "Actualiza la información de un usuario."
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = new_username
        self.departament = department
        self.major = major

    @staticmethod
    def eliminar_cuenta(username, usuarios):
        "Elimina una cuenta de usuario."
        usuario_encontrado = next(
            (usuario for usuario in usuarios if username == usuario.username), None)
        if usuario_encontrado:
            usuarios.remove(usuario_encontrado)
            print("Cuenta eliminada exitosamente.")
        else:
            print("Perfil no encontrado.")

    @staticmethod
    def mostrar_informacion_otro_usuario(otro_usuario, datos):
        "Muestra la información de un usuario en específico."
        usuario_seleccionado = None

        for usuario in datos:
            if usuario['username'] == otro_usuario:
                usuario_seleccionado = usuario
                break

        if usuario_seleccionado:
            print(
                f"Nombre: {usuario_seleccionado['firstName']} {usuario_seleccionado['lastName']}")
            print(f"Username: {usuario_seleccionado['username']}")

            publicaciones = usuario_seleccionado.get('publicaciones', [])
            if publicaciones:
                print("\nListado de publicaciones:")
                for i, publicacion in enumerate(publicaciones, start=1):
                    print(f"{i}. {publicacion}")

                opcion = input(
                    "Ingrese el número de la publicación para acceder (o 'Q' para salir): ")
                if opcion.lower() != "q" and opcion.isdigit():
                    opcion = int(opcion)
                    if 0 < opcion <= len(publicaciones):
                        publicacion_seleccionada = publicaciones[opcion - 1]
                        print(
                            f"\nAccediendo a la publicación:\n{publicacion_seleccionada}\n")
                    else:
                        print("Opción inválida.")
        else:
            print("Usuario no encontrado.")

    @staticmethod
    def crear_nueva_publicacion(usuario_id, tipo, descripcion, hashtags):
        "Crea una nueva publicación."
        nuevaPublicacion = {
            'usuario': usuario_id,
            'tipo': tipo,
            'descripcion': descripcion,
            'hashtags': hashtags,
            'fecha': datetime.datetime.now().isoformat(),
            'multimedia': {}
        }
        return nuevaPublicacion

    @staticmethod
    def obtener_usuario_actual(usuarios):
        "Obtiene el usuario actual."
        username = input("Ingresa tu nombre de usuario: ")

        for usuario in usuarios:
            if usuario['username'] == username:
                return usuario

        print("Usuario no encontrado. Por favor, verifica tu nombre de usuario.")
        return None

    # Funcion de busqueda de publicaciones refactorizada, es una funcion para las 2
    @staticmethod
    def buscar_publicaciones_por_username(datos, username):
        "Busca las publicaciones de un usuario."
        publicaciones_encontradas = [
            dato['publicaciones'] for dato in datos
            if dato.get('username') == username and 'publicaciones' in dato
        ]
        return [pub for publicaciones in publicaciones_encontradas for pub in publicaciones]

    @staticmethod
    def buscar_publicaciones_por_tag(datos, tag):
        "Busca las publicaciones de un usuario."
        publicaciones_coincidentes = [
            publicacion
            for usuario in datos
            if 'publicaciones' in usuario
            for publicacion in usuario['publicaciones']
            if 'tags' in publicacion and tag in publicacion['tags']
        ]
        return publicaciones_coincidentes

    def ver_publicaciones(usuario_actual, usuario_a_ver):
        "Muestra las publicaciones de un usuario."
        if usuario_a_ver['id'] in usuario_actual['following']:
            posts_to_show = usuario_a_ver.get('publicaciones', [])

            for index, post in enumerate(posts_to_show, start=1):
                print(f"Publicación {index}:")
                print(f"   Tipo: {post['tipo']}")
                print(f"   Descripción: {post['descripcion']}")
                print(f"   Fecha: {post['fecha']}")
                print(f"   Tags: {', '.join(post['tags'])}")
                print(f"   Multimedia: {post['multimedia']}")

                if 'likes' in post:
                    print(f"   Likes: {len(post['likes'])}")

                if 'comentarios' in post:
                    print("   Comentarios:")
                    for comment in post['comentarios']:
                        print(
                            f"   - {comment['texto']} by {comment['usuario']}")
                    print("--------")

            selected_post = int(
                input("Selecciona el número de la publicación para comentar (0 para salir): "))
            if 0 < selected_post <= len(posts_to_show):
                new_comment = input("Ingresa tu comentario: ")
                commenter_username = usuario_actual['username']
                comment = {
                    'usuario': commenter_username,
                    'texto': new_comment,
                    'fecha': datetime.datetime.now().isoformat()
                }
                chosen_post = posts_to_show[selected_post - 1]
                chosen_post['comentarios'].append(comment)
                print("Comentario agregado exitosamente.")
            elif selected_post != 0:
                print("Número de publicación inválido.")
        else:
            print(
                f"No puedes ver las publicaciones de {usuario_a_ver['username']} porque no lo sigues.")

    @staticmethod
    def seguir_usuario(username_seguidor, username_a_seguir, datos_usuarios):
        "Sigue a un usuario."
        seguidor = Usuario.buscar_por_username(
            username_seguidor, datos_usuarios)
        a_seguir = Usuario.buscar_por_username(
            username_a_seguir, datos_usuarios)

        if not (seguidor and a_seguir):
            print("Usuario no encontrado.")
            return

        if "solicitudes_pendientes" not in a_seguir:
            a_seguir["solicitudes_pendientes"] = [seguidor["id"]]
        else:
            same_major = seguidor["type"] == "student" and a_seguir["type"] == "student" and seguidor["major"] == a_seguir["major"]
            if same_major:
                seguidor["following"].append(a_seguir['id'])
                print(
                    f"{seguidor['username']} ahora sigue a {a_seguir['username']}.")
            else:
                a_seguir["solicitudes_pendientes"].append(seguidor["id"])
                print(
                    f"Solicitud de seguimiento enviada a {a_seguir['username']}. Esperando aprobación.")

        with open("usuarios.json", "w") as file:
            json.dump(datos_usuarios, file, indent=4)

    def gestionar_solicitudes_seguimiento(usuario, usuarios):
        "Gestiona las solicitudes de seguimiento de un usuario."
        if not usuario['solicitudes_pendientes']:
            print("No tienes solicitudes de seguimiento pendientes.")
            return

        print("Solicitudes de seguimiento pendientes:")
        for i, solicitud in enumerate(usuario['solicitudes_pendientes'], 1):
            print(f"{i}. {solicitud.username}")

        try:
            opcion = int(input(
                "¿Deseas aceptar alguna solicitud? (Ingrese el número o '0' para cancelar): "))
            if opcion == 0:
                print("Cancelaste la gestión de solicitudes.")
                return
            elif 0 < opcion <= len(usuario['solicitudes_pendientes']):
                estudiante_solicitante = usuario['solicitudes_pendientes'][opcion - 1]
                accion = input(
                    f"¿Deseas aceptar (A) o rechazar (R) la solicitud de {estudiante_solicitante.username}? (A/R): ").lower()

                if accion == "a":
                    Usuario.seguir_usuario(estudiante_solicitante)
                    usuario['solicitudes_pendientes'].remove(
                        estudiante_solicitante)
                    print(
                        f"Aceptaste la solicitud de seguimiento de {estudiante_solicitante.username}.")
                elif accion == "r":
                    usuario['solicitudes_pendientes'].remove(
                        estudiante_solicitante)
                    print(
                        f"Rechazaste la solicitud de seguimiento de {estudiante_solicitante.username}.")
                else:
                    print(
                        "Opción no válida. Selecciona 'A' para aceptar o 'R' para rechazar.")
            else:
                print(
                    "Opción no válida. Ingresa un número correspondiente a una solicitud.")
        except ValueError:
            print("Entrada no válida. Debes ingresar un número.")

    @staticmethod
    def dejar_de_seguir_usuario(usuarios):
        "Deja de seguir a un usuario."
        username_actual = input('Ingresa tu nombre de usuario. ')
        username_actual = Usuario.buscar_por_username(
            username_actual, usuarios)
        usuarios_a_dejar_de_seguir = [
            usuario for usuario in usuarios if usuario['id'] in username_actual['following']]
        for i, usuario in enumerate(usuarios_a_dejar_de_seguir, 1):
            if usuario['id'] in username_actual['following']:
                print(f"{i}.{usuario['username']}")

            opcion_usuario_dejar_de_seguir = input(
                "Ingrese el numero del usuario que quiere dejar de seguir. ")
            if opcion_usuario_dejar_de_seguir.isdigit():
                opcion_usuario_dejar_de_seguir = int(
                    opcion_usuario_dejar_de_seguir)-1
                if 0 <= opcion_usuario_dejar_de_seguir < len(usuarios_a_dejar_de_seguir):
                    usuario_a_dejar_de_seguir = usuarios_a_dejar_de_seguir[
                        opcion_usuario_dejar_de_seguir]
                    if usuario_a_dejar_de_seguir['id'] in username_actual['following']:
                        username_actual['following'].remove(
                            usuario_a_dejar_de_seguir['id'])
                        print(
                            f"{username_actual} a dejado de seguir a {usuario_a_dejar_de_seguir}")
                    else:
                        print(f"No estas siguiendo a este usuario")
                else:
                    print("Opcion invalida.")
            else:
                print("Opcion invalida")

    @staticmethod
    def comentar_publicacion(username_comentador, usuarios):
        "Comenta la publicacion de un usuario."
        usuario_comentador = Usuario.buscar_por_username(
            username_comentador, usuarios)

        if not usuario_comentador:
            print("Usuario comentador no encontrado.")
            return

        usuarios_a_comentar = [
            usuario for usuario in usuarios
            if usuario['id'] != usuario_comentador['id'] and usuario['id'] in usuario_comentador['following']
        ]

        if not usuarios_a_comentar:
            print("No sigues a nadie a quien puedas comentar.")
            return

        print("Usuarios a los que sigues y puedes comentar:")
        for i, otro_usuario in enumerate(usuarios_a_comentar, 1):
            print(f"{i}. {otro_usuario['username']}")

        opcion_usuario = int(
            input("Ingresa el número del usuario al que quieres comentar: ")) - 1
        if 0 <= opcion_usuario < len(usuarios_a_comentar):
            usuario_a_comentar = usuarios_a_comentar[opcion_usuario]
            publicaciones = usuario_a_comentar.get('publicaciones', [])

            print(f"Publicaciones de {usuario_a_comentar['username']}:")
            for i, publicacion in enumerate(publicaciones, 1):
                print(f"{i}: {publicacion.get('descripcion', 'Sin descripción')}")

            opcion_publicacion = int(
                input("Ingresa el número de la publicación a comentar: ")) - 1
            if 0 <= opcion_publicacion < len(publicaciones):
                publicacion_a_comentar = publicaciones[opcion_publicacion]
                texto_comentario = input("Ingresa el comentario: ")

                comentario = {
                    'usuario': usuario_comentador['id'],
                    'texto': texto_comentario,
                    'fecha': datetime.datetime.now().isoformat()
                }

                publicacion_a_comentar.setdefault(
                    'comentarios', []).append(comentario)
                Usuario.guardar_datos_usuarios(usuarios)
            else:
                print("Opción de publicación no válida.")
        else:
            print("Opción de usuario no válida.")

    @staticmethod
    def buscar_por_username(username, usuarios):
        "Busca un usuario por su nombre de usuario."
        return next((usuario for usuario in usuarios if usuario["username"] == username), None)

    @staticmethod
    def eliminar_comentario(publicacion, comentario):
        "Elimina un comentario."
        if comentario in publicacion.get('comentarios', []):
            publicacion['comentarios'].remove(comentario)
            print("Comentario eliminado exitosamente.")
        else:
            print("Comentario no encontrado o no tienes permisos para eliminarlo.")

    @staticmethod
    def dar_like(publicacion, usuario):
        "Da like a una publicacion."
        if not usuario:
            print("Usuario no encontrado.")
            return
        if not publicacion:
            print("Publicación no encontrada.")
            return
        if not publicacion.get('likes'):
            publicacion['likes'] = []
        if usuario in publicacion.get('likes', []):
            print("Ya le diste like a la publicación")
            return
        publicacion['likes'].append({
            'usuario': usuario,
            'fecha': datetime.now().isoformat()
        })
        print("Like agregado exitosamente")
        likes = publicacion.get('likes', [])
        usuarios_que_dieron_like = [like['usuario'] for like in likes]

        if usuario in usuarios_que_dieron_like:
            print("Ya le diste like a la publicación")
        else:
            nuevo_like = {
                'usuario': usuario,
                'fecha': datetime.now().isoformat()
            }
            publicacion.setdefault('likes', []).append(nuevo_like)
            print("Like agregado exitosamente")

    @staticmethod
    def eliminar_post_ofensivo(usuario, publicaciones):
        "Elimina un post."
        if not usuario.get('Administrador'):
            print("No tienes permisos de administrador para realizar esta acción.")
            return

        if not publicaciones:
            print("No hay publicaciones para mostrar")
            return

        def cargar_datos_moderacion():
            "Carga los datos de moderación"
            try:
                with open('moderacion.json', 'r') as file:
                    return json.load(file)
            except FileNotFoundError:
                return []

        def guardar_datos_moderacion(datos_moderacion):
            "Guarda los datos de moderación"
            with open('moderacion.json', 'w') as file:
                json.dump(datos_moderacion, file, indent=4)

        print("Publicaciones:")
        for i, publicacion in enumerate(publicaciones, 1):
            print(f"{i}. Descripcion: {publicacion['descripcion']}")
            print(f"Fecha: {publicacion['fecha']}")
            print("*" * 50)

        opcion_eliminar = input(
            "Ingresa el numero de la publicacion que desea eliminar(0 para cancelar): ")
        if opcion_eliminar.isdigit():
            opcion_eliminar = int(opcion_eliminar)
            if 0 < opcion_eliminar <= len(publicaciones):
                publicacion_a_eliminar = publicaciones[opcion_eliminar - 1]
                publicaciones.remove(publicacion_a_eliminar)
                print("Post eliminado correctamente.")

                # Registrar la acción de moderación
                moderacion = {
                    "tipo": "eliminacion_post",
                    "usuario": usuario['username'],
                    "Carrera": usuario['major'],
                    "publicacion_eliminada": {
                        "descripcion": publicacion_a_eliminar['descripcion'],
                        "fecha": publicacion_a_eliminar['fecha']
                    },
                    "fecha": datetime.now().isoformat()
                }

                # Cargar datos de moderación existentes o crear una nueva lista
                moderacion_data = cargar_datos_moderacion()

                # Agregar la nueva acción de moderación
                moderacion_data.append(moderacion)

                # Guardar la información de moderación actualizada
                guardar_datos_moderacion(moderacion_data)

            elif opcion_eliminar == 0:
                print("Cancelaste la eliminacion del post.")
            else:
                print("Numero de publicacion no valido.")
        else:
            print("Entrada no valida. Debe ingresar un numero.")

    @staticmethod
    def eliminar_comentario_ofensivo(usuario, publicaciones):
        "Elimina un comentario."
        if not usuario.get('Administrador'):
            print("No tienes permisos de administrador para realizar esta acción.")
            return

        if not publicaciones:
            print("No hay publicaciones para mostrar comentarios.")
            return

        def cargar_datos_infracciones():
            "Carga los datos de infracciones"
            try:
                with open('infracciones.json', 'r') as file:
                    return json.load(file)
            except FileNotFoundError:
                return []

        def guardar_datos_infracciones(datos_infracciones):
            "Guarda los datos de infracciones"
            with open('infracciones.json', 'w') as file:
                json.dump(datos_infracciones, file, indent=4)

        print("Publicaciones:")
        for i, publicacion in enumerate(publicaciones, 1):
            print(f"{i}. Descripcion: {publicacion['descripcion']}")
            print(f"Fecha: {publicacion['fecha']}")
            print("Comentarios:")
            for j, comentario in enumerate(publicacion['comentarios'], 1):
                print(f"   {j}. Usuario: {comentario['usuario']}")
                print(f"      Comentario: {comentario['comentario']}")
                print(f"      Fecha: {comentario['fecha']}")
                print(f"      carrera: {comentario['carrera']}")
                print("-" * 50)

        opcion_publicacion = int(input(
            "Ingresa el numero de la publicacion para ver comentarios (0 para cancelar): "))
        if 0 < opcion_publicacion <= len(publicaciones):
            publicacion_seleccionada = publicaciones[opcion_publicacion - 1]
            comentarios = publicacion_seleccionada.get('comentarios', [])
            if not comentarios:
                print("Esta publicacion no tiene comentarios.")
                return
            for i, comentario in enumerate(comentarios, 1):
                print(f"{i}. Usuario: {comentario['usuario']}")
                print(f"   Comentario: {comentario['comentario']}")
                print(f"   Fecha: {comentario['fecha']}")
                print("-" * 50)

            opcion_eliminar = int(input(
                "Ingresa el numero del comentario que deseas eliminar (0 para cancelar): "))
            if 0 < opcion_eliminar <= len(comentarios):
                comentario_a_eliminar = comentarios[opcion_eliminar - 1]
                comentarios.remove(comentario_a_eliminar)
                print("Comentario eliminado correctamente.")

                # Crear datos de moderacion
                moderacion = {
                    "tipo": "eliminacion_comentario",
                    "usuario": comentario_a_eliminar['usuario'],
                    "carrera": comentario_a_eliminar['carrera'],
                    "comentario_eliminado": {
                        "comentario": comentario_a_eliminar['comentario'],
                        "fecha": comentario_a_eliminar['fecha']
                    },
                    "fecha": datetime.now().isoformat()
                }

                # Cargar datos actuales del archivo infracciones.json
                datos_actuales = cargar_datos_infracciones()

                # Actualizar los datos con los cambios
                datos_actuales.append(moderacion)

                # Guardar cambios en infracciones.json
                guardar_datos_infracciones(datos_actuales)
            elif opcion_eliminar == 0:
                print("Cancelaste la eliminacion del comentario.")
            else:
                print("Numero de comentario no valido.")
        elif opcion_publicacion == 0:
            print("Cancelaste la visualizacion de comentarios.")
        else:
            print("Numero de publicacion no valido.")

    @staticmethod
    def eliminar_usuario_infractor(usuario_actual, usuarios):
        "Elimina un usuario."
        if not usuario_actual.get('Administrador'):
            print("No tienes permisos de administrador para realizar esta acción.")
            return

        if not usuarios:
            print("No hay usuarios para mostrar.")
            return

        def cargar_datos_infracciones():
            "Carga los datos de infracciones"
            try:
                with open('infracciones.json', 'r') as file:
                    return json.load(file)
            except FileNotFoundError:
                return []

        def guardar_datos_infracciones(datos_infracciones):
            "Guarda los datos de infracciones"
            with open('infracciones.json', 'w') as file:
                json.dump(datos_infracciones, file, indent=4)

        print("Usuarios:")
        for i, usuario in enumerate(usuarios, 1):
            print(f"{i}. Username: {usuario['username']}")

        opcion_usuario = int(
            input("Ingresa el número del usuario a eliminar (0 para cancelar): "))
        if 0 < opcion_usuario <= len(usuarios):
            usuario_a_eliminar = usuarios[opcion_usuario - 1]
            usuarios.remove(usuario_a_eliminar)
            print(
                f"Usuario: {usuario_a_eliminar['username']} eliminado por múltiples infracciones.")

            # Crear datos de moderación
            moderacion = {
                "tipo": "eliminacion_usuario",
                "usuario_eliminado": {
                    "username": usuario_a_eliminar['username']
                },
                "fecha": datetime.now().isoformat()
            }

            # Cargar datos actuales del archivo infracciones.json
            datos_actuales = cargar_datos_infracciones()

            # Actualizar los datos con los cambios
            datos_actuales.append(moderacion)

            # Guardar cambios en infracciones.json
            guardar_datos_infracciones(datos_actuales)
        elif opcion_usuario == 0:
            print("Cancelaste la eliminación de usuario.")
        else:
            print("Número inválido.")

class Profesor(Usuario):
    "Clase para representar a un profesor."
    def __init__(self, identification, firstname, lastname, email, username, department, following, publicaciones=None):
        super().__init__(identification, firstname, lastname, email,
                         username, "profesor", department, following, publicaciones)
        self.department = department

    def __str__(self):
        return (f"ID: {self.identification}\n"
                f"Nombre: {self.firstname} {self.lastname}\n"
                f"Correo electrónico: {self.email}\n"
                f"Nombre de usuario: {self.username}\n"
                f"Tipo: Profesor\n")

class Estudiante(Usuario):
    "Clase para representar a un estudiante."
    def __init__(self, identification, firstname, lastname, email, username, major, following, publicaciones=None):
        super().__init__(identification, firstname, lastname, email,
                         username, "estudiante", major, following, publicaciones)
        self.major = major
        self.solicitudes_seguimiento = []

    def __str__(self):
        return (f"ID: {self.identification}\n"
                f"Nombre: {self.firstname} {self.lastname}\n"
                f"Correo electrónico: {self.email}\n"
                f"Nombre de usuario: {self.username}\n"
                f"Tipo: Estudiante\n")