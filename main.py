import xlrd
import csv
import urllib.request as urlr
import ssl
import os
import gzip
import socket

print("Working on the data set, please wait....")
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

# download metadata from ENA
ssl._create_default_https_context = ssl._create_unverified_context
def downloaddata(url, path):
    counter = 1
    while counter <= 5:
        try:
            down = urlr.urlopen(url, timeout = 2)
            with open(path,'w+') as f:
                f.write(str(down.read()))
                break
        except:
            counter += 1
    if counter > 5:
        return(0)

# create directory for ENA data
if os.path.exists("./ENADATA") == False:
    os.makedirs("./ENADATA")
else:
    pass

print("Downloading data from ENA...")
download_data_ena_failed = []
print("Current downloading:")
for ID in sample_id_list:
    print('\r'+">>>>"+ID+".xml<<<<", end='', flush=True)
    if downloaddata("https://www.ebi.ac.uk/ena/browser/api/xml/"+ID+"?download=true", "./ENADATA/"+ID+".xml") == 0:
        download_data_ena_failed.append(ID)
        pass

# Export failed downloads
print("\n"+"Download completed,",str(len(download_data_ena_failed)),"failed.")
if len(download_data_ena_failed) != 0:
    print("Outputting failed sample ID to ./ENADATA/Failure.txt")
    with open("./ENADATA/Failure.txt", "w+") as f:
        for i in download_data_ena_failed:
            f.write(i[0]+':'+i[1])

# process the paths, get ready for download
sample_id_path_processed = []
for i in sample_id_path:
    i_trim = i[1][8:]
    sample_id_path_processed.append(i_trim)

# create directory for genome data
if os.path.exists("./WHOLE_GENOME_SEQUENCE") == False:
    os.makedirs("./WHOLE_GENOME_SEQUENCE")
else:
    pass

# download from ftp server
print("Downloading required data from ftp server...")
downloaded_data = []
download_data_ftp_failed = []
socket.setdefaulttimeout(2)
i = 0
print("Current downloading:")
for path in sample_id_path_processed:
    print(downloaded_data)
    counter = 1
    while counter<=5:
        print('\r'+">>>>"+sample_id_path[i][0]+".contigs.fa.gz<<<<", end='', flush=True)
        try:
            urlr.urlretrieve("http://ftp.ebi.ac.uk" + path, "./WHOLE_GENOME_SEQUENCE/" + sample_id_path[i][0] + ".contigs.fa.gz")
            downloaded_data.append(sample_id_path[i][0])
            i += 1
            break
        except socket.timeout:
            counter += 1
            pass
    if counter > 5:
        download_data_ftp_failed.append([sample_id_path[i][0], "http://ftp.ebi.ac.uk" + path])

print("Download completed,",str(len(download_data_ftp_failed)),"failed.")

# Export failed downloads
if len(download_data_ftp_failed) != 0:
    print('\n'+"Outputting failed sample ID to ./WHOLE_GENOME_SEQUENCE/Failure.txt")
    with open("./ENADATA/Failure.txt", "w+") as f:
        for i in download_data_ftp_failed:
            f.write(i)

# unzip the genome data
print("Unzipping downloaded data...")
if not os.path.exists("./WHOLE_GENOME_SEQUENCE_unzipped"):
    os.makedirs("./WHOLE_GENOME_SEQUENCE_unzipped")
else:
    pass

print("Currently unzipping:")
for i in downloaded_data:
    print('\r' + ">>>>" + i + ".contigs.fa.gz<<<<", end='', flush=True)
    with open("./WHOLE_GENOME_SEQUENCE_unzipped/" + i + ".fa","w+") as f:
        unzip = gzip.GzipFile("./WHOLE_GENOME_SEQUENCE/" + i + ".contigs.fa.gz")
        while True:
            line = str(unzip.readline())
            if len(line) <= 3:
                break
            else:
                line = line[2:-3]
                f.write(line+'\n')
print("\n"+"Unzip completed.")

print("All done.")




