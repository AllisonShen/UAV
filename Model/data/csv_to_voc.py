import os
import xml.etree.cElementTree as ET
import csv

SAVE_DIR="/content/drive/MyDrive/UAV/Model/data/voc_mixed"

            
def read_file(file_path):


    with open(file_path, 'r') as file:
        lines = csv.reader(file)
        header=next(lines)
        voc_prefix='000' #first prefix
        voc_labels = []
        for line in lines:
            file_prefix=line[0].split(".")[0]
            w=line[1]
            h=line[2]
            
            if voc_prefix==file_prefix:
                pass
            else: #new prefix
                if len(voc_labels)!=0:create_file(voc_prefix,w,h,voc_labels) #make xml file by prefer prefix
                voc_labels=[] #labels initialization
                voc_prefix=file_prefix #prefix initialization
                
            voc = []
            voc.append(line[3]) #class
            for i in range(4,8):
              if line[i]!='':voc.append(int(float(line[i]))) #xmin, ymin, xmax, ymax
            if len(voc)==5:voc_labels.append(voc)
            
        if len(voc_labels)!=0:create_file(voc_prefix,w,h,voc_labels) #make xml file for last image
  
          
            
def create_file(file_prefix, width, height, voc_labels):
    root = create_root(file_prefix, width, height)
    root = create_object_annotation(root, voc_labels)
    tree = ET.ElementTree(root)
    tree.write("{}/{}.xml".format(SAVE_DIR, file_prefix))
    
    
def create_object_annotation(root, voc_labels):
    for voc_label in voc_labels:
        obj = ET.SubElement(root, "object")
        ET.SubElement(obj, "name").text = voc_label[0]
        ET.SubElement(obj, "pose").text = "Unspecified"
        ET.SubElement(obj, "truncated").text = str(0)
        ET.SubElement(obj, "difficult").text = str(0)
        bbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bbox, "xmin").text = str(voc_label[1])
        ET.SubElement(bbox, "ymin").text = str(voc_label[2])
        ET.SubElement(bbox, "xmax").text = str(voc_label[3])
        ET.SubElement(bbox, "ymax").text = str(voc_label[4])
    return root

def create_root(file_prefix, width, height):
    root = ET.Element("annotations")
    ET.SubElement(root, "filename").text = "{}.jpg".format(file_prefix)
    ET.SubElement(root, "folder").text = "images"
    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"
    return root

if __name__=="__main__":
    read_file("/content/drive/MyDrive/UAV/Model/data/mixedImg_info.csv")