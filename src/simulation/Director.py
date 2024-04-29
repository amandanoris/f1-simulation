from Agent import Agente
import random
from enum import Enum
from Driving import normalize
from enum import Enum
from Team import Team


class Director(Agente):
    def __init__(self, creencias, deseos, intenciones, equipo, sistema_mensajeria):
        super().__init__(creencias, deseos, intenciones, sistema_mensajeria)
        self.equipo = equipo
        self.creencias = creencias
        self.deseos = deseos
        self.intenciones = intenciones

    @staticmethod
    def generate_random_director(race):       
        deseos = DirectorDesires
        intenciones = DirectorActions
        
        equipo = Team.generate_random_team(race)
        creencias = False

        sistema_mensajeria = equipo.sistema_mensajeria 

        return Director(creencias, deseos, intenciones, equipo, sistema_mensajeria)

class DirectorBeliefs:
    def __init__(self, race, team, tournament):
        self.tournament = tournament
        self.race = race
        self.team = team
        self.posicion, self.puntos = tournament.obtener_posicion_y_puntos(team.name)
        self.diferencia_puntos_arriba, self.diferencia_puntos_abajo = tournament.calcular_diferencia_puntos(team.name)
    
    def determinar_deseo(self):
        #eres el primero y el segundo no t va a pasar ni auqnue gane
        if self.posicion == 1 and self.diferencia_puntos_abajo > 18+25:
            return DirectorDesires.mantener_posicion_dos
        
        #eres el primero y el segundo te puede pasar si gana
        if self.posicion == 1 and self.diferencia_puntos_abajo < 18+25:
            return DirectorDesires.mantener_posicion_uno

        #no eres el primero y le puedes ganar al de arriba
        if self.posicion != 1 and self.diferencia_puntos_arriba < 18+25:
            return DirectorDesires.ganar_carrera
        
        #no eres el primero y no le puedes ganar al de arriba pero el de abajo tampoco t gana a ti
        if self.posicion != 1 and self.diferencia_puntos_arriba > 18+25 and self.diferencia_puntos_abajo > 18+25:
            return DirectorDesires.mantener_posicion_dos
        
        #no eres el primero y no le puedes ganar al de arriba pero el de abajo t puede ganar a ti
        if self.posicion != 1 and self.diferencia_puntos_arriba > 18+25 and self.diferencia_puntos_abajo < 18+25:
            return DirectorDesires.mantener_posicion_uno     

class DirectorDesires(Enum):
    """
    Enumeración que representa los posibles deseos de un director de equipo.
    """
    ganar_carrera = 1
    mantener_posicion_uno = 2
    mantener_posicion_dos = 3
    informar_piloto = 4

class DirectorActions:
    director_actions_map = {
       DirectorDesires.mantener_posicion_uno: 'mantener_posicion_uno',
       DirectorDesires.ganar_carrera: 'ganar_carrera',
       DirectorDesires.mantener_posicion_dos: 'mantener_posicion_dos',
       DirectorDesires.informar_piloto: 'informar_piloto'
    }

    def ejecutar_accion_por_deseo(self, deseo, *args, **kwargs):
        action_method_name = self.director_actions_map[deseo]
        action_method = getattr(self, action_method_name)
        return action_method(self, *args, **kwargs)
    
    def informar_piloto(self, piloto, carrera, sistema_mensajeria):
        self.inform(self, piloto, carrera,  sistema_mensajeria)
        print("Informando al piloto que va a competir")
    
    def inform(self, piloto, carrera, sistema_mensajeria):
 
        contenido_mensaje = carrera
        
        sistema_mensajeria.enviar_mensaje(
            remitente=Director,
            destinatario=piloto,
            contenido=contenido_mensaje
        )

    def mantener_posicion_uno(self, pilotos, carrera):
        piloto_aleatorio = self.seleccionar_piloto(self, pilotos)

        pilotos_copia = []
        for pilot in pilotos:
            if(piloto_aleatorio != pilot):
                pilotos_copia.append(pilot)       

        piloto_bueno = self.seleccionar_mejor_piloto(self, pilotos_copia, carrera)

        print("Seleccionando un piloto para mantener la posición y otro para ganar la carrera")
        return piloto_aleatorio, piloto_bueno
    
    def mantener_posicion_dos(self, pilotos):
        piloto_aleatorio1 = self.seleccionar_piloto(self, pilotos)

        pilotos_copia = []
        for pilot in pilotos:
            if(piloto_aleatorio1 != pilot):
                pilotos_copia.append(pilot) 

        piloto_aleatorio2 = self.seleccionar_piloto(self, pilotos_copia)
        print("Seleccionando los pilotos para mantener la posición ")
        return piloto_aleatorio1, piloto_aleatorio2

    def seleccionar_piloto(self, pilotos):
        # Selecciona un piloto aleatorio de la lista
        piloto_aleatorio = random.choice(pilotos)
        return piloto_aleatorio
    
    def ganar_carrera(self, pilotos, carrera):

        mejor_piloto1 = self.seleccionar_mejor_piloto(self, pilotos, carrera)

        pilotos_copia = []
        for pilot in pilotos:
            if(mejor_piloto1 != pilot):
                pilotos_copia.append(pilot) 

        mejor_piloto2 = self.seleccionar_mejor_piloto(self, pilotos_copia, carrera)

        print("Seleccionando los mejores piloto para ganar la carrera")
        return mejor_piloto1, mejor_piloto2

    def seleccionar_mejor_piloto(self, pilotos, carrera):
        valores_fitness = [(piloto, self.fitness(self, piloto, carrera)) for piloto in pilotos]
        mejor_piloto = max(valores_fitness, key=lambda x: x[1])[0]
        
        #mejor_piloto = max(pilotos, key=lambda piloto: self.fitness(self, piloto, carrera))
        return mejor_piloto

    def fitness(self, piloto, carrera):
        """Calcula el valor de fitness para cada piloto"""
        # Asigna pesos a cada factor
        peso_experiencia = 0.25
        peso_habilidad_pista = 0.3
        peso_wins = 0.2
        peso_habilidad_clima = 0.2
        peso_accidentes = 0.05

        # Calcula las puntuaciones
        track_punct = piloto.habilidad_track[carrera.track.type.name]
        puntuacion_habilidad_pista = normalize(track_punct, 0, 10)
        
        weather_punct = piloto.habilidad_weather[carrera.weather.name]
        puntuacion_habilidad_clima = normalize(weather_punct, 0, 10)

        puntuacion_wins = normalize(piloto.no_racewins, 0, 100)
        puntuacion_experiencia = normalize(piloto.anos_de_experiencia, 0, 30) 
        puntuacion_accidentes = normalize(piloto.no_accidentes, 0, 10)

        # Calcula la puntuación total de fitness
        fitness_total = (peso_habilidad_pista * puntuacion_habilidad_pista +
                         peso_habilidad_clima * puntuacion_habilidad_clima +
                         peso_experiencia * puntuacion_experiencia +
                         peso_accidentes * puntuacion_accidentes+
                         peso_wins * puntuacion_wins)

        return fitness_total


