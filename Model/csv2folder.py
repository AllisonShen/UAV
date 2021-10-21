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


flags.DEFINE_string('path_images', '', 'path to dataset')
flags.DEFINE_string('path_anno', '', 'path to dataset')
flags.DEFINE_string('path_csv', '', 'path to csv')
flags.DEFINE_string('path_output', '', 'path to csv')

path_csv_output = path_output


flags.DEFINE_string('path_csv_output', '', 'path to csv')
flags.DEFINE_string('path_train', 'None', 'path to train')
flags.DEFINE_string('path_val', 'None', 'path to val')
flags.DEFINE_string('yolo_labels', 'None', 'path to train')
flags.DEFINE_string('yolo_labels_train', 'None', 'path to train')
flags.DEFINE_string('yolo_labels_val', 'None', 'path to val')
flags.DEFINE_float('test_size', 0.2, 'path to csv')




