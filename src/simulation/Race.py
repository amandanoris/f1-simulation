from enum import Enum
import time
from utils import car_factor
import random

class Weather(Enum):
    """
    Enumeración que representa las posibles condiciones climáticas para un día de carrera.
    """
    sunny = 1
    cloudy = 2
    rainy = 3
    stormy = 4

class Difficulty(Enum):
    """
    Enumeración que representa las posibles dificultades de la pista.
    """
    easy = 1
    medium = 2
    hard = 3

class Segment:
    def __init__(self, length, curve, slippery):
        self.length= length # longitud en metros 
        self.curve = curve # grado de curvatura, minimo 0 si es una recta y maximo 10 si es una curva muy cerrada
        self.slippery = slippery # grado de agarre de la pista, minimo 0 si es lisa completa y maximo 10 si es muy rugosa

class Track:
    def __init__(self):
        self.segments = []                  # Lista de segmentos que componen la pista
        self.type = self.difficulty_level() # tipo de pista segun la dificultad, uno de los valores del enum dificulty
        self.length = self.get_length()     # largo total de la pista
        self.pits_position = 0              # metros de la ubicacion de los pits dentro de la pista

    def get_length(self):
        if(len(self.segments) == 0): return 0

        track_length = 0
        for seg in self.segments:
          track_length += seg.length
        return track_length

    def add_segment(self, length, curve, slippery):
        """Agrega un segmento a la pista."""
        segment = Segment(length, curve, slippery)
        self.segments.append(segment)
        self.difficulty_level()

    def difficulty_level(self):
        if(len(self.segments) == 0): return Difficulty.easy 

        """Determina el nivel de dificultad de la pista basado en los segmentos."""
        total_curve = 0
        total_slippery = 0

        for segment in self.segments:
            total_curve += segment.curve
            total_slippery += segment.slippery

        avg_curve = total_curve / len(self.segments)
        avg_slippery = total_slippery / len(self.segments)

        # Definir reglas para determinar el nivel de dificultad
        if avg_curve < 4 and avg_slippery < 4:
            return Difficulty.easy
        elif avg_curve > 7 and avg_slippery > 7 :
            return Difficulty.hard
        else:
            return Difficulty.medium
   
    def create_track(self, num_segments):
        
        for _ in range(num_segments):
            length = random.randint(10, 50)  # Random length between 100 and 1000
            curve = random.randint(1, 10)       # Random curve between 1 and 10
            slippery = random.randint(1, 10)    # Random slippery between 1 and 10
            self.add_segment(length, curve, slippery)

        self.length = self.get_length()
        self.type = self.difficulty_level()    
        self.pits_position = random.randint(1, self.length)

class Race:

    def __init__(self, start_time, weather, duration, track, no_teams, pos_table, is_happening, no_laps, actual_lap, metros_recorridos, pilots_lap, equipos):
        self.no_laps = no_laps
        self.actual_lap = actual_lap
        self.weather = weather
        self.track = track
        self.duration = duration
        self.pos_table = pos_table
        self.is_happening = is_happening
        self.start_time = start_time
        self.no_teams = no_teams
        self.metros_recorridos = metros_recorridos
        self.pilots_lap = pilots_lap
        self.equipos = equipos

    def update_lap(self):
        self.update_pilots_lap()
        self.actual_lap = min(self.pilots_lap)

    def update_pilots_lap(self): 
        self.pilots_lap =  [1 + (pos // self.track.length) for pos in self.metros_recorridos]

    def update_metros_recorridos(self, velocidades, tiempo, directors, segments):
        for i in range(0, len(velocidades), 2):

            self.metros_recorridos[i] += velocidades[i] * tiempo
            self.metros_recorridos[i + 1] += velocidades[i + 1] * tiempo

            directors[i // 2].equipo.car.tires.resistencia -= velocidades[i]/100 + car_factor(directors[i // 2].equipo.car.tires, segments[i], self) +1

            if i + 1 < len(velocidades):
                directors[i // 2].equipo.car.tires.resistencia -= velocidades[i + 1]/100 + car_factor(directors[i // 2].equipo.car.tires, segments[i + 1], self) +1


    def update(self, nueva_tabla):   
        self.pos_table = nueva_tabla

        if not self.is_happening:
            self.duration = time.time() - self.start_time

    def condicion_de_finalizacion(self):
        if( min(self.metros_recorridos) > self.track.length*self.no_laps):
            return True
        else:
            return False
           

    @staticmethod
    def create_race( duration=0, actual_lap=0, is_happening=False):

        equipos = []

        no_laps = random.randint(1, 5)
     
        num_segments = random.randint(1, 10)
        no_teams = random.randint(2, 10)

        metros_recorridos = [0] * no_teams *2
        pilots_lap = [0] * no_teams*2

        track = Track()
        track.create_track(num_segments)
       
        weather = random.choice(list(Weather))
        
        # Establecer el tiempo de inicio ahora
        start_time = time.time()
        
        # Crear una tabla de metros_recorridos con tantas metros_recorridos como equipos haya
        pos_table = {i: [] for i in range(1, no_teams*2 + 1)}
        
        # Crear la instancia de Race
        race = Race(start_time, weather, duration, track, no_teams, pos_table, is_happening, no_laps, actual_lap, metros_recorridos, pilots_lap, equipos)
        
        return race
