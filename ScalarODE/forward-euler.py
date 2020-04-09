#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from matplotlib.pyplot import *

alpha = 0.2
R = 1.0

def ForwardEuler(f, U0, T, n):
    """Solve for u'=f(u,t), u(0)=U0 """
    """with n steps until t=T """
    t = np.zeros(n+1)
    u = np.zeros(n+1)
    u[0] = U0
    t[0] = 0
    dt = T / float(n)
    for k in range(n):
        t[k+1] = t[k] + dt
        u[k+1] = u[k] + dt * f(u[k], t[k])
    return u, t

def f(u, t):
    return u

u, t = ForwardEuler(f, U0=1, T=40, n=400)

plot(u,t)
xlabel('t')
ylabel('u')
title('Logistic growth: alpha=%s, R=%g, dt=%g' % 
        (alpha, R, t[-1]-t[0]))
show()
