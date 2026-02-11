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
Algoritm de una neurona binaria:
$$
z = \sum_{i=1}^{i=n}{w_ix_i = b}
$$
**Funcion de activacion**: El valor z se pasa a una funcion de activación para determinar la salida del perceptron. La funcion de activacion más comunmente utilizada es la funcoin escalon, que se define como:
$$
y =
\begin{Bmatrix}   1 & si & z\ge0\\   0 & si & z < 0   \end{Bmatrix}
$$
Esto se puede compactar como:
$$
y = \sigma(z)
$$
###### Actualizacion de pesos
El perceptron ajusta sus pesos en funcion del error en la salida predicha. 
$$
e = t -y
$$
Los pesos se actualizacion segun la regla de aprendizaje del perceptron, que es:
$$
w_i = w_i + \triangle w_i
$$

donde el cambio en el peso de $\triangle w_i$ se calcula como:
$$
\triangle w_i = n e x_i
$$
n = learning rate

