import time 

class PitStop:
    def __init__(self, start_time, mechanic):
        self.start_time = start_time
        self.mechanic = mechanic



    def is_happening(self):
        tiempo_inicial = self.start_time
        
        tiempo_maximo = 60 # tiempo bastante malo en segundos

        impacto = (self.mechanic.conocimiento_tecnico / 10 + self.mechanic.rapidez / 10) / 2

        tiempo_cambio = tiempo_maximo - (impacto * tiempo_maximo) + 1.8 # record de pit stop más rápido de la historia
        
        tiempo_actual = time.time()
        tiempo_transcurrido = tiempo_actual- tiempo_inicial

        # Comprobar si el tiempo transcurrido es menor que el tiempo de cambio
        if tiempo_transcurrido < tiempo_cambio:
            return True
        else:
            return False




