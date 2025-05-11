import turtle
import time
import random
import pygame
import sys
import os

posponer = 1/10

#Contador de números e intento
score = 0
high_score = 0
intento = 0
intentoMáx = 5
juegoPerdido = False

#Ubicación de los archivos necesarios
ubicación = os.path.dirname(__file__)
mbeju = os.path.join(ubicación, "mbeju.gif")
serpienteComiendoMbeju = os.path.join(ubicación, "eat.wav")



#La pluma
pluma = turtle.Turtle()
pluma.speed(100)

#La pantalla donde muestra
anchura = 500
altura = 500
ven = turtle.Screen()
ven.title("Mi Propio Juego")
ven.bgcolor("#000000")
ven.setup(width= anchura, height= altura)
ven.tracer(0)

#Esta función contiene el código para poder tirar eventos de error de carga de archivo
def mensaje_de_error(mensaje):
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    #Antes de utilizar cualquier evento, hay que iniciar pygame
    pygame.init()
    en_ejecución = True
    pantalla = pygame.display.set_mode((600, 200))
    pygame.display.set_caption("Error")
    fuente = pygame.font.Font(None, 36)
    while en_ejecución:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pantalla.fill(BLANCO)
        texto = fuente.render(mensaje, True, NEGRO)
        rec_texto = texto.get_rect(center=(pantalla.get_width()//2, pantalla.get_height()//2))
        pantalla.blit(texto, rec_texto)
        pygame.display.flip()
    pygame.quit()
    sys.exit()

#Posibles excepciones que surgen. AQUÍ ES REGIÓN DE EXCEPCIONES
#Crearé un código para manejar excepciones a la carga de archivo
try:
    turtle.register_shape(mbeju)
except turtle.TurtleGraphicsError as e:
    mensaje_de_error("La imagen no se cargó correctamente", e)

#Sonido para el juego
try:
    pygame.mixer.init()
    comer = pygame.mixer.Sound(serpienteComiendoMbeju)
except pygame.error as e:
    mensaje_de_error(f"No se cargó el audio correctamente o no existe el mismo: {e}")


#La cabeza de serpiente
cabeza = turtle.Turtle()
cabeza.speed(0)
cabeza.shape("square")
cabeza.color("white")
cabeza.penup()
cabeza.goto(0,0)
cabeza.direction = "stop"

#La comida
comida = turtle.Turtle()
comida.speed(0)
comida.shape(mbeju)
comida.penup()
comida.goto(0,100)

#Marcador de resultado
texto = turtle.Turtle()
texto.speed(0)
texto.color("#FFFFFF")
texto.penup()
texto.hideturtle()
texto.goto(10,400)
texto.write(f"Resultado: {score}          Resultado más alto: {high_score}",
            align = "center", font =("Century", 25, "normal"))
texto.goto(-100,-400)
texto.write("Game made by Ramiro Mateo Vera",
                    align = "center", font =("Century", 12, "normal"))

#El Cuerpo de la Serpiente
segmentos = []

#Funciones para hacer mover a la serpiente
def arriba():
    dirección_contraria_abajo = cabeza.direction != "down"
    if dirección_contraria_abajo:
        cabeza.direction = "up"
def abajo():
    dirección_contraria_arriba = cabeza.direction != "up"
    if dirección_contraria_arriba:
        cabeza.direction = "down"
def derecha():
    dirección_contraria_izquierda = cabeza.direction != "left"
    if dirección_contraria_izquierda:
        cabeza.direction = "right"
def izquierda():
    dirección_contraria_derecha = cabeza.direction != "right"
    if dirección_contraria_derecha:
        cabeza.direction = "left"
#def pausa():   
def mov():
    cabeza_dirección_arriba = cabeza.direction == "up"
    cabeza_dirección_abajo = cabeza.direction == "down"
    cabeza_dirección_derecha = cabeza.direction == "right"
    cabeza_dirección_izquierda = cabeza.direction == "left"
    
    if cabeza_dirección_arriba:
        y = cabeza.ycor()
        cabeza.sety(y + 20)
        
    elif cabeza_dirección_abajo:
        y = cabeza.ycor()
        cabeza.sety(y - 20)
        
    elif cabeza_dirección_derecha:
        x = cabeza.xcor()
        cabeza.setx(x + 20)
        
    elif cabeza_dirección_izquierda:
        x = cabeza.xcor()
        cabeza.setx(x - 20)
        
#Funciones de teclado
ven.listen()
ven.onkeypress(arriba, "Up")
ven.onkeypress(abajo, "Down")
ven.onkeypress(derecha, "Right")
ven.onkeypress(izquierda, "Left")

#Lo que voy a hacer a continuación es crear una función para iniciar el juego
#tanta cantidad de veces que deseo yo
def iniciar_juego():
    global high_score
    ven.update()
    #Colisión de borde
    colisión_de_cabeza_positive_axe_x = cabeza.xcor() > anchura - 80
    colisión_de_cabeza_negative_axe_x = cabeza.xcor() < -anchura + 80
    colisión_de_cabeza_positive_axe_y = cabeza.ycor() > altura - 520
    colisión_de_cabeza_negative_axe_y = cabeza.ycor() < -altura + 520
    if colisión_de_cabeza_positive_axe_x or colisión_de_cabeza_negative_axe_x or colisión_de_cabeza_positive_axe_y or colisión_de_cabeza_negative_axe_y:
        time.sleep(1)
        cabeza.goto(0,0)
        cabeza.direction = "stop"
        
    #Desaparición de segmentos
        for segmento in segmentos:
             segmento.goto(1000,1000)
             
    #Limpieza de segmentos
        segmentos.clear()
        score = 0
        texto.goto(10,400)
        texto.clear()
        texto.write(texto.write(f"Resultado: {score}          Resultado más alto: {high_score}",
                    align = "center", font =("Century", 25, "normal")), align = "center", font =("Century", 25, "normal"))
        texto.goto(-100,-400)
        texto.write("Game made by Ramiro Mateo Vera",
                    align = "center", font =("Century", 12, "normal"))
        
    #Colisión de comida
    distancia = cabeza.distance(comida) < 20
    if distancia:
        x = random.randint(-890, 890)
        y = random.randint(-190, 190)
        comida.goto(x,y)
        segmento = turtle.Turtle()
        segmento.speed(0)
        segmento.shape("circle")
        segmento.color("#FF0000")
        segmento.penup()
        comer.play()
        segmentos.append(segmento)
        
    #Contador de números
        score += 5
        contador = score > high_score
        if contador:
            high_score = score
        texto.clear()
        texto.goto(10,400)
        texto.write(f"Resultado: {score}          Resultado más alto: {high_score}",
                    align = "center", font =("Century", 25, "normal"))
        texto.goto(-100,-400)
        texto.write("Game made by Ramiro Mateo Vera",
                    align = "center", font =("Century", 12, "normal"))
        
    #Movimiento del cuerpo de la serpiente
    totalSeg = len(segmentos)
    for index in range (totalSeg -1, 0, -1):
        x = segmentos[index - 1].xcor()
        y = segmentos[index - 1].ycor()
        segmentos[index].goto(x,y)
    total_de_seg = totalSeg >= 1
    if total_de_seg:
        x = cabeza.xcor()
        y = cabeza.ycor()
        segmentos[0].goto(x,y)
    mov()
    reiniciar_juego()
    

#Aquí voy a crear una función llamada reiniciar_juego() para que pueda reiniciar
#sin que se inicie el juego pero se cierre durante 5 segundos
def reiniciar_juego():
    global score, high_score, juegoPerdido, posponer
    for segmento in segmentos:
        if segmento.distance(cabeza) < 20:
            time.sleep(1/2)
            cabeza.goto(0,0)
            cabeza.direction = "stop"
            score = 0
            texto.clear()
            texto.goto(10,400)
            texto.write(f"Resultado: {score}          Resultado más alto: {high_score}",
                    align = "center", font =("Century", 25, "normal"))
            texto.goto(-100,-400)
            texto.write("Game made by Ramiro Mateo Vera",
                    align = "center", font =("Century", 12, "normal"))
            #Desaparición de los segmentos
            for segmento in segmentos:
                segmento.goto(1000,1000)
            segmentos.clear()
            
            juegoPerdido = True
            time.sleep(posponer)
            return


#Acá recorro el juego hasta que los intentos lleguen a 5, al llegar a la cantidad
#exacta, el juego se cierra
def bucle_del_juego():
    global intento, juegoPerdido

    #Creo una condición para evitar cierres inesperados
    if juegoPerdido:
        intento += 1
        juegoPerdido = False
    
    
    if intento >= intentoMáx:
        turtle.bye()
        return
    
    reiniciar_juego()
    iniciar_juego()
    ven.ontimer(bucle_del_juego, 500)

bucle_del_juego()
turtle.mainloop()
