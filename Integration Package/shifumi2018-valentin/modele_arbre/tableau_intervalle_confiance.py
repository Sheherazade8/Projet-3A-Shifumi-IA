# -*- coding: utf-8 -*-
"""

.. moduleauthor:: Valentin Emiya
"""

import numpy as np
import matplotlib.pyplot as plt


def ic(alpha, n):
    return np.sqrt(2/n * np.log(2/alpha))


n_values = 2**np.arange(10)
alpha_values = (0.5, 0.3, 0.1, 0.05, 0.01)

print(r'\begin{tabular}{|' + 'c|' * (n_values.size + 1) + '}')
print(r'\hline')
for n in n_values:
    print('& $n={}$ '.format(n), end='')
print(r'\\')
print(r'\hline')
for alpha in alpha_values:
    print(r'$\alpha = {}$ '.format(alpha), end='')
    for n in n_values:
        print('& ${:.2f}$ '.format(ic(alpha, n)), end='')
    print(r'\\')
    print(r'\hline')
print(r'\end{tabular}')

plt.figure()
for alpha in alpha_values:
    plt.plot(n_values, ic(alpha, n_values), label=r'$\alpha={}$'.format(alpha))
plt.legend()
plt.grid()
plt.xlabel('Nombre de réalisations ($n$)')
plt.ylabel("Rayon de l'intervalle de confiance ($\epsilon$)")
plt.savefig('ic.pdf')
