from src.Director import Director, DirectorBeliefs, DirectorDesires
from src.Pilots import  PilotBeliefs
from src.Mechanics import MechanicDesires
from src.PitStop import PitStop
import time
import random
from src.Tournament import Torneo
from src.Race import Race
import csv

def encontrar_indice_director_por_piloto(nombre_piloto, lista_directores):
    indice = False
    for i in range(len(lista_directores)):
        for piloto in lista_directores[i].equipo.pilotos:
            if piloto.name == nombre_piloto:
                indice = i
    return indice

def encontrar_indice_de_piloto(nombre_piloto, lista_pilotos):
    indice = False
    for i in range(len(lista_pilotos)):
            if lista_pilotos[i] == nombre_piloto:
                indice = i
    return indice


def generate_n_random_directors(race):
    directors = []
    for _ in range(race.no_teams):
        director = Director.generate_random_director(race)
        directors.append(director)
    return directors

def race_prep(directors,race):
    pilots = []
    deseos = []
    
    for dir in directors:

        desire = dir.creencias.determinar_deseo()
        deseos.append(desire.value)

        if desire == DirectorDesires.mantener_posicion_dos:
           selected_pilot1, selected_pilot2 = dir.intenciones.ejecutar_accion_por_deseo(dir.intenciones, desire , dir.equipo.pilotos)
        else:
           selected_pilot1, selected_pilot2 = dir.intenciones.ejecutar_accion_por_deseo(dir.intenciones, desire , dir.equipo.pilotos, dir.creencias.race)
        
        pilots.append(selected_pilot1)
        pilots.append(selected_pilot2)
        #print(selected_pilot1.name + " y " + selected_pilot2.name + "fueron seleccionado para la carrera por el director del equipo "+ dir.equipo.name)
        
        desire_inform = DirectorDesires.informar_piloto
        dir.intenciones.ejecutar_accion_por_deseo(dir.intenciones, desire_inform, selected_pilot1, race, dir.equipo.sistema_mensajeria)
        known_race = selected_pilot1.recibir_mensajes()[0].contenido
        selected_pilot1.creencias = PilotBeliefs(dir.equipo.car, False, known_race, 5, 0, 0)

        desire_inform = DirectorDesires.informar_piloto
        dir.intenciones.ejecutar_accion_por_deseo(dir.intenciones, desire_inform, selected_pilot2, race, dir.equipo.sistema_mensajeria)
        known_race = selected_pilot2.recibir_mensajes()[0].contenido
        selected_pilot2.creencias = PilotBeliefs(dir.equipo.car, False, known_race, 5, 0, 0)
        #print("El director y los pilotos seleccionados estan hablando")

    return pilots, deseos

from src.utils import fitness, strategy_factor, car_factor

