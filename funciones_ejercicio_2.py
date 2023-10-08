#EJERCICIO 2

def extraer_campos(imagen):
    """Permite separar campos en una imagen de interes y guardar sus coordenadas
    en un dicionario."""
    umbral = 100
    imagen_binaria = np.where(imagen >= umbral, 1, 0)

    # Suma valores de píxeles a lo largo de las columnas y filas
    suma_columnas = np.sum(imagen_binaria, axis=0)
    suma_filas = np.sum(imagen_binaria, axis=1)

    # Define umbrales para detectar líneas en columnas y filas
    umbral_columnas = 0.7 * np.max(suma_columnas)
    umbral_filas = 0.5 * np.max(suma_filas)

    # Detectar líneas en columnas y filas
    lineas_columnas = np.where(suma_columnas < umbral_columnas)[0]
    lineas_filas = np.where(suma_filas < umbral_filas)[0]

    #Extraigo los renglones 
    renglon = {}
    for i in range(len(lineas_filas)-1):
        if i >= 1 and i <= 4: 
            renglon[i] = (lineas_filas[i], lineas_filas[i+1], lineas_columnas[1], lineas_columnas[3])    
        elif i >= 6 and i <= 8:
            renglon[i] = [(lineas_filas[i], lineas_filas[i+1], lineas_columnas[1], lineas_columnas[2]),
                        (lineas_filas[i], lineas_filas[i+1], lineas_columnas[2], lineas_columnas[3])]
        elif i == 9:
            renglon[i] = (lineas_filas[i], lineas_filas[i+1], lineas_columnas[1], lineas_columnas[3])
    renglon = {
        0: renglon[1], #NOMBRE Y APELLIDO
        1: renglon[2], #EDAD
        2: renglon[3], #MAIL
        3: renglon[4], #LEGAJO
        4: renglon[6], #PREGUNTA 1
        5: renglon[7], #PREGUNTA 2
        6: renglon[8], #PREGUNTA 3
        7: renglon[9]  #COMENTARIOS
    }
    return renglon

#---------------------------------------------------------------------------------------------------------------------------------------#    

def contar_caracteres_palabras(array, rango_inicial, rango_final):
    """Permite  calcular  la cantidad de caracteres y palabras de una imagen.
    Recibe como argumento un array con coordenadas de los boundign box de los
    caracteres y rango incicial y final sobre el cual establecer la condición
    de detección de caracteres y palabras."""
    #Ordeno el array en base a la primer coordenada (x inicial)
    array = array[array[:,0].argsort()]
    #Inicializo variables para guardar el total de caracteres y palabras
    x_finales = []
    caracteres = 0
    palabras = 0
    posicion_x_final = -1
    #Itero y actualizo las variables inicializadas si es condición
    if len(array) > rango_inicial and len(array) <= rango_final:
        palabras += 1
        for stat in array:
            x_finales.append(stat[0]+stat[2])
            caracteres += 1
        x_finales = x_finales[:-1]
        for st in array[1:]:
            posicion_x_final += 1
            if abs(st[0] - x_finales[posicion_x_final] ) > 7:
                palabras += 1
                #caracteres += 1 #Por si es necesario contar espacios
    return (caracteres,palabras)

def validar_si_no(img,coordenadas):
    """Permite validar campos de opcíon doble retornado cantidad de carecteres para cada opción.
    Recibe  como  argumento  una  imagen  binaria  y una lista de dos tuplas con coordenadas."""
    y1,y2,x1,x2 = coordenadas[0]
    num_labels_0, labels_0, stats_0, centroids_0 = cv2.connectedComponentsWithStats(img[y1:y2,x1:x2], 8, cv2.CV_32S)
    stats_0 = stats_0[2:]
    cant_caracteres_0, cant_palabras_0 = contar_caracteres_palabras(stats_0,0,1)
    y_1,y_2,x_1,x_2 = coordenadas[1]
    num_labels_1, labels_1, stats_1, centroids_1 = cv2.connectedComponentsWithStats(img[y_1:y_2,x_1:x_2], 8, cv2.CV_32S)
    stats_1 = stats_1[2:]
    cant_caracteres_1, cant_palabras_1 = contar_caracteres_palabras(stats_1,0,1)
    return (cant_caracteres_0,cant_caracteres_1)

