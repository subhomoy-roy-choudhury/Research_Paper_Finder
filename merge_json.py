import json
import glob
import os

# master_file = 'Research_Paper_Title_Citation_JSON_master.json'
master_file = 'Research_Paper_JSON_master.json'

data = []

if os.path.isfile(master_file) :
    with open(master_file, 'r') as file:
        data = json.load(file)

PATH_PAPER = os.getcwd()
# FOLDERNAME = f'/Research_Paper_Title_Citation_JSON_11_20/'
FOLDERNAME = f'/Research_Paper_JSON_1_10/'
PATH_PAPER = PATH_PAPER + FOLDERNAME

files=glob.glob(PATH_PAPER + '*.json')
print(len(files)) 

for file in files :
    with open(file, 'r') as f:
        data1 = json.load(f)
        for data2 in data1 :
            data.append(data2)

seen = []
for x in data:
    if x not in seen:
        seen.append(x)



with open(master_file,'w') as file :
        json.dump(seen,file,ensure_ascii=False, indent=1)