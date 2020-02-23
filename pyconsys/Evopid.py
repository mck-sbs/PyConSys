# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import random

class Evopid():

    def __init__(self):
        self._pop_size = 800
        self._fittest_cnt = 10
        self._lucky_few = 150
        self._children_cnt = 10

        self._chance_of_mutation = 5
        self._number_of_generation = 20
        self._pop_size = int((self._fittest_cnt + self._lucky_few) / 2 * self._children_cnt)

    def get_iter_cnt(self):
        return self._number_of_generation

    def get_first_pop_lst(self):
        pop = []
        for _ in range(self._pop_size):
            pid_p = self._get_p()
            pid_i = self._get_i()
            pid_d = self._get_d()
            lst = [pid_p, pid_i, pid_d]
            pop.append(lst)
        return pop

    def select_from_pop(self, perf_lst):
        next_gen = []
        for i in range(self._fittest_cnt):
            next_gen.append(perf_lst[i][1])
        for i in range(self._lucky_few):
            next_gen.append(random.choice(perf_lst)[1])
        random.shuffle(next_gen)
        return next_gen

    def _create_children(self, breeders):
        next_population = []
        for i in range(len(breeders) // 2):
            for j in range(self._children_cnt):
                parent1 = breeders[i]
                parent2 = breeders[len(breeders) - 1 - i]
                child = []
                for k in range(3):
                    if int(100 * random.random()) < 50:
                        child.append(parent1[k])
                    else:
                        child.append(parent2[k])
                next_population.append(child)
        return next_population

    def next_generation(self, next_breeders):
        next_pop = self._create_children(next_breeders)
        nex_gen = self._mutate_pop(next_pop)
        return nex_gen

    def _mutate_pop(self, pop):
        for i in range(len(pop)):
            if random.random() * 100 < self._chance_of_mutation:
                rand = random.randint(0, 3)
                item = pop[i]
                if rand == 0:
                    item[0] = self._get_p()
                elif rand == 1:
                    item[1] = self._get_i()
                else:
                    item[2] = self._get_d()
                pop[i] = item
        return pop

    def _get_p(self):
        return random.randint(0, 2000) / 100

    def _get_i(self):
        return random.randint(0, 2000) / 100

    def _get_d(self):
        return random.randint(0, 1000) / 1000
