import streamlit as st
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import cv2



model = load_model('models/mask_best_model.keras')

st.title('Mask Classification')

uploaded = st.file_uploader('Put An Image', type=['jpg' , 'jpeg' , 'png'])

if uploaded is not None :

    img = Image.open( uploaded )
    img = img.resize((224 , 224))
    img = np.array(img)

    img = np.expand_dims( img , axis= 0 )

    st.image( img )


if st.button('Predict'):

    prediction = model.predict(img, verbose=0)

    probability = float(prediction[0][0])

    if probability >= 0.50:
        result = 'With Mask'
        confidence = probability
    else:
        result = 'Without Mask'
        confidence = 1 - probability

    st.write(f'Prediction: {result}')
    st.write(f'Confidence: {confidence * 100:.2f}%')
