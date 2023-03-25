#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Author: Echedey Luis Álvarez
Date: 2023-03-21
Subject: Instrumentación electrónica (Sensors, basically)

File: Ej01.py

Abstract: Ejercicio voluntario 01, ajuste de una NTC a distintos modelos.
Voluntary exercise about fitting a NTC thermistor to different models.

Sources:
[1] Los wenos apuntes
[2] https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
[3] https://web.archive.org/web/20110708192840/http://www.cornerstonesensors.com/reports/ABC%20Coefficients%20for%20Steinhart-Hart%20Equation.pdf
  - From https://en.wikipedia.org/wiki/Steinhart%E2%80%93Hart_equation
[4] https://en.wikipedia.org/wiki/Thermistor
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scienceplots
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d

plt.style.use(['science', 'no-latex'])

# %%
# Read NTC data / Leer datos de la NTC
data = pd.read_csv('Ej01_data.csv')
# Keys are 'Temp_C', 'DC_Resistance_Ohms'
data_temp = data['Temp_C'] + 273.13  # Kelvins
data_ohms = data['DC_Resistance_Ohms']

# %%
# Define models to use / Definir modelos a utilizar
# Ambas entradas en Kelvin
# Temperature inputs are in Kelvin
# First two use ref [1]
model_2params = lambda T, B, T0, R0: R0 * np.exp(B * (1/T - 1/T0))
model_3params = lambda T, A, B, C, R0: (R0 * np.exp(A
                                                    + B/T
                                                    + C/np.power(T, 2)))
def model_steinhart_hart(T, A, B, C):  # [3]
    x = (A - 1/T) / C
    y = np.sqrt(np.power(B / (3*C), 3)
                + np.square(x) / 4)
    R = np.exp(np.cbrt(y - x/2) - np.cbrt(y + x/2))
    return R



# %%
# Get constant parameters for the models at 25ºC, so we get funcs we can fit
# Obtenemos los parámetros para centrar la regresión a 25ºC
# y hallamos las funciones que los rigen
T0 = 25. + 273.13 # Kelvin
R0 = data_ohms[data_temp == T0].values[0]
print(f'R0 at T = {T0}K is {R0}Ω')

# %%
# Reference models to (25ºC, R(25ºC)) points, to limit degrees of freedom
# Fits only parameter B
model_2params_populated = lambda T, B: model_2params(T, B, T0, R0)
# Fits ABC parameters
model_3params_populated = lambda T, A, B, C: model_3params(T, A, B, C, R0)

# %%
# Calculate fitting parameters
# m2_* prefix for model_2params
m2_popt, m2_pcov = curve_fit(model_2params_populated,
                             data_temp, data_ohms)
print(f'Model 2 params fitting results [ Beta ]:')
print(m2_popt)
print(f'STD [ Beta ]: {np.sqrt(np.diag(m2_pcov))}')
# m3_* prefix for model_3params
m3_popt, m3_pcov = curve_fit(model_3params_populated,
                             data_temp, data_ohms)
print(f'Model 3 params fitting results [ A B C ]:')
print(m3_popt)
print(f'STD [ A B C ]: {np.sqrt(np.diag(m3_pcov))}')
# shh_* prefix for model_steinhart_hart
# p0 from [4]
shh_popt, shh_pcov = curve_fit(model_steinhart_hart,
                               data_temp, data_ohms,
                               p0=(1.4e-3, 2.4e-4, 9.9e-8))
print(f'Model Steinhart-Hart params fitting results [ A B C ]:')
print(shh_popt)
print(f'STD [ A B C ]: {np.sqrt(np.diag(shh_pcov))}')

# %%
# Linearization with parallel resistor
# Linealización mediante resistencia en paralelo
print('Linearization')

# Common values
t1, t3 = data_temp.min(), data_temp.max()
t2 = np.mean([t1, t3])

# Method 1: 3 points over range
# Método 1: 3 puntos del rango
r1 = data_ohms[data_temp == t1].values[0]
r3 = data_ohms[data_temp == t3].values[0]
# Use model to compute resistance at the middle of the range
# Procedure agnostic of input data. Thank me later.
r2 = model_steinhart_hart(t2, *shh_popt)
method1_R_calc = lambda R1, R2, R3: ((R2*(R1 + R3) - 2*R1*R3)
                                     / (R1+R3-2*R2))
R_fixed_m1 = method1_R_calc(r1, r2, r3)
print(f'Method 1 - resulting parallel resistance: {R_fixed_m1}Ω')

