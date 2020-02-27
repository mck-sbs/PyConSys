# Any copyright is dedicated to the Public Domain.
# https://creativecommons.org/publicdomain/zero/1.0/


from pyconsys.PIDControl import PIDControl
from pyconsys.PT2 import PT2
from pyconsys.Rating import Rating
from random import randint
import matplotlib.pyplot as plt

pid_p = 10
pid_i = 20
pid_d = 0.9

pt2_a2 = 0.2
pt2_a1 = 0.1
pt2_a0 = 1
pt2_b0 = 1

pid_control = PIDControl(pid_p, pid_i, pid_d)
pt2 = PT2(pt2_a2, pt2_a1, pt2_a0, pt2_b0)
rating = Rating()

xe_lst = [x for x in range(0, 5000)]
w_lst = [1 for x in xe_lst]
e_lst = []
y_lst = []
x_lst = []
z_lst = []

best_pid_p = best_pid_i = best_pid_d = best_rating = 0

for _ in range(0, 100):

    e = y = x = z = 0
    pid_p = randint(0, 2000) / 100
    pid_i = randint(0, 2000) / 100
    pid_d = randint(0, 1000) / 1000
    pid_control.update_params(pid_p, pid_i, pid_d)
    pt2.reset()

    for w in w_lst:
        e = w - x
        y = pid_control.get_xa(e)
        x = pt2.get_xa(y) + z
        e_lst.append(e)
        y_lst.append(y)
        x_lst.append(x)
        z_lst.append(z)

    ret = rating.get_update_rating(x_lst, w)
    if ret > best_rating:
        best_pid_p = pid_p
        best_pid_i = pid_i
        best_pid_d = pid_d
        best_rating = ret

    print("Rating = {:7.2f}, P = {:6.2f}, I = {:6.2f}, D = {:6.2}".format(ret, pid_p, pid_i, pid_d))
    e_lst.clear()
    y_lst.clear()
    x_lst.clear()
    z_lst.clear()

# once again with the best params for plotting
pid_control.update_params(best_pid_p, best_pid_i, best_pid_d)
pt2.reset()
print("##### Best rating: {:7.2f} #####".format(best_rating))
e = y = x = z = 0
for w in w_lst:
    e = w - x
    y = pid_control.get_xa(e)
    x = pt2.get_xa(y) + z
    e_lst.append(e)
    y_lst.append(y)
    x_lst.append(x)
    z_lst.append(z)

txt_pid = "PID with P = {}, I = {}, D = {}".format(best_pid_p, best_pid_i, best_pid_d)
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

plt.xlabel('k')
plt.title("PT2 control loop with random PID")
plt.text(1.5, 0.3, txt_pid, bbox=dict(facecolor='white', alpha=0.5))
plt.text(1.5, 0.1, txt_pt2, bbox=dict(facecolor='white', alpha=0.5))
plt.legend()
plt.ylim(top=2, bottom=0)
plt.show()
