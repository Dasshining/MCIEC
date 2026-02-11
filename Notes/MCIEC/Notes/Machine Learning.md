Supervised Learning
![[Pasted image 20260202113135.png]]
error = diferencia entre salida esperada y resultado del sistma de aprendizaje
$$ e = y - \hat{y}$$
Datos de entrada = (input, salida)
$$
D = \{(x_1,y_1),(x_2,y_2),...,(x_3,y_3)\}
$$
### Aprendizaje no supervisado
![[Pasted image 20260202113610.png]]
### Aprendizaje reforzado
![[Pasted image 20260202113935.png]]

### Neurona Biologica
![[Pasted image 20260202115115.png]]
La sinapsis es la distancia entre el axon y el soma de otra neurona
La memoria se guarda en la topologia formada a traves de las sinapsis entre neuronas.

Traduccion de neuronas biologicas a neuronas artificiales

![[Pasted image 20260202120133.png]]
Dendritras = inputs $x_1, x_2, ..., x_n$
Distancia entre dendritas y soma = pesos $w_1, w_2,..., w_n$
Soma = sumatoria de producto punto entre input y pesos
bias (b) = acumulacion de energia en la neuorona
Axon = y (salida de neurona artificial)

simplificando utilizando vectores
![[Pasted image 20260202120939.png]]
Aprendizaje de una neurona con 2 entradas, division del plano en 2 debido respuesta binaria
![[Pasted image 20260202121958.png]]