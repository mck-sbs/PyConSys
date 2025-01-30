# Any copyright is dedicated to the Public Domain.
# https://creativecommons.org/publicdomain/zero/1.0/

from pyconsys.Control import Control
from pyconsys.PIDControl import PIDControl
from pyconsys.PT2 import PT2
from pyconsys.Rating import Rating
import matplotlib.pyplot as plt
import time
import pygad

# Hyperparameters

# number of genes
num_genes = 3
# number of generations
num_generations = 20
# number of chromosomes
sol_per_pop = 10
# number of parents
num_parents_mating = 10
# probably of mutation
mutation_percent_genes = 34

# lower limit of the random number
init_range_low = 0
# upper limit of the random number
init_range_high = 100
# data type
gene_type = float


pt2_a2 = 0.2
pt2_a1 = 0.05
pt2_a0 = 1
pt2_b0 = 1

pid_control = PIDControl(0, 0, 0)
pt2 = PT2(pt2_a2, pt2_a1, pt2_a0, pt2_b0)
rating = Rating()


def fitness_func(ga_instance, solution, solution_idx):
    p = solution[0]
    i = solution[1]
    d = solution[2]

    time_steps = [x * Control.DELTA_T for x in range(0, 500)]
    w_lst = [1 for x in time_steps]
    x_lst = []
    x = 0

    pid_control.update_params(p, i, d)
    pt2.reset()

    ww = 0
    for w in w_lst:
        e = w - x
        y = pid_control.get_xa(e)
        x = pt2.get_xa(y)
        x_lst.append(x)
        ww = w

    fitness = rating.get_update_rating(x_lst, ww)

    return fitness

# define a function to get the fitness score of a pid triple
ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_func,
                       sol_per_pop=sol_per_pop,
                       init_range_low=init_range_low,
                       init_range_high=init_range_high,
                       num_genes=num_genes,
                       mutation_percent_genes=mutation_percent_genes,
                       gene_type=gene_type)

#####################################################
# start the evolution


time_stamp = time.time()
print("Evolution is running. Please wait...")
# The constructor needs the fitness function as a callback
ga_instance.run()
# start the evolution

tm = time.time() - time_stamp

solution, solution_fitness, solution_idx = ga_instance.best_solution()

print("Required time:", tm)
print("Best parameters:", solution)
print("Highest fitness value:", solution_fitness)
ga_instance.plot_fitness()
####################################################
# plot the fittest control loop

time_steps_fin = [x * Control.DELTA_T for x in range(0, 500)]
w_lst_fin = [1 if x > 1 else 0 for x in time_steps_fin]
#w_lst_fin = [1 for x in time_steps_fin]
x_lst_fin = []
x = 0
best_pid_p = solution[0]
best_pid_i = solution[1]
best_pid_d = solution[2]

pid_control.update_params(best_pid_p, best_pid_i, best_pid_d)
pt2.reset()

for w in w_lst_fin:
    e = w - x
    y = pid_control.get_xa(e)
    x = pt2.get_xa(y)
    x_lst_fin.append(x)

print("##### best score: {:7.2f}".format(solution_fitness))
print("##### evolution time: {:7.2f}".format(tm))

txt_pid = "PID with P = {}, I = {}, D = {}".format(best_pid_p, best_pid_i, best_pid_d)
txt_pt2 = "PT2 with a2 = {}, a1 = {}, a0 = {}, b0 = {}".format(pt2_a2, pt2_a1, pt2_a0, pt2_b0)
plt.plot(time_steps_fin, w_lst_fin, label="w")
plt.plot(time_steps_fin, x_lst_fin, label="x")
plt.grid()
plt.minorticks_on()
plt.grid(which='major', linestyle='-', linewidth='0.5')
plt.grid(which='minor', linestyle=':', linewidth='0.3')

plt.xlabel('k in hundreds')
plt.title("PT2 control loop with evolution PID")
plt.text(1.5, 0.3, txt_pid, bbox=dict(facecolor='white', alpha=0.5))
plt.text(1.5, 0.1, txt_pt2, bbox=dict(facecolor='white', alpha=0.5))
plt.legend()
plt.ylim(top=2, bottom=0)
plt.show()
