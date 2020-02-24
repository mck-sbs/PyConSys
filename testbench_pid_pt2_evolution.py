# Any copyright is dedicated to the Public Domain.
# https://creativecommons.org/publicdomain/zero/1.0/


from pyconsys.PIDControl import PIDControl
from pyconsys.PT2 import PT2
from pyconsys.Rating import Rating
from pyconsys.Evopid import Evopid
from operator import itemgetter
import matplotlib.pyplot as plt
import statistics
import time

pt2_a2 = 0.2
pt2_a1 = 0.1
pt2_a0 = 1
pt2_b0 = 1

pid_control = PIDControl(0, 0, 0)
pt2 = PT2(pt2_a2, pt2_a1, pt2_a0, pt2_b0)
rating = Rating()

time_stamp = time.time()

def calculate(pid_lst):
    p = pid_lst[0]
    i = pid_lst[1]
    d = pid_lst[2]

    xe_lst = [x for x in range(0, 500)]
    w_lst = [1 for x in xe_lst]
    x_lst = []
    x = 0

    pid_control.update_params(p, i, d)
    pt2.reset()

    for w in w_lst:
        e = w - x
        y = pid_control.get_xa(e)
        x = pt2.get_xa(y)
        x_lst.append(x)

    r = rating.get_update_rating(x_lst, w)
    return r

#####################################################
# start the evolution
evo = Evopid()
pop_lst = evo.get_first_pop_lst()

plot_score = []
plot_score_mean = []

best_score = 0
best_pid = []
# first run
perf_lst = []
for elem in pop_lst:
    score = calculate(elem)
    if score > best_score:
        best_score = score
        best_pid = elem
    plot_score.append(score)
    perf_lst.append([score, elem])
perf_lst.sort(key=itemgetter(0), reverse=True)
breeders = evo.select_from_pop(perf_lst)
final_pop = evo.next_generation(breeders)
plot_score_mean.append(statistics.mean(plot_score))
plot_score.clear()

# get the rest done
for i in range(evo.get_iter_cnt() - 1):
    p_lst = []
    n_pop = final_pop
    for elem in n_pop:
        score = calculate(elem)
        if score > best_score:
            best_score = score
            best_pid = elem
        p_lst.append([score, elem])
        plot_score.append(score)
    p_lst.sort(key=itemgetter(0), reverse=True)
    brs = evo.select_from_pop(p_lst)
    n_pop = evo.next_generation(brs)
    final_pop = n_pop

    plot_score_mean.append(statistics.mean(plot_score))
    plot_score.clear()

plt.title("evolution score")
plt.plot(plot_score_mean, label="mean score (generation)")
plt.show()
####################################################
# final_pop are the fittest, but which one is the most fittest
# best_score = 0
# best_pid = []
# for elem in final_pop:
#     score = calculate(elem)
#     if score > best_score:
#         best_score = score
#         best_pid = elem

xe_lst_fin = [x for x in range(0, 500)]
w_lst_fin = [1 for x in xe_lst_fin]
x_lst_fin = []
x = 0
best_pid_p = best_pid[0]
best_pid_i = best_pid[1]
best_pid_d = best_pid[2]

pid_control.update_params(best_pid_p, best_pid_i, best_pid_d)
pt2.reset()

for w in w_lst_fin:
    e = w - x
    y = pid_control.get_xa(e)
    x = pt2.get_xa(y)
    x_lst_fin.append(x)


tm = time.time() - time_stamp
print("##### best score: {:7.2f}".format(best_score))
print("##### evolution time: {:7.2f}".format(tm))

txt_pid = "PID with P = {}, I = {}, D = {}".format(best_pid_p, best_pid_i, best_pid_d)
txt_pt2 = "PT2 with a2 = {}, a1 = {}, a0 = {}, b0 = {}".format(pt2_a2, pt2_a1, pt2_a0, pt2_b0)
plt.plot(xe_lst_fin, w_lst_fin, label="w")
plt.plot(xe_lst_fin, x_lst_fin, label="x")
plt.grid()
plt.minorticks_on()
plt.grid(which='major', linestyle='-', linewidth='0.5')
plt.grid(which='minor', linestyle=':', linewidth='0.3')

plt.xlabel('k')
plt.title("PT2 control loop with evolution PID")
plt.text(1.5, 0.3, txt_pid, bbox=dict(facecolor='white', alpha=0.5))
plt.text(1.5, 0.1, txt_pt2, bbox=dict(facecolor='white', alpha=0.5))
plt.legend()
plt.ylim(top=2, bottom=0)
plt.show()

