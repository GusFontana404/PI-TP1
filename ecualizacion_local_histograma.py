#Función de ecualización local del histograma
def ecualizacion_local_histo(imagen, tamaño_ventana):
    altura, ancho = imagen.shape
    imagen_de_salida = np.copy(imagen) #Imágen de salida (ecualizada)
    mitad_ventana = tamaño_ventana[0] // 2

    for y in range(mitad_ventana, altura - mitad_ventana):
        for x in range(mitad_ventana, ancho - mitad_ventana):
            window = imagen[y - mitad_ventana:y + mitad_ventana, x - mitad_ventana:x + mitad_ventana]
            histograma = cv2.calcHist([window], [0], None, [256], [0, 256])
            histograma_eq = cv2.equalizeHist(window)
            imagen_de_salida[y, x] = histograma_eq[mitad_ventana, mitad_ventana]
    return imagen_de_salida
