import tkinter as tk

import os
import cv2
import numpy as np
import time
import warnings 
from PIL import Image , ImageTk 
import matplotlib.image as mpimg

warnings.filterwarnings("ignore", category=DeprecationWarning)
from keras.models import load_model

#import CNNModel 

from win32com.client import Dispatch
speak = Dispatch("SAPI.SpVoice")

##############################################+=============================================================
image_x, image_y = 64, 64
basepath="E:\E:\Social Distance live camera"

##############################################+=============================================================
root = tk.Tk()
root.configure(background="red")
root.state('zoomed')
root.title("Social Distancing System")
#####################################################+
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
image2 =Image.open('img2.png')
image2 =image2.resize((w,h), Image.ANTIALIAS)

background_image=ImageTk.PhotoImage(image2)

background_label = tk.Label(root, image=background_image)

background_label.image = background_image

background_label.place(x=0, y=0) #, relwidth=1, relheight=1)
#


##########

label_l1 = tk.Label(root, text=" Sign Language Recognition Using Deep Learning On Custom Processed Gesture Image",
                    font=("Times New Roman", 25, 'bold'),
                    background="#E16666", fg="black", width=65, height=2)
label_l1.place(x=25, y=20)

############################################


frame_CP = tk.LabelFrame(root, text="-------------- Control Panel ------------------", width=300, height=250, bd=5, font=('times', 12, ' bold '),
                         bg="#29A6A6",fg="white")
frame_CP.grid(row=0, column=0, sticky='s')
frame_CP.place(x=10, y=150)

# frame_display = tk.LabelFrame(root, text=" ---WorkSpace--- ", width=1150, height=750, bd=5, font=('times', 12, ' bold '),bg="white",fg="red")
# frame_display.grid(row=0, column=0, sticky='s')
# frame_display.place(x=210, y=60)

# frame_noti = tk.LabelFrame(root, text=" Notification ", width=250, height=750, bd=5, font=('times', 12, ' bold '),bg="black",fg="white")
# frame_noti.grid(row=0, column=0, sticky='nw')
# frame_noti.place(x=300, y=60)

# ges_name =tk.StringVar()
# ges_name="Ges1"
# gesEL = tk.Entry(frame_CP, textvariable = ges_name)
# gesEL.place(x=25, y=100)
# gesEL.insert(0,'G1')

###########################################################################################################
#def clear_lbl():
    
 #   img11 = tk.Label(root, background='black',width=600,height=850)
  #  img11.place(x=0, y=0)

def update_label(str_T):
    result_label = tk.Label(root, text=str_T, font=("italic", 20),bg='red',fg='white',width=50 )
    result_label.place(x=400, y=150)
#    result_label.after(4000, lambda:result_label.config(text='') )
    
################################################################################################################
def create_folder(folder_name):
    if not os.path.exists('E:\Main_Sign_Recognition\Main_Sign_Recognition\Main_Sign_Recognition' +'/data/training_set/' + folder_name):
        os.mkdir('E:\Main_Sign_Recognition\Main_Sign_Recognition\Main_Sign_Recognition' + '/data/training_set/' + folder_name)
    if not os.path.exists('E:\Main_Sign_Recognition\Main_Sign_Recognition\Main_Sign_Recognition' + '/data/test_set/' + folder_name):
        os.mkdir('E:\Main_Sign_Recognition\Main_Sign_Recognition\Main_Sign_Recognition' + '/data/test_set/' + folder_name)
    
               
def capture_images(ges_name):
    create_folder(str(ges_name))
    
    cam = cv2.VideoCapture(0)

