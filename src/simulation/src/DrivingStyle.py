import random

class DrivingStyle:
    def __init__(self, aceleracion, cautela, braking_strategy):
        self.aceleracion = aceleracion
        self.cautela = cautela
        self.braking_strategy = braking_strategy

    @staticmethod
    def generate_random_driving_style():
        aceleracion = random.randint(1, 10) 
        cautela = random.randint(1, 10) 
        braking_strategy = random.randint(1, 10) 

        return DrivingStyle(aceleracion, cautela, braking_strategy)

