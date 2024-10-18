import streamlit as st
import csv
import ai
import os
from tkinter import *
import tkinter.filedialog
import tkinter as tk
import pandas as pd
import shutil

csv_file_path = os.path.dirname(os.getcwd()) + "\\" + "images/processedimages/data.csv"

with st.sidebar:
    st.write('Choose a folder:')
    browse_button = st.button('Browse Files')

    if browse_button:
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        current_directory = str(tk.filedialog.askdirectory(master=root))

        # Filter image files
        image_extensions = ('.jpg', '.png')
        images = [file for file in os.listdir(current_directory) if file.lower().endswith(image_extensions)]
        print(images)
        print(current_directory)
        output = pd.DataFrame({"Folder Name": images})

        # Copy selected images to a different directory
        for image in images:
            source_path = os.path.join(current_directory, image)
            destination_path = os.path.join("..\images", image)
            print(f"Source Path: {source_path}")
            print(f"Destination Path: {destination_path}")
            shutil.copyfile(source_path, destination_path)

request = st.text_input("Enter your request:", placeholder="2 cats")
worker_amount = st.slider('Choose number of workers()', max_value=10, min_value= 1)
threshold = st.number_input('Choose the threshold', max_value=1.0, min_value= 0.0, step = 0.1)
if st.button("Search"):
    target_directory = os.path.join(os.path.dirname(os.getcwd())+ "\\photoshelf\\", "results", request)
    if not os.path.exists(str(target_directory)):
        os.makedirs(target_directory)
    result = ai.result(request,worker_amount,threshold)
    print(result)
    for img in result:
        print(img)
        splitted = img.split("\\")
        img_file_name = splitted[-1]
        destination_path = os.path.join(target_directory,img_file_name)
        source_path = os.path.join(os.path.dirname(os.getcwd()) + "\\photoshelf\\", "images", img_file_name)
        print(f"Source Path: {source_path}")
        print(f"Destination Path: {destination_path}")
        shutil.copyfile(source_path, destination_path)




