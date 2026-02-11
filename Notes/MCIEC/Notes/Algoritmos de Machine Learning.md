- **Aprendizaje supervisado**: aprendizaje previo basado en un sistema de etiquetas asociadas a unos datos que les permiten tomar decisiones o hacer predicciones.
- **Aprendizaje no supervisado**: no cuentan con conocimiento previo. Su objetivo es encontrar patrones que permitan organizarlos de alguna manera.
- **Aprendizaaje por refuerzo**: aprendizaje a partir de la propia experiencia, que sea capaz de tomar la mejor decision ante diferentes situaciones de acuerdo a un proceso de prueba y error en el que se recompensan las decisoines correctas.

### Conceptos basicos
Neuronas: Procesador de información muy simple
Canal de entrada: dendritas
Procesador: soma
Canal de salida: axón

Una neurona puede recibir unas 10,000 entradas y enviar a su vez su salida a varios cientos de neuronas
![[Pasted image 20260204113546.png]]

###### Perceptron
imita el funcionamiento de las neuronas en el cerebro

**Reglas de aprendizaje**: Como aprende nuestra neurona a reconocer los patrones en base a los datos de entrada

###### Algoritmo preceptron
$$
v_j = w_{1j}x_1 + w_{2j}x_2 + ... + w_{nj}x_n
$$
Algoritmo de una neurona binaria:
$$
z = \sum_{i=1}^{i=n}{w_ix_i + b}
$$
Ecuaciones para actualizacion de pesos:
$$
z = ???? 
$$

#### Redes neuronales artificiales (ANN)

- Una sola capa oculta -> shallow neural network
- Dos o más capas ocultas -> deep neural networks
#### Redes neuronales prealimentadas
La propagacion hacia adelante es el proceso mediante el cual als entradas inciales se transmiten a traves de la red neuronal hasta generar una salida

### Funciones de activación
Función lineal: sin una funcion de activacion, una red neuronal con multiples capas se comportaria como una simple combinacion lineal de las entradas, lo que limita su capaciad para resolver problemas complejos.
#### Funciones comunes
- Sigmoide: salidas entre 0 y 1, util para problemas de clasificaicon binaria.
$$
Sigmoid(z) = \frac{1}{1 + e^-z}
$$
- ReLU (Rectified Linear Unit): devuelve 0 para entradas negativas y el valor de entrada para entradas positivas. Es ampliamente utilizado por su eficiencia computacional y su capacidad para reducir problemas de gradiente atenuados.
$$
ReLU(z) = max(0,z)
$$
- Tanh: similar a la sigmoide pero su salida oscila entre -1 y 1, lo que puede ayudar a centrar los datos.
$$
Tan(z) = \frac{e^z - e^-z}{e^z + e^-z}
$$
### Entrenamiento de red neuronal
- Propagacion hacia atras: es un algoritmo que ajusta los pesos de las conexiones de la red con el objetivo de minimizar el error en la salida predicha por el modelo.
	- Calculo del error: el entrenamiento comienza con una pasada de propagaqcion hacia adelante, donde os datos de entrada se apasan a traves de la red para generar una salida predicha.
	- La salida predicha secompara con la salida real utilizando una funcion de costo, la diferencia entre ambas se denomina error.
- Retropopagación del error:
	- Una vez calculado el error, este se retropropaga a traves de la red, durante este proceso se calcula el gradiente del error con respecto a cada peso en la red. Este gradiente indica como se debe ajustar cada peso para reducir.
### Funciones de coste
- Error cuadratico medio (MSE):
$$
MSE = \frac{1}{n}\sum_{i=1}^{i=n}{(y_i - y_{output})}
$$

### Gradiente descendente
