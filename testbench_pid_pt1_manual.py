# Any copyright is dedicated to the Public Domain.
# https://creativecommons.org/publicdomain/zero/1.0/

from pyconsys.Control import Control
from pyconsys.PIDControl import PIDControl
from pyconsys.PT1 import PT1
import matplotlib.pyplot as plt


pid_p = 10
pid_i = 20
pid_d = 0

pt1_p = 0.2
pt1_t = 0.5

pid_control = PIDControl(pid_p, pid_i, pid_d)
pt1 = PT1(pt1_p, pt1_t)

time_steps = [x * Control.DELTA_T for x in range(0, 500)]
w_lst = [1 if x > 1 else 0 for x in time_steps]
e_lst = []
y_lst = []
x_lst = []
z_lst = []

e = y = x = z = i = 0
for w in w_lst:
    e = w - x
    y = pid_control.get_xa(e)
    if i > 250:
        z = 0.5
    else:
        z = 0
    x = pt1.get_xa(y) + z
    e_lst.append(e)
    y_lst.append(y)
    x_lst.append(x)
    z_lst.append(z)
    i = i + 1

txt_pid = "PID with P = {}, I = {}, D = {}".format(pid_p, pid_i, pid_d)
txt_pt2 = "PT1 with P = {}, T = {}".format(pt1_p, pt1_t)
plt.plot(time_steps, w_lst, label="w")
plt.plot(time_steps, e_lst, label="e")
plt.plot(time_steps, y_lst, label="y")
plt.plot(time_steps, x_lst, label="x")
plt.plot(time_steps, z_lst, label="z")
plt.grid()
plt.minorticks_on()
plt.grid(which='major', linestyle='-', linewidth='0.5')
plt.grid(which='minor', linestyle=':', linewidth='0.3')

plt.xlabel('k in hundreds')
plt.title("PT1 control loop with PID (interference z = 0.5 at k = 250)")
plt.text(1.5, 0.3, txt_pid, bbox=dict(facecolor='white', alpha=0.5))
plt.text(1.5, 0.1, txt_pt2, bbox=dict(facecolor='white', alpha=0.5))
plt.legend()
plt.ylim(top=2, bottom=0)
plt.show()
