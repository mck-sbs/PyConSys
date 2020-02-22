# Any copyright is dedicated to the Public Domain.
# https://creativecommons.org/publicdomain/zero/1.0/

# 2020, Metin Karatas (m.karatas@sbs-herzogenaurach.de)

from pyconsys.PIDControl import PIDControl
from pyconsys.Control import Control
from pyconsys.PT2 import PT2
import matplotlib.pyplot as plt
from math import sin

pid_p = 10
pid_i = 20
pid_d = 0.9

pt2_a2 = 0.02
pt2_a1 = 0.05
pt2_a0 = 1
pt2_b0 = 1

pid_control = PIDControl(pid_p, pid_i, pid_d)
pt2 = PT2(pt2_a2, pt2_a1, pt2_a0, pt2_b0)

xe_lst = [x * Control.DELTA_T for x in range(0, 500)]
w_lst = [1 if x > 1 else 0 for x in xe_lst]
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
    x = pt2.get_xa(y) + z
    e_lst.append(e)
    y_lst.append(y)
    x_lst.append(x)
    z_lst.append(z)
    i = i + 1

txt_pid = "PID with P = {}, I = {}, D = {}".format(pid_p, pid_i, pid_d)
txt_pt2 = "PT2 with a2 = {}, a1 = {}, a0 = {}, b0 = {}".format(pt2_a2, pt2_a1, pt2_a0, pt2_b0)
plt.plot(xe_lst, w_lst, label="w")
plt.plot(xe_lst, e_lst, label="e")
plt.plot(xe_lst, y_lst, label="y")
plt.plot(xe_lst, x_lst, label="x")
plt.plot(xe_lst, z_lst, label="z")
plt.grid()
plt.minorticks_on()
plt.grid(which='major', linestyle='-', linewidth='0.5')
plt.grid(which='minor', linestyle=':', linewidth='0.3')

plt.xlabel('k in hundreds')
plt.title("PT2 control loop with PID (interference z = 0.5 at k = 250)")
plt.text(1.5, 0.3, txt_pid, bbox=dict(facecolor='white', alpha=0.5))
plt.text(1.5, 0.1, txt_pt2, bbox=dict(facecolor='white', alpha=0.5))
plt.legend()
plt.ylim(top=2, bottom=0)
plt.show()
