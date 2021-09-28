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

flags.DEFINE_string('list_dataset_images', '', 'path to dataset')
flags.DEFINE_string('list_annotation_csv', '', 'path to annotation')
flags.DEFINE_string('list_path_output', '', 'path to output')
flags.DEFINE_string('list_source_tags', '['adh', 'daytime','night']', 'path to output')
flags.DEFINE_string('list_', '[daytime_adh, daytime,night]', 'path to output')


list_dataset_images = FLAGS.list_dataset_images
list_annotation_csv = FLAGS.list_annotation_csv
list_path_output = FLAGS.list_path_output
list_tags = FLAGS.list_tags


def main(_argv):
    df = None
    for dataset_image
    df = pd.read_csv(FLAGS.annotation_csv) #full label
    df = df.dropna()
    print(df.head(50))
    test_list = df.sample(frac=1)['filename'].unique().tolist() #all image filenames
if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass