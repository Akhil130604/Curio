from guizero import App, PushButton, TextBox,Text



def show():
    text_box.show()
    yes_button.destroy()
    no_button.destroy()
    enter_button.show()
    intro.hide()
    text2.show()

def hide():
    text_box.hide()

def destroy():
    text_box.destroy()
    yes_button.destroy()
    no_button.destroy()
    
def save():
    txt=text_box.tk.get()
    print(txt)
    

    
app = App("Face recognition")
intro=Text(app,text="would you like to register new face")
text2=Text(app,text="Enter your name")
text2.hide()
text_box = TextBox(app)
text_box.hide()
yes_button = PushButton(app, text="Yes", command=show)
no_button = PushButton(app, text="No", command=destroy)
enter_button=PushButton(app,text="Enter",command=save)
enter_button.hide()

app.display()
