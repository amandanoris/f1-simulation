
class Agente:
    def __init__(self, creencias, deseos, intenciones, sistema_mensajeria):
        self.creencias = creencias
        self.deseos = deseos 
        self.intenciones = intenciones
        self.sistema_mensajeria = sistema_mensajeria

    def enviar_mensaje(self, destinatario, contenido):
        self.sistema_mensajeria.enviar_mensaje(self, destinatario, contenido)

    def recibir_mensajes(self):
        return self.sistema_mensajeria.recibir_mensajes(self)

