import os
import numpy as np
import matplotlib.pyplot as plt
downloads_dir = os.path.expanduser('~/Downloads')

def logistic(L, k, x_0, x):
    return L / (1 + np.exp(-k*(x - x_0)))

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def plot_functions():
    x = np.linspace(-10, 10, 400)

    # Logistic function parameters
    L = 1
    k = 1
    x_0 = 0

    y_logistic = logistic(L, k, x_0, x)
    y_sigmoid = sigmoid(x)

    plt.figure(figsize=(10, 5))
    plt.title('Logistic Function')
    plt.plot(x, y_logistic, label='Logistic Function', color='blue')
    
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid()
    plt.plot(x, y_sigmoid, label='Sigmoid Function', color='orange')

    plt.legend()
    plt.tight_layout()
    plt.savefig('logistic.png')
