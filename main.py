 
from gtts import gTTS
import pygame
from pygame import mixer
from PIL import Image
import pytesseract
import os
import glob
import PySimpleGUI as sg
import tkinter as tk
import fitz


 
def get_text(value):

    string = value
    string = string.strip()
    if "-" in string:
        first_page_number = int(string.split("-")[0])
        last_page_number = int(string.split("-")[1])
    else:
        first_page_number = int(string)
        last_page_number = 0

    return first_page_number,last_page_number

def main():
    global e,first_page_number,last_page_number
     
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory,r'Text_to_speech_software')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    print(current_directory)
    print(final_directory)

    # GUI

     
    layout = [  [sg.Text('Choose PDF File to read'),sg.Input(),sg.FileBrowse()],
                [sg.Text('Enter PDF Page number or range separated by - '), sg.InputText()],
                [sg.Button('Ok'), sg.Button('Cancel')]
            ]
 
    window = sg.Window('Input', layout)
    valid = False
   
    while True:
        event, values = window.read()
         
        pdf_to_read = values[0]

        if event in (None, 'Cancel'):	 
            print("Exitting")
            window.close()
            exit()

        if event == "Ok":

            if values[0] == "":
                sg.Popup("Enter value", "Enter PDF file to be transcribed ")
            if values[1] == "":
                sg.Popup("Enter value", "Enter page number(s) to be transcribed")

            if values[0]!="" and values[1]!="":
                for char in values[1]:
                    if char.isdigit()==False:
                        sg.Popup("Invalid value","Enter valid number or numbers separated by -")
                        break
                    else:
                        valid=True
                        break
         
        if valid==True:
            print('You entered ', values[1])
            break

    window.close()
    first_page_number,last_page_number = get_text(values[1])

     
    image_directory = glob.glob(final_directory)
    for file in os.listdir(final_directory):
        filepath = os.path.join(final_directory,file)
        print(filepath)
        os.chmod(filepath, 0o777)
        os.remove(filepath)

 
    doc = fitz.open(pdf_to_read)
    k=1
    
    if last_page_number == 0:
        page = doc.loadPage(first_page_number-1) #number of page
        zoom_x = 2.0
        zoom_y = 2.0
        mat = fitz.Matrix(zoom_x,zoom_y)
        pix = page.getPixmap(matrix=mat)
        output = os.path.join(final_directory, r"image_to_read.png")
        pix.writePNG(output)

     
    else:
        for i in range(first_page_number-1,last_page_number):
            page = doc.loadPage(i) #number of page
            zoom_x = 2.0
            zoom_y = 2.0
            mat = fitz.Matrix(zoom_x,zoom_y)
            pix = page.getPixmap(matrix=mat)
            output = os.path.join(final_directory, r"image_"+str(k)+"_to_read.png")
            pix.writePNG(output)
            k+=1

    print("Done")

  


    mytext = []

   
    for file in os.listdir(final_directory):
        data = pytesseract.image_to_string(Image.open(os.path.join(final_directory,file)),lang="eng")
        data = data.replace("|","I") # For some reason the image to text translation would put | instead of the letter I. So we replace | with I
        data = data.split('\n')
        mytext.append(data)


   
    language = 'en'

    print(mytext)

    

    newtext= ""
    for text in mytext:
        for line in text:
            line = line.strip()
            
            if len(line.split(" ")) < 10 and len(line.split(" "))>0:
                newtext= newtext + " " + str(line) + "\n"

            elif len(line.split(" "))<2:
                pass
            else:
                if line[-1]!=".":
                    newtext = newtext + " " + str(line)
                else:
                    newtext = newtext + " " + line + "\n"

    print(newtext)

     
    myobj = gTTS(text=newtext, lang=language, slow=False)

     
    myobj.save(os.path.join(final_directory,"pdf_audio.mp3"))
 
    pygame.init()
    mixer.init()
    mixer.music.load(os.path.join(final_directory,"pdf_audio.mp3"))
    mixer.music.play()
    pygame.event.wait()

 
if __name__ == '__main__':
    main()
