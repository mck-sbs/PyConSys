# Any copyright is dedicated to the Public Domain.
# https://creativecommons.org/publicdomain/zero/1.0/


from pyconsys.PControl import PControl
from pyconsys.IControl import IControl
from pyconsys.DControl import DControl
#from pyconsys.PIDControl import PIDControl
from pyconsys.Control import Control
from pyconsys.PT1 import PT1
from pyconsys.PT2 import PT2

import matplotlib.pyplot as plt

p_control = PControl(1)
i_control = IControl(1)
d_control = DControl(1)
#pid_control = PIDControl(1, 1, 1)

pt1 = PT1(1, 0.5)
pt2 = PT2(0.02, 0.05, 1, 1)

xe_lst = [x for x in range(0, 500)]

xa_lst_p = [p_control.get_xa(1) if x > 1 else p_control.get_xa(0) for x in xe_lst]
xa_lst_i = [i_control.get_xa(1) if x > 1 else i_control.get_xa(0) for x in xe_lst]
xa_lst_d = [d_control.get_xa(1) if x > 1 else d_control.get_xa(0) for x in xe_lst]
#xa_lst_pid = [pid_control.get_xa(1) if x > 1 else pid_control.get_xa(0) for x in xe_lst]
xa_lst_pt1 = [pt1.get_xa(1) if x > 1 else pt1.get_xa(0) for x in xe_lst]
xa_lst_pt2 = [pt2.get_xa(1) if x > 1 else pt2.get_xa(0) for x in xe_lst]


plt.plot(xe_lst, xa_lst_p, label="P control")
plt.plot(xe_lst, xa_lst_i, label="I control")
plt.plot(xe_lst, xa_lst_d, label="D control")
#plt.plot(xe_lst, xa_lst_pid, label="PID control")
plt.plot(xe_lst, xa_lst_pt1, label="PT1")
plt.plot(xe_lst, xa_lst_pt2, label="PT2")
plt.grid()
plt.minorticks_on()
plt.grid(which='major', linestyle='-', linewidth='0.5')
plt.grid(which='minor', linestyle=':', linewidth='0.3')
plt.ylim(top=5, bottom=0)

plt.xlabel('xe')
plt.ylabel('xa')
plt.title("control units - step response")
plt.legend()
plt.show()
