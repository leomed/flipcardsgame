from tkinter import *
from tkinter import messagebox
import random
import pandas as pd
import json

BACKGROUND_COLOR = "#B1DDC6"
window = Tk()
window.title("Flip Cards")
window.config(padx=50,pady=50, bg=BACKGROUND_COLOR)


current_word = {}
to_learn = {}


try:
    #Csv Read
    """It starts from words_to_learn in order to start
    with the saving words that the user do not know
    The first time that the program is executed this file does not exist
    thats why it is inside the (TRY)
    """
    data = pd.read_csv("words_to_learn.csv")
except FileNotFoundError:
    """If it is the first time, words_to_learn does not exist
    in that case it should run the program with the original file with all the words
    """
    original_data = pd.read_csv("words.csv")
    #After reading the csv data, it is neccessary to convert it to any other data
    #Records is a parameter to filter the data properly into a dict
    to_learn = original_data.to_dict(orient="records")
else:
    # Records is a parameter to filter the data properly into a dict
    """If the program had been executed, it starts from the previous point"""
    to_learn = data.to_dict(orient="records")



#Functions

def new_word():
    """With global the data is saved outside the function,
    so if there is another function that needs it,the scope
    is not going to make problems
    """
    global current_word
    """After cancel prevents the bug of going to the next
    card with out waiting the 3 seconds
    """
    global flip_timer
    window.after_cancel(flip_timer)
    current_word = random.choice(to_learn)
    """Itemconfig is used to change some attributes dynamically
    the first input is the item that i need to change ex:card_word
    and then which parameter in this case (text=)
    """
    # "Spanish" is one of the series of the csv file
    """After clicking any button it is neccesary to
    show the white card with another word
    """
    canvas.itemconfig(card_word, text=current_word["Spanish"], fill="black")

    # In this case i want to change the TEXT only
    canvas.itemconfig(card_title, text="Spanish",fill="black")

    canvas.itemconfig(card_bakground, image=card_front)

    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    """After 3 seconds the title,word, the color of the cards
    and the language its changed
    """
    canvas.itemconfig(card_title, text="German")
    canvas.itemconfig(card_word, text=current_word["German"])
    canvas.itemconfig(card_bakground, image=card_back)

    #The color of the letters
    canvas.itemconfig(card_title, fill="white")
    canvas.itemconfig(card_word, fill="white")

#After class execute something after 3000miliseconds
flip_timer = window.after(3000, func=flip_card)

def is_known():
    """Remove is a method that deletes an entry, in this case the word
    that the user knows it is deleted and inserted then in a new file
    """
    to_learn.remove(current_word)

    #It is neccessary to create a new file with the known words
    data = pd.DataFrame(to_learn)
    """By default pandas adds the number of the index
    to the data frame with (index=false) it prevents from doing it
    """
    data.to_csv("words_to_learn.csv", index=False)



    new_word()









#UI
canvas = Canvas(width=800,height=526, highlightthickness=0)

#Background of the canvas
canvas.config(bg=BACKGROUND_COLOR)

# Cards
card_back = PhotoImage(file="card_back.png")
card_front = PhotoImage(file="card_front.png")

#The canvas needs to be the same size as the image
card_bakground = canvas.create_image(400,263, image=card_front)



#Texts in the cards
"""To change something dinamically it is better to save the data in to
a variable 
"""
card_title = canvas.create_text(400,150,text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400,263, text="",  font=("Ariel", 60, "bold"))

#The position of the entire grid
#Columnspan to center the data between 0 and 1
canvas.grid(column=0,row=0,columnspan=2)


#Buttons images
right_button_img = PhotoImage(file="right.png")
wrong_button_img = PhotoImage(file="wrong.png")

#Known Answer
right_button = Button(image=right_button_img, highlightthickness=0 ,command=is_known)
right_button.grid(row=1,column=0)

#Wrong or unknown
wrong_button = Button(image=wrong_button_img, highlightthickness=0, command=new_word)
wrong_button.grid(row=1,column=1)




























#Here i execute the function to change the texts in the canvas immediately
new_word()


window.mainloop()