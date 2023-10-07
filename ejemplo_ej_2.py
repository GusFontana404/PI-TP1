import cv2
import numpy as np

#PRUEBA
f0 = cv2.imread('formulario_vacio.png', cv2.IMREAD_GRAYSCALE)
f1 = cv2.imread('formulario_01.png', cv2.IMREAD_GRAYSCALE)
f2 = cv2.imread('formulario_02.png', cv2.IMREAD_GRAYSCALE)
f3 = cv2.imread('formulario_03.png', cv2.IMREAD_GRAYSCALE)
f4 = cv2.imread('formulario_04.png', cv2.IMREAD_GRAYSCALE)
f5 = cv2.imread('formulario_05.png', cv2.IMREAD_GRAYSCALE)

validar_formulario(f0)
validar_formulario(f1)
validar_formulario(f2)
validar_formulario(f3)
validar_formulario(f4)
validar_formulario(f5)