def calcular_velocidades(directors, pilots, race, segments):
    velocidades = [100] * len(pilots)

    for i in range(0, len(pilots), 2): # Ahora se incrementa el índice en 2 para manejar dos pilotos por director
        factor_piloto_1 = fitness(pilots[i], race)
        factor_estrategia_1 = strategy_factor(pilots[i].estrategia, segments[i])
        factor_car_1 = car_factor(directors[i // 2].equipo.car.tires, segments[i], race)
        velocidades[i] = ( (factor_piloto_1 + factor_estrategia_1 + factor_car_1)/3 ) * directors[i // 2].equipo.car.velocidad_max +100

        # Asegurarse de que hay un segundo piloto para el director actual
        if i + 1 < len(pilots):
            factor_piloto_2 = fitness(pilots[i + 1], race)
            factor_estrategia_2 = strategy_factor(pilots[i + 1].estrategia, segments[i + 1])
            factor_car_2 = car_factor(directors[i // 2].equipo.car.tires, segments[i + 1], race)
            velocidades[i + 1] = ( (factor_piloto_2 + factor_estrategia_2 + factor_car_2)/3 ) * directors[i // 2].equipo.car.velocidad_max +100

    return velocidades


def calcular_segmentos(race):
    segmentos = race.track.segments
    segmentos_pilotos = []

    for metros_recorridos in race.metros_recorridos:
        
        remaining_meters = metros_recorridos % race.track.length
        
        current_segment_index = 0
        while remaining_meters >= segmentos[current_segment_index].length:
            remaining_meters -= segmentos[current_segment_index].length
            current_segment_index += 1

        segmentos_pilotos.append(segmentos[current_segment_index])

    return segmentos_pilotos


def calcular_tabla(tiempos, pilots, directors):
    # Ordenar los tiempos junto con sus índices
    tiempos_ordenados = sorted(enumerate(tiempos), key=lambda x: x[1])
    
    pos_table = {}
    
    # Iterar sobre todos los elementos en metros_ordenados
    for piloto_index, metros in tiempos_ordenados:
        name = pilots[piloto_index].name
        dir = directors[encontrar_indice_director_por_piloto(name, directors)] 
        pos_table[name] = dir.equipo.name
     
    return pos_table


def calcular_tabla_intermedia(metros_recorridos, pilots, directors):
    # Ordenar los metros recorridos en orden descendente
    metros_ordenados = sorted(enumerate(metros_recorridos), key=lambda x: x[1], reverse=True)
    
    pos_table = {}
    
    # Iterar sobre todos los elementos en metros_ordenados
    for piloto_index, metros in metros_ordenados:
        name = pilots[piloto_index].name
        dir = directors[encontrar_indice_director_por_piloto(name, directors)] 
        pos_table[name] = dir.equipo.name
     
    return pos_table

def get_finals(race, final_times, tiempo_transcurrido):
    for i in range (len(final_times)):
        if(race.metros_recorridos[i] > (race.track.length*race.no_laps) and final_times[i] == 0 ):
            final_times[i] = tiempo_transcurrido
    return final_times

def extraer_parametros_carrera(race, tiempos, deseos, directors, rapido, lento, pilotos):
    variables = []

    #pista y general
    #tiempo promedio de carrera
    tiempo_promedio = sum(tiempos*100) / len(tiempos)
    variables.append(tiempo_promedio)
       
    #clima de la carrera
    clima = race.weather.value
    variables.append(clima)

    #cantidad de vueltas
    no_vueltas = race.no_laps
    variables.append(no_vueltas)

    #largo de la pista
    largo_pista = race.track.length
    variables.append(largo_pista*100)

    #dificulatd de la pista
    dificultad_pista = race.track.type
    variables.append(dificultad_pista)
    
    #piloto mas lento
    #indice del director del piloto mas lento
    dir_lento_index = encontrar_indice_director_por_piloto(lento, directors)
    
    #deseo del director del mas lento
    dir_lento_deseo = deseos[dir_lento_index]
    variables.append(dir_lento_deseo)

    #velocidad maxima del carro del mas lento
    car_lento_velocidad_max = directors[dir_lento_index].equipo.car.velocidad_max
    variables.append(car_lento_velocidad_max)
    
    #indice del piloto mas lento 
    lento_index = encontrar_indice_de_piloto(lento, pilotos)

    #tiempo del piloto mas lento
    lento_tiempo = tiempos[lento_index]
    variables.append(lento_tiempo*100)

    #anos de experiencia del lento
    lento_experiencia = pilotos[lento_index].anos_de_experiencia
    variables.append(lento_experiencia)

    #cantidad de carreras ganadas del lento
    lento_victorias = pilotos[lento_index].no_racewins
    variables.append(lento_victorias)

    #cantidad de paradas del lento
    lento_paradas = pilotos[lento_index].no_stops
    variables.append(lento_paradas)

    #confianza del lento
    lento_confianza = pilotos[lento_index].creencias.confianza
    variables.append(lento_confianza)
    
    #velocidad media
    lento_velocidad_media = largo_pista*no_vueltas/lento_tiempo
    variables.append(lento_velocidad_media)

    #piloto mas rapido
    #indice del director del piloto mas rapido
    dir_rapido_index = encontrar_indice_director_por_piloto(rapido, directors)
    
    #deseo del director del mas rapido
    dir_rapido_deseo = deseos[dir_rapido_index]
    variables.append(dir_rapido_deseo)

    #velocidad maxima del carro del mas rapido
    car_rapido_velocidad_max = directors[dir_rapido_index].equipo.car.velocidad_max
    variables.append(car_rapido_velocidad_max)
    
    #indice del piloto mas rapido 
    rapido_index = encontrar_indice_de_piloto(rapido, pilotos)

    #tiempo del piloto mas rapido
    rapido_tiempo = tiempos[rapido_index]
    variables.append(rapido_tiempo*100)

    #anos de experiencia del rapido
    rapido_experiencia = pilotos[rapido_index].anos_de_experiencia
    variables.append(rapido_experiencia)

    #cantidad de carreras ganadas del rapido
    rapido_victorias = pilotos[rapido_index].no_racewins
    variables.append(rapido_victorias)

    #cantidad de paradas del rapido
    rapido_paradas = pilotos[rapido_index].no_stops
    variables.append(rapido_paradas)

    #confianza del rapido
    rapido_confianza = pilotos[rapido_index].creencias.confianza
    variables.append(rapido_confianza)
    
    #velocidad media
    rapido_velocidad_media = largo_pista*no_vueltas/rapido_tiempo
    variables.append(rapido_velocidad_media)
   
    return variables

def race_sim(directors, pilots, race, deseos):
    print("The race begins")
    print("The length of the track is "+ str(race.track.length) + " with "+str(race.no_laps) +" laps to go" )

    # Comienza la carrera
    race.is_happening = True
    
    # Paso de tiempo para los updates
    paso_tiempo = 5

    # Lista de tiempos finales
    final_times = [0] * len(pilots)
    laps_times = [[0 for _ in range(len(pilots))] for _ in range(race.no_laps)]
    
    tabla_inicial = calcular_tabla_intermedia(race.metros_recorridos, pilots, directors)
    race.update(tabla_inicial)

    segmentos_actuales = [race.track.segments[0]] * len(pilots)

    for pil in pilots:
        pil.creencias.segment = segmentos_actuales[0]

    piloto_dir =[]
    for i in range(len(pilots)):
        piloto_dir.append(directors[encontrar_indice_director_por_piloto(pilots[i].name, directors)])


    # Lista de pitstops
    stops = [0] * len(pilots)

    while True:
        
        # Tiempo transcurrido en la carrera
        tiempo_transcurrido = time.time() - race.start_time

        # Revisar si ya todos los pilotos completaron todas las vueltas
        if race.condicion_de_finalizacion():
            race.is_happening = False
            break
 
        # Calcular el segmento de la carrera en que se encuentra cada piloto
        segmentos_actuales = calcular_segmentos(race)

        # Calcular la velocidad con la que va a manejar cada piloto en el segmento en el que se encuentra
        velocidades_actuales = calcular_velocidades(directors, pilots, race, segmentos_actuales)
        
        # Los pilotos chekean sus neumaticos y la necesidad de hacer un pitstop
        for i in range(len(pilots)): 

            pilots[i].check_tires()
            
            if(pilots[i].do_pitstop):
                stops[i] = PitStop(time.time(), random.choice(piloto_dir[i].equipo.mecanicos))

                stops[i].mechanic.intenciones.ejecutar_accion_por_deseo(stops[i].mechanic.intenciones, MechanicDesires.cambiar_neumatico, piloto_dir[i].equipo.car, race, segmentos_actuales[i], stops[i].mechanic.creencias.tire_adaptation_system)
                stops[i].mechanic.intenciones.ejecutar_accion_por_deseo(stops[i].mechanic.intenciones, MechanicDesires.informar_piloto, pilots[i], segmentos_actuales[i], piloto_dir[i].equipo.sistema_mensajeria)
                
                known_segment = pilots[i].recibir_mensajes()[0].contenido
                pilots[i].creencias.segment = known_segment
                intencion = pilots[i].creencias.determinar_intencion()
                pilots[i].estrategia = pilots[i].intenciones.ejecutar_accion_por_deseo(pilots[i].intenciones, intencion, known_segment)
             
                pilots[i].do_pitstop = False

            if(stops[i] != 0 and stops[i].is_happening()):
                velocidades_actuales[i] = 0
            
            pilots[i].creencias.update_conocimiento(segmentos_actuales[i], race.pos_table, pilots[i].name)


        # Actualizar las posiciones de los pilotos mediante los metros que han recorrido
        race.update_metros_recorridos(velocidades_actuales, paso_tiempo, directors, segmentos_actuales)
        # Actualiza las vueltas
        race.update_lap()
        # Actualiza los tiempos finales
        final_times = get_finals(race, final_times, tiempo_transcurrido)
        # Actualiza los tiempos x vueltas
                
        # Actualizar la tabla de posiciones
        nueva_tabla = calcular_tabla_intermedia(race.metros_recorridos, pilots, directors)
        race.update(nueva_tabla)

        for i in range(0, len(pilots)):
           print("The actual speed of the driver" + pilots[i].name + " is " + str(int(velocidades_actuales[i]))   )


        time.sleep(paso_tiempo)     
    
    tabla_final = calcular_tabla(final_times, pilots, directors)
    race.update(tabla_final)
    # Iterar sobre los elementos del diccionario
    print("Below is the final table of race positions.")
    for posicion, (piloto, equipo) in enumerate(tabla_final.items(), start=1):
       print(f"Posición {posicion} pilotos {piloto} del equipo {equipo}")


    print(f"The race lasted {int(race.duration)} seconds.")
    '''
    print(final_times)
    for i in range(len(pilots)):
        print(pilots[i].name +" "+ str(final_times[i]))
    '''
   
    primer_piloto = next(iter(tabla_final.items()))
    rapido = primer_piloto[0]

    ultimo_piloto = next(reversed(list(tabla_final.items())))
    lento = ultimo_piloto[0]

    variables = extraer_parametros_carrera(race, final_times, deseos, directors, rapido, lento, pilots)
    return variables

def escribir_lista_en_csv(lista_valores, nombre_archivo):
    with open(nombre_archivo, 'a', newline='') as archivo_csv:
        # Crea un objeto writer
        escritor = csv.writer(archivo_csv)
        # Escribe la lista de valores como una nueva fila en el archivo CSV
        escritor.writerow(lista_valores)

def extraer_datos():
    
    for _ in range(100):
        
        race = Race.create_race()
        directors = generate_n_random_directors(race)
        for dir in directors:
           race.equipos.append(dir.equipo.name)
        torneo_random = Torneo.generar_torneo_random(race.equipos)
        for dir in directors:
           dir.creencias = DirectorBeliefs(race, dir.equipo, torneo_random)
        pilots, deseos = race_prep(directors)
        variables = race_sim(directors,pilots,race, deseos)

        escribir_lista_en_csv(variables, "simulacion.csv")
        

import sys

def redirect_stdout_to_file(file_path):

    # Guarda la salida estándar original
    original_stdout = sys.stdout
    

    with open(file_path, 'w') as file:

        sys.stdout = file
 
        race = Race.create_race()
        directors = generate_n_random_directors(race)
        for dir in directors:
           race.equipos.append(dir.equipo.name)
        torneo_random = Torneo.generar_torneo_random(race.equipos)
        for dir in directors:
           dir.creencias = DirectorBeliefs(race, dir.equipo, torneo_random)
        pilots, deseos = race_prep(directors, race)
        variables = race_sim(directors,pilots,race, deseos)
        #print(variables)
        # Restaura la salida estándar original
        sys.stdout = original_stdout
