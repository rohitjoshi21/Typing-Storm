#!/usr/bin/python3

from tkinter import *
import random
import time

class Box:
    def __init__(self,canvas,color,score,game):
        self.canvas=canvas
        self.id=canvas.create_rectangle(0,0,200,50,fill=color)
        self.id1=canvas.create_text(0,0,text=word_list[n],fill="black",font=("Times",30))
        self.canvas.move(self.id,250,5)
        self.canvas.move(self.id1,350,30)
        self.w=""
        
        self.box2=canvas.create_rectangle(0,0,200,50,fill="#6666ff")
        self.typed_text=self.canvas.create_text(0,0,text=self.w,font=("times",30))
        self.canvas.move(self.box2,10,110)
        self.canvas.move(self.typed_text,110,135)
        self.canvas_height=canvas.winfo_height()
        self.cursor=0
        self.canvas.bind_all('<KeyPress>',self.collect)
        
    def help_box(self):
        self.canvas.itemconfig(self.typed_text,text=self.w)

    def collect(self,event):
        if game.state==True:
            if word_list[n][self.cursor]==event.keysym:
                self.cursor+=1
                self.w+=event.keysym
                self.help_box()
                if self.w==word_list[n]:
                    self.new_word()
                    self.w=""
                    score.change_score()
                    self.cursor=0
                    self.help_box()

    def new_word(self):
        self.change_index()
        self.canvas.move(self.id,0,-self.pos[3])
        self.canvas.move(self.id1,0,-self.pos[3])
        self.canvas.itemconfig(self.id1,text=word_list[n])

    def fall(self):
        global lower_limit,miss,new_box,old_box,n,speed
        self.pos=self.canvas.coords(self.id)
        self.canvas.move(self.id,0,speed)
        self.canvas.move(self.id1,0,speed)
        if self.pos[3]>=lower_limit:
            miss+=1
            new_box=old_box+1
            self.change_index()      
            lower_limit=lower_limit-(self.pos[3]-self.pos[1])

    def change_index(self):
        global n,speed
        if n<len(word_list)-1:
            n+=1
        else:
            n=0
            speed+=0.8
            random.shuffle(word_list)

    def game_over(self):
        self.gameover=self.canvas.create_text(350,250,text="Game Over",font=("times",50))
        self.gameover=self.canvas.create_text(350,320,text="Press Space or Enter to play again",font=("times",30))
        
class Container:

    def __init__(self,canvas,color):
        self.canvas=canvas
        self.id=canvas.create_polygon(0,0,0,190,280,190,280,0,240,0,240,150,40,150,40,0,fill=color)
        self.canvas.move(self.id,210,410)
        
class Score:

    def __init__(self,canvas,color,high_score):
        self.canvas=canvas
        self.id=canvas.create_rectangle(0,0,200,100,fill=color)
        self.canvas.move(self.id,10,10)
        self.points=0
        self.id1=self.canvas.create_text(0,0,text="High Score = "+str(high_score),font=("Times",20))
        self.id2=self.canvas.create_text(0,0,text=self.points,font=("Times",30))
        self.canvas.move(self.id1,110,25)
        self.canvas.move(self.id2,100,70) 

    def change_score(self):
        self.points=self.points+1
        self.canvas.itemconfig(self.id2,text=self.points)

class Text:

    def __init__(self,canvas,color):
        self.canvas=canvas
        self.state=False
        self.id1=canvas.create_text(0,0,text="Press Space or Enter to start the game",state="normal",font=("Times",30),fill=color)
        self.canvas.move(self.id1,350,300)
        self.canvas.bind_all('<Button-1>',self.interrupt)
        self.canvas.bind_all('<KeyPress-Return>',self.interrupt)
        self.canvas.bind_all('<KeyPress-space>',self.interrupt)

    def interrupt(self,event):
        global play,play_again
        if play==True:
            if self.state==True:
                self.canvas.itemconfig(self.id1,state="normal")
                self.state=False
                play=True
            else:
                self.state=True
                self.canvas.itemconfig(self.id1,state="hidden")
        else:
            play=True
            play_again=True

def highscore_read():
    file=open("high_score.txt")
    high_score=int(file.read())
    return high_score

def highscore_write(high_score):
    if high_score > highscore_read():
        file=open("High_score.txt","w")
        file.write(str(high_score))
        file.close()


tk=Tk()
tk.title("Typing-Storm")
canvas=Canvas(tk,width=700,height=600,bg="#c0ceab")
canvas.pack()
tk.update()
play=True

try:
    while play==True:
        score=Score(canvas,"orange",highscore_read())
        container=Container(canvas,"Blue")
        game=Text(canvas,"#cc0000")    
        f = open('words.txt','r')
        word_list = f.readlines()
        for i in range(len(word_list)):
            word_list[i] = word_list[i].replace('\n','')
        random.shuffle(word_list)

        old_box,new_box,n,miss=0,0,0,0
        speed=1
        play_again=False
        lower_limit=canvas.winfo_height()-40

        box=[]
        for i in range(3):
            box.append("")
        box[old_box]=Box(canvas,"tomato",score,game)

        while True:
            if game.state==True:
                if miss<=2:
                    if old_box==new_box:
                        box[old_box].fall()
                    else:
                        box[new_box]=Box(canvas,"tomato",score,game)
                        
                        old_box=new_box
                else:
                    box[old_box].w=0
                    box[old_box].help_box()
                    box[old_box].game_over()
                    highscore_write(score.points)
                    play=False
            tk.update()
            time.sleep(0.01)
            if play_again==True:
                break
        tk.update()
        canvas.delete("all")
except TclError:
    print("Game Closed")



