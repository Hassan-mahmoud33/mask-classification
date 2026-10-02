import cv2
import numpy as np
from tensorflow.keras.models import load_model

model = load_model('../models/mask_best_model.keras')

cap = cv2.VideoCapture(0)


while cap.isOpened():

    ret , frame = cap.read()

    if not ret :
        break

    input_frame = cv2.cvtColor( frame , cv2.COLOR_BGR2RGB )
    input_frame = cv2.resize( input_frame , ( 224 , 224  ))
    input_frame = np.expand_dims( input_frame , axis= 0 )

    results = model.predict( input_frame )
    label = ( 1 if results[0][0] >= 0.50 else 0 )

    if label == 1 :
        cv2.putText( frame , 'With Mask' , ( 100 , 70 ) , cv2.FONT_ITALIC , 
                    2 , ( 0 , 255 , 0 ) , 5 )
    else:
        cv2.putText( frame , 'No Mask' , ( 100 , 70 ) , cv2.FONT_ITALIC , 
            2 , ( 0 , 0 , 255 ) , 5 )
        cv2.putText( frame , "Put A Mask" , ( 10 , 120 ) , cv2.FONT_HERSHEY_SIMPLEX , 
            2 , ( 0 ,240 , 0 ) , 5 )
        


    cv2.imshow('Frame' , frame )
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break


cap.release()
cv2.destroyAllWindows()