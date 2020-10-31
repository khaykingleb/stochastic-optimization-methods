import numpy as np 
import copy


def func(x):
    return (1 - x[0]) ** 2 + 100 * (x[1] - x[0] ** 2) ** 2


class Particle:    
    def __init__(self, arg, search_space):
        self.pos = np.asarray([])      # расположение частицы
        self.velocity = np.asarray([]) # вектор скорости частицы
        self.pos_best = None           # лучшее расположение 
        
        for i in range(arg):
            pos_i = np.random.uniform(search_space[i][0], search_space[i][1])
            self.pos = np.append(self.pos, pos_i)
            vel_i = np.random.uniform(0.2 * search_space[i][0] , 0.2 * search_space[i][1])
            self.velocity = np.append(self.velocity, vel_i)
        
        # pos_best --- это список, состоящий из лучшего расположения частицы 
        # и значения функции в данной точке
        self.pos_best = [self.pos.copy(), func(self.pos)] 
    
    def update_position(self):
        self.pos += self.velocity
    
    def update_velocity(self, w, c1, c2, swarm_best):
        inertion = w * self.velocity
        cognitive_acceler = c1 * np.random.uniform() * (self.pos_best[0] - self.pos)
        social_acceler = c2 * np.random.uniform() * (swarm_best - self.pos)
        self.velocity = inertion + cognitive_acceler + social_acceler
    
    def choose_personal_best(self):
         if func(self.pos) < func(self.pos_best[0]):
                    self.pos_best[0] = self.pos.copy()
                    self.pos_best[1] = func(self.pos)


class ParticleSwarmOptimisation:
    def __init__(self, ell=40, w=1.0, c1=0.2, c2=0.2, max_iter=1000, tol=1e-24):
        """
        PARAMETERS:
        ell — количество частиц в рое.
        w — инерционный вес.
        c1 — коэффициент ускорения когнитивного воздействия на частицу.
        c2 — коэффициент ускорения социального воздействия на частицу.
        max_iter — максимальное количество итераций.
        tol — точность.
        """
        self.ell = ell
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.max_iter = max_iter
        self.tol = tol
        
        self.swarm_best = None # лучшее расположение для всего роя
        self.swarm = None      # расположение всех частиц (рой)
        
    def search_global(self, arg, search_space):
        """
        PARAMETERS:
        arg — количество аргументов функции.
        search_space — область поиска оптимума. Задается как список из кортежей, где 
        кортеж — это область значений одного аргумента функции.
        """
        self.arg = arg
        self.search_space = np.array(search_space)
        self.swarm = np.asarray([])
        
        # генерируем расположение роя 
        for _ in range(self.ell):
            self.swarm = np.append(self.swarm, 
                                   Particle(self.arg, self.search_space))
    
        for k in range(self.max_iter):
            for i in range(self.ell):
                # обновляем расположение частицы
                self.swarm[i].update_position()
                # сравниваем с лучшей точкой частицы
                self.swarm[i].choose_personal_best()
            
            # выбираем лучшую точку для роя
            if k != 0:
                dist_0 = self.dist(self.swarm_best[0])
                self.choose_social_best()
                dist_1 = self.dist(self.swarm_best[0])
                
                # останавливаем поиск в условиях заданной точности
                if (dist_0 != dist_1) and (abs(dist_0 - dist_1) <= self.tol):
                    break
            else:
                self.choose_social_best()
                
            # обновляем вектор скорости
            for i in range(self.ell):
                self.swarm[i].update_velocity(self.w, self.c1, self.c2, self.swarm_best[0])
        
        print(f"Глобальный оптимум: {self.swarm_best[0]}.")
        print(f"Значение функции в данной точке: {self.swarm_best[1]}.")
        
        
    def choose_social_best(self):
        self.swarm_best = min([[self.swarm[i].pos_best[0], 
                                self.swarm[i].pos_best[1]] for i in range(self.ell)],
                                key=lambda x: x[1])
        
    def dist(self, x):
        return np.sqrt(np.sum(x ** 2))