# Create temperature dependant model
R_lin_m1 = lambda T: (R_fixed_m1 * model_steinhart_hart(T, *shh_popt)
                      / (R_fixed_m1 + model_steinhart_hart(T, *shh_popt)))

# Method 2: centering inflection point
# Método 2: punto de inflexión centrado
# Requires model of two parameters
beta = m2_popt[0]
# Use model to compute resistance at the middle of the range
# Procedure agnostic of input data. Thank me later.
tc = np.mean([t1, t3])
rc = model_2params_populated(tc, beta)

method2_R_calc = lambda Rc, Tc, beta: Rc * (beta - 2*Tc)/(beta + 2*Tc)
R_fixed_m2 = method2_R_calc(rc, tc, beta)
print(f'Method 2 - resulting parallel resistance: {R_fixed_m2}Ω')

# Create temperature dependant model
R_lin_m2 = lambda T: (R_fixed_m2 * model_2params_populated(T, beta)
                      / (R_fixed_m2 + model_2params_populated(T, beta)))

# %%
# Linearization methods - check linearity
# Métodos de linealización - comprobar linealidad
# I'll test each model against the end-points line, for simplicity
# Compararé cada modelo con su recta entre puntos finales, por simplicidad
# Line equation y(Tx) = (ΔR/ΔT)*(Tx - T_min) + R(T0) is done via a
# numpy 1d interpolator

t_min, t_max = data_temp.min(), data_temp.max()
temps2test = np.linspace(t_min, t_max, 1000)

# Method 1
R_t_min = R_lin_m1(t_min)
R_t_max = R_lin_m1(t_max)
method1_interpolator = interp1d([t_min, t_max], [R_t_min, R_t_max])
method1_diffs = method1_interpolator(temps2test) - R_lin_m1(temps2test)
method1_max_err = np.max(np.abs(method1_diffs))
print(f'NTC||{R_fixed_m1:.0f}Ω max linearity error is {method1_max_err:.5f}Ω')

# Method 2
R_t_min = R_lin_m2(t_min)
R_t_max = R_lin_m2(t_max)
method2_interpolator = interp1d([t_min, t_max], [R_t_min, R_t_max])
method2_diffs = method2_interpolator(temps2test) - R_lin_m2(temps2test)
method2_max_err = np.max(np.abs(method2_diffs))
print(f'NTC||{R_fixed_m2:.0f}Ω max linearity error is {method2_max_err:.5f}Ω')

# %% 
# Calculate & plot everything
# Temp. range of the plot (from exercise)
# Rango de temperaturas para la figura (del ejercicio)
temps = np.linspace(t_min, t_max, 50)

# NTC models
m2_regress = model_2params_populated(temps, *m2_popt)
m3_regress = model_3params_populated(temps, *m3_popt)
shh_regress = model_steinhart_hart(temps, *shh_popt)

# Linearization models
R_lin_m1_points = R_lin_m1(temps)
R_lin_m2_points = R_lin_m2(temps)

# Agregamos los resultados en un mismo gráfico
# Plot everything in the same figure
fig, ax = plt.subplots()
fig.suptitle('Regresión de los distintos modelos de NTCs',
              **{'fontsize': 'x-large'})
ax.set_title(f'Valor $R_0$ a ${T0}K$')
ax.set_xlabel('Temperatura [$K$]')
ax.set_ylabel('Resistencia [$Ω$]')

# Plot source data
ax.scatter(data_temp.values, data_ohms.values, color='k',
           label='Medidas NTC')
# Plot 2 params model
ax.plot(temps, m2_regress, color='b', linestyle='--',
        label='NTC: Modelo 2 params')
# Plot 3 params model
ax.plot(temps, m3_regress, color='g', linestyle='solid',
        label='NTC: Modelo 3 params')
# Plot Steinhart-Hart model
ax.plot(temps, shh_regress, color='r', linestyle=':',
        label='NTC: Modelo Steinhart-Hart')

# Plot linearized Method 1: 3 points over range
ax.plot(temps, R_lin_m1_points, color='darkorchid', linestyle='-.',
        label=f'$NTC||{R_fixed_m1:.0f}Ω$: linearized by 3 equidistant points')
# Plot linearized Method 2: centering inflection point
ax.plot(temps, R_lin_m2_points, color='deeppink', linestyle='-.',
        label=f'$NTC||{R_fixed_m2:.0f}Ω$: linearized by inflection point')

ax.legend()
ax.grid(axis='both', which='both')

plt.show()