#    cv2.namedWindow("Sign Capture Window")

    img_counter = 0
    t_counter = 1
    training_set_image_name = 1
    test_set_image_name = 1
    listImage = [1,2,3,4,5]


    for loop in listImage:
        while True:

            ret, frame = cam.read()
            frame = cv2.flip(frame, 1)

            l_h = 0
            l_s = 0
            l_v = 0
            u_h = 179 
            u_s = 255
            u_v = 152 
            
            img = cv2.rectangle(frame, (425, 100), (625, 300), (0, 255, 0), thickness=2, lineType=8, shift=0)

            lower_blue = np.array([l_h, l_s, l_v])
            upper_blue = np.array([u_h, u_s, u_v])
            imcrop = img[102:298, 427:623]
            hsv = cv2.cvtColor(imcrop, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_blue, upper_blue)

#            result = cv2.bitwise_and(imcrop, imcrop, mask=mask)
            str_T="Please Capture your Sign by pressing << c >> Key" 
            cv2.putText(frame, str(str_T), (10, 30), cv2.FONT_HERSHEY_TRIPLEX, .6, (0, 0,0))
            
            str_T= "Press << s >> Key to Exit the window"

            cv2.putText(frame, str(str_T), (10, 50), cv2.FONT_HERSHEY_TRIPLEX, .6, (0, 0,0))


            str_T= "Please capture 2000 images for single Gesture "

            cv2.putText(frame, str(str_T), (10, 70), cv2.FONT_HERSHEY_TRIPLEX, .6, (0, 0,255))

            cv2.putText(frame, str(img_counter), (30, 400), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (127, 0, 255))
            cv2.imshow("Sign Capture Window", frame)
            cv2.imshow("Silhouettes Image", mask)
#            cv2.imshow("result", result)

            if cv2.waitKey(1) == ord('c'):

                if t_counter <= 350:
                    img_name = basepath + "/data/training_set/" + str(ges_name) + "/{}.png".format(training_set_image_name)
                    save_img = cv2.resize(mask, (image_x, image_y))
                    cv2.imwrite(img_name, save_img)
                    print("{} written!".format(img_name))
                    training_set_image_name += 1


                if t_counter > 350 and t_counter <= 400:
                    img_name = basepath + "/data/test_set/" + str(ges_name) + "/{}.png".format(test_set_image_name)
                    save_img = cv2.resize(mask, (image_x, image_y))
                    cv2.imwrite(img_name, save_img)
                    print("{} written!".format(img_name))
                    test_set_image_name += 1
                    if test_set_image_name > 250:
                        break


                t_counter += 1
                if t_counter == 401:
                    t_counter = 1
                img_counter += 1


            elif cv2.waitKey(1) == 27:
                cam.release()
                cv2.destroyAllWindows()
                break

        if test_set_image_name > 250:
            break


    cam.release()
    cv2.destroyAllWindows()

###################################################################################################################
def cap_webcam():
    
    update_label("Please Capture your Sign by pressing << c >> Key and Press << s >> Key to Exit the window")

  #  if len(gesEL.get()) == 0:
   #     clear_lbl()
    #    update_label("Please Enter Gesture Name!!")
     #   gesEL.focus_set()
   # else:
    #    capture_images(ges_name)

def train_sign():

    #clear_lbl()
    
    update_label("Model Training Start...............")
    
    start = time.time()

    X= CNNModel.main()
    
    end = time.time()
        
    ET="Execution Time: {0:.4} seconds \n".format(end-start)
    
    msg="Model Training Completed.."+'\n'+ X + '\n'+ ET

    update_label(msg)

      
#################################################################################################################
#################################################################################################################

def sign_recognize():
    
  #  clear_lbl()
    
