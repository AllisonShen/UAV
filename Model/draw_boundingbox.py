import os
import time
import sys
import yaml
import numpy as np
import pandas as pd
from absl import flags, app
from absl.flags import FLAGS

from matplotlib import pyplot
from matplotlib.patches import Rectangle



flags.DEFINE_string('dataset_images', '', 'path to dataset')
flags.DEFINE_string('annotation_csv', '', 'path to annotation')
flags.DEFINE_string('path_output', 'None', 'path to output')
flags.DEFINE_string('type_dataset', 'voc', 'dataset format, can be yolo, voc, json')
flags.DEFINE_string('printImage', 'True', 'if printing image')



def convert_yolo_coordinates_to_voc(x_c_n, y_c_n, width_n, height_n, img_width, img_height):
  ## remove normalization given the size of the image
  x_c = float(x_c_n) * img_width
  y_c = float(y_c_n) * img_height
  width = float(width_n) * img_width
  height = float(height_n) * img_height
  ## compute half width and half height
  half_width = width / 2
  half_height = height / 2
  ## compute left, top, right, bottom
  ## in the official VOC challenge the top-left pixel in the image has coordinates (1;1)
#   left = int(x_c - half_width) + 1 #xmin
#   top = int(y_c - half_height) + 1 #ymin
#   right = int(x_c + half_width) + 1 #xmax
#   bottom = int(y_c + half_height) + 1 #ymax
  xmin = int(x_c - half_width) + 1 #xmin
  ymin = int(y_c - half_height) + 1 #ymin
  xmax = int(x_c + half_width) + 1 #xmax
  ymax = int(y_c + half_height) + 1 #ymax
#   return left, top, right, bottom
  return ymin, xmin, ymax, xmax
  
def draw_bounding_box_resize(image_name,pathResizeImages,df, printImage = True,output_path= None, type_dataset = "voc"):
  pathDataset = pathResizeImages
  print(f"<<<<<<<<<drawing bounding box for {image_name}>>>>>>>>")
  filename = f"{pathDataset}/{image_name}"
  data = pyplot.imread(filename)
  pyplot.imshow(data)
  ax = pyplot.gca()
  # plot each box
  allLinesSameImage = df[df.filename == image_name]
  for i, row in allLinesSameImage.iterrows():
    # get coordinates
    if(type_dataset == "voc"):
        y1, x1, y2, x2 = row['ymin'], row['xmin'], row['ymax'], row['xmax']
    elif(type_dataset == "yolo"):
        x_c_n = row['xcen']
        y_c_n = row['ycen']
        width_n = row['w_yolo']
        height_n = row['h_yolo']
        img_width = row['width']
        img_height = row['height']
        y1, x1, y2, x2 = convert_yolo_coordinates_to_voc(x_c_n, y_c_n, width_n, height_n, img_width, img_height)
		# calculate width and height of the box
    width, height = x2 - x1, y2 - y1
    rect = Rectangle((x1, y1), width, height, fill=False, color='white')
    ax.add_patch(rect)
    label = f"{row['class']}" 
    pyplot.text(x1, y1, label, color='white')
  # show the plot
  figName = os.path.basename(filename)
  print(f"figName: {image_name}")
  if(output_path != None):
      isExist = os.path.exists(output_path)
      if not isExist:
          os.makedirs(output_path)
          print(f"The new directory {output_path} is created!")
      figPath = f"{output_path}/{image_name}"
      print(f"<<<<<<<<saving {image_name} at the path {figPath}>>>>>>>>")
      pyplot.savefig(figPath)
  if(printImage == True):
    # print("plot is shown: ")
    pyplot.figure(figsize=((320,320)))
    pyplot.show()
  # print("plot is closed")
  pyplot.close()
  
def main(_argv):
    df = None
    df = pd.read_csv(FLAGS.annotation_csv) #full label
    df = df.dropna()
    print(df.head(50))
    test_list = df.sample(frac=1)['filename'].unique().tolist() #all image filenames
    for item in test_list:
      draw_bounding_box_resize(item, FLAGS.dataset_images, df,  FLAGS.printImage, FLAGS.path_output, FLAGS.type_dataset)
    
if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass

    
