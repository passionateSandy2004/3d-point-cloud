import streamlit as st 
import frameMaker as fm 
import os 
import converter as ct

def deletePics(folder_name):
    try:
        # Get the list of files in the folder
        files = os.listdir(folder_name)
        
        # Iterate over the files and delete them
        for file_name in files:
            file_path = os.path.join(folder_name, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
        
        print("All files deleted successfully.")
    except Exception as e:
        print(f"Error deleting files: {e}")

vid=st.file_uploader("Enter the video file",type=['mp4', 'jpeg', 'jpg', 'png'])

def save_file(uploaded_file, folder):
    st.write(vid.type)
    if not os.path.exists(folder):
        os.makedirs(folder)
    if folder=='video':
        file_path = os.path.join(folder, 'video.mp4')
    else:
        file_path = os.path.join(folder, '1.png')
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

if vid:
    deletePics('images')
    if vid.type=='video/mp4':
        deletePics('video')
        save_file(vid,'video')
        fm.Start()
    else:
        save_file(vid,'images')
    ct.convert()
    no_file = len(os.listdir('depth'))
    cols=st.columns(no_file)
    n=1
    for i in cols:
        i.image(f"depth/{n}.png")
        i.image(f"images/{n}.png")
        n+=1
    folder_path = 'cloud'
    file_contents = {}
    for filename in os.listdir(folder_path):
        with open(os.path.join(folder_path, filename), 'rb') as file:
            file_contents[filename] = file.read()
            st.write(filename)
            
    # Create a download button for each file
    for filename, content in file_contents.items():
        st.download_button(f'Download {filename}', content, file_name=filename, mime=None)

        
