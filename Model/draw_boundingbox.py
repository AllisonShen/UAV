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
flags.DEFINE_string('path_output', '', 'path to output')

def draw_bounding_box_resize(image_name,pathResizeImages,df, printImage = True,output_path= None):
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
    y1, x1, y2, x2 = row['ymin'], row['xmin'], row['ymax'], row['xmax']
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
  if(printImage):
    pyplot.show()
  pyplot.close()
  
def main(_argv):
    df = None
    df = pd.read_csv(FLAGS.annotation_csv) #full label
    df = df.dropna()
    print(df.head(50))
    test_list = df.sample(frac=1)['filename'].unique().tolist() #all image filenames
    # test_list = df.sample(frac=0.01)['filename'].unique().tolist()
    # print(f"length: {len(test_list)}")
    for item in test_list:
      draw_bounding_box_resize(item, FLAGS.dataset_images, df,  True, FLAGS.path_output)
    
if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass

    
