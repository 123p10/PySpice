#!# This example shows a low-pass RC Filter.

####################################################################################################

import math
import numpy as np
import matplotlib.pyplot as plt

####################################################################################################

import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

####################################################################################################

from PySpice.Plot.BodeDiagram import bode_diagram
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit.Units import *

####################################################################################################

#cm# low-pass-rc-filter.m4

circuit = Circuit('Low-Pass RC Filter')

circuit.Sinusoidal('input', 'in', circuit.gnd, amplitude=1)
R1 = circuit.R(1, 'in', 'out', kilo(1))
C1 = circuit.C(1, 'out', circuit.gnd, micro(1))

#!# The break frequency is given by :math:`f_c = \frac{1}{2 \pi R C}`

break_frequency = 1 / (2 * math.pi * float(R1.resistance * C1.capacitance))
print("Break frequency = {:.1f} Hz".format(break_frequency))
#o#

simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.ac(start_frequency=1, stop_frequency=mega(1), number_of_points=10,  variation='dec')
# print(analysis.out)

#!# We plot the Bode diagram.

figure = plt.figure(1, (20, 10))
plt.title("Bode Diagram of a Low-Pass RC Filter")
axes = (plt.subplot(211), plt.subplot(212))
bode_diagram(axes=axes,
             frequency=analysis.frequency,
             gain=20*np.log10(np.absolute(analysis.out)),
             phase=np.angle(analysis.out, deg=False),
             marker='.',
             color='blue',
             linestyle='-',
         )
for axe in axes:
    axe.axvline(x=break_frequency, color='red')

plt.tight_layout()
plt.show()

#fig# save_figure(figure, 'low-pass-rc-filter-bode-diagram.png')
