import glob
import os

pathToDataset = "./dataset"
listAllFiles = []
for filename in glob.glob(f"{pathToDataset}/*.jpg"):
    basename = os.path.basename(filename)
    numIndex = int(basename[:3])
    listAllFiles.append(numIndex)
listAllFiles.sort()

print(listAllFiles)
prev_i = None
count = 0
for i, v in enumerate(listAllFiles):
    if(i == 0):
        prev_v = v
    else:
        if((prev_v + 1) != v):
            print(f"Not continuous between {prev_v} and {v}")
            count +=1
        prev_v = v
print(f"Total not continuous: {count}")
