# Any copyright is dedicated to the Public Domain.
# https://creativecommons.org/publicdomain/zero/1.0/

from pyconsys.Control import Control
from pyconsys.PIDControl import PIDControl
from pyconsys.PT2 import PT2
from pyconsys.Rating import Rating
from pyconsys.Evopid import Evopid
import matplotlib.pyplot as plt
import time

pt2_a2 = 0.2
pt2_a1 = 0.05
pt2_a0 = 1
pt2_b0 = 1

pid_control = PIDControl(0, 0, 0)
pt2 = PT2(pt2_a2, pt2_a1, pt2_a0, pt2_b0)
rating = Rating()


def calculate(pid_lst):
    p = pid_lst[0]
    i = pid_lst[1]
    d = pid_lst[2]

    xe_lst = [x * Control.DELTA_T for x in range(0, 500)]
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


time_stamp = time.time()

evo = Evopid(calculate)
best_pid, best_score, plot_score_mean = evo.run()

tm = time.time() - time_stamp

plt.title("evolution score")
plt.plot(plot_score_mean, label="mean score (generation)")
plt.show()
####################################################
# plot the fittest control loop
xe_lst_fin = [x * Control.DELTA_T for x in range(0, 500)]
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

plt.xlabel('k in hundreds')
plt.title("PT2 control loop with evolution PID")
plt.text(1.5, 0.3, txt_pid, bbox=dict(facecolor='white', alpha=0.5))
plt.text(1.5, 0.1, txt_pt2, bbox=dict(facecolor='white', alpha=0.5))
plt.legend()
plt.ylim(top=2, bottom=0)
plt.show()
