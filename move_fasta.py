import os
import csv

path_list = []
nomatch_list = []
with open('geographical_samples/combined_path2.csv', 'r') as input:
    reader = csv.reader(input)
    for line in reader:
        path_list.append(line[1])

if os.path.exists("D:/PythonProject_H_pylori_genome/1/moved_fasta2"):
    pass
else:
    os.makedirs("D:/PythonProject_H_pylori_genome/1/moved_fasta2")

root = "D:/PythonProject_H_pylori_genome/1/moved_fasta2/"
for path in path_list:
    print("\r",path,end='',flush=True)
    try:
        with open("NCBI_GENOME_unzipped/"+path,'r') as origin:
            with open(root+path, 'w+') as copy:
                copy.write(origin.read())
    except:
        try:
            with open("Moodley_paper_genome/"+path,'r') as origin:
                with open(root+path, 'w+') as copy:
                    copy.write(origin.read())
        except:
            try:
                with open("samples_genome/" + path, 'r') as origin:
                    with open(root + path, 'w+') as copy:
                        copy.write(origin.read())
            except:
                nomatch_list.append(path)

if len(nomatch_list) != 0:
    print("\n*****************Failed***********************")
    for i in nomatch_list:
        print(i)
print("\nAll done")
