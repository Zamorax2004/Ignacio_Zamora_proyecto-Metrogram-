import datetime
class Comentario:
    "Clase que representa un comentario."
    def __init__(self, autor, publicacion, texto):
        self.autor = autor
        self.publicacion = publicacion
        self.texto = texto
        self.fecha = datetime.datetime.now()

    def __str__(self):
        "Devuelve un string con los parametros."
        return f"{self.autor.firstname} {self.autor.lastname}: {self.texto} ({self.fecha})"