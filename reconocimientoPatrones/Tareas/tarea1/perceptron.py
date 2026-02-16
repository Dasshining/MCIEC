import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable

class Perceptron:
    def __init__(self, input_size, learning_rate=0.1, epochs=100, output_file=None):
        self.w = np.zeros(input_size + 1)
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.output_file = output_file
    
    def activation_fn(self, x):
        return 1 if x >= 0 else 0
    
    def predict(self, x):
        x = np.insert(x, 0, 1)
        z = self.w.T.dot(x)
        a = self.activation_fn(z)
        return a
    
    def train(self, X, y):
        table = PrettyTable()
        table.field_names = ["Epoch", "Inputs", "Prediction", "Weights"]
        for epoch in range(self.epochs):
            for inputs, label in zip(X, y):
                prediction = self.predict(inputs)
                self.w += self.learning_rate * (label - prediction) * np.insert(inputs, 0, 1)
                table.add_row([epoch + 1, inputs, prediction, self.w.copy()])        
        
        if self.output_file == None:
            print(table)
        else:
            with open(f"output/{self.output_file}", "w") as text_file:
                    text = table.get_string()
                    text_file.write(text)
                    text_file.write("\n")
                    text = table.get_latex_string()
                    text_file.write(text)
    
    def print_weights(self):
        print("Pesos después del entrenamiento", self.w)



if __name__ == '__main__':
    # Set initial parameters
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    
    ### OR gate ###
    y = np.array([0, 1, 1, 1])
    output_file = "or_gate.txt"
    learning_rate = 0.1
    epochs = 10
    
    # Crear el perceptron y entrenarlo
    perceptron = Perceptron(input_size=2, learning_rate=learning_rate, epochs=epochs, output_file=output_file)
    perceptron.train(X, y)
    # Imprmir los pesos después del entrenamiento
    perceptron.print_weights()
    # Probar el perceptrón
    print("Probar compuerta OR:")
    for inputs in X:
        print(f"Entrada: {inputs} -> Salida predicha: {perceptron.predict(inputs)}")
    print("\n")

    ### OR gate with hiperparameters modification ###
    y = np.array([0, 1, 1, 1])
    output_file = "or_gate_modified.txt"
    learning_rate = 0.5
    epochs = 10
    
    # Crear el perceptron y entrenarlo
    perceptron = Perceptron(input_size=2, learning_rate=learning_rate, epochs=epochs, output_file=output_file)
    perceptron.train(X, y)
    # Imprmir los pesos después del entrenamiento
    perceptron.print_weights()
    # Probar el perceptrón
    print("Probar compuerta OR con modificación de hiperparámetros:")
    for inputs in X:
        print(f"Entrada: {inputs} -> Salida predicha: {perceptron.predict(inputs)}")
    print("\n")
    
    ### AND gate ###
    y = np.array([0, 0, 0, 1])
    output_file = "and_gate.txt"
    learning_rate = 0.1
    epochs = 10
    
    # Crear el perceptron y entrenarlo
    perceptron = Perceptron(input_size=2, learning_rate=learning_rate, epochs=epochs, output_file=output_file)
    perceptron.train(X, y)
    # Imprmir los pesos después del entrenamiento
    perceptron.print_weights()
    # Probar el perceptrón
    print("Probar compuerta AND")
    for inputs in X:
        print(f"Entrada: {inputs} -> Salida predicha: {perceptron.predict(inputs)}")
    print("\n")

    ### AND gate with hiperparameters modification ###
    y = np.array([0, 0, 0, 1])
    output_file = "and_gate_modified.txt"
    learning_rate = 0.5
    epochs = 10
    
    # Crear el perceptron y entrenarlo
    perceptron = Perceptron(input_size=2, learning_rate=learning_rate, epochs=epochs, output_file=output_file)
    perceptron.train(X, y)
    # Imprmir los pesos después del entrenamiento
    perceptron.print_weights()
    # Probar el perceptrón
    print("Probar compuerta AND con modificación de hiperparámetros")
    for inputs in X:
        print(f"Entrada: {inputs} -> Salida predicha: {perceptron.predict(inputs)}")
    print("\n")

    ### XOR gate ###
    y = np.array([0, 1, 1, 0])
    output_file = "xor_gate.txt"
    learning_rate = 0.1
    epochs = 10
    
    # Crear el perceptron y entrenarlo
    perceptron = Perceptron(input_size=2, learning_rate=learning_rate, epochs=epochs, output_file=output_file)
    perceptron.train(X, y)
    # Imprmir los pesos después del entrenamiento
    perceptron.print_weights()
    # Probar el perceptrón
    print("Probar compuerta XOR")
    for inputs in X:
        print(f"Entrada: {inputs} -> Salida predicha: {perceptron.predict(inputs)}")
    print("\n")
    