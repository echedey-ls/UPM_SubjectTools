#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Author: Echedey Luis Álvarez
Date: 06/11/2022
Project: Analog graph

File: prev_bode.py

Abstract: just another grapher

Sources:
'''

import numpy as np
import matplotlib.pyplot as plt
import mplcyberpunk
import scienceplots
from scipy.stats import linregress
from scipy import signal

def main():
    #plt.clf()
    plt.style.use(['science', 'bright'])
    fig, ax = plt.subplots()

    # Subtitle
    fig.suptitle('Circuito no inversor')

    system = signal.lti([67], [1/(17543*2*np.pi),1])
    f = np.logspace(1, 5)
    w = 2 * np.pi * f
    w, mag, phase = signal.bode(system,w)
    ax.semilogx(f, mag, label='Ganancia')

    plt.xlabel(r"Frecuencia $f \, [Hz]$")
    plt.ylabel(r"Ganancia $A_v \, [dB]$")
    plt.grid()

    plt.show()

if __name__ == '__main__':
    main()
    print('☭Data was analyzed successfully. Have a nice day☭')
