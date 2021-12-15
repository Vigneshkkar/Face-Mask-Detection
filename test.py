import requests
import json

serverToken = 'AAAAO5T7NUo:APA91bFj3mgtfeVJUp8OM7AqVOXhvPMTjbWJpncUnD2f3jXEkxDXh3F5eBqRvxTMFyUopxQOa-kcALIiNNrjdXN4RqZzuxTF0qXhgw2OnJcTqVWPtT_qVcV_1Cbj02rWHff0w3Y90O-5'
deviceToken = 'dMYdDuEwMFtJ58w_L42fv-:APA91bESoIFbnmG-6bkLN6a0VFqHCMhQ8YPndtAz1snjTpoGnTKjFkrPBr9K6pxck3uJDkZzkHjVXgOTZFITZ9alixSPelkIoiCfTeQkvoa4uXDnl88ssWvbko92Q-MvIzGZVSffaA9z'

headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + serverToken,
      }

body = {
          'notification': {'title': 'Alert Hight Risk',
                            'body': 'A Person Entered the Store without Mask.',
                            },
          "topic": "Alert",
          'priority': 'high',
        #   'data': dataPayLoad,
        }
def send_alert():
    response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
    print(response.status_code)

    print(response.json())









import cv2
import numpy as np
from tensorflow.keras.models import load_model
from time import time
model=load_model("./model2-019.model")

results={0:'without mask',1:'mask'}
GR_dict={0:(0,0,255),1:(0,255,0)}

rect_size = 4
cap = cv2.VideoCapture(0) 


haarcascade = cv2.CascadeClassifier('/Users/vigneshkkar/opt/anaconda3/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_alt.xml')

check_alert = False
alert_sent = False

time_diff = time()

while True:
    (rval, im) = cap.read()
    im=cv2.flip(im,1,1) 

    
    rerect_size = cv2.resize(im, (im.shape[1] // rect_size, im.shape[0] // rect_size))
    faces = haarcascade.detectMultiScale(rerect_size)
    for f in faces:
        (x, y, w, h) = [v * rect_size for v in f] 
        
        face_img = im[y:y+h, x:x+w]
        rerect_sized=cv2.resize(face_img,(150,150))
        normalized=rerect_sized/255.0
        reshaped=np.reshape(normalized,(1,150,150,3))
        reshaped = np.vstack([reshaped])
        result=model.predict(reshaped)

        
        label=np.argmax(result,axis=1)[0]
      
        cv2.rectangle(im,(x,y),(x+w,y+h),GR_dict[label],2)
        cv2.rectangle(im,(x,y-40),(x+w,y),GR_dict[label],-1)
        cv2.putText(im, results[label], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
        
        if(label == 1):
            check_alert =  False
            alert_sent = False
        if(label == 0 and check_alert == False):
            check_alert = True
            time_diff = time()
        if(int(time() - time_diff) > 5 and check_alert and alert_sent == False):
            send_alert()
            check_alert = False
            alert_sent = True
            
    cv2.imshow('Face Mask Detection',   im)
    key = cv2.waitKey(10)
    
    if key == 27: 
        break

cap.release()

cv2.destroyAllWindows()


