import os
import csv

path_list = []
with open('geographical_samples/combined_path.csv', 'r') as input:
    reader = csv.reader(input)
    for line in reader:
        if ".fna" in line[1]:
            path_list.append(line[1][:-4])
        else:
            path_list.append(line[1][:-6])

if os.path.exists("D:/PythonProject_H_pylori_genome/1/panaroo_output_extract_2"):
    pass
else:
    os.makedirs("D:/PythonProject_H_pylori_genome/1/panaroo_output_extract_2")

root = "D:/PythonProject_H_pylori_genome/1/panaroo_output_2/"
for path in path_list:
    for files in os.walk(root + path):
        for file in files[2]:
            if ".gff" in file:
                with open(root+path+"/"+file,"r") as fin:
                    with open("D:/PythonProject_H_pylori_genome/1/panaroo_output_extract_2/"+path+".gff", "w+") as fout:
                        fout.write(fin.read())
print("All done")
