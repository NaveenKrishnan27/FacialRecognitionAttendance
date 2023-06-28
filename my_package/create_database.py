import face_recognition
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np
import os
from pathlib import Path as p
from datetime import datetime
from calendar import monthrange


class create_database:
    def func():
            filenames=filedialog.askopenfilenames(initialdir="./cseb22/database",title="select images", filetypes = (('jpeg files', '*.jpeg')
                                                                                                      ,('All files', '*.*')))
            print(type(filenames[0]))
            #make these dynamic inputs
            data="./cseb22/database/cseb22.bin"
            names="./cseb22/database/cseb.csv"
            meta_names="./cseb22/database/meta.txt"
            year=int((str(datetime.now())[0:4]))
            month=int((str(datetime.now())[5:7]))
            month_days= monthrange(year,month)[1]+1

            fp=open(data,"wb")
            fp1=open(names,"w")
            fp2=open(meta_names,"w")
            fp1.write('NAME')
            for i in range(1,month_days):
                fp1.write(',{}'.format(i))
            for filename in filenames:
                image=face_recognition.load_image_file(filename)
                enc=face_recognition.face_encodings(image,num_jitters=3)
                #text
                path=filename                
                i=len(path)-1
                while path[i]!='/':
                    if path[i]=='.':
                        j=i
                    i-=1
                path=path[i+1:j]
                fp2.writelines('{}\n'.format(len(path)))
                fp1.write('\n{}'.format(path))
                for i in range(1,month_days):
                    fp1.write(',  ')
                
                #binary
                s=enc[0].tobytes()
                fp.write(s)
            print("database created")
            fp.close()
            fp1.close()
            fp2.close()

    
    #fp.read(1023)
    
    #print(face_recognition.compare_faces(enc,enc1,tolerance=0.6))
    #print(enc1)
