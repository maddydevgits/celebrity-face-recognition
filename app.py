import streamlit as st
from PIL import Image
import os
import boto3

accessKey='' # ask admin to share access key
secretAccessKey='' # ask admin to share secret access
region='us-east-1'

st.title('Celebrity Face Recognition')

img_file=st.file_uploader('Upload celebrity face',type=['png','jpg','jpeg'])

def load_img(img):
    img=Image.open(img)
    return img

if img_file is not None:
    file_details={}
    file_details['name']=img_file.name
    file_details['size']=img_file.size
    file_details['type']=img_file.type
    st.write(file_details)
    st.image(load_img(img_file),width=255)

    with open(os.path.join('uploads','src.jpg'),'wb') as f:
        f.write(img_file.getbuffer())
    
    st.success('Image Saved')
    client=boto3.client('rekognition',aws_access_key_id=accessKey,aws_secret_access_key=secretAccessKey,region_name=region)
    image=open('uploads/src.jpg','rb')
    response=client.recognize_celebrities(Image={'Bytes': image.read()})
    #st.write(response)
    try:
        st.success(response['CelebrityFaces'][0]['Name'])
        st.warning(response['CelebrityFaces'][0]['Urls'][0])
    except:
        st.error('No Celebrity Found')

    
