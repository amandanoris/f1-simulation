import uuid
class Mensaje:
    def __init__(self, remitente, destinatario, contenido):
        self.id = uuid.uuid4() # Genera un identificador único para cada mensaje
        self.remitente = remitente
        self.destinatario = destinatario
        self.contenido = contenido

class SistemaMensajeria:
    def __init__(self):
        self.mensajes = []

    def enviar_mensaje(self, remitente, destinatario, contenido):
        mensaje = Mensaje(remitente, destinatario, contenido)
        self.mensajes.append(mensaje)

    def recibir_mensajes(self, destinatario):
        mensajes_destinatario = [mensaje for mensaje in self.mensajes if mensaje.destinatario == destinatario]
        # Elimina los mensajes recibidos de la lista
        for mensaje in mensajes_destinatario:
            self.mensajes.remove(mensaje)
        return mensajes_destinatario
