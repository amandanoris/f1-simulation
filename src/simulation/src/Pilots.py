from src.Agent import Agente
from enum import Enum
from src.Race import Difficulty, Weather
import names
import random
from src.DrivingStyle import DrivingStyle
from src.GeneticStrategySelection import GeneticStrategySelection

class Pilot(Agente):
    def __init__(self, name, estrategia, habilidad_track, habilidad_weather, anos_de_experiencia, no_racewins, no_accidentes, creencias, deseos, intenciones, sistema_mensajeria, do_pitstop, no_stops):
        super().__init__(creencias, deseos, intenciones, sistema_mensajeria)
        self.name = name
        self.estrategia = estrategia
        self.habilidad_track = habilidad_track
        self.habilidad_weather = habilidad_weather
        self.anos_de_experiencia = anos_de_experiencia
        self.no_accidentes = no_accidentes
        self.no_racewins = no_racewins
        self.sistema_mensajeria = sistema_mensajeria
        self.do_pitstop = do_pitstop
        self.no_stops = no_stops
    
    def check_tires(self):
        if(self.creencias.car.tires.resistencia < 2):
           print( self.name + " va pal pit")
           self.no_stops += 1
           self.do_pitstop = True
        
    @staticmethod
    def generate_random_pilot(creencias=False, sistema_mensajeria=False, do_pitstop=False, no_stops=0):
        name = names.get_full_name()

        estrategia = DrivingStyle.generate_random_driving_style()
        
        habilidad_track = {track: random.randint(1, 10) for track in Difficulty._member_names_}
        habilidad_weather = {weather: random.randint(1, 10) for weather in Weather._member_names_}
        
        anos_de_experiencia = random.randint(1, 10)
        no_accidentes = random.randint(0, 10)
        no_racewins = random.randint(0, 10)

        deseos = PilotDesires
        intenciones = PilotActions 

        return Pilot(name,estrategia, habilidad_track, habilidad_weather, anos_de_experiencia, no_racewins, no_accidentes, creencias, deseos, intenciones, sistema_mensajeria, do_pitstop, no_stops)

class PilotBeliefs:
    def __init__(self, car, segment, race, confianza, posicion, pareja_pos) :
        self.confianza = confianza
        self.race = race
        self.posicion = posicion
        self.car = car
        self.segment = segment
        self.pareja_pos = pareja_pos

    def update_conocimiento(self, segmentos_actuales, pos_table, name):
        claves = list(pos_table.keys())
    
        indice_piloto = claves.index(name)
        self.posicion = indice_piloto+1

        #print(f"El piloto {name} se encuentra en la posición {self.posicion} en la tabla.")
    
        equipo_piloto = pos_table[name]
        otros_pilotos_equipo = [clave for clave, valor in pos_table.items() if valor == equipo_piloto and clave != name]
        indices_otros_pilotos = [claves.index(piloto) + 1 for piloto in otros_pilotos_equipo]

        self.pareja_pos = indices_otros_pilotos[0]
    
        #print(f"Los otros pilotos del equipo {equipo_piloto} se encuentran en las posiciones {self.pareja_pos} en la tabla.")

        if(self.segment != segmentos_actuales):
            self.confianza -= 1
        else:
            self.confianza += 1
 
    def determinar_deseo(self):
        #si tu equipo es muy malo contigo les jodes la carrera
        if self.confianza < 5:
            print("Un piloto le ha perdido la confinaza a su equipo")
            return PilotDesires.sabotear_carrea
        else:
            return PilotDesires.ganar_carrera
    
    def determinar_intencion(self):
        deseo = self.determinar_deseo()
        
        #si kieres ganar la carrera y eres el primero de tu equipo
        if(deseo == PilotDesires.ganar_carrera and self.posicion > self.pareja_pos):
            return PilotIntentions.buena_estrategia
        
        #si kieres ganar la carrera y eres el segundo de tu equipo
        if(deseo == PilotDesires.ganar_carrera and self.posicion < self.pareja_pos):
            return PilotIntentions.acelerar
        
        #si kieres sabotear la carrera 
        if(deseo == PilotDesires.sabotear_carrea):
            return PilotIntentions.peor_estrategia
        
class PilotDesires(Enum):
    ganar_carrera = 1
    sabotear_carrea = 2

class PilotIntentions(Enum):
    buena_estrategia = 1
    acelerar = 2
    peor_estrategia = 3
    
class PilotActions:

    pilot_actions_map = {
       PilotIntentions.buena_estrategia: 'buena_estrategia',
       PilotIntentions.acelerar: 'acelerar',
       PilotIntentions.peor_estrategia: 'peor_estrategia'
    }

    def ejecutar_accion_por_deseo(self, deseo, *args, **kwargs):
        action_method_name = self.pilot_actions_map[deseo]
        action_method = getattr(self, action_method_name)
        return action_method( self, *args, **kwargs)
    
    def peor_estrategia(self, segment):
        print("Saboteando")
        peor = DrivingStyle(1,1,1)
        return peor
    
    def acelerar(self, segment):
        print("Acelerando")
        mejor_estrategia = self.seleccionar_mejor_estrategia(self, segment)
        mejor_estrategia.aceleracion = 10
        return mejor_estrategia

    def buena_estrategia(self, segment):
        mejor_estrategia = self.seleccionar_mejor_estrategia(self, segment)
        print("Seleccionando la mejor estrategia para este segmento de carrera")
        return mejor_estrategia
    
    def seleccionar_mejor_estrategia(self, segment):
        genetic = GeneticStrategySelection()
        mejor_estrategia = genetic.busqueda_genetica(segment)
        return mejor_estrategia

   