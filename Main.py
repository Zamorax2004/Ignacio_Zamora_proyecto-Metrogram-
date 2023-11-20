from Usuarios import Usuario, Estudiante, Profesor
from Estadisticas import Estadisticas
from Datos import *


def imprimir_estadistica(titulo, datos_json):
    "Imprime una estadistica en formato de datos."
    try:
        print(titulo)
        for dato in datos_json:
            username = dato.get('username')
            informacion_estadistica = dato.get('informacion_estadistica')

            if username and callable(informacion_estadistica):
                print(f"{username}: {informacion_estadistica()}")
            else:
                print("Los datos no son válidos para imprimir estadísticas.")
    except Exception as e:
        print(f"Error al imprimir estadísticas: {str(e)}")


# Menu principal de la app
while True:
    opcion = input(
        """Bienvenido a METROGRAM!
        ----------------------------
        -> 1. Gestión de perfiles
        -> 2. Gestión multimedia
        -> 3. Gestión de interacciones
        -> 4. Gestión de moderacion
        -> 5. Indicadores de gestion
        -> 6. Salir.
        -> 0. Cargar datos de 0
        -> """)

    if opcion == "1":
        opcion_perfiles = input(
            """-> 1. Registrar nuevo usuario
            -> 2. Buscar Perfiles
            -> 3. Cambiar información de la cuenta
            -> 4. Borrar datos de la cuenta
            -> 5. Acceder a la cuenta de otro usuario
            -> """)

        usuarios = cargar_datos_usuarios()

        if opcion_perfiles == "1":
            es_profesor = input("¿Es un profesor? (Sí/No): ").lower() == "si"
            if es_profesor:
                usuarios = Usuario.agregar_profesor(usuarios)
            else:
                usuarios = Usuario.agregar_estudiante(usuarios)
            actualizar_datos_usuarios(usuarios)

        elif opcion_perfiles == "2":
            usuarios = cargar_datos_usuarios()
            opcion_busqueda = input(
                """-> 1. Búsqueda por departamento
                -> 2. Búsqueda por carrera
                -> """)
            perfiles_encontrados = Usuario.buscar_por_departamento_o_carrera(
                opcion_busqueda, usuarios)
            for perfil in perfiles_encontrados:
                print("ID:", perfil['id'])
                print("Nombre completo:",
                      perfil['firstName'], perfil['lastName'])
                print("Correo electrónico:", perfil['email'])
                print("Nombre de usuario:", perfil['username'])
                print("Tipo:", perfil['type'])

                if perfil['type'] == 'professor':
                    print("Departamento:", perfil['department'])
                elif perfil['type'] == 'student':
                    print("Carrera:", perfil['major'])

                    print("\n")
        elif opcion_perfiles == "3":
            usuarios = cargar_datos_usuarios()
            username = input("Ingrese el username: ")
            usuario_encontrado = None

            # Buscar usuario por username
            for usuario in usuarios:
                if username == usuario['username']:
                    usuario_encontrado = usuario
                    print(
                        f"\nPerfil encontrado: {usuario['firstName']} {usuario['lastName']}\n")
                    break

            if usuario_encontrado:
                print("Seleccione los campos a actualizar:")
                print("1. Nuevo nombre")
                print("2. Nuevo apellido")
                print("3. Nuevo correo electrónico")
                print("4. Nuevo username")

                if isinstance(usuario_encontrado, Profesor):
                    print("5. Nuevo departamento")
                elif isinstance(usuario_encontrado, Estudiante):
                    print("5. Nueva carrera")

                campos_a_actualizar = input(
                    "Ingrese los números de los campos a actualizar separados por comas: ")
                campos_a_actualizar = campos_a_actualizar.split(',')

                # Actualizar campos seleccionados
                for campo in campos_a_actualizar:
                    campo = int(campo.strip())
                    if campo == 1:
                        firstname = input("Nuevo nombre: ")
                        usuario_encontrado['firstName'] = firstname
                    elif campo == 2:
                        lastname = input("Nuevo apellido: ")
                        usuario_encontrado['lastName'] = lastname
                    elif campo == 3:
                        email = input("Nuevo correo electrónico: ")
                        usuario_encontrado['email'] = email
                    elif campo == 4:
                        new_username = input("Nuevo username: ")
                        usuario_encontrado['username'] = new_username
                    elif campo == 5:
                        if 'department' in usuario_encontrado:
                            department = input("Nuevo departamento: ")
                            usuario_encontrado['department'] = department
                        elif 'major' in usuario_encontrado:
                            major = input("Nueva carrera: ")
                            usuario_encontrado['major'] = major

                print("\nInformación actualizada:")
                print(
                    f"Nombre: {usuario_encontrado['firstName']} {usuario_encontrado['lastName']}")
                print(f"Correo Electrónico: {usuario_encontrado['email']}")
                print(f"Username: {usuario_encontrado['username']}")
                if usuario_encontrado['type'] == 'professor':
                    print("Departamento:",
                          usuario_encontrado['department'])
                elif usuario_encontrado['type'] == 'student':
                    print("Carrera:", usuario_encontrado['major'])

                # Guarda la información actualizada
                actualizar_datos_usuarios(usuarios)
            else:
                print("Perfil no encontrado.")

        elif opcion_perfiles == "4":
            usuarios = cargar_datos_usuarios()
            nombre_usuario = input(
                "Ingrese el nombre del usuario a eliminar: ")

            # Encuentra y elimina el usuario por su nombre de usuario
            usuario_encontrado = None
            for usuario in usuarios:
                if nombre_usuario == usuario['username']:
                    usuario_encontrado = usuario
                    usuarios.remove(usuario)
                    print(f"La cuenta de {nombre_usuario} ha sido eliminada.")
                    # Guarda la lista actualizada de usuarios
                    actualizar_datos_usuarios(usuarios)
                    break

            if not usuario_encontrado:
                print("Usuario no encontrado.")
        elif opcion_perfiles == "5":
            usuarios = cargar_datos_usuarios()
            usuario = input("Ingresa el nombre de usuario")
            Usuario.mostrar_informacion_otro_usuario(usuario, usuarios)
    elif opcion == "2":
        print("Gestión de multimedia")
        opcionGM = input(
            """-> 1. Subir post
            -> 2. Ver post de otro usuario
            -> 3. Buscar post por filtros
            -> """)
        if opcionGM == "1":
            usuarios = cargar_datos_usuarios()
            usuario_actual = Usuario.obtener_usuario_actual(usuarios)
            if usuario_actual:
                try:
                    tipo_multimedia = input(
                        "Tipo de multimedia (foto o video): ").lower()
                    if tipo_multimedia not in ['foto', 'video']:
                        raise ValueError(
                            "Tipo de multimedia no válido. Debe ser 'foto' o 'video'.")

                    descripcion = input("Descripción: ")
                    hashtags = input(
                        "Hashtags (separados por comas): ").split(',')

                    nueva_publicacion = Usuario.subir_publicacion(
                        usuario_actual['id'], tipo_multimedia, descripcion, hashtags)

                    if 'publicaciones' not in usuario_actual:
                        usuario_actual['publicaciones'] = []

                    usuario_actual['publicaciones'].append(nueva_publicacion)
                    print("Publicación subida exitosamente.")
                    actualizar_datos_usuarios(usuarios)
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                print("Debes iniciar sesión primero.")
        elif opcionGM == "2":
            usuarios = cargar_datos_usuarios()
            try:
                username_buscado = input(
                    "Ingresa el nombre de usuario que buscas: ")
                usuario_a_seguir = Usuario.buscar_por_username(
                    username_buscado, usuarios)

                if usuario_a_seguir:
                    username_actual = input("Ingresa tu nombre de usuario: ")
                    usuario_actual = Usuario.buscar_por_username(
                        username_actual, usuarios)

                    if usuario_actual:
                        Usuario.ver_publicaciones(
                            usuario_actual, usuario_a_seguir)
                        actualizar_datos_usuarios(usuarios)
                    else:
                        print(
                            f"No se encontró al usuario actual con nombre de usuario '{username_actual}'.")
                else:
                    print(
                        f"No se encontró al usuario con nombre de usuario '{username_buscado}'.")

            except Exception as e:
                print(f"Ocurrió un error: {e}")

        elif opcionGM == "3":
            opcionBP = input(
                """-> 1. Buscar publicaciones por usuario (username)
                -> 2. Buscar publicaciones por hashtags (#)""")
            usuarios = cargar_datos_usuarios()
            if opcionBP == "1":
                username_a_buscar = input(
                    "Ingresa el username del usuario cuyas publicaciones deseas buscar: ")
                publicaciones_usuario = Usuario.buscar_publicaciones_por_username(
                    usuarios, username_a_buscar)

                if publicaciones_usuario:
                    print(f"Publicaciones del usuario '{username_a_buscar}':")

                    for publicacion in publicaciones_usuario:
                        print(f"Tipo: {publicacion['tipo']}")
                        print(f"Descripción: {publicacion['descripcion']}")
                        print(f"Fecha: {publicacion['fecha']}")
                        print(f"Tags: {', '.join(publicacion['tags'])}")
                        print(
                            f"Multimedia: {publicacion['multimedia']['url']}")
                        print(f"Likes: {len(publicacion['likes'])}")

                        print("Comentarios:")
                        if publicacion['comentarios']:
                            for comentario in publicacion['comentarios']:
                                print(f"Usuario: {comentario['usuario']}")
                                print(f"Texto: {comentario['texto']}")
                                print(f"Fecha: {comentario['fecha']}")
                                print("-" * 15)
                        else:
                            print("No hay comentarios.")

                        print("--------")
                else:
                    print(
                        f"No se encontraron publicaciones del usuario '{username_a_buscar}'.")
            elif opcionBP == "2":
                hashtag_buscado = input(
                    "Ingresa el hashtag que deseas buscar: ")
                publicaciones_hashtag = Usuario.buscar_por_tags(
                    usuarios, hashtag_buscado)

                if publicaciones_hashtag:
                    print(
                        f"\nPublicaciones con el hashtag '{hashtag_buscado}':")

                    for publicacion in publicaciones_hashtag:
                        print(f"Tipo: {publicacion['tipo']}")
                        print(f"Descripción: {publicacion['descripcion']}")
                        print(f"Fecha: {publicacion['fecha']}")
                        print(f"Tags: {', '.join(publicacion['tags'])}")
                        print(
                            f"Multimedia: {publicacion['multimedia']['url']}")
                        print(f"Likes: {len(publicacion['likes'])}")

                        print("Comentarios:")
                        if publicacion['comentarios']:
                            for comentario in publicacion['comentarios']:
                                print(f"Usuario: {comentario['usuario']}")
                                print(f"Texto: {comentario['texto']}")
                                print(f"Fecha: {comentario['fecha']}")
                                print("-" * 15)
                        else:
                            print("No hay comentarios.")

                        print("--------")
                else:
                    print(
                        f"No se encontraron publicaciones con el hashtag '{hashtag_buscado}'.")

    elif opcion == "3":
        opcionGI = input("""
                         -> 1. Seguir a un usuario
                         -> 2. Dejar de seguir a un usuario
                         -> 3. Comentar una publicación
                         -> 4. Dar like a una publicación
                         -> 5. Eliminar comentario de una publicación
                         -> 6. Acceder al perfil de otro usuario desde likes o comentarios
                         -> 7. Gestionar solicitudes de seguimiento""")
        usuarios = cargar_datos_usuarios()
        if opcionGI == "1":
            username_seguidor = input("Ingresa tu nombre de usuario: ")
            usuario_seguidor = Usuario.buscar_por_username(
                username_seguidor, usuarios)

            username_a_seguir = input(
                "Ingresa el nombre de usuario a seguir: ")
            usuario_a_seguir = Usuario.buscar_por_username(
                username_a_seguir, usuarios)

            if usuario_seguidor and usuario_a_seguir:
                Usuario.seguir_usuario(
                    username_seguidor, username_a_seguir, usuarios)
            else:
                print("Al menos uno de los usuarios no fue encontrado.")

        elif opcionGI == "2":
            username_seguidor = input("Ingresa tu nombre de usuario: ")
            usuario_seguidor = Usuario.buscar_por_username(
                username_seguidor, usuarios)

            username_a_dejar_de_seguir = input(
                "Ingresa el nombre de usuario a dejar de seguir: ")
            usuario_a_dejar_de_seguir = Usuario.buscar_por_username(
                username_a_dejar_de_seguir, usuarios)

            if usuario_seguidor and usuario_a_dejar_de_seguir:
                Usuario.dejar_de_seguir_usuario(usuario_a_dejar_de_seguir)
            else:
                print("Usuario no encontrado.")

        elif opcionGI == "3":
            usuarios = cargar_datos_usuarios()
            username_comentador = input("Ingresa tu nombre de usuario: ")
            Usuario.comentar_publicacion(username_comentador, usuarios)

        elif opcionGI == "4":
            username_liker = input("Ingresa tu nombre de usuario: ")
            usuario_liker = Usuario.buscar_por_username(
                username_liker, usuarios)

            if usuario_liker:
                usuarios_a_dar_like = [usuario for usuario in usuarios if usuario["id"] !=
                                       usuario_liker["id"] and usuario["id"] in usuario_liker.get("following", [])]

                if not usuarios_a_dar_like:
                    print("No sigues a nadie a cuyas publicaciones puedas dar 'like'.")
                else:
                    print(
                        "Usuarios a los que sigues y cuyas publicaciones puedes dar 'like':")
                    for i, otro_usuario in enumerate(usuarios_a_dar_like, 1):
                        print(f"{i}. {otro_usuario['username']}")

                    opcion_usuario = input(
                        "Ingresa el número del usuario cuya publicación quieres dar 'like': ")

                    if opcion_usuario.isdigit():
                        opcion_usuario = int(opcion_usuario) - 1

                        if 0 <= opcion_usuario < len(usuarios_a_dar_like):
                            usuario_a_dar_like = usuarios_a_dar_like[opcion_usuario]
                            publicaciones_usuario = usuario_a_dar_like.get(
                                "publicaciones", [])

                            print(
                                f"Publicaciones de {usuario_a_dar_like['username']}:")
                            for i, publicacion in enumerate(publicaciones_usuario, 1):
                                print(f"{i}. {publicacion['descripcion']}")

                            opcion_publicacion = input(
                                "Ingresa el número de la publicación a la que quieres dar 'like': ")

                            if opcion_publicacion.isdigit():
                                opcion_publicacion = int(
                                    opcion_publicacion) - 1

                                if 0 <= opcion_publicacion < len(publicaciones_usuario):
                                    publicacion_a_dar_like = publicaciones_usuario[opcion_publicacion]

                                    if usuario_liker["id"] in publicacion_a_dar_like.get("likes", []):
                                        print(
                                            "Ya has dado 'like' a esta publicación.")
                                    else:
                                        publicacion_a_dar_like.setdefault(
                                            "likes", []).append(usuario_liker["id"])
                                        print(
                                            "Has dado 'like' a la publicación exitosamente.")
                                        actualizar_datos_usuarios(usuarios)
                                else:
                                    print("Opción de publicación no válida.")
                            else:
                                print(
                                    "Ingresa un número válido para la publicación.")
                        else:
                            print("Opción de usuario no válida.")
                    else:
                        print("Ingresa un número válido para el usuario.")
            else:
                print("Usuario que da 'like' no encontrado.")

        elif opcionGI == "5":
            username_dueno_post = input("Ingresa tu nombre de usuario: ")
            usuario_dueno_post = Usuario.buscar_por_username(
                username_dueno_post, usuarios)

            if usuario_dueno_post:
                publicaciones_usuario = usuario_dueno_post.get(
                    'publicaciones', [])
                if not publicaciones_usuario:
                    print(
                        f"No hay publicaciones para el usuario '{usuario_dueno_post['username']}'")
                else:
                    print(
                        f"Publicaciones de {usuario_dueno_post['username']}:")
                    for i, publicacion in enumerate(publicaciones_usuario, 1):
                        print(f"{i}. {publicacion['descripcion']}")

                    opcion_publicacion = input(
                        "Ingresa el número de la publicación en la que quieres eliminar un comentario: ")
                    if opcion_publicacion.isdigit():
                        opcion_publicacion = int(opcion_publicacion) - 1
                        if 0 <= opcion_publicacion < len(publicaciones_usuario):
                            publicacion_a_eliminar_comentario = publicaciones_usuario[
                                opcion_publicacion]

                            comentarios_publicacion = publicacion_a_eliminar_comentario.get(
                                'comentarios', [])
                            if not comentarios_publicacion:
                                print("La publicación no tiene comentarios.")
                            else:
                                print("Comentarios en la publicación:")
                                for i, comentario in enumerate(comentarios_publicacion, 1):
                                    print(f"{i}. {comentario}")

                                opcion_comentario = input(
                                    "Ingresa el número del comentario que deseas eliminar (o '0' para cancelar): ")
                                if opcion_comentario.isdigit():
                                    opcion_comentario = int(
                                        opcion_comentario) - 1
                                    if 0 <= opcion_comentario < len(comentarios_publicacion):
                                        comentario_a_eliminar = comentarios_publicacion[opcion_comentario]
                                        print(
                                            f"Comentario seleccionado: {comentario_a_eliminar}")

                                        confirmacion = input(
                                            "¿Seguro que deseas eliminar este comentario? (s/n): ")
                                        if confirmacion.lower() == "s":
                                            Usuario.eliminar_comentario(
                                                publicacion_a_eliminar_comentario, comentario_a_eliminar)
                                            print(
                                                "Comentario eliminado exitosamente.")
                                            actualizar_datos_usuarios(usuarios)
                                        else:
                                            print(
                                                "Eliminación de comentario cancelada.")
                                    elif opcion_comentario == "0":
                                        print(
                                            "Cancelaste la eliminación de comentario.")
                                    else:
                                        print("Opción de comentario no válida.")
                                else:
                                    print(
                                        "Ingresa un número válido para el comentario.")
                        else:
                            print("Opción de publicación no válida.")
                    else:
                        print("Ingresa un número válido para la publicación.")
            else:
                print("Usuario dueño del post no encontrado.")

        elif opcionGI == "6":
            usuarios = cargar_datos_usuarios()
        # Acceder al perfil de otro usuario desde comentarios
            publicacion_id = input("Ingrese el ID de la publicación: ")
            publicacion_a_ver = None
            publicaciones = usuarios
            for publicacion in publicaciones:
                if publicacion.identification == publicacion_id:
                    publicacion_a_ver = publicacion
                    break

            if publicacion_a_ver:
                # Ver comentarios y acceder a perfiles desde los comentarios
                publicacion_a_ver.ver_comentarios(usuarios)
            else:
                print("Publicación no encontrada.")
        elif opcionGI == "7":
         # Después de que un usuario inicie sesión con éxito, asigna el usuario actual
            usuario_actual = Usuario.obtener_usuario_actual(usuarios)
            Usuario.gestionar_solicitudes_seguimiento(usuarios)
    elif opcion == "4":
        print("Gestion moderacion")
        opcionGmo = input(
            "-> 1. Hacer un administradorn\n-> 2. Eliminar post ofensivo\n-> 3. Eliminar comentario ofensivo\n-> 4.  Eliminar usuario infractor")
        usuarios = cargar_datos_usuarios()
        if opcionGmo == "1":
            admin = input("Ingresa tu nombre de usuario: ")
            administrador = Usuario.buscar_por_username(admin, usuarios)
            if administrador:
                administrador['Administrador'] = True
                print(f"El usuario {admin} ahora es administrador. ")
                actualizar_datos_usuarios(usuarios)

        elif opcionGmo == "2":
            usuarios = cargar_datos_usuarios()
            admin = input("Ingresa tu nombre de usuario: ")
            administrador = Usuario.buscar_por_username(admin, usuarios)
            usuario = input(
                'Ingrese el usuario de la persona cuyos posts desea revisar: ')
            usuario = Usuario.buscar_por_username(usuario, usuarios)

            if administrador and usuario:
                if administrador.get('Administrador'):
                    if 'publicaciones' in usuario:
                        Usuario.eliminar_post_ofensivo(
                            administrador, usuario['publicaciones'])
                        actualizar_datos_usuarios(usuarios)
                    else:
                        print("El usuario no tiene publicaciones para revisar.")
                else:
                    print(
                        "No tienes permiso de administrador para realizar esta acción.")
            else:
                print("Alguno de los usuarios no fue encontrado.")

        elif opcionGmo == "3":
            admin = input("Ingresa tu nombre de usuario: ")
            administrador = Usuario.buscar_por_username(admin, usuarios)
            usuario = input(
                'Ingrese el usuario de la persona que desea revisarle los post')
            usuario = Usuario.buscar_por_username(usuario, usuarios)
            if administrador['Administrador']:
                Usuario.eliminar_comentario_ofensivo(
                    administrador, usuario['publicaciones'])
                actualizar_datos_usuarios(usuarios)
            else:
                print("No tienes permiso de administrador")
        elif opcionGmo == "4":
            usuarios = cargar_datos_usuarios()
            admin = input("Ingresa tu nombre de usuario: ")
            administrador = Usuario.buscar_por_username(admin, usuarios)
            if administrador['Administrador']:
                Usuario.eliminar_usuario_infractor(administrador, usuarios)
                actualizar_datos_usuarios(usuarios)
            else:
                print("No tienes permiso de administrador")
    elif opcion == "5":
        # Estadísticas
        print("Indicadores de gestión (Estadísticas)")
        opcion_estadisticas = input(
            "-> 1. Usuarios con más publicaciones\n-> 2. Carreras con más publicaciones\n-> 3. Post con más interacciones\n-> 4. Usuarios con más interacciones\n-> 5. Usuarios con más post tumbados\n-> 6. Carreras con más comentarios inadecuados\n-> 7. Usuarios eliminados por infracciones")

        if opcion_estadisticas == "1":
            top_usuarios_publicaciones = Estadisticas.usuarios_con_mas_publicaciones(
                usuarios)
            imprimir_estadistica(
                "Usuarios con más publicaciones", top_usuarios_publicaciones)

        elif opcion_estadisticas == "2":
            top_carreras_publicaciones = Estadisticas.carreras_con_mas_publicaciones(
                usuarios)
            imprimir_estadistica(
                "Carreras con más publicaciones", top_carreras_publicaciones)

        elif opcion_estadisticas == "3":
            top_post_interacciones = Estadisticas.post_con_mas_interacciones(
                publicaciones)
            imprimir_estadistica(
                "Post con más interacciones", top_post_interacciones)

        elif opcion_estadisticas == "4":
            top_usuarios_interacciones = Estadisticas.usuarios_con_mas_interacciones(
                usuarios)
            imprimir_estadistica(
                "Usuarios con más interacciones", top_usuarios_interacciones)

        elif opcion_estadisticas == "5":
            top_usuarios_tumbados = Estadisticas.usuarios_con_mas_post_tumbados(
                usuarios)
            imprimir_estadistica(
                "Usuarios con más post tumbados", top_usuarios_tumbados)

        elif opcion_estadisticas == "6":
            top_carreras_comentarios_inadecuados = Estadisticas.carreras_con_mas_comentarios_inadecuados(
                usuarios)
            imprimir_estadistica(
                "Carreras con más comentarios inadecuados", top_carreras_comentarios_inadecuados)

        elif opcion_estadisticas == "7":
            usuarios_eliminados = []  # Lista de usuarios eliminados
            top_usuarios_eliminados = Estadisticas.usuarios_eliminados_por_infracciones(
                usuarios_eliminados)
            imprimir_estadistica(
                "Usuarios eliminados por infracciones", top_usuarios_eliminados)
    elif opcion == "6":
        break
    elif opcion == "0":
        usuarios = cargar_datos()
        guardar_usuarios_desde_0(usuarios)