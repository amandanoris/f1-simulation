from Pilots import Pilot
from Driving import Car
from Mechanics import Mechanic
from Message import SistemaMensajeria
import random
import names

class Team:
    def __init__(self, pilotos, mecanicos, car, sistema_mensajeria, name):
        self.name = name
        self.sistema_mensajeria = sistema_mensajeria 
        self.car = car
        self.pilotos = pilotos # Lista de instancias de pilots
        self.mecanicos = mecanicos # Lista de instancias de mechanics

    def add_piloto(self, piloto):
        """Agrega un piloto al equipo."""
        self.pilotos.append(piloto)

    def add_mecanico(self, mecanico):
        """Agrega un mecánico al equipo."""
        self.mecanicos.append(mecanico)

    @staticmethod
    def generate_random_team(race):
        sistema_mensajeria = SistemaMensajeria()
        name = "Team "+ names.get_last_name()
   
        num_pilotos = random.randint(2, 5) 
        pilotos = []
        for _ in range(num_pilotos):
            piloto = Pilot.generate_random_pilot()
            piloto.sistema_mensajeria = sistema_mensajeria
            pilotos.append(piloto)


        num_mecanicos = random.randint(1, 3) 
        mecanicos = []
        for _ in range(num_mecanicos):
            mecanico = Mechanic.generate_random_mechanic(race)
            mecanico.sistema_mensajeria = sistema_mensajeria
            mecanicos.append(mecanico)

        # Generar un carro aleatorio
        car = Car.generate_random_car()

        # Crear el objeto Team con los valores generados aleatoriamente
        return Team(pilotos, mecanicos, car, sistema_mensajeria, name )