#-----------------------------------------------------------------------------------------------------------------------------------------#

def validar_formulario(img_formulario):
    """Permite validar un formulario en base a las condiciones solicitadas. Retorna un
    diciconario con el nombre de cada campo y el valor 'OK' o 'MAL' según corresponda.
    Recibe como argumento la imagen del formulario a procesar."""
    #Se crea una instancia de un formulario llamando a la función 'extraer_campos'
    diccionario_formulario = extraer_campos(img_formulario)
    formulario = {'Nombre y Apellido':None,
                   'Edad':None,
                   'Mail':None,
                   'Legajo':None,
                   'Pregunta 1':None,
                   'Pregunta 2':None,
                   'Pregunta 3':None,
                   'Comentarios':None}
    #Se itera sobre sobra las claves y valores del diccionario
    for indice_campo, coordenada in diccionario_formulario.items():
        #Se convierte la imagen a binaria 
        imagen = np.where(img_formulario >= 128, 0, 1); imagen = cv2.convertScaleAbs(imagen)
        if indice_campo == 0: #NOMBRE Y APELLIDO
            y1,y2,x1,x2 = coordenada
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(imagen[y1:y2,x1:x2], 8, cv2.CV_32S)
            stats = stats[2:]
            cant_caracteres_0, cant_palabras_0 = contar_caracteres_palabras(stats,0,25)
            formulario['Nombre y Apellido'] = 'OK' if cant_caracteres_0 <= 25 and cant_palabras_0 >= 2 else 'MAL'
        elif indice_campo == 1: #EDAD
            y1,y2,x1,x2 = coordenada
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(imagen[y1:y2,x1:x2], 8, cv2.CV_32S)
            stats = stats[2:]
            cant_caracteres_1, cant_palabras_1 = contar_caracteres_palabras(stats,0,3) #cant_palabras <= 2 si se considera válido al espacio
            formulario['Edad'] = 'OK' if cant_caracteres_1 > 0 and cant_caracteres_1 < 4 and cant_palabras_1 <= 1 else 'MAL'
        elif indice_campo == 2: #MAIL
            y1,y2,x1,x2 = coordenada
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(imagen[y1:y2,x1:x2], 8, cv2.CV_32S)
            stats = stats[2:]
            cant_caracteres_2, cant_palabras_2 = contar_caracteres_palabras(stats,0,25)
            formulario['Mail'] = 'OK' if cant_caracteres_2 > 0 and cant_caracteres_2 <= 25 and cant_palabras_2 == 1 else 'MAL'
        elif indice_campo == 3: #LEGAJO
            y1,y2,x1,x2 = coordenada
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(imagen[y1:y2,x1:x2], 8, cv2.CV_32S)
            stats = stats[2:]
            cant_caracteres_3, cant_palabras_3 = contar_caracteres_palabras(stats,0,8)
            formulario['Legajo'] = 'OK' if cant_caracteres_3 == 8 and cant_palabras_3 == 1 else 'MAL'
        elif indice_campo == 4: #PREGUNTA1
            si, no = validar_si_no(imagen,coordenada)
            formulario['Pregunta 1'] = 'OK' if (si == 1) ^ (no == 1) else 'MAL'
        elif indice_campo == 5: #PREGUNTA2
            si, no = validar_si_no(imagen,coordenada)
            formulario['Pregunta 2'] = 'OK' if (si == 1) ^ (no == 1) else 'MAL'
        elif indice_campo == 6: #PREGUNTA3
            si, no = validar_si_no(imagen,coordenada)
            formulario['Pregunta 3'] = 'OK' if (si == 1) ^ (no == 1) else 'MAL'
        elif indice_campo == 7: #COMENTARIOS
            y1,y2,x1,x2 = coordenada
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(imagen[y1:y2,x1:x2], 8, cv2.CV_32S)
            stats = stats[2:]
            cant_caracteres_7, cant_palabras_7 = contar_caracteres_palabras(stats,0,25)
            formulario['Comentarios'] = 'OK' if cant_caracteres_7 > 0 and cant_caracteres_7 <= 25 else 'MAL'
    return formulario

#------------------------------------------------------------------------------------------------------------#
