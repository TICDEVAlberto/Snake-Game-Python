from tkinter import *
import random

#Constantes de la ventana de juego
GAME_WIDTH = 900
GAME_HEIGHT = 900
GAME_BOARD_BACKGROUND_COLOR = "#331a00"
WINDOW_BACKGROUND_COLOR = "black"

#Constantes de la serpiente y ratón
ENTITY_SIZE = 50
SNAKE_PARTS = 3
SNAKE_COLOR = "#fff200"
SNAKE_COLOR_2 = "#3557f2"
LISTA = [SNAKE_COLOR, SNAKE_COLOR_2]
MOUSE_COLOR = "#6d6d6d"
SPEED = 100

#Variables
score = 0
direction = "down"

class Mouse:
    def __init__(self):
        mouse_x = random.randint(0, (GAME_WIDTH / ENTITY_SIZE) - 1) * ENTITY_SIZE #Le damos a la coordenada x un valor random dentro de los límites del canvas
        mouse_y = random.randint(0, (GAME_HEIGHT / ENTITY_SIZE) - 1) * ENTITY_SIZE #Le damos a la coordenada y un valor random dentro de los límites del canvas

        self.mouse_coords = [mouse_x, mouse_y]

        game_board_canvas.create_oval(mouse_x, mouse_y, (mouse_x + ENTITY_SIZE), (mouse_y + ENTITY_SIZE), fill=MOUSE_COLOR, tag="mouse") #creamos el ratón en pantalla 


class Snake:
    def __init__(self):
        self.snake_size = SNAKE_PARTS
        self.snake_coords = [] #Lista de las diferentes coordenadas de cada parte de la serpiente
        self.snake_parts = [] #Lista de las partes visuales de la serpiente

        for i in range(0, SNAKE_PARTS): #Añadimos a la lista de coordenadas de la serpiente 3 sublistas, las cuales cada una corresponde a una parte de la serpiente
            self.snake_coords.append([0, 0])
        
        for snake_x, snake_y in self.snake_coords: #Creamos 3 cuadrados iniclaes que representan el cuerpo de la serpiente y las añadimos a la lista de partes de la serpiente
            snake_part = game_board_canvas.create_rectangle(snake_x, snake_y, (snake_x + ENTITY_SIZE), (snake_y + ENTITY_SIZE), fill=random.choice(LISTA), tag="snake")
            self.snake_parts.append(snake_part)

    def move(self, new_direction):
        '''ESP: Esta función permite cambiar la varibale dirección, la cuál según que valor tenga la serpiente uirá en una direción u otra.
        ING: In this function we change the value of the variable "dirección", which according to the value of the variable, the sanke will going in a one direccion or another.'''
        
        global direction

        if new_direction == "left":
            if direction != "right":
                direction = new_direction
        elif new_direction == "right":
            if direction != "left":
                direction = new_direction
        elif new_direction == "up":
            if direction != "down":
                direction = new_direction
        elif new_direction == "down":
            if direction != "up":
                direction = new_direction

