import random
import Parser

from deap import base
from deap import creator
from deap import tools
from scoop import futures


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin) #Hacemos una lista (por mas que sea una lista de un solo elemento) por si despues se desea modificar y agregar mas factores

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("attr_int", random.randint, 1, 100) #Generamos un numero randomico entre 1 y 100, este sera el porcentaje de rojo que estara el semadforo en el lado vertical
# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, 1) #Genero el individuo con una lista de 4 posiciones. Esto lo que hace es crear un individuo del tipo Individual que se genera repitiendo 4 veces el metodo attr_int
toolbox.register("population", tools.initRepeat, list, toolbox.individual) #Hacemos lo mismo que la pasada, solo que repetimos la inicializacion de individuos y los ponemos en una lista, el parametro que falta que es de veces se lo pasamos directo al metodo


def evaluarPromedio(individual):
    return Parser.evaluar(individual),

#def evalOneMax(individual):
 #   return sum(individual),

#Operadores
toolbox.register("evaluate", evaluarPromedio)
toolbox.register("mate", tools.cxUniform)
toolbox.register("mutate", tools.mutUniformInt, low=1, up=100, indpb=0.02)
toolbox.register("select", tools.selTournament, tournsize=3)
#toolbox.register("map", futures.map)


ind1 = toolbox.individual()
#print ind1[0]
#print ind1[1]
#print ind1
#Parser.modificar_fase_semaforos(ind1)

pop1 = toolbox.population(n=5)
print ind1
print pop1

NGEN = 10
#CXPB = 0.50
#MUTPB = 0.20

#Algoritmo
def main():
    print("GENERACION INICIAL")
    pop = toolbox.population(n=10) #Inicializamos poblacion, una lista de 10 individuos. Recordemos que cada individuo es una lista de enteros
    print pop
    # Evaluamos la poblacion inicial,  lo que hacemos aca es crear una lista con el fitness de cada individuo de la poblacion
    fitnesses = list(map(toolbox.evaluate, pop))

    #Recorremos los fitness y se lo asignamos a la propiedad fitness de cada individuo.
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print("INDIVIDUOS EVALUADOS: %i " % len(fitnesses))


    fits = [ind.fitness.values[0] for ind in pop]
    print(" ESTADISITICAS DE FITNESSES")
    print("  MIN %s" % min(fits))
    print("  MAX %s" % max(fits))

    #Comienza la evolucion generacion a generacion
    for g in range(NGEN):
        print("-- GENERACION %i --" % g)
        # Seleccionamoa a la nueva generacion de individuos
        offspring = toolbox.select(pop, len(pop))
        print offspring
        #Clonamos a los individuos seleccionados
        offspring = list(map(toolbox.clone, offspring))
        print offspring
        #Aplicacmos crossover y mutacion en el offSpring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            #if random.random() < CXPB:
            toolbox.mate(child1, child2, 0.10)
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
        print(" ESTADISITICAS DE FITNESSES")
        print("  MIN %s" % min(fits))
        print("  MAX %s" % max(fits))

        print fits

    print("FIN DE TODAS LAS GENERACIONES")
    best_ind = tools.selBest(pop, 1)[0]
    print("MEJOR INDIVIDUO ES %s, %s" % (best_ind, best_ind.fitness.values))


main()


