import random
import math
from src.DrivingStyle import DrivingStyle

class GeneticStrategySelection:
    def __init__(self):
        pass

    def fitness(self, driving_style, segment):

        if (segment.slippery > 8 and segment.curve > 8):
            peso_aceleracion = 0.01
            peso_cautela = 0.495
            peso_breaking_strategy = 0.495

        elif (segment.slippery > 8 and segment.curve < 8):
            peso_aceleracion = 0.15
            peso_cautela = 0.7
            peso_breaking_strategy = 0.15

        elif(segment.slippery < 8 and segment.curve > 8):
            peso_aceleracion = 0.15
            peso_cautela = 0.15
            peso_breaking_strategy = 0.7
        else:
            peso_aceleracion = 0.8
            peso_cautela = 0.1
            peso_breaking_strategy = 0.1

        puntuacion_aceleracion = normalize(driving_style[0], 0, 10)
        puntuacion_cautela = normalize(driving_style[1], 0, 10) 
        puntuacion_breaking_strategy = normalize(driving_style[2], 0, 10)

        fitness_total = (
                         peso_cautela * puntuacion_cautela +
                         peso_breaking_strategy * puntuacion_breaking_strategy+
                         peso_aceleracion * puntuacion_aceleracion)

        return fitness_total

    def seleccionar(self, poblacion, k, segment):
        seleccionados = []
        for _ in range(k):
            seleccionados.append(random.choice(poblacion))
        seleccionados.sort(key=lambda x: self.fitness(x, segment), reverse=True)
        return seleccionados[:k]

    def driving_style_a_lista(self, driving_style):
        return [driving_style.aceleracion, driving_style.cautela, driving_style.braking_strategy]

    def cruzar(self, driving_style1, driving_style2):
        punto_cruce = random.randint(1, len(driving_style1) - 1)
        hijo1 = driving_style1[:punto_cruce] + driving_style2[punto_cruce:]
        hijo2 = driving_style2[:punto_cruce] + driving_style1[punto_cruce:]
        return hijo1, hijo2

    def mutar(self, driving_style_lista):
        probabilidad_mutacion = 0.05
        indice_a_mutar = random.randint(0, len(driving_style_lista) - 1)
        if random.random() < probabilidad_mutacion:
            nuevo_valor = random.randint(0, 10)
            driving_style_lista[indice_a_mutar] = nuevo_valor

    def busqueda_genetica(self, segment):
        
        poblacion_inicial = [ DrivingStyle.generate_random_driving_style()] * random.randint(10, 30)
        
        generaciones = 100
        static = 0
        maximo = -math.inf

        tamaño_poblacion = 10
        
        poblacion_inicial_lista = []
        
        for pil in poblacion_inicial:
            poblacion_inicial_lista.append(self.driving_style_a_lista(pil))
        poblacion = poblacion_inicial_lista

        while (static < generaciones):
            nueva_poblacion = []
            for _ in range(len(poblacion) // 2):
                padre1, padre2 = self.seleccionar(poblacion, 2, segment)
                hijo1, hijo2 = self.cruzar(padre1, padre2)
                self.mutar(hijo1)
                self.mutar(hijo2)
                nueva_poblacion.extend([hijo1, hijo2])
            poblacion_ordenada = sorted(poblacion + nueva_poblacion, key=lambda x: self.fitness(x, segment), reverse=True)
            poblacion = poblacion_ordenada[:int(0.2 * tamaño_poblacion)]
            nuevo_maximo = self.fitness(poblacion[0], segment)
            static = 0 if maximo < nuevo_maximo else 1 + static
            maximo = nuevo_maximo
        mejor_estilo_lista = max(poblacion, key=lambda x: self.fitness(x, segment))
        mejor_estilo = DrivingStyle(mejor_estilo_lista[0], mejor_estilo_lista[1], mejor_estilo_lista[2])
        return mejor_estilo

def normalize( x, min_value, max_value):
    return (x - min_value) / (max_value - min_value)

