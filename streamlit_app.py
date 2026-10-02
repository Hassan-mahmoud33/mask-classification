import streamlit as st
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import cv2



model = load_model('../models/mask_best_model.keras')

st.title('Mask Detection')

uploaded = st.file_uploader('Put An Image', type=['jpg' , 'jpeg' , 'png'])

if uploaded is not None :

    img = Image.open( uploaded )
    img = img.resize((224 , 224))
    img = np.array(img)

    img = np.expand_dims( img , axis= 0 )

    st.image( img )


    if st.button('Predict') :

        prediction = model.predict( img )
        result = [ 'With Mask' if prediction >= 0.50 else 'Without Mask']

        st.write(f'Prediction: {result[0]}' )
        st.write(f'Confidance: {np.round( prediction[0][0] , 2 )}%' )