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
            

root = TkinterDnD.Tk()
root.geometry("700x880")
#root.minsize(700,880)
#root.maxsize(700,880)





#create scrollbar
my_frame1=tk.Frame(root)
my_frame1.grid(row=0,column=0)
text_scroll1 = tk.Scrollbar(my_frame1)
text_scroll1.pack(side=tk.RIGHT,fill=tk.Y)
#horizonral scroll bar
text_scroll1x=tk.Scrollbar(my_frame1,orient=tk.HORIZONTAL)
text_scroll1x.pack(side=tk.TOP,fill=tk.X)
gtextb = tk.Text(my_frame1,yscrollcommand=text_scroll1.set,xscrollcommand=text_scroll1x.set)
gtextb.pack(fill=tk.X)

text_scroll1.config(command=gtextb.yview)
text_scroll1x.config(command=gtextb.xview)

#refresh button 2
icon=Image.open('refresh.png')
icon=icon.resize((10,10),Image.ANTIALIAS)
icon=ImageTk.PhotoImage(icon)
refresh_button0 = tk.Button(root,image=icon,command=refresh_grp)
refresh_button0.place(x=624,y=20)

gtextb.drop_target_register(DND_FILES)


gtextb.dnd_bind("<<Drop>>", drop_grp_photo)

#create dataase button
button = tk.Button(root,text='Create database')
button.config(command=cd.create_database.func) #performs call back of function
button.config(font=('Helvetica',14,'bold'),padx=0,pady=0)
button.config(bg='red')
button.config(fg='white')
button.config(activebackground='#FF0000')
button.config(activeforeground='#fffb1f')
button.place(x=200,y=420)

#avan code
button = tk.Button(root,text='Mark')
button.config(command=start_finding) #performs call back of function
button.config(font=('Helvetica',14,'bold'),padx=0,pady=0)
button.config(bg='red')
button.config(fg='white')
button.config(activebackground='#FF0000')
button.config(activeforeground='#fffb1f')
button.place(x=570,y=420)


root.mainloop()