def main(snake, mouse):
    '''ESP: Esta función se encarga de darle movimiento a la serpien te y comprobar si nos comemos o no al ratón 
    ING: This function is responsible for give movement to the snake, and chek if we ate or not the mouse'''

    snake_x_coord, snake_y_coord = snake.snake_coords[0]

    if direction == "up":
        snake_y_coord -= ENTITY_SIZE
    elif direction == "down":
        snake_y_coord += ENTITY_SIZE
    elif direction == "left":
        snake_x_coord -= ENTITY_SIZE
    elif direction == "right":
        snake_x_coord += ENTITY_SIZE

    snake.snake_coords.insert(0, (snake_x_coord, snake_y_coord)) #Inserta las coordenadas nuevas de la serpiente en la lista al principio de esta
    snake_part = game_board_canvas.create_rectangle(snake_x_coord, snake_y_coord, (snake_x_coord + ENTITY_SIZE), (snake_y_coord + ENTITY_SIZE), fill=random.choice(LISTA))
    snake.snake_parts.insert(0, snake_part) #Inserta la parte nueva creada al inicio de la lista de partes

    if snake_x_coord == mouse.mouse_coords[0] and snake_y_coord == mouse.mouse_coords[1]: #Comprueba si tocamos al ratón, en caso de que si, lo elimina, suma 1pt a la varibale score y crea otro ratón en pantalla
        global score
        score += 1
        score_label.config(text="Score: {}".format(score))

        game_board_canvas.delete("mouse")
        mouse = Mouse()
    else: #En caso de no tocar el ratñón: 
        del snake.snake_coords[-1] #Eliminamos las últimas cóordenadas de la lista de coordenadas de la serpiente
        game_board_canvas.delete(snake.snake_parts[-1]) #Eliminamos el último cuadrado de la serpiente
        del snake.snake_parts[-1] #Eliminamos dicho cuadrado de la lista

    if check_colosions(snake): #Si chocamos (es decir, la func devuelve True), se llama a la función game over
        game_over()
    else:
        window.after(SPEED, main, snake, mouse) #Esta func llama a la func main para poder hacer que la serpiente se mueva de forma indefinida

def check_colosions(snake):
    '''ESP: Esta función se encarga de comprobar si nos hemos chocado o no con el borde del canvas
    ING: This function is responsible of chek if we crash with the canva's border'''

    snake_x_coord, snake_y_coord = snake.snake_coords[0] #A estas varibales le asignamos las coordenadas x e y de la cabeza de la serpiente 

    if snake_x_coord < 0 or snake_x_coord >= GAME_WIDTH: #Si chocamos con las paredes devuelve True
        return True
    elif snake_y_coord < 0 or snake_y_coord >= GAME_HEIGHT: #Si chocamos con el techo o suelo, devolvemos True
        return True
    
    for snake_part in snake.snake_coords[1:]: #Si chocamos con nuestro cuerpo devuelve True
        if snake_x_coord == snake_part[0] and snake_y_coord == snake_part[1]:
            return True
    
    return False

def game_over():
    '''ESP: Esta función elimina todo del canvas, lo vuelve de color negro y pone un texto de "Game Over".
    ING: This function erase all the elements of the canvas, makes the canvas black and adds a "Game Over text"'''

    game_board_canvas.delete(ALL)
    game_board_canvas.config(bg="black")
    game_board_canvas.create_text(game_board_canvas.winfo_width()/2, game_board_canvas.winfo_height()/2,
                       font=('consolas',70), text="GAME OVER", fill="red", tag="gameover") #Crea un texto de game over


window = Tk()
window.title("Snake Game")
window.state("zoomed") #Esta función hace que la pantalla salga en full screen al iniciar el programa
window.config(bg=WINDOW_BACKGROUND_COLOR)
icon = PhotoImage(file="icon.png")
window.iconphoto(True, icon)

score_label = Label(window, text="Score: {}".format(score), font=("calibri", 40), bg=WINDOW_BACKGROUND_COLOR, fg="white") #Creamos un texto que nod dice nuestra puntuación a lo largo del juego
score_label.pack()

game_board_canvas = Canvas(window, bg=GAME_BOARD_BACKGROUND_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT) #Creamos el tablero de juego
game_board_canvas.pack()

window.bind("<w>", lambda event: snake.move("up")) #Nos permite detectar cuando se presiona w y así llamar a la función move() y pasarle el valor "up"
window.bind("<s>", lambda event: snake.move("down")) #Nos permite detectar cuando se presiona d y así llamar a la función move() y pasarle el valor "down"
window.bind("<a>", lambda event: snake.move("left")) #Nos permite detectar cuando se presiona a y así llamar a la función move() y pasarle el valor "left"
window.bind("<d>", lambda event: snake.move("right")) #Nos permite detectar cuando se presiona d y así llamar a la función move() y pasarle el valor "right"

snake = Snake() #Creamos un objeto serpiente
mouse = Mouse() #Creamos un objeto ratón

main(snake, mouse) #Llamamos al método main() y le pasamos los objetos anteriormente creados

window.mainloop()