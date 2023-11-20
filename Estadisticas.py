import matplotlib.pyplot as plt
from collections import Counter
import json

class Estadisticas:
    "Clase para calcular etsadisticas."
    @staticmethod
    def usuarios_con_mas_publicaciones(usuarios_json, top_n=5):
        "Devuelve los usuarios con más publicaciones"
        usuarios = json.loads(usuarios_json)
        usuarios_sorted = sorted(usuarios, key=lambda x: len(x.get('publicaciones', [])), reverse=True)
        top_usuarios = usuarios_sorted[:top_n]
        return top_usuarios

    @staticmethod
    def carreras_con_mas_publicaciones(usuarios_json, top_n=5):
        "Devuelve las carreras con más publicaciones"
        usuarios = json.loads(usuarios_json)
        carreras_publicaciones = Counter([usuario.get('department', '') for usuario in usuarios for _ in usuario.get('publicaciones', [])])
        carreras_sorted = dict(sorted(carreras_publicaciones.items(), key=lambda x: x[1], reverse=True)[:top_n])
        return carreras_sorted

    @staticmethod
    def post_con_mas_interacciones(publicaciones_json, top_n=1):
        "Devuelve los posts con más interacciones"
        publicaciones = json.loads(publicaciones_json)
        post_sorted = sorted(publicaciones, key=lambda x: len(x.get('likes', [])) + len(x.get('comentarios', [])), reverse=True)
        top_post = post_sorted[:top_n]
        return top_post

    @staticmethod
    def usuarios_con_mas_interacciones(usuarios_json, top_n=5):
        "Devuelve los usuarios con más interacciones"
        usuarios = json.loads(usuarios_json)
        usuarios_sorted = sorted(usuarios, key=lambda x: len(x.get('likes', [])) + len(x.get('comentarios', [])), reverse=True)
        top_usuarios = usuarios_sorted[:top_n]
        return top_usuarios

    @staticmethod
    def usuarios_con_mas_post_tumbados(usuarios_json, top_n=5):
        "Devuelve los usuarios con mas posts eliminados."
        usuarios = json.loads(usuarios_json)
        usuarios_sorted = sorted(usuarios, key=lambda x: x.get('post_tumbados', 0), reverse=True)
        top_usuarios = usuarios_sorted[:top_n]
        return top_usuarios

    @staticmethod
    def carreras_con_mas_comentarios_inadecuados(usuarios_json, top_n=5):
        "Devuelve las carreras con mas comentarios inadecuados"
        usuarios = json.loads(usuarios_json)
        carreras_comentarios = Counter([usuario.get('department', '') for usuario in usuarios for comentario in usuario.get('comentarios_inadecuados', [])])
        carreras_sorted = dict(sorted(carreras_comentarios.items(), key=lambda x: x[1], reverse=True)[:top_n])
        return carreras_sorted

    @staticmethod
    def usuarios_eliminados_por_infracciones(usuarios_eliminados_json, top_n=5):
        "Devuelve los usuarios eliminados por infracciones"
        usuarios_eliminados = json.loads(usuarios_eliminados_json)
        usuarios_eliminados_sorted = sorted(usuarios_eliminados, key=lambda x: x.get('infracciones', 0), reverse=True)
        top_usuarios_eliminados = usuarios_eliminados_sorted[:top_n]
        return top_usuarios_eliminados