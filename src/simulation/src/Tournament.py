import random

class Torneo:
    def __init__(self):
        self.tabla_posiciones = {}

    @staticmethod
    def generar_torneo_random(lista_equipos):
        # Crear una instancia de Torneo
        torneo = Torneo()
        
        # Asegurarse de que la lista de equipos no esté vacía
        if not lista_equipos:
            raise ValueError("La lista de equipos no puede estar vacía.")
        
        # Generar una tabla de posiciones aleatoria
        for i in range(len(lista_equipos)):
            equipo = random.choice(lista_equipos)
            puntos = random.randint(1, 100) # Asumiendo que los puntos pueden variar entre 1 y 10
            torneo.tabla_posiciones[equipo] = {'puntos': puntos}
            lista_equipos.remove(equipo) # Remover el equipo seleccionado para evitar duplicados
        
        # Ordenar la tabla de posiciones por puntos
        torneo.tabla_posiciones = dict(sorted(torneo.tabla_posiciones.items(), key=lambda item: item[1]['puntos'], reverse=True))
        
        return torneo

    def actualizar_tabla_posiciones_f1(self, nueva_tabla):
        puntos_por_posicion = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
        
        for piloto, equipo in nueva_tabla.items():

            posicion = list(nueva_tabla.keys()).index(piloto) + 1

            if posicion > 10:
                continue

            puntos = puntos_por_posicion[posicion - 1]
            
            self.tabla_posiciones[equipo]['puntos'] += puntos

        self.tabla_posiciones = dict(sorted(self.tabla_posiciones.items(), key=lambda item: item[1]['puntos'], reverse=True))

    def obtener_posicion_y_puntos(self, nombre_equipo):
   
        posicion = list(self.tabla_posiciones.keys()).index(nombre_equipo) + 1

        puntos = self.tabla_posiciones[nombre_equipo]['puntos']
        
        return posicion, puntos
    


    def calcular_diferencia_puntos(self, nombre_equipo):
        tabla_ordenada = dict(sorted(self.tabla_posiciones.items(), key=lambda item: item[1]['puntos'], reverse=True))
    
        posicion_equipo = list(tabla_ordenada.keys()).index(nombre_equipo) + 1

        puntos_equipo = tabla_ordenada[nombre_equipo]['puntos']

        diferencia_puntos_arriba = 0
        diferencia_puntos_abajo = 0
 
        if posicion_equipo > 1:
           equipo_arriba = list(tabla_ordenada.keys())[posicion_equipo - 2]
           puntos_equipo_arriba = tabla_ordenada[equipo_arriba]['puntos']
           diferencia_puntos_arriba = puntos_equipo_arriba - puntos_equipo
  
        if posicion_equipo < len(tabla_ordenada):
           equipo_abajo = list(tabla_ordenada.keys())[posicion_equipo]
           puntos_equipo_abajo = tabla_ordenada[equipo_abajo]['puntos']
           diferencia_puntos_abajo = puntos_equipo - puntos_equipo_abajo
    
        return diferencia_puntos_arriba, diferencia_puntos_abajo




'''
# Ejemplo de uso
lista_equipos = ['Equipo A', 'Equipo B', 'Equipo C', 'Equipo D', 'Equipo E']
torneo_random = Torneo.generar_torneo_random(lista_equipos)

# Imprimir la tabla de posiciones del torneo generado aleatoriamente
for pos, equipo in enumerate(torneo_random.tabla_posiciones, start=1):
    print(f"{pos}. {equipo}: {torneo_random.tabla_posiciones[equipo]['puntos']} puntos")

nueva_tabla = {
    'Piloto 1': 'Equipo A',
    'Piloto 2': 'Equipo B',
    'Piloto 3': 'Equipo A',
    'Piloto 4': 'Equipo C',
    'Piloto 5': 'Equipo B',
    'Piloto 6': 'Equipo A'
}

torneo_random.actualizar_tabla_posiciones_f1(nueva_tabla)
for pos, equipo in enumerate(torneo_random.tabla_posiciones, start=1):
    print(f"{pos}. {equipo}: {torneo_random.tabla_posiciones[equipo]['puntos']} puntos")

posicion, puntos = torneo_random.obtener_posicion_y_puntos('Equipo A')
print(f"Equipo A está en la posición {posicion} con {puntos} puntos.")

diferencia_puntos_arriba, diferencia_puntos_abajo = torneo_random.calcular_diferencia_puntos('Equipo A')
print(f"La diferencia de puntos entre 'Equipo A' y el equipo de arriba es: {diferencia_puntos_arriba}")
print(f"La diferencia de puntos entre 'Equipo A' y el equipo de abajo es: {diferencia_puntos_abajo}")
'''
