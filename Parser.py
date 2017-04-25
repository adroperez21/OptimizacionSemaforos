from xml.etree import ElementTree
import os


#Semaforos a tener en cuenta
#917490524
#917618484


def load_paths():
    global path_configuracion_semaforos
    global path_salida
    global path_ejecucion_sumo
    with open('./paths.xml', 'rt') as pt:
        print pt
        parser_tree = ElementTree.parse(pt)
        p = parser_tree.getroot()
    for node in p.findall('path'):
        name = node.attrib.get('name')
        if name == 'configuracion':
            path_configuracion_semaforos = node.attrib.get('path')
        if name == 'salida':
            path_salida = node.attrib.get('path')
        if name == 'ejecucion_sumo':
            path_ejecucion_sumo = node.attrib.get('path')

def parse_salida_sumo():
    with open(path_salida, 'rt') as ps:
        tree = ElementTree.parse(ps)
        e = tree.getroot()

    print(e)
    vehicle_map = {}

    total_up = 0
    total_left = 0

    sum_up = 0.0
    sum_left = 0.0

    for atype in e.findall('timestep'):
        for vtype in atype.findall('vehicle'):
            if vtype.get('id') in vehicle_map:
                actual_value = vehicle_map[vtype.get('id')][0]
                if actual_value < float(vtype.get('waiting')):
                    vehicle_map[vtype.get('id')] = (float(vtype.get('waiting')), vtype.get('route'))
                    if vtype.get('route') == 'left':
                        sum_left = sum_left - actual_value + float(vtype.get('waiting'))
                    else:
                        sum_up = sum_up - actual_value + float(vtype.get('waiting'))
            else:
                vehicle_map[vtype.get('id')] = (float(vtype.get('waiting')), vtype.get('route'))
                if vtype.get('route') == 'left':
                    total_left = total_left + 1
                    sum_left = sum_left + float(vtype.get('waiting'))
                else:
                    total_up = total_up + 1
                    sum_up = sum_up + float(vtype.get('waiting'))

    print('TIempo de espera promedio ruta UP: ', sum_up / total_up)
    print('TIempo de espera promedio ruta LEFT: ', sum_left / total_left)
    print(vehicle_map)
    promedio_vertical = (sum_up / total_up)
    promedio_horizontal = (sum_left / total_left)
    return promedio_horizontal, promedio_vertical


def modificar_fase_semaforos_v2(individual):
    load_paths()
    tree = ElementTree.parse(path_configuracion_semaforos)
    root = tree.getroot()
    ciclo_semaforos = 60

    semaforos = root.findall("tlLogic")

    alfa = individual[0]
    alfa2 = individual[0]
    print "Alfa: %s" % str(alfa)
    porcentaje = (alfa / 100.0)
    porcentaje2 = (alfa2 / 100.0)
    duracion_rojo = ciclo_semaforos * porcentaje
    duracion_rojo_2 = ciclo_semaforos * porcentaje2
    #print "La duracion de la luz roja en la via vertical es: %s" % str(duracion_rojo_vertical)

    for tlLogic in semaforos:
        if tlLogic.get('id') == '917490524':
            durations = tlLogic.findall("phase")
            durations[0].set("duration", str(ciclo_semaforos - duracion_rojo - 1))
            durations[1].set("duration", str(1))
            durations[2].set("duration", str(duracion_rojo - 1))
            durations[3].set("duration", str(1))
        if tlLogic.get('id') == '917618484':
            durations = tlLogic.findall("phase")
            durations[0].set("duration", str(ciclo_semaforos - duracion_rojo_2 - 1))
            durations[1].set("duration", str(1))
            durations[2].set("duration", str(duracion_rojo_2 - 1))
            durations[3].set("duration", str(1))

    tree.write(path_configuracion_semaforos)

modificar_fase_semaforos_v2([100,100])

def modificar_fase_semaforos(individual):
    load_paths()
    tree = ElementTree.parse(path_configuracion_semaforos)
    root = tree.getroot()
    ciclo_semaforos = 60
    semaforos = root.findall("tlLogic/phase")

    alfa = individual[0]
    print "Alfa: %s" % str(alfa)
    porcentaje = (alfa / 100.0)

    duracion_rojo_vertical = ciclo_semaforos * porcentaje
    print "La duracion de la luz roja en la via vertical es: %s" % str(duracion_rojo_vertical)

    # Para este caso como tenemos 4 fases vamo a dejar la segunda que incluye la amarilla en 1.
    semaforos[0].set("duration", str(ciclo_semaforos - duracion_rojo_vertical - 1))
    semaforos[1].set("duration", str(1))
    semaforos[2].set("duration", str(duracion_rojo_vertical - 1))
    semaforos[3].set("duration", str(1))

    tree.write(path_configuracion_semaforos)


def ejejcutar_sumo():
    os.system(path_ejecucion_sumo)


def evaluar(individual):
    load_paths()
    modificar_fase_semaforos(individual)
    ejejcutar_sumo()
    tiempo_promedio_horizontal, tiempo_promedio_vertical = parse_salida_sumo()
    return tiempo_promedio_horizontal, tiempo_promedio_vertical
