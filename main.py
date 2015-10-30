#!/usr/bin/env python
# coding:utf-8

import numpy as np
import matplotlib.pyplot as plt

plt.plot([1,2,3,4], [1,4,9,16], 'ro')
plt.ylabel("some numbers")
plt.axis([0,6,0,20])
plt.show()

"""
t = np.arange(0, 5, 0.2)
print t

plt.plot(t,t,'r--', t,t**2,'bs', t,t**3,'g^')
plt.show()
"""

"""
def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t)

t1 = np.arange(0, 5, 0.1)
t2 = np.arange(0, 5, 0.02)

plt.figure(1)
plt.subplot(211)
plt.plot(t1, f(t1), 'bo', t2, f(t2), 'k')

plt.subplot(212)
plt.plot(t2, np.cos(2*np.pi*t2), 'r--')
"""

