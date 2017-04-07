import xml.etree.ElementTree
import os

PATH_SALIDA = '/Users/adrianperezgarrone/Desktop/pruebasumodesdeprog/sumo-0.23-2.0/docs/tutorial/traci_tls_mandado_snow/emission2.xml'
PATH_CONFIGURACION_SEMAFOROS = '/Users/adrianperezgarrone/Desktop/pruebasumodesdeprog/sumo-0.23-2.0/docs/tutorial/traci_tls_mandado_snow/data/cross.net.xml'
EJECUCION_SUMO = 'sumo /Users/adrianperezgarrone/Desktop/pruebasumodesdeprog/sumo-0.23-2.0/docs/tutorial/traci_tls_mandado_snow/data/cross.sumocfg'
CONF_SUMO = 'sumo /Users/adrianperezgarrone/Desktop/pruebasumodesdeprog/sumo-0.23-2.0/docs/tutorial/traci_tls_mandado_snow/data/cross.sumocfg.xml'

OUTPUT_PATH = '/Users/adrianperezgarrone/Desktop/pruebasumodesdeprog/sumo-0.23-2.0/docs/tutorial/traci_tls_mandado_snow/emission_'

CICLO = 60

class parametros_parser():

    def __init__(self, secuencia_emissions = 0):
        self.secuencia_emissions = secuencia_emissions

    def set_secuencia_emissions(self, valor):
        self.secuencia_emissions = valor


parametros = parametros_parser()

def parse_salida_sumo():
    e = xml.etree.ElementTree.parse(PATH_SALIDA).getroot()

    print(e)
    vehicleMap = {}
    actualValue = 0

    totalUp = 0
    totalLeft = 0

    sumUp = 0.0
    sumLeft = 0.0

    for atype in e.findall('timestep'):
        for vtype in atype.findall('vehicle'):
            if vtype.get('id') in vehicleMap:
                actualValue = vehicleMap[vtype.get('id')][0]
                if actualValue < float(vtype.get('waiting')):
                    vehicleMap[vtype.get('id')] = (float(vtype.get('waiting')), vtype.get('route'))
                    if vtype.get('route') == 'left':
                        sumLeft = sumLeft - actualValue + float(vtype.get('waiting'))
                    else:
                        sumUp = sumUp - actualValue + float(vtype.get('waiting'))
            else:
                vehicleMap[vtype.get('id')] = (float(vtype.get('waiting')), vtype.get('route'))
                if vtype.get('route') == 'left':
                    totalLeft = totalLeft + 1
                    sumLeft = sumLeft + float(vtype.get('waiting'))
                else:
                    totalUp = totalUp + 1
                    sumUp = sumUp + float(vtype.get('waiting'))

    print('TIempo de espera promedio ruta UP: ', sumUp/totalUp)
    print('TIempo de espera promedio ruta LEFT: ', sumLeft/totalLeft)
    print(vehicleMap)
    promedioVertical = (sumUp/totalUp)
    promedioHorizontal = (sumLeft/totalLeft)
    return (promedioHorizontal + promedioVertical)/2



#Nos estamos adaptando al ejemplo que ya tenemos hecho, asi que modificamos esas 4 fases de acuerdo al porcentaje
#< phase duration = "60" state = "GrGr" / >   las letras en posicion dos y cuatro son las horizontales
#< phase duration = "6" state = "yryr" / >
#< phase duration = "30" state = "rGrG" / >
#< phase duration = "6" state = "ryry" / >
def modificar_fase_semaforos(individual):
    tree = xml.etree.ElementTree.parse(PATH_CONFIGURACION_SEMAFOROS)
    root = tree.getroot()

    semaforos = root.findall("tlLogic/phase")

    alfa = individual[0]
    print "Alfa: %s" %  str(alfa)
    porcentaje = (alfa/100.0)

    duracionEnRojoVertical = CICLO * porcentaje
    print "La duracion de la luz roja en la via vertical es: %s" % str(duracionEnRojoVertical)

    #Para este caso como tenemos 4 fases vamo a dejar la segunda que incluye la amarilla en 1.
    semaforos[0].set("duration", str(CICLO - duracionEnRojoVertical -1))
    semaforos[1].set("duration", str(1))
    semaforos[2].set("duration", str(duracionEnRojoVertical-1))
    semaforos[3].set("duration", str(1))

    tree.write(PATH_CONFIGURACION_SEMAFOROS);


def modificar_output():
    tree = xml.etree.ElementTree.parse(CONF_SUMO)
    root = tree.getroot()

    output = root.findall("output/emission-output")

    secuencia_emissions = parametros.secuencia_emissions + 1

    value = OUTPUT_PATH + str(secuencia_emissions) + '.xml'

    #Para este caso como tenemos 4 fases vamo a dejar la segunda que incluye la amarilla en 1.
    output[0].set("value", str(value))

    tree.write(PATH_CONFIGURACION_SEMAFOROS);
    parametros.set_secuencia_emissions(secuencia_emissions)


def evaluar(individual):
    modificar_fase_semaforos(individual)
    #modificar_output()
    os.system(EJECUCION_SUMO)
    tiempoPromedio = parse_salida_sumo()
    return tiempoPromedio

#modificar_fase_semaforos([50])
#evaluar()