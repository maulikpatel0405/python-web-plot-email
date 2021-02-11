import math
import matplotlib.pyplot as plt

array_1 = [n for n in range(1, 10)]
array_2 = [math.exp(n) for n in range(1, 10)]

plt.plot(array_1, array_2)

print(array_2)

plt.show()

