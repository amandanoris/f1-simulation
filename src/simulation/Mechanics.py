from Agent import Agente
import time
from enum import Enum
from Tires import TireAdaptationSystem
import random
from Race import Segment

class Mechanic(Agente):
    def __init__(self, creencias, deseos, intenciones, rapidez, conocimiento_tecnico, sistema_mensajeria):
        super().__init__(creencias, deseos, intenciones, sistema_mensajeria)
        self.rapidez = rapidez
        self.conocimiento_tecnico = conocimiento_tecnico
    
    @staticmethod
    def generate_random_mechanic(race, sistema_mensajeria=False):
        tire_system = TireAdaptationSystem()
        creencias = MechanicBeliefs(race, tire_system) 
        deseos = MechanicDesires
        intenciones = MechanicActions
         
        # Generar valores aleatorios para la rapidez y el conocimiento técnico
        rapidez = random.randint(1, 10) # Asumiendo una escala de 1 a 10
        conocimiento_tecnico = random.randint(1, 10) # Asumiendo una escala de 1 a 10
        
        # Crear el objeto Mechanic con los valores generados aleatoriamente
        return Mechanic(creencias, deseos, intenciones, rapidez, conocimiento_tecnico, sistema_mensajeria)

class MechanicBeliefs:
    def __init__(self, race, tire_adaptation_system):
        self.race = race
        self.tire_adaptation_system = tire_adaptation_system

class MechanicDesires(Enum):
    """
    Enumeración que representa los posibles deseos de un ingeniero mecanico de equipo.
    """
    cambiar_neumatico = 1
    informar_piloto = 2

class MechanicActions:
    # Crear el diccionario mapeando los valores de la enumeración a los nombres de los métodos
    Mechanic_actions_map = {
       MechanicDesires.cambiar_neumatico: 'cambiar_neumatico',
       MechanicDesires.informar_piloto: 'informar_piloto',
    }

    def ejecutar_accion_por_deseo(self, deseo, *args, **kwargs):
        action_method_name = self.Mechanic_actions_map[deseo]
        action_method = getattr(self, action_method_name)
        return action_method(self, *args, **kwargs)

    def cambiar_neumatico(self, car, race, segment, tire_system):
        self.tires(self, car, race, segment, tire_system)
        print("Cambiando neumaticos al carro ")

    def tires(self, car, race, segment, tire_system):
        tire_set = tire_system.simulate(race, segment)
        tire_set.resistencia = 10
        car.tires = tire_set
    
    def informar_piloto(self, piloto, segment, sistema_mensajeria):
        self.inform(self, piloto, segment, sistema_mensajeria)
        print("Informando al piloto " + piloto.name +" del tramo de la carrera que sigue ")
    
    def inform(self, piloto, segment, sistema_mensajeria):
 
        numero_aleatorio = random.random()
        probabilidad = 0.95

        if numero_aleatorio <= probabilidad:
           contenido_mensaje = segment

        else: 
            segmento_malicioso = Segment(random.randint(100,500), random.randint(1,10), random.randint(1,10))
            contenido_mensaje = segmento_malicioso
        
        sistema_mensajeria.enviar_mensaje(
            remitente=Mechanic,
            destinatario=piloto,
            contenido=contenido_mensaje
        )

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




