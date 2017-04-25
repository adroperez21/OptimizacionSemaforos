import random
import Parser
import Entorno
from deap import base
from deap import creator
from deap import tools
from scoop import futures


def evaluarPromedio(individual):
    return Parser.evaluar(individual),

def algorithm_genetic():

    #Lo hago asi para asi despues lo cargamos desde otro lado y no hardcodeado, neniarol inteligencia
    parametros = Entorno.parametros()

    parametros.set_NGEN(10)                 #Numero de generaciones
    parametros.set_CXPB(0.10)               #Termino de crossover
    parametros.set_MUTPB(0.20)              #Probabilidad de mutacion
    parametros.set_individual_min(1)        #Menor valor que puede obtener un individuo
    parametros.set_individual_max(100)      #Mayor valor que puede obtener un individuo
    parametros.set_individual_lengh(1)      #Cantidad de valores que se representa un individuo
    parametros.set_population(10)           #Cantidad inicial de la poblacion
    parametros.set_indbp(0.05)              #Parametro de mutacion
    parametros.set_tournament_size(3)       #Parametro de seleccion

    creator.create("FitnessMin", base.Fitness, weights=(-1.0, 1.0))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()

    toolbox.register("attr_int", random.randint, parametros.individual_min, parametros.individual_max)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, parametros.individual_lengh)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    #Operadores
    toolbox.register("evaluate", evaluarPromedio)
    toolbox.register("mate", tools.cxUniform)
    toolbox.register("mutate", tools.mutUniformInt, low=1, up=100, indpb=parametros.indbp)
    toolbox.register("select", tools.selTournament, tournsize=parametros.tournament_size)
    toolbox.register("map", futures.map)



    NGEN,CXPB,MUTPB,population  = parametros.NGEN, parametros.CXPB, parametros.MUTPB, parametros.population

    print("-------Poblacion inicial-------")
    pop = toolbox.population(n=population)
    print pop

    print("Evaluacion de fitness de poblacion inicial")
    fitnesses = list(map(toolbox.evaluate, pop))

    #Recorremos los fitness y se lo asignamos a la propiedad fitness de cada individuo.
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print("Se han evaluado %i individuos" % len(fitnesses))

    fits = [ind.fitness.values[0] for ind in pop]
    print("Estadistica del fitness")
    print("  Min: %s" % min(fits))
    print("  Max: %s" % max(fits))

    for g in range(NGEN):
        print("-------Generacion %i -------" % g)
        # Seleccionamoa a la nueva generacion de individuos
        offspring = toolbox.select(pop, len(pop))
        #Clonamos a los individuos seleccionados
        offspring = list(map(toolbox.clone, offspring))
        #Aplicacmos crossover y mutacion en el offSpring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            #if random.random() < CXPB:
            toolbox.mate(child1, child2, CXPB)
            del child1.fitness.values
            del child2.fitness.values

        for mutant in offspring:
            toolbox.mutate(mutant)
            del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring

        fits = [ind.fitness.values[0] for ind in pop]
        print("-------Fin de la eneracion %i -------" % g)

        print("Estadistica del fitness de la generacion %i" %g)
        print fits
        print("  Min: %s" % min(fits))
        print("  Max: %s" % max(fits))

    print("#######  FIN DEL ALGORITMO  #######")
    best_ind = tools.selBest(pop, 1)[0]
    print("El mejor individuo es: %s, %s" % (best_ind, best_ind.fitness.values))