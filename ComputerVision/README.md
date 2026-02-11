Contraste e iluminacion
Contraste: relacion que existe entre los diferentes valores de intesidad presentes en una imagen
Iluminacion: 

$$
I(x,y) = cI(x,y) + b
$$
Limitado a la escala rgb, 0 a 255

Complemento de la imagen: 
$$

$$

Histogramas: que tantas veces se repite cierto valor de intesidad en la imagen.
Una imagen tendra mejor contraste a medida que la diferencia entre el valor
minimo de su histograma y el valor maximo aumente. De la misma manera podemos
definir el brillo de la imagen dependiendo a donde esten cargada la mayor
cantidad de elementso del histograma.

Dinamica: numero de pixeles difernetes en una imagen. A medida que se reducen
pierdes informacion. La dinamica no puede ser elevada porque literalmente no hay
información.

Histograma acumulado:


Adaptacion automatica del contraste (Normalizacion): 
El pixel más oscuro es mapeado a 0 y el más claro a 255. Todos los demas los
quedan interpolados entre esos dos valores.

$$
f = (p - p_low) (p_max - p_min) / (p_high - p_low)
f = (p - p_low) (255 / p_high - p_low)
$$


Adaptacion automatica del contraste (Normalizacion) - variante: 
En caso de tener pixeles en 0 o 255, acotas los limites para la escala, por
ejemplo tomar como minimo el primer valor encontrado despues de 10% o el maximo
despues de 90%

Ecualizacion lineal del histograma:
$$
I(i,j) = H(I(i,j))255/MN
$$
I(i,j) = valor del pixel
H() = frecuencia en histograma acumulado
MN = total de pixeles de la imagen

Ecualizacion por especifiacion:
