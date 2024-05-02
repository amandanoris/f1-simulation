from src.Tires import  C0Tire, C1Tire, C2Tire, C3Tire, GreenIntermediateTire,FullWetBlueTire
import random

class Car:
    def __init__(self, velocidad_max, maniobrabilidad, tires):
        self.velocidad_max = velocidad_max
        self.maniobrabilidad = maniobrabilidad
        self.tires = tires

    @staticmethod
    def generate_random_car():
        velocidad_max = random.randint(300, 500) 
        maniobrabilidad = random.randint(1, 10) 

        # Seleccionar un tipo de neumático aleatorio
        tire_types = [C0Tire, C1Tire, C2Tire, C3Tire, GreenIntermediateTire, FullWetBlueTire]
        tire_class = random.choice(tire_types)
        tires = tire_class()

        return Car(velocidad_max, maniobrabilidad, tires)