#    update_label("Press << c >> for Gesture Detection with Voice")
    
    
    classifier = load_model('E:/Main_Sign_Recognition/Main_Sign_Recognition/Main_Sign_Recognition/SignR_model.h5')
    
    sentence = ['O:']    
    def predictor():
        import numpy as np
        from keras.preprocessing import image
        test_image = image.load_img(basepath + '/1.png', target_size=(64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result = classifier.predict(test_image)
        print(np.argmax(result))
        import numpy
        print(numpy.argmax(result))
        answer = {0: 'A', 1: 'B', 2: 'C', 3: 'D',
                  4: 'E',5: 'F',6: 'G',7: 'H',
                  8: 'I',9: 'J',10: 'K',11: 'L',
                  12: 'M',13: 'N',14: 'O', 15: 'P',
                  16: 'Q', 17: 'R', 18: 'S', 19:" ",
                  20: 'T', 21: 'U', 22: 'V', 23: 'W',
                  24: 'X', 25: 'Y',27: 'Z'}
        

        
        if numpy.argmax(result) in answer.keys():
            print("Present, ", end=" ")
            print("value =", answer[numpy.argmax(result)])
           # if cv2.waitKey(1) == ord('s'):
            sentence.append(answer[numpy.argmax(result)])
            print(''.join(sentence))
                
            return answer[numpy.argmax(result)]
        else:
            print("Not present")



    cam = cv2.VideoCapture(0)
#    update_label("Press << c >> for Gesture Detection with Voice")

    img_text = ''
    while True:
        ret, frame = cam.read()
        frame = cv2.flip(frame,1)
        #update_label("Press << c >> for Gesture Detection with Voice")

        l_h = 0
        l_s = 0
        l_v = 0
        u_h = 179 
        u_s = 255
        u_v = 152 
    
        img = cv2.rectangle(frame, (425,100),(625,300), (0,255,0), thickness=2, lineType=8, shift=0)
    
        lower_blue = np.array([l_h, l_s, l_v])
        upper_blue = np.array([u_h, u_s, u_v])
        imcrop = img[102:298, 427:623]
        hsv = cv2.cvtColor(imcrop, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        tense = ''.join(sentence[1:])
        
        cv2.putText(frame, img_text, (30, 400), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255, 0))
        cv2.putText(frame, str(tense), (30, 450), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255, 0))
        out="Output Recognized Text:"+str(tense)
        print(out)
        update_label(out)
        #esult_label1 = tk.Label(root, text=out, font=("italic", 50),justify=tk.LEFT, wraplength=200 ,bg='black',fg='white' )
        #result_label1.place(x=100, y=150)
        """
        if  not sentence:
            print('some')
            
        else:
            print('here')
            cv2.putText(frame, sentence, (30, 450), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255, 0))"""
        cv2.imshow("Sign Capture Window", frame)
        cv2.imshow("Silhouettes Image", mask)
        
        #if cv2.waitKey(1) == ord('c'):
            
        img_name = basepath + "/1.png"
        save_img = cv2.resize(mask, (image_x, image_y))
        cv2.imwrite(img_name, save_img)
    #    print("{} written!".format(img_name))
        img_text = predictor()
        speak.Speak(img_text)
        
        # if cv2.waitKey(1) == ord('c'):
        #     img_text = predictor()
        #     speak.Speak(str(tense))
            
        if cv2.waitKey(1) == ord('s'):
            cam.release()
            cv2.destroyAllWindows()
            break
            
#################################################################################################################

def window():
    root.destroy()

#################################################################################################################

#button1 = tk.Button(frame_CP, text=" Capture Sign Data ", command=cap_webcam,width=19, height=1, font=('times', 12, ' bold '),bg="white",fg="black")
#button1.place(x=5, y=50)

# button2 = tk.Button(frame_CP, text=" Train Sign Model ", command=train_sign,width=19, height=1, font=('times', 12, ' bold '),bg="white",fg="black")
# button2.place(x=5, y=150)
#Analysis Electricity Theft data
button3 = tk.Button(frame_CP, text=" Sign Reconition ", command=sign_recognize,width=19, height=1, font=('times', 15, ' bold '),bg="white",fg="black")
button3.place(x=15, y=50)


exit = tk.Button(frame_CP, text="Exit", command=window, width=19, height=1, font=('times', 15, ' bold '),bg="red",fg="white")
exit.place(x=15, y=130)



root.mainloop()