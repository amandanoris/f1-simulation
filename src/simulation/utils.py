def normalize(x, min_value, max_value):
    return (x - min_value) / (max_value - min_value)

def fitness(piloto, carrera):
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
                     peso_accidentes * puntuacion_accidentes +
                     peso_wins * puntuacion_wins)

    return fitness_total

def strategy_factor(driving_style, segment):

    if (segment.slippery > 6 and segment.curve > 6):
      
        peso_aceleracion = 0.01
        peso_cautela = 0.495
        peso_breaking_strategy = 0.495

    elif (segment.slippery > 6 and segment.curve < 6):
   
        peso_aceleracion = 0.15
        peso_cautela = 0.7
        peso_breaking_strategy = 0.15

    elif(segment.slippery < 6 and segment.curve > 6):
       
        peso_aceleracion = 0.15
        peso_cautela = 0.15
        peso_breaking_strategy = 0.7
         
    else:

        peso_aceleracion = 0.8
        peso_cautela = 0.1
        peso_breaking_strategy = 0.1

    puntuacion_aceleracion = normalize(driving_style.aceleracion, 0, 10)
    puntuacion_cautela = normalize(driving_style.cautela, 0, 10) 
    puntuacion_breaking_strategy = normalize(driving_style.braking_strategy, 0, 10)

    fitness_total = (
                     peso_cautela * puntuacion_cautela +
                     peso_breaking_strategy * puntuacion_breaking_strategy +
                     peso_aceleracion * puntuacion_aceleracion)

    return fitness_total


from Tires import TireAdaptationSystem
def car_factor( tire_type, segment, race):
    
    system =  TireAdaptationSystem()

    tire = tire_type
    
    # Asignar las propiedades del neumático y las características del segmento de carrera a las variables de entrada
    system.tire_sim.input['rugosidad'] = tire.rugosidad
    system.tire_sim.input['resistencia'] = tire.resistencia
    system.tire_sim.input['presion_de_aire'] = tire.presion_de_aire
    system.tire_sim.input['dry_performance'] = tire.dry_performance
    system.tire_sim.input['wet_performance'] = tire.wet_performance
    # Asignar las características del segmento de carrera y el clima
    system.tire_sim.input['longitud'] = segment.length
    system.tire_sim.input['curva'] = segment.curve
    system.tire_sim.input['rugosidad_pista'] = segment.slippery
    system.tire_sim.input['clima'] = race.weather.value
    
    # Calcular la adecuación para el tipo de neumático especificado
    system.tire_sim.compute()
    adecuacion = system.tire_sim.output['adecuacion']
    
    # Devolver la adecuación calculada
    return adecuacion/10
