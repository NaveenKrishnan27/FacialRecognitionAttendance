import tkinter as tk
import requests

HEIGHT = 500
WIDTH = 600


root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

background_image = tk.PhotoImage(file='BG2.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

lower_frame = tk.Frame(root, bg='#541690', bd=5)
lower_frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.6, anchor='n')

frame = tk.Frame(root, bg='#541690', bd=5)
frame.place(relx=0.5, rely=0.73, relwidth=0.75, relheight=0.1, anchor='n')

button = tk.Button(frame, text="Create Database", font=60)
button.place(relx=0.31, relheight=1, relwidth=0.69)
button = tk.Button(frame, text="Scan", font=60)
button.place(relx=0,relheight=1,relwidth=0.3)



label = tk.Label(lower_frame)
label.place(relwidth=1, relheight=1)



root.mainloop()
