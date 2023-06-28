import tkinter as tk
import requests

import tkinter as tk
import face_recognition
from PIL import Image,ImageTk,ImageDraw
from TkinterDnD2 import DND_FILES,TkinterDnD
from tkinter import filedialog
import numpy as np
from datetime import datetime

from my_package import create_database as cd


#global img, count,knowns_name,knowns,count1,img2
global face_encodings
face_encodings=[]
img=[]
img2=[]
knowns_name=[]
knowns=[]
count=0
count1=0
def refresh_grp():
    global face_encodings,face_locations,count1,img2
    count1=0
    img2=[]
    face_encodings={}
    face_locations={}

def drop_grp_photo(event):
    global face_encodings,face_locations,group_image
    group_image=face_recognition.load_image_file(event.data)
    face_locations=face_recognition.face_locations(group_image, number_of_times_to_upsample=1)
    face_encodings=face_recognition.face_encodings(group_image,face_locations)
        
    #GUI
    global count1,img2
    im= (Image.open(event.data))
    resized_im= im.resize((600,400), Image.ANTIALIAS)
    img2.append( ImageTk.PhotoImage(resized_im) )
    gtextb.image_create("current", image=img2[count1])
    count1+=1

def start_finding():
    #retrieve all student encoding from database
    fp=open("./cseb22/database/cseb22.bin","rb")
    read_data=fp.read(1024)
    enc=[]
    while read_data:
        enc.append(np.frombuffer(read_data,dtype=np.float64))
        read_data=fp.read(1024)
        
    #update attendance
    excel='./cseb22/database/cseb.csv'
    meta='./cseb22/database/meta.txt'
    fp=open(excel,'r+')
    m_data=open(meta,"r")
    i=0
    fp.seek(0,0)
    curr_date=str(datetime.now())[8:10]
    curr_date=int(curr_date)-1
    x=0
    fp.readline()
    for en in enc:
        #less efficient due to ease in excel according to roll_no
        matches=face_recognition.compare_faces(face_encodings,en,tolerance=0.5)
        #placing file pointers at appropriate place
        a=m_data.readline()
        a=int(a)
        t=fp.tell()
        s=fp.readline()
        count=a+1+(curr_date)*3
        fp.seek(t)
        if True in matches:
            fp.write(s[0:count+1]+'P'+s[count+2:len(s)])
        else:
            fp.write(s[0:count+1]+'AB'+s[count+3:len(s)])
            
    fp.close()
    m_data.close()
    print("attendance updated")
            
HEIGHT = 500
WIDTH = 800

w=TkinterDnD.Tk()
w.title("Face Recogniton for MGNREGA")
root = tk.Frame(w, height=HEIGHT, width=WIDTH)
root.pack()


background_image = tk.PhotoImage(file='BG2.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)


#background_label = tk.Label(root, image=background_image)
#background_label.place(relwidth=1, relheight=1)

#lower_frame = tk.Frame(background_label, bg='#541690', bd=2)
rame = tk.Frame(background_label, bd=4,height=HEIGHT, width=WIDTH)
rame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.6, anchor='n')
gtextb=tk.Text(rame,height=HEIGHT, width=WIDTH)
gtextb.pack()

lower_frame = tk.Frame(root, bg='#541690', bd=5)
lower_frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.6, anchor='n')

frame = tk.Frame(background_label, bg='#541690', bd=2)
frame.place(relx=0.5, rely=0.73, relwidth=0.75, relheight=0.1, anchor='n')

button2 = tk.Button(frame, text="Create Database", font=60)
button2.place(relx=0.31, relheight=1, relwidth=0.69)
button1 = tk.Button(frame, text="Scan", font=60)
button1.place(relx=0,relheight=1,relwidth=0.3)



label = tk.Label(lower_frame)
label.place(relwidth=1, relheight=1)

button1.config(command=start_finding)
button2.config(command=cd.create_database.func)

#refresh button 2
icon=Image.open('refresh.png')
icon=icon.resize((10,10),Image.ANTIALIAS)
icon=ImageTk.PhotoImage(icon)
refresh_button0 = tk.Button(root,image=icon,command=refresh_grp)
refresh_button0.place(x=624,y=20)

gtextb.drop_target_register(DND_FILES)


gtextb.dnd_bind("<<Drop>>", drop_grp_photo)



w.mainloop()

