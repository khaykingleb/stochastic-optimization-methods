import numpy as np 
import random


def ackley_func(x):
    part_1 = 20 * np.exp(-0.2 * np.sqrt(0.5 * (x[0] ** 2 + x[1] ** 2)))
    part_2 = np.exp(0.5 * (np.cos(2 * np.pi * x[0]) + np.cos(2 * np.pi * x[0])))
    return 20 + np.exp(1) - part_1 - part_2
    


class Individual:
    def __init__(self, search_space, chromosome_len):
        self.search_space = search_space
        self.chromosome_len = chromosome_len 
        self.chromosome = np.array([self.create_gene(j) for j in range(chromosome_len)])
        self.target_value = None # значение целевой функции, используя данную особь
        self.fitness = None # значение приспособленности особи относительно других
        self.name = '#' + ''.join(map(str, np.random.randint(0,9, size=7).tolist()))
    
    def create_gene(self, pos):
        return np.random.uniform(self.search_space[pos][0], 
                                 self.search_space[pos][1])
    
    def __repr__(self):
        chromosome = '; '.join(list(map(str, a.fittest_indivdual.chromosome.tolist())))
        return f'{self.name}: chromosome = ({(chromosome)}); target_value = {self.target_value}'


class GeneticAlgorithm:
    def __init__(self, ell=1000, k=200, mutation_rate=0.1, max_iter=100):
        """
        PARAMETERS:
        ell — количество особей в поколении
        k — количество особей для размножения
        mutation_rate — максимальная мутация гена
        max_iter — максимальное количество эволюций поколения (новых поколений)
        """
        self.ell = ell
        self.k = k
        self.mutation_rate = mutation_rate
        self.max_iter = max_iter
        
        self.search_space = None 
        self.chromosome_len = None # длина хромосомы особи
        self.best_individuals = None # k наиболее приспособленных особей
        self.fittest_indivdual = None # самая приспособленная особь
        self.population = None
        self.best_target_value_history = None
        
    def search_global(self, search_space, func):
        """
        INPUT:
        search_space — область поиска оптимума. Задается как список из кортежей, где 
        кортеж — это область значений одного аргумента функции
        """        
        self.search_space = np.array(search_space)
        self.chromosome_len = len(self.search_space)
        self.best_target_value_history = []

        # создаем первое поколение
        self.population = self.create_population(self.search_space)
        
        # проходим этапы эволюции
        for i in tqdm(range(self.max_iter)):
            # оцениваем приспособленность наших особей
            self.evaluate_population(func)
            # отбираем k наиболее наиболее приспособленных особей
            self.selection()
            
            self.best_target_value_history.append(self.fittest_indivdual.target_value)
            # формируем новые поколения
            # скрещиваем особи
            for idx in range(self.k, self.ell):
                # случайно выбираем одну из наилучших особей
                select_fitted_individual = np.random.choice(self.best_individuals)
                # создаем потомка и заменяем им старую особь
                offspring = self.crossover(select_fitted_individual,
                                           self.population[idx])
                self.population[idx].chromosome = offspring
            
            # мутируем все особи, кроме самой приспособленной
            for individual in self.population[1:]:
                self.mutate(individual)
        
        return self.fittest_indivdual
            
    def create_population(self, search_space):
        """
        INPUT:
        search_space — область поиска оптимума. Задается как список из кортежей, где 
        кортеж — это область значений одного аргумента функции
        """
        self.search_space = np.array(search_space)
        self.chromosome_len = len(self.search_space)

        return np.array([Individual(self.search_space,
                                    self.chromosome_len) for i in range(self.ell)])

    def evaluate_population(self, func):
        """        
        INPUT:
        func — оптимизируемая функция, которая принимает список в качестве аргументов
        """
        F = []
        
        for individual in self.population:
            individual.target_value = func(individual.chromosome)
            F.append(individual.target_value)

        for individual in self.population:
            individual.fitness = self.normalize(individual.target_value,
                                                min(F), max(F))

    def normalize(self, z, F_best, F_worst):
        """
        Нормализует значения целевой функции
        
        INPUT:
        z — масштабируемое значение
        F_best — лучшее значение целевой функции
        F_worst — худшее значение целевой функции
        """
        return (z - F_worst) / (F_best - F_worst)

    def selection(self):
        """
        Оператор отбора
        """
        self.population = sorted(self.population,
                                 key=lambda individual: individual.fitness, reverse=True)
        self.best_individuals = self.population[:self.k]
        self.fittest_indivdual = self.population[0]

    def crossover(self, parent_fitted, parent_random):
        """
        Оператор скрещивания
        
        INPUT:
        parent_fitted — одна из самых приспособленных особей
        parent_random — случайная особь
        """
        return np.array([parent_random.chromosome[j]
                         if np.random.uniform(0, 1) < parent_random.fitness
                         else parent_fitted.chromosome[j]
                         for j in range(parent_fitted.chromosome_len)])

    def mutate(self, individual):
        """
        Оператор мутации
        
        INPUT:
        individual — особь, подвергающаяся мутации
        """
        individual_hat_chromosome = np.asarray([])
 
        for j in range(individual.chromosome_len):
            j_hat = individual.chromosome[j] + np.random.uniform(-self.mutation_rate, 
                                                                  self.mutation_rate)
            # на случай, если ген выйдет за пределы гиперкуба или гиперпрямоугольника
            j_hat = min(max(j_hat, self.search_space[j][0]), self.search_space[j][1])
            individual_hat_chromosome = np.append(individual_hat_chromosome, j_hat)
      
        individual.chromosome = individual_hat_chromosome
