import xlrd
import csv
import urllib.request as urlr
import ssl
import os

print("Working on your data set, please wait....")
species = "Helicobacter pylori"
sample_id_list = []
sample_id_path = []
unmatched = []
id_output_array = []

# find H. pylori ID
print("Retrieving sample ID...")
with open("D:\Python_project\Python_Project\File2_taxid_lineage_661K.txt","r+") as file:
    lines = file.readlines()
    for line in lines:
        if species in line:
            ID = line.split("	")[0]
            sample_id_list.append(ID)

# find corresponding file path
print("Getting paths...")
with open("D:\Python_project\Python_Project\sampleid_assembly_paths.txt","r+") as file_2:
    lines = file_2.readlines()
    for line in lines:
        for ID in sample_id_list:
            if ID in line:
                path_temp = line.split("	")[1].strip('\n')
                sample_id_path.append([ID, path_temp])

# filter out sampleID without a corresponding file path
for i in sample_id_list:
    count = 0
    for x in sample_id_path:
        if i == x[0]:
            break
        else:
            count += 1
    if count >= len(sample_id_path):
        unmatched.append(i)

# match SampleID with metadata
print("Retrieving related metadata...")
data = xlrd.open_workbook('D:\Python_project\Python_Project\H_pylori_metadata_enterobase.xls')
table = data.sheets()[0]
col = table.col_values(26)
row_header = table.row_values(0)
row_header.insert(0,'path')
row_header.insert(0,'SampleID')
wanted_row = []
wantedID = []
unmatched_2 = []

# match sampleID with row number in the sheet
for ID in sample_id_list:
    num = 0
    for i in col:
        if ID == i:
            wanted_row.append([ID,num])
            wantedID.append(ID)
        num += 1

# filter out sampleIDs without metadata
for ID in sample_id_list:
    count = 0
    for i in col:
        if ID == i:
            break
        else:
            count += 1
    if count >= len(col):
        unmatched_2.append(ID)

# combine sampleID, file path, metadata to form a list for output
for ID in sample_id_list:
    # combine sampleID and file path
    id_output_list = [ID]
    count = 0
    for i in sample_id_path:
        if ID == i[0]:
            id_output_list.append(i[1])
            break
        else:
            count += 1
        if count >= len(sample_id_path):
            id_output_list.append("")
    # adding metadata to the list
    count = 0
    for i in wanted_row:
        if ID == i[0]:
            row_tmp = table.row_values(i[1])
            id_output_list = id_output_list + row_tmp
            break
        else:
            count += 1
    if count >= len(wanted_row):
        num = 0
        while num < 44:
            num += 1
            id_output_list.append("")
    # combine all lists to form an array for output
    id_output_array.append(id_output_list)

# output in txt format
print("Outputting sorted data to output.txt")
with open("output.txt", "w+") as output_txt:
    for i in id_output_array:
        for x in i:
            if str(x) != '':
                output_txt.write(str(x))
                output_txt.write(' ')
            else:
                output_txt.write('* ')
        output_txt.write('\n')

# output in csv format
print("Outputting sorted data to output.csv")
with open('output.csv', 'w+') as output_csv:
    writer = csv.writer(output_csv, dialect="unix")
    writer.writerow(row_header)
    for i in id_output_array:
        writer.writerow(i)

print("All Done.")

# download metadata from ENA
ssl._create_default_https_context = ssl._create_unverified_context
def downloaddata(url, path):
    down = urlr.urlopen(url)
    with open(path,'w+') as f:
        f.write(str(down.read()))

if os.path.exists("./ENADATA") == False:
    os.makedirs("./ENADATA")
else:
    pass
for ID in sample_id_list:
    downloaddata("https://www.ebi.ac.uk/ena/browser/api/xml/"+ID+"?download=true", "./ENADATA/"+ID+".xml")
