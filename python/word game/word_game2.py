import tkinter as tk
import random
from tkinter import ttk
import pandas as pd
from tkinter import Button

root = tk.Tk()


#set size window
root.geometry('800x600')
#set left and right from monitor
root.geometry('+50+50')
##set max size for windows
root.maxsize(800,600)
##set min size for windows
root.minsize(700,500)
#set title
root.title("word game")
# change word function

# title canvase
canvas_title = tk.Canvas(root, width=400, height=60)
canvas_title.place(x=10,y=10)

# score canvase
canvas_score = tk.Canvas(root, width=200, height=60)
canvas_score.place(x=400,y=10)

# time canvase
canvas_time = tk.Canvas(root, width=200, height=60)
canvas_time.place(x=560,y=10)

#question canvase
canvas_question = tk.Canvas(root, width=780, height=60,bg="brown")
canvas_question.place(x=10,y=70)

#status canvase
canvas_status = tk.Canvas(root, width=780, height=30,bg="brown")
canvas_status.place(x=10,y=140)

#answer canvase
canvas_answer = tk.Canvas(root, width=780, height=200,bg="orange")
canvas_answer.place(x=10,y=180)

# downbutton canvas
canvas_DownButton =tk.Canvas(root,width=780,height=50,bg="lightgreen")
canvas_DownButton.place(x=10,y=390)

#increases word
canvas_increases = tk.Canvas(root, width=780, height=100,bg="green")
canvas_increases.place(x=10,y=450)
   
#list for back button  
Bkanji=[]
Bpersian=[]
Benglish=[]

backanswers0=[]
backanswers1=[]
backanswers2=[]
backanswers3=[]

#change word function
def change_word():
    btn1.config(bg="lightblue",fg="red")
    btn2.config(bg="lightblue",fg="red")
    btn3.config(bg="lightblue",fg="red")
    btn4.config(bg="lightblue",fg="red")

    
    random_row = df.sample()
    random_kanji=random_row["kanji"].to_string(index=False,header=False)
    global random_hiragana
    random_hiragana=random_row["hiragana/katakana"].to_string(index=False,header=False)
    random_persian=random_row["persian"].to_string(index=False,header=False)
    random_english=random_row["english"].to_string(index=False,header=False)
    
    answers=[]
    for i in range(3):
        random_row2=df.sample()
        random_hragana2=random_row2["hiragana/katakana"].to_string(index=False,header=False)
        answers.append(random_hragana2)
    answers.append(random_hiragana)
    random.shuffle(answers)
    
    backanswers0.append(answers[0])
    backanswers1.append(answers[1])
    backanswers2.append(answers[2])
    backanswers3.append(answers[3])
    
    btn1.config(text=answers[0])
    btn2.config(text=answers[1])
    btn3.config(text=answers[2])
    btn4.config(text=answers[3])
        
    # change text for next button 
    next_btn.config(text="Next")
    
    label_kanji.config(text=f"kanji :{random_kanji}")
    label_status_persian.config(text=f"Persian : {random_persian}")
    label_status_english.config(text=f"English : {random_english}")
    
    
    Bkanji.append(random_kanji)
    Bpersian.append(random_persian)
    Benglish.append(random_english)

    
def back_word():

    
    label_kanji.config(text=f"kanji :{Bkanji[-2]}")
    label_status_persian.config(text=f"Persian : {Bpersian[-2]}")
    label_status_english.config(text=f"English : {Benglish[-2]}")
    
    btn1.config(text=backanswers0[-2])
    btn2.config(text=backanswers1[-2])
    btn4.config(text=backanswers2[-2])
    btn3.config(text=backanswers3[-2])
    
score = 0  
def score_cal(btnNumber):
    global score
    if btn1.cget("text") == random_hiragana and btnNumber==1:
        score +=1
        label_score.config(text=f"امتیاز : {score}")
    if btn2.cget("text") == random_hiragana and btnNumber==2:
        score +=1
        label_score.config(text=f"امتیاز : {score}")
    if btn3.cget("text")== random_hiragana and btnNumber==3:
        score +=1
        label_score.config(text=f"امتیاز : {score}")
    if btn4.cget("text")== random_hiragana and btnNumber==4:
        score +=1
        label_score.config(text=f"امتیاز : {score}")
            
    change_word()
    


#insert database

df = pd.read_csv('D:/code/end_project/python/word game/vocabulary-csv.csv')
kanji,hiragana,persian,english=df["kanji"],df["hiragana/katakana"],df["persian"],df["english"]

# send data to sqlite3 database
import sqlite3
conn = sqlite3.connect('D:/code/end_project/python/word game/vocabulary.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS vocabulary (kanji TEXT, hiragana TEXT, persian TEXT, english TEXT)''')
for i in range(len(kanji)):
    c.execute("INSERT INTO vocabulary (kanji,hiragana,persian,english) VALUES (?,?,?,?)",(kanji[i],hiragana[i],persian[i],english[i]))
conn.commit()
conn.close()

title_up = tk.Label(canvas_title, text="آموزش لغات به صورت تخصصی", font=('Arial', 20), fg='blue')
title_up.place(x=10,y=10)
#score label
label_score = tk.Label(canvas_score, text="امتیاز : 0", font=('Arial',20))
label_score.place(x=10,y=10)

#time label
label_time = tk.Label(canvas_time, text="زمان باقی مانده : 10", font=('Arial',20))
label_time.place(x=10,y=10)

#kanji label
label_kanji=tk.Label(canvas_question,text="دکمه شروع را بزنید",font=("tahoma",20),fg="white",bg="brown")
label_kanji.place(x=10,y=10)

#status label
label_persian=tk.Label(canvas_status,text=persian[1])
label_persian.place(x=20,y=2)
label_status_persian = tk.Label(canvas_status,text="Persian :",font=("Arial,15"),bg="brown",fg="yellow")
label_status_persian.place(x=2,y=2)
label_status_english = tk.Label(canvas_status,text="English :",font=("Arial,15"),bg="brown",fg="yellow")
label_status_english.place(x=390,y=2)

# answer label
label_hiragana = tk.Label(canvas_answer,text="hiragana/katakana",font=("tahoma,20"),bg="brown",fg="white")
label_hiragana.place(x=5,y=5)

# answer button
btn1=Button(master=canvas_answer,text="answer1",font=("tahoma,30"),fg="red",bg="lightblue",width=15,height=2,command=lambda:score_cal(1))
btn1.place(x=5,y=40)

btn2=Button(master=canvas_answer,text="answer2",font=("tahoma,30"),fg="red",bg="lightblue",width=15,height=2,command=lambda:score_cal(2))
btn2.place(x=185,y=40)

btn3=Button(master=canvas_answer,text="answer3",font=("tahoma,30"),fg="red",bg="lightblue",width=15,height=2,command=lambda:score_cal(3))
btn3.place(x=365,y=40)

btn4=Button(master=canvas_answer,text="answer4",font=("tahoma,30"),fg="red",bg="lightblue",width=15,height=2,command=lambda:score_cal(4))
btn4.place(x=545,y=40)

# down button
next_btn = Button(master=canvas_DownButton, text="Back", font=("tahoma,20"),fg="green",width=10,height=1,command=back_word)
next_btn.place(x=10,y=6)
next_btn = Button(master=canvas_DownButton, text="شروع", font=("tahoma,20"),fg="green",width=10,height=1,command=change_word)
next_btn.place(x=150,y=6)











#view app
root.mainloop()