import pygame as pg
import sys
import random
import pygame_menu as pm
import datetime as dt
import psycopg2 as sql

insert_data = '''
    INSERT INTO snake VALUES (DEFAULT,%s,%s,%s)'''
update_data = '''
    UPDATE snake
    SET score = %s
    WHERE name = %s AND level = %s
    '''
show_data = '''
    SELECT name , score , level
    FROM snake
    GROUP BY name , score
    ORDER BY score DESC'''

name = input('Please write the name :') 

connection = sql.connect(host = 'localhost',
                         dbname = 'postgres',
                         user = 'postgres',
                         password = 'Adil$notlove',
                         port = '5432')
cursor = connection.cursor()

pg.init()

back_image = pg.transform.scale(pg.image.load(r'C:\Users\user\Downloads\R.png'),(500,600))

SIZE_BLOCK = 20
WHITE, RED , BLUE , GREEN , BLACK = (255,255,255) , (255,0,0) , (0,0,255) , (0,255,0) , (0,0,0)
SNAKE_COLOR , HEADER_COLOR ,FRAME_COLOR  = 'YELLOW' , (0,0,0) , (0,0,0)
 
COUNT_BLOCKS = 20
MARGIN = 1
HEADER_MARGIN = 70 
SIZE = [SIZE_BLOCK*COUNT_BLOCKS+2*SIZE_BLOCK*COUNT_BLOCKS,
              SIZE_BLOCK*COUNT_BLOCKS+2*SIZE_BLOCK+MARGIN*COUNT_BLOCKS+HEADER_MARGIN]

screen = pg.display.set_mode((800,550)) 
timer = pg.time.Clock()
courier = pg.font.SysFont('courier',36,1)
lil_courier = pg.font.SysFont('courier',20,1) 

class SnakeParams:
    def __init__(self, x , y ):
        self.x = x 
        self.y = y

    def is_inside(self):
        return 0<=self.x<COUNT_BLOCKS and 0 <= self.y<COUNT_BLOCKS
    
    def __eq__(self, other):
        return isinstance(other,SnakeParams) and self.x == other.x and self.y == other.y
    
def draw_parts (color, row, column):
    pg.draw.rect(screen , color  , [SIZE_BLOCK+column*SIZE_BLOCK + MARGIN*column ,
                                    HEADER_MARGIN+SIZE_BLOCK+row*SIZE_BLOCK+MARGIN*row ,
                                    SIZE_BLOCK,SIZE_BLOCK])
    
def point_position(row, column):
    SIZE = [SIZE_BLOCK+column*SIZE_BLOCK+MARGIN*column,
            HEADER_MARGIN+SIZE_BLOCK+row*SIZE_BLOCK+MARGIN*row -10,
            SIZE_BLOCK,SIZE_BLOCK]  
    return SIZE 

def start():
    print([SIZE_BLOCK+10*SIZE_BLOCK + MARGIN*10 ,
           HEADER_MARGIN+SIZE_BLOCK+10*SIZE_BLOCK+MARGIN*10,
           SIZE_BLOCK,SIZE_BLOCK]) 
    def product_generator():
        x = random.randint(0,COUNT_BLOCKS-1)
        y = random.randint(0,COUNT_BLOCKS-1) 
        point = random.randint(1, 5)
        spawn_time = dt.datetime.now()
        empty_point = SnakeParams(x, y)
        while empty_point in snake_blocks:
            empty_point.x = random.randint(0, COUNT_BLOCKS-1)
            empty_point.y = random.randint(0, COUNT_BLOCKS-1-6) 
        return empty_point, point, spawn_time 
    
    snake_blocks = [SnakeParams(9,9),SnakeParams(9,10),SnakeParams(9,11)] 
    product, point , spawn = product_generator() 

    some_row = 0
    some_column = 1 
    global totalen  
    velocity = 1

    while True: 
        for event in pg.event.get():
            if event.type == pg.QUIT:
                print('exit')
                pg.quit()
                sys.exit() 
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP and some_column != 0:
                    some_row = -1
                    some_column = 0
                elif event.key == pg.K_DOWN and some_column != 0:
                    some_row = 1
                    some_column = 0
                elif event.key == pg.K_RIGHT and some_row != 0: 
                    some_row = 0
                    some_column = 1 
                elif event.key == pg.K_LEFT and some_row != 0: 
                    some_row = 0
                    some_column = -1
        
        screen.fill(FRAME_COLOR) 
        pg.draw .rect(screen , HEADER_COLOR , [0, 0, SIZE[0], HEADER_MARGIN]) 

        text_sum = courier.render(f"TOTAL:{totalen}", 1, WHITE)
        text_velocity = courier.render(f"VELOCITY:{velocity}", 1, WHITE) 
        text_level = courier.render(f"LEVEL:{totalen//5}",1,WHITE)
        text_name = courier.render(f"Your name:{name}",1, WHITE)
        point_surface = courier.render(f"{point}", 1, WHITE) 
        screen.blit(text_sum,(SIZE_BLOCK+530, SIZE_BLOCK)) 
        screen.blit(text_velocity,(SIZE_BLOCK+530,SIZE_BLOCK+250))
        screen.blit(text_level,(SIZE_BLOCK+530,SIZE_BLOCK+450))
        screen.blit(text_name,(SIZE_BLOCK,SIZE_BLOCK))
        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                if (row+column)%2==0: color = RED
                else : color = BLACK  

                draw_parts(color, row, column)
        
        head = snake_blocks[-1] 
        if not head.is_inside(): 
            level = totalen//5 
            print('avaria') 
            cursor.execute(update_data,(totalen,name,level)) 
            cursor.execute(insert_data,(name,totalen,level)) 
            break 

        draw_parts(GREEN, product.x, product.y) 
        screen.blit(point_surface, point_position(product.x,product.y))
        for block in snake_blocks:
            draw_parts(SNAKE_COLOR ,block.x , block.y )
        
        now = dt.datetime.now()
        if (now - spawn).seconds.real >= point + 1:
            product, point, spawn = product_generator()

        if product == head:
            totalen += point 
            velocity = totalen//3 + 1 
            snake_blocks.append(product)
            product , point , spawn = product_generator() 

        new_head = SnakeParams(head.x + some_row, head.y + some_column)
        if new_head in snake_blocks: 
            print('SAM SEBE "VYRYL YAMU"') 
            level = totalen//5 
            cursor.execute(update_data,(totalen,name,level))
            cursor.execute(insert_data,(name,totalen,level))
            break 

        snake_blocks.append(new_head) 
        snake_blocks.pop(0) 

        time = lil_courier.render("Time for respawn food: " + str(point+1 -(now - spawn).seconds.real), 1, WHITE)
        screen.blit(time,(20,508)) 

        pg.display.flip() 
        timer.tick(3+velocity) 

totalen = 0

menu = pm.Menu('Snake', 400, 300,theme=pm.themes.THEME_DARK.set_background_color_opacity(1))
menu.add.text_input('Name :',default= name)
menu.add.button('Play', start)
menu.add.button('Quit', pm.events.EXIT) 

while True:
    screen.blit(back_image,(200,0))

    events = pg.event.get() 
    for event in events:
        if event.type == pg.QUIT:
            cursor.close()
            connection.close()
            exit()
        if menu.is_enabled():
            menu.update(events)
            menu.draw(screen) 

        pg.display.update()
        connection.commit()