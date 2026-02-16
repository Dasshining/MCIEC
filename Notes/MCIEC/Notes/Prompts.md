I need to find 3 different research topics over which to make a paper from, I'm currently doing a masters on electrical and computations engineering, please make a list of papers that review and concentrate the latest advances on engineering research topics such as Machine Learning, Patter recognition, Quadruped Robots and Computer Vision. My goal is to have wider view of the available topics at hand and what are the available topics to research on those fields. 

# 2
Context: I'm doing a research paper that utilizes bio-inspired optimization algorithms and graph theory to simulate the affluence of people through the city (which is model using a graphos) using public transportation and if the current bus main lines in the metropolitan area of guadalajara, Mexico, are fit to cover the demand of mobility.

  

Task: I need you to help me develop the methodology for this paper.

Current advancements:


Utilize the following papers or links as reference for your analysis or related ones:
- No papers so far

Output: the delivered version should be written in English, cite the references within the generated introduction and provide a list at the end with all the references, please at the citations using brackets "[n]" after the lines that reference each paper.


## 3
I'm utilizing a genetic algorithm to look for the best path solution within a multidimensional graph, the cost function evaluated utilizes multiple cycles and conditional statements making it unfit for traditional maximization or minimization algorithms. I need to find one or multiple papers that can help me verify this or in the contrary propose a better solution for this issue.

# 4
Context: I'm creating the reports for a series of homework of my Pattern recognition class, each report contain the development and result of a machine learning algorithm. I'm going to send you all the files produced during the execution of the task including the python code, the output of the iterations of the algorithm using prettytable in .txt format and even the output on the terminal of the print statements within the code. I will also send you a file called "report1.tex" which you can use as reference, you must preserve the title page from this file in the new report.

Guidelines for the report:
- Portada
- Resumen machine learning y perceptrón simple
- Enunciado del problema:  
    La tarea 1 consta de los siguientes enunciados: 1. Experimentar con el Código proporcionado de la implementación de la compuerta OR en la presentación Clase 1.1 y realizar la implementación de la compuerta AND. Hacer la comprobación manual e identificar qué pasa si modificamos los hiperparametros de la red (learning rate y el número de épocas).  
    2.Que sucede con la compuerta digital XOR?. Se puede resolver utilizando el perceptrón simple?. Justifique su respuesta. Considere la tabla de verdad. 
- Codigo utilizado
- Conclusiones y observaciones
- Referencias

Task: Build a Latex (.tex) report with the following conditions.
- The report must be in Spanish
- This is a single perceptron neuron algorithm.
- You can add graphs, figures, text, math equations, or whatever other utility
you seem fit, I'm using TeXLive as compiler with all its packages.
- Each line in the .tex document should ideally fit in 80 characters for
  readability while edting, this must not affect the size of the contents of the
  text, is just a mesure to edit and read the .tex files in an easier way.
- I'll send you the python files that implement the bio-inspired algorithm so
you can take the snippets of code from them or more context for structuring
the report.
- Do not use Python 3 when mentioning to the utilized language, is redundant due to
  the class context just use Python.
- While answering the questions within sections "Enunciado del problema" and "Conclusiones" utilize the attached preetyTable txt file to reference the iterations of the algorithm while answering them.
  
  Output of the code in the terminal:
  esos después del entrenamiento [-0.1  0.1  0.1]
Probar compuerta OR:
Entrada: [0 0] -> Salida predicha: 0
Entrada: [0 1] -> Salida predicha: 1
Entrada: [1 0] -> Salida predicha: 1
Entrada: [1 1] -> Salida predicha: 1


Pesos después del entrenamiento [-0.5  0.5  0.5]
Probar compuerta OR con modificación de hiperparámetros:
Entrada: [0 0] -> Salida predicha: 0
Entrada: [0 1] -> Salida predicha: 1
Entrada: [1 0] -> Salida predicha: 1
Entrada: [1 1] -> Salida predicha: 1


Pesos después del entrenamiento [-0.2  0.2  0.1]
Probar compuerta AND
Entrada: [0 0] -> Salida predicha: 0
Entrada: [0 1] -> Salida predicha: 0
Entrada: [1 0] -> Salida predicha: 0
Entrada: [1 1] -> Salida predicha: 1


Pesos después del entrenamiento [-1.5  1.   0.5]
Probar compuerta AND con modificación de hiperparámetros
Entrada: [0 0] -> Salida predicha: 0
Entrada: [0 1] -> Salida predicha: 0
Entrada: [1 0] -> Salida predicha: 0
Entrada: [1 1] -> Salida predicha: 1


Pesos después del entrenamiento [ 0.  -0.1  0. ]
Probar compuerta XOR
Entrada: [0 0] -> Salida predicha: 1
Entrada: [0 1] -> Salida predicha: 1
Entrada: [1 0] -> Salida predicha: 0
Entrada: [1 1] -> Salida predicha: 0

# 5
Task: Create a python code that utilize the following libraries to open the web cam and while recording video apply normalization to the histogram of the current image being recorder, the output should be a window divide in 4 quadrants, the first one should display the current video, the second one the video after the histogram normalization, the third one the first quadrant histogram and the fourth one the second quadrant histogram. Please structure the code in a modular way, to accomplish this you will need to create a function several functions each of the encapsulating certain functionality (normalize image histogram, read image, plot histogram, etc). Take in account this images are in rgb format.

Python libraries: 
import cv2 
from google.colab.patches import cv2_imshow 
from matplotlib import pyplot as plt 
import numpy as np 
import mediapipe as mp



Task: Create a python code that utilize the following libraries to create a function that takes 2 images as input, normalize their histogram and search through their histograms exchanging the color that match in frequency, the output should be the 2 images but with their colors "interchange". For example an winter image and a sunny image will change color make the sunny image look whiter and with cold colors while the winter image will portrait heated colors or even kind of like sand colors. Please structure the code in a modular way, to accomplish this you will need to create a function several functions each of the encapsulating certain functionality (normalize image histogram, read image, interchange image histogram, etc). Additionally please create functions that allow us to plot the image histogram and display the images, take in account this images are in rgb format and the script will be run locally. Additionally I will send you the last computer vision file so you can reuse or extract relevant functions from it.

Python libraries: 
import cv2 
from matplotlib import pyplot as plt 
import numpy as np 