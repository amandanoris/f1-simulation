import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class Tire:
    def __init__(self, rugosidad, resistencia, presion_de_aire, dry_performance, wet_performance):
        self.rugosidad = rugosidad
        self.resistencia = resistencia
        self.presion_de_aire = presion_de_aire
        self.dry_performance = dry_performance
        self.wet_performance = wet_performance
    
class C0Tire(Tire):
    def __init__(self):
        super().__init__(5, 9.5, 7, 8, 2)

class C1Tire(Tire):
    def __init__(self):
        super().__init__(4, 6,9, 9, 4)

class C2Tire(Tire):
    def __init__(self):
        super().__init__(7, 8, 7, 8, 3)

class C3Tire(Tire):
    def __init__(self):
        super().__init__(2, 4, 10, 10, 1)

class GreenIntermediateTire(Tire):
    def __init__(self):
        super().__init__(6, 8,7, 5, 8)

class FullWetBlueTire(Tire):
    def __init__(self):
        super().__init__( 4, 6, 5, 3, 10)

class TireAdaptationSystem:
    def __init__(self):
        # Definir las variables de entrada de los neumaticos
        self.rugosidad = ctrl.Antecedent(np.arange(0, 11, 1), 'rugosidad')
        self.resistencia = ctrl.Antecedent(np.arange(0, 11, 1), 'resistencia')
        self.presion_de_aire = ctrl.Antecedent(np.arange(0, 11, 1), 'presion_de_aire')
        self.dry_performance = ctrl.Antecedent(np.arange(0, 11, 1), 'dry_performance')
        self.wet_performance = ctrl.Antecedent(np.arange(0, 11, 1), 'wet_performance')

        # Definir las variables de entrada del medio
        self.longitud = ctrl.Antecedent(np.arange(0, 1000, 100), 'longitud')
        self.curva = ctrl.Antecedent(np.arange(0, 11, 1), 'curva')
        self.rugosidad_pista = ctrl.Antecedent(np.arange(0, 11, 1), 'rugosidad_pista')
        self.clima = ctrl.Antecedent(np.arange(1, 6), 'clima')

        # Definir la variable de salida
        self.adecuacion = ctrl.Consequent(np.arange(0, 11, 1), 'adecuacion')

        # Definir los conjuntos difusos para las propiedades de los neumaticos
        self.define_fuzzy_sets()

        # Definir las reglas difusas
        self.rules = self.define_rules()

        # Agregar las nuevas reglas al sistema de control
        self.tire_ctrl = ctrl.ControlSystem(self.rules)
        self.tire_sim = ctrl.ControlSystemSimulation(self.tire_ctrl)

    def define_fuzzy_sets(self):
        # Definir los conjuntos difusos para las propiedades de los neumaticos
        self.rugosidad['bajo'] = fuzz.trimf(self.rugosidad.universe, [0, 0, 5])
        self.rugosidad['medio'] = fuzz.trimf(self.rugosidad.universe, [0, 5, 10])
        self.rugosidad['alto'] = fuzz.trimf(self.rugosidad.universe, [5, 10, 10])

        self.resistencia['bajo'] = fuzz.trimf(self.resistencia.universe, [0, 0, 5])
        self.resistencia['medio'] = fuzz.trimf(self.resistencia.universe, [0, 5, 10])
        self.resistencia['alto'] = fuzz.trimf(self.resistencia.universe, [5, 10, 10])

        self.presion_de_aire['bajo'] = fuzz.trimf(self.presion_de_aire.universe, [0, 0, 5])
        self.presion_de_aire['medio'] = fuzz.trimf(self.presion_de_aire.universe, [0, 5, 10])
        self.presion_de_aire['alto'] = fuzz.trimf(self.presion_de_aire.universe, [5, 10, 10])

        self.dry_performance['bajo'] = fuzz.trimf(self.dry_performance.universe, [0, 0, 5])
        self.dry_performance['medio'] = fuzz.trimf(self.dry_performance.universe, [0, 5, 10])
        self.dry_performance['alto'] = fuzz.trimf(self.dry_performance.universe, [5, 10, 10])

        self.wet_performance['bajo'] = fuzz.trimf(self.wet_performance.universe, [0, 0, 5])
        self.wet_performance['medio'] = fuzz.trimf(self.wet_performance.universe, [0, 5, 10])
        self.wet_performance['alto'] = fuzz.trimf(self.wet_performance.universe, [5, 10, 10])

        # Definir los conjuntos difusos para las propiedades del medio
        self.longitud['corta'] = fuzz.trimf(self.longitud.universe, [0, 0, 500])
        self.longitud['media'] = fuzz.trimf(self.longitud.universe, [0, 500, 1000])
        self.longitud['larga'] = fuzz.trimf(self.longitud.universe, [500, 1000, 1000])

        self.curva['recta'] = fuzz.trimf(self.curva.universe, [0, 0, 5])
        self.curva['curva'] = fuzz.trimf(self.curva.universe, [0, 5, 10])

        self.rugosidad_pista['lisa'] = fuzz.trimf(self.rugosidad_pista.universe, [0, 0, 5])
        self.rugosidad_pista['intermedia'] = fuzz.trimf(self.rugosidad_pista.universe, [0, 5, 10])
        self.rugosidad_pista['rugosa'] = fuzz.trimf(self.rugosidad_pista.universe, [5, 10, 10])

        self.clima['soleado'] = fuzz.trimf(self.clima.universe, [1, 1, 3])
        self.clima['nublado'] = fuzz.trimf(self.clima.universe, [2, 3, 4])
        self.clima['lluvioso'] = fuzz.trimf(self.clima.universe, [3, 4, 5])

        # Definir los conjuntos difusos para la adecuación
        self.adecuacion['bajo'] = fuzz.trimf(self.adecuacion.universe, [0, 0, 5])
        self.adecuacion['medio'] = fuzz.trimf(self.adecuacion.universe, [0, 5, 10])
        self.adecuacion['alto'] = fuzz.trimf(self.adecuacion.universe, [5, 10, 10])

    def define_rules(self):
        # Definir las reglas difusas
        rule1 = ctrl.Rule(self.rugosidad['bajo'] & self.resistencia['bajo'], self.adecuacion['alto'])
        rule2 = ctrl.Rule(self.presion_de_aire['alto'] & self.dry_performance['alto'], self.adecuacion['medio'])
        rule3 = ctrl.Rule(self.wet_performance['alto'], self.adecuacion['bajo'])
        rule4 = ctrl.Rule(self.longitud['corta'] & self.curva['curva'] & self.rugosidad_pista['rugosa'] & self.clima['lluvioso'], self.adecuacion['alto'])
        rule5 = ctrl.Rule(self.longitud['media'] & self.curva['recta'] & self.rugosidad_pista['lisa'] & self.clima['soleado'], self.adecuacion['medio'])
        rule6 = ctrl.Rule(self.longitud['larga'] & self.curva['curva'] & self.rugosidad_pista['intermedia'] & self.clima['nublado'], self.adecuacion['bajo'])
        rule7 = ctrl.Rule(self.clima['lluvioso'] & self.wet_performance['alto'], self.adecuacion['alto'])
        rule8 = ctrl.Rule(self.clima['soleado'] & self.dry_performance['alto'], self.adecuacion['alto'])
        rule9 = ctrl.Rule(self.rugosidad_pista['lisa'] & self.rugosidad['alto'], self.adecuacion['alto'])
        rule10 = ctrl.Rule(self.rugosidad_pista['rugosa'] & self.rugosidad['bajo'], self.adecuacion['alto'])
        rule11 = ctrl.Rule(self.rugosidad_pista['lisa'] & self.resistencia['medio'], self.adecuacion['alto'])
        rule12 = ctrl.Rule(self.rugosidad_pista['rugosa'] & self.resistencia['alto'], self.adecuacion['alto'])

        return [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12]

    def simulate(self, race, segment):
        # Inicializar un diccionario para almacenar la adecuación de cada tipo de neumático
        adecuaciones = {}

        # Iterar sobre cada tipo de neumático
        for tire_class in [C0Tire, C1Tire, C2Tire, C3Tire, GreenIntermediateTire, FullWetBlueTire]:
            # Crear una instancia del neumático
            tire = tire_class()
            
            # Asignar las propiedades del neumático y las características del segmento de carrera a las variables de entrada
            self.tire_sim.input['rugosidad'] = tire.rugosidad
            self.tire_sim.input['resistencia'] = tire.resistencia
            self.tire_sim.input['presion_de_aire'] = tire.presion_de_aire
            self.tire_sim.input['dry_performance'] = tire.dry_performance
            self.tire_sim.input['wet_performance'] = tire.wet_performance
            # Asignar las características del segmento de carrera y el clima
            self.tire_sim.input['longitud'] = segment.length
            self.tire_sim.input['curva'] = segment.curve
            self.tire_sim.input['rugosidad_pista'] = segment.slippery
            self.tire_sim.input['clima'] = race.weather.value
            
            # Calcular la adecuación para el tipo de neumático actual
            self.tire_sim.compute()
            adecuacion = self.tire_sim.output['adecuacion']
            
            # Almacenar la adecuación en el diccionario
            adecuaciones[tire_class.__name__] = adecuacion
        
        # Encontrar el tipo de neumático con la mejor adecuación
        mejor_adecuacion_nombre = max(adecuaciones, key=adecuaciones.get)

        # Obtener la referencia a la clase por su nombre
        mejor_adecuacion_clase = globals()[mejor_adecuacion_nombre]
    
        # Crear una instancia de la clase del mejor tipo de neumático
        mejor_adecuacion_instancia = mejor_adecuacion_clase()

        return mejor_adecuacion_instancia


