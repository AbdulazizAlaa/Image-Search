from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from multiprocessing import Process
import os
import shutil
import sys
import numpy as np
import cv2


def augment(images_dir, num_iter_per_image=20, npy_file='face_images.npy'):
    #data generator for augmentating images
    datagen = ImageDataGenerator(
                rotation_range=360,
                width_shift_range=0.2,
                height_shift_range=0.2,
                shear_range=0.2,
                zoom_range=0.4,
                horizontal_flip=True,
                vertical_flip=True,
                fill_mode='nearest')

    #getting dir and num iter per image from arguments
    folder = images_dir
    num = num_iter_per_image

    print ("num of iter per image:", num)

    #folder to save the output of the augmentation
    augmented_dir = folder+'_augmented_'+str(num)
    if not os.path.exists(augmented_dir):
        os.makedirs(augmented_dir)

    #iterating on subfolders in the images folder
    jobs = []
    for subfolder in os.listdir(folder):
        jobs.append(Process(target=do_augmentation, args=(datagen, folder, subfolder, augmented_dir, num)))

    for j in jobs:
        j.start()

    for k in jobs:
        k.join()

    images, labels = read_images(augmented_dir, folder, npy_file)

    return [images, labels]

def read_images(augmented_dir, folder, npy_file):
    # reading images
    images = []
    labels = []
    i = 0
    for subfolder in os.listdir(augmented_dir):
        if not "." in subfolder: #checking it is not a file
            # print(subfolder)
            for filename in os.listdir(augmented_dir+"/"+subfolder):
                # print(filename)
                img = cv2.imread(augmented_dir+"/"+subfolder+"/"+filename)

                images.append(img)
                labels.append(i)

            i=i+1

    # reading npy file of images and appending to new images
    loaded_images = []
    if(os.path.exists(folder+'/'+npy_file)):
        [loaded_images, loaded_labels]  = np.load(folder+'/'+npy_file)
        images.extend(loaded_images)
        labels.extend(loaded_labels)
        print("Loaded")

    print('-----------------')
    print('num images: ', len(images))
    print('-----------------')

    # saving new images
    np.save(folder+'/'+npy_file, [images, labels])

    # deleting augmented images folder
    shutil.rmtree(augmented_dir)
    print('remove Augmented Tree')
    print('-----------------')


    for subfolder in os.listdir(folder):
        if not "." in subfolder: #checking it is not a file
            for filename in os.listdir(folder+"/"+subfolder):
                os.remove(folder+"/"+subfolder+'/'+filename)


    print('remove original files')
    print('-----------------')

    return [images, labels]


def do_augmentation(datagen, folder, subfolder, augmented_dir, num):
    save_prefix = 'person_'+subfolder #save prefix for images
    save_dir = augmented_dir+'/'+subfolder #save directory for this subfolder images

    print(subfolder)

    if not "." in subfolder: #checking it is not a file
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        for filename in os.listdir(folder+"/"+subfolder):
            # print(filename)
            # load image
            img = load_img(folder+"/"+subfolder+"/"+filename)
            x = img_to_array(img)
            x = x.reshape((1,) + x.shape)

            i = 0
            for batch in datagen.flow(x, batch_size=1, save_to_dir=save_dir, save_prefix=save_prefix, save_format='jpeg'):
                i += 1
                if i > num:
                    break

    # return
