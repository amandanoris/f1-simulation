
def extraer_parametros_carrera():
    variables = []

    variables.append("tiempo_promedio")

    variables.append("clima")

    variables.append("no_vueltas")

    variables.append("largo_pista")

    variables.append("dificultad_pista")

    variables.append("dir_lento_deseo")

    variables.append("car_lento_velocidad_max")

    variables.append("lento_tiempo")

    variables.append("lento_experiencia")

    variables.append("lento_victorias")

    variables.append("lento_paradas")

    variables.append("lento_confianza")
    
    variables.append("lento_velocidad_media")

    variables.append("dir_rapido_deseo")

    variables.append("car_rapido_velocidad_max")

    variables.append("rapido_tiempo")

    variables.append("rapido_experiencia")

    variables.append("rapido_victorias")

    variables.append("rapido_paradas")

    variables.append("rapido_confianza")
    
    variables.append("rapido_velocidad_media")
   
    return variables


import csv

def escribir_lista_en_csv(lista_valores, nombre_archivo):
    with open(nombre_archivo, 'a', newline='') as archivo_csv:
        # Crea un objeto writer
        escritor = csv.writer(archivo_csv)
        # Escribe la lista de valores como una nueva fila en el archivo CSV
        escritor.writerow(lista_valores)

escribir_lista_en_csv(extraer_parametros_carrera(), "simulacion.csv")