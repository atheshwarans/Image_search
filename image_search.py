import PIL
import zipfile
from PIL import ImageDraw
from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np

def func(name,fileName):  
    #name is the keyword to be searched for
    #fileName is the name of the zip archive containing images with captions
    
    # Opens a zip file for reading and returns a file descriptor to it
    z=zipfile.ZipFile(fileName,'r')
    
    #Getting the names of all the files in the zip archive 
    zl=z.namelist()
    
       
    for i in zl:
        #Extracting image file present in the zip archive
        photo = z.extract(i)   
        
        #Converts all the text seen in the image file to string
        pgTxtCntnt = pytesseract.image_to_string(photo)
        
        if name in pgTxtCntnt:
            print('Results found in file ',photo)
            
            #Opening the image file using imread function of OpenCV for detecting faces in the image
            img = cv.imread(photo)
            
            #Converting the image to grayscale for better detection
            imgGray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
            
            #Initialising the haar cascade classifier for detecting faces
            face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
            
            #Using the cascade classifier to detect faces in the image which had been converted to gray scale
            #The below function returns the faces detected as a list of rectangular dimensions
            faces_rect = face_cascade.detectMultiScale(imgGray,1.35)
            
            
            #Opening the image using pillow module for cropping the faces recognised (based on caption) and creating a contactsheet using that
            img = Image.open(photo)
            
            #For seeing the region of interest within an outlined box
            #obj=ImageDraw.Draw(img)
            #obj.rectangle((51,39,177,165),outline='yellow')
            
            #Initialising list to store the images by resizing them to the required dimensions
            images=[]
            for face_rect in faces_rect:
                
                #Initialising the dimensions for cropping based on the rectangular dimensions returned by the classsifier
                x,y,w,h = face_rect
                
                #Cropping the faces based on the dimensions
                imgCrpped = img.crop((x,y,x+w,y+h))
                
                #For seeing the region of interest within an outlined box
                #obj.rectangle((x,y,x+w,y+h),outline='red')
                
                #Appending the images to the images list after resizing to the required size
                images.append(imgCrpped.resize((126,126)))

            
            l=len(images)
            
            #Conditional to check if faces have been found by
            if l!=0:
                # Creating an empty contact sheet for pasting the images of faces found (based on caption)
                contact_sheet=PIL.Image.new(img.mode,(630,int(np.ceil(l/5))*126))
                
                #For debugging
                #display(img)
                
                #Setting the initial coordinates to origin which is upper left corner in our case
                x=0
                y=0
                #Iterating through the images list and pasting the images in the contact sheet
                for image in images:
                    contact_sheet.paste(image,(x,y))
                    
                    #Checking if current row is filled and moving onto the next row
                    if x+126==630:
                        x=0
                        y+=126
                    else:
                        x+=126
                        
                #Displaying the contact sheet conataining the faces recognised based on the caption
                display(contact_sheet)
            else:
                print('There are no faces in the file!')
