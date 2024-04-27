import numpy as np
import matplotlib.pyplot as plt

tentativa1 = np.load('tentativa1.npy')
tentativa2 = np.load('tentativa2.npy')
tentativa3 = np.load('tentativa3.npy')

media = []
for i in range(len(tentativa1)):
    media.append((tentativa1 + tentativa2 + tentativa3)/3)

plt.plot(tentativa1, label='Tentativa 1')
plt.plot(tentativa2, label='Tentativa 2')
plt.plot(tentativa3, label='Tentativa 3')
plt.legend(loc="lower right")
#plt.plot(media, label='Média')

plt.title('Acompanhamento de soluções - KNAPDATA100.TXT')
plt.xlabel('Gerações', fontsize=7, fontweight='normal')
plt.ylabel('Fitness', fontsize=15, fontweight='normal')

output = 'grafico.png'
plt.savefig(output)

