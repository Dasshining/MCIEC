import numpy as np
import matplotlib.pyplot as plt

class Perceptron:
    def __init__(self, input_size, learning_rate=0.1, epochs=100):
        self.weights = -1 + 2 *np.random.rand(input_size)
        self.bias = -1 + 2 *np.random.rand()
        self.learning_rate = learning_rate
        self.epochs = epochs


    def activation_fn(self, x):
        return 1 if x >= 0 else 0

    def predict(self, x):
        z = self.weights.T.dot(np.insert(x, 0, 1))
        return self.activation_fn(z)

    def train(self, X, d):
        for _ in range(self.epochs):
            for i in range(d.shape[0]):
                y = self.predict(X[i])
                error = d[i] - y
                self.weights = self.weights + self.learning_rate * error * np.insert(X[i], 0, 1)

class Perceptron:

  def __init__(self, n_inputs, learning_rate):
    self.w = - 1 + 2 * np.random.rand(n_inputs)
    self.b = - 1 + 2 * np.random.rand()
    self.eta = learning_rate

  def predict(self, X):
    _, p = X.shape
    y_est = np.zeros(p)
    for i in range(p):
      y_est[i] = np.dot(self.w, X[:,i])+self.b
      if y_est[i] >= 0:
        y_est[i]=1
      else:
        y_est[i]=0
    return y_est

  def fit(self, X, Y, epochs=50):
    _, p = X.shape
    for _ in range(epochs):
      for i in range(p):
        # Escribe las ecuaciones del perceptrón
        y_est = self.predict(X[:,i].reshape(-1,1))
        self.w += self.eta * (Y[i] - y_est.item()) * X[:,i]
        self.b += self.eta * (Y[i] - y_est.item())


if __name__ == '__main__':
    Perceptron(input_size=2, learning_rate=0.1, epochs=100)
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([0, 0, 0, 1])

    Perceptron.train(X, y)
    Perceptron.predict(X)