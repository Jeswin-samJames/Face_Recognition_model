import os
import dlib
import csv
import numpy as np
import logging
import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import shutil


#  Path of cropped faces
path_images_from_camera = "data/data_faces_from_camera/"

#  Use frontal face detector of Dlib
detector = dlib.get_frontal_face_detector()

#  Get face landmarks
predictor = dlib.shape_predictor('data/data_dlib/data_dlib/shape_predictor_68_face_landmarks.dat')

#  Use Dlib resnet50 model to get 128D face descriptor
face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/data_dlib/dlib_face_recognition_resnet_model_v1.dat")


#  Return 128D features for single image

def return_128d_features(path_img):
    img_rd = cv2.imread(path_img)
    faces = detector(img_rd, 1)

    logging.info("%-40s %-20s", " Image with faces detected:", path_img)

    # For photos of faces saved, we need to make sure that we can detect faces from the cropped images
    if len(faces) != 0:
        shape = predictor(img_rd, faces[0])
        face_descriptor = face_reco_model.compute_face_descriptor(img_rd, shape)
    else:
        face_descriptor = 0
        logging.warning("no face")
    return face_descriptor


#   Return the mean value of 128D face descriptor for person X

def return_features_mean_personX(path_face_personX):
    features_list_personX = []
    photos_list = os.listdir(path_face_personX)
    if photos_list:
        for i in range(len(photos_list)):
            #  return_128d_features()  128D  / Get 128D features for single image of personX
            logging.info("%-40s %-20s", " / Reading image:", path_face_personX + "/" + photos_list[i])
            features_128d = return_128d_features(path_face_personX + "/" + photos_list[i])
            #  Jump if no face detected from image
            if features_128d == 0:
                i += 1
            else:
                features_list_personX.append(features_128d)
    else:
        logging.warning(" Warning: No images in%s/", path_face_personX)

   
    if features_list_personX:
        features_mean_personX = np.array(features_list_personX, dtype=object).mean(axis=0)
    else:
        features_mean_personX = np.zeros(128, dtype=object, order='C')
    return features_mean_personX


def main():
    logging.basicConfig(level=logging.INFO)
    #  Get the order of latest person
    person_list = os.listdir("data/data_faces_from_camera/")
    person_list.sort()

    with open("data/features_all.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for person in person_list:
            # Get the mean/average features of face/personX, it will be a list with a length of 128D
            logging.info("%sperson_%s", path_images_from_camera, person)
            features_mean_personX = return_features_mean_personX(path_images_from_camera + person)

            if len(person.split('_', 2)) == 2:
                # "person_x"
                person_name = person
            else:
                # "person_x_tom"
                person_name = person.split('_', 2)[-1]
            features_mean_personX = np.insert(features_mean_personX, 0, person_name, axis=0)
            # features_mean_personX will be 129D, person name + 128 features
            writer.writerow(features_mean_personX)
            logging.info('\n')
        logging.info("Save all the features of faces registered into: data/features_all.csv")


if __name__ == '__main__':
    main()


def upload_image(self):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")])
    if file_path:
        # Display a message indicating that the image has been uploaded
        self.log_all["text"] = "Image uploaded: " + file_path
        
        # Create a directory for the current face (you can modify this logic if needed)
        self.current_face_dir = self.path_photos_from_camera + "person_" + str(self.existing_faces_cnt)
        os.makedirs(self.current_face_dir, exist_ok=True)
        
        # Copy the uploaded image to the current face directory
        shutil.copy(file_path, self.current_face_dir)

        # Now, you can choose to perform any additional actions on the uploaded image,
        # such as displaying it in your GUI or processing it in some way.
        # For example, you can display the uploaded image in your GUI like this:
        uploaded_image = Image.open(file_path)
        uploaded_image = uploaded_image.resize((200, 200), Image.ANTIALIAS)  # Resize if needed
        uploaded_image = ImageTk.PhotoImage(uploaded_image)
        
        # Create a label to display the uploaded image in your GUI
        self.uploaded_image_label = tk.Label(self.frame_right_info, image=uploaded_image)
        self.uploaded_image_label.grid(row=13, column=0, columnspan=3, padx=5, pady=2)
        self.uploaded_image_label.image = uploaded_image

        # You can also perform further processing on the uploaded image as needed.


