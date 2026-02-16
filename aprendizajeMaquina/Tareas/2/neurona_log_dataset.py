import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class Logistic_Neuron:

    def __init__(self, n_inputs, learning_rate=0.1):
        self.w = - 1 + 2 * np.random.rand(n_inputs)
        self.b = - 1 + 2 * np.random.rand()
        self.eta = learning_rate

    def predict_proba(self, X):
        Z = np.dot(self.w, X) + self.b
        Y_est = 1/(1+np.exp(-Z))
        return Y_est
    
    def predict(self, X, umbral=0.5):
        Y_est = self.predict_proba(X)
        return 1 * (Y_est > umbral)

    def train(self, X, Y, epochs=100):
        p = X.shape[1]
        for _ in range(epochs):
            Y_est = self.predict_proba(X)
            diff = Y - Y_est
            self.w += (self.eta/p) * np.dot((diff), X.T).ravel()
            self.b += (self.eta/p) * np.sum(diff)

if __name__ == '__main__':
    
    # Cargar datos
    df = pd.read_csv('cancer.csv')
    
    # Preprocesamiento
    X = df.drop(['Class'], axis=1).values
    Y = df['Class'].values
    
    # Transponer
    X = X.T

    neuron = Logistic_Neuron(X.shape[0], 0.1)
    neuron.train(X,Y, epochs=2000)

    def predict_measure(X, Y):
        return np.sum(neuron.predict(X) == Y)
    
    print("Prediction measure:", predict_measure(X,Y),"of", Y.shape[0])
    print("Accuracy:", np.mean(neuron.predict(X) == Y))

    # Prediction measure: 661 of 683
    # Accuracy: 0.9677891654465594