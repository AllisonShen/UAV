import pandas as pd
import numpy as np
import os
import glob
import sys

from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit

from natsort import natsorted # pip install natsort # used for sort str+num
import math

from absl import flags, app
from absl.flags import FLAGS

import shutil

#method two: train_test_split
flags.DEFINE_string('path_images', '', 'path to dataset')
flags.DEFINE_string('path_csv', '', 'path to csv')

flags.DEFINE_string('path_csv_output', '', 'path to csv')
flags.DEFINE_string('path_train', 'None', 'path to train')
flags.DEFINE_string('path_val', 'None', 'path to val')
flags.DEFINE_string('yolo_labels', 'None', 'path to train')
flags.DEFINE_string('yolo_labels_train', 'None', 'path to train')
flags.DEFINE_string('yolo_labels_val', 'None', 'path to val')
flags.DEFINE_float('test_size', 0.2, 'path to csv')

def create_train_val_csv():
  df = None
  grouped = None
  df = pd.read_csv(FLAGS.path_csv)
  df = df.dropna()
  grouped = df.groupby('filename')
  # print(grouped.head())
  grouped = df.groupby('filename').first()
  # print(grouped.head()) #filename becomes index


  print(f"grouped: tag==1: {sum(grouped['tag'])}, tag==0: {len(grouped['tag'])-sum(grouped['tag'])}")

  train, test = train_test_split(grouped, test_size=FLAGS.test_size, shuffle = True, stratify = grouped['class']) #, stratify = df['class']
  print(f"len of train (# images): {len(train)}")
  print(f"train: tag==1: {sum(train['tag'])}, tag==0: {len(train['tag'])-sum(train['tag'])}")

  print(f"len of test (# images): {len(test)}")
  print(f"test: tag==1: {sum(test['tag'])}, tag==0: {len(test['tag'])-sum(test['tag'])}")
  
  train_filename = train.index.tolist()
  print(f"train images: {len(train_filename)}")
  test_filename = test.index.tolist()
  print(f"test_images: {len(test_filename)}")

  train = df[df['filename'].isin(train_filename)]
  test = df[df['filename'].isin(test_filename)]


  print(f"len of train (#rows): {len(train)}")
  print(train.head(100))
  print(f"len of test (#rows): {len(test)}")
  print(test.head(100))
  os.makedirs(FLAGS.path_csv_output, exist_ok=True)
  os.makedirs(FLAGS.path_csv_output, exist_ok=True)



  filenameTrain = f"{FLAGS.path_csv_output}/train_labels.csv"
  filenameTest = f"{FLAGS.path_csv_output}/test_labels.csv"

  train.to_csv(filenameTrain, index=False, header= True)
  test.to_csv(filenameTest, index=False, header= True)
  return filenameTrain, filenameTest

def copy_image(path_csv, old_path, new_path):
  df = pd.read_csv(path_csv)
  images_names = df['filename'].unique().tolist()
  for image_name in images_names:
    old_image_path = f"{old_path}/{image_name}"
    # print(old_image_path)
    new_image_path = f"{new_path}/{image_name}"
    # print(new_image_path)
    shutil.copy2(old_image_path, new_image_path) # complete target filename given
def copy_labels(path_csv, old_path, new_path):
  df = pd.read_csv(path_csv)
  images_names = df['filename'].unique().tolist()
  for image_name in images_names:
    old_image_path = f"{old_path}/{image_name[:-4]}.txt"
    # print(old_image_path)
    new_image_path = f"{new_path}/{image_name[:-4]}.txt"
    # print(new_image_path)
    shutil.copy2(old_image_path, new_image_path) # complete target filename given




def main(_argv):
  path_train_csv, path_test_csv = create_train_val_csv()
  if((FLAGS.path_train and FLAGS.path_val)!= 'None'):
    print("copy images to train and val folders")
    if os.path.exists(FLAGS.path_train) and os.path.isdir(FLAGS.path_train):
      shutil.rmtree(FLAGS.path_train)
    if os.path.exists(FLAGS.path_val) and os.path.isdir(FLAGS.path_val):
      shutil.rmtree(FLAGS.path_val)
    if os.path.exists(FLAGS.yolo_labels_train) and os.path.isdir(FLAGS.yolo_labels_train):
      shutil.rmtree(FLAGS.yolo_labels_train)
    if os.path.exists(FLAGS.yolo_labels_val) and os.path.isdir(FLAGS.yolo_labels_val):
      shutil.rmtree(FLAGS.yolo_labels_val)
    # print(FLAGS.path_train)
    # print(FLAGS.path_val)
    # isExist = os.path.exists(FLAGS.path_train)
    #   if not isExist:
    #       os.makedirs(FLAGS.path_train)
    os.makedirs(FLAGS.path_train, exist_ok=True)
    os.makedirs(FLAGS.path_val, exist_ok=True)
    os.makedirs(FLAGS.yolo_labels_train, exist_ok=True)
    os.makedirs(FLAGS.yolo_labels_val, exist_ok=True)

    copy_image(path_train_csv,FLAGS.path_images, FLAGS.path_train)
    copy_image(path_test_csv,FLAGS.path_images, FLAGS.path_val)
    copy_labels(path_train_csv,FLAGS.yolo_labels, FLAGS.yolo_labels_train)
    copy_labels(path_test_csv,FLAGS.yolo_labels, FLAGS.yolo_labels_val)
if __name__ == '__main__':
  try:
      app.run(main)
  except SystemExit:
      pass
