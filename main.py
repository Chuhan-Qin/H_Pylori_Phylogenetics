import xlrd
import csv
import urllib.request as urlr
import ssl
import os
import gzip
import socket
import eutils
from Bio import Entrez
from Bio import SeqIO

import sys
from typing import List

from ncbi.datasets.openapi import ApiClient as DatasetsApiClient
from ncbi.datasets.openapi import ApiException as DatasetsApiException
from ncbi.datasets.openapi import GenomeApi as DatasetsGenomeApi
from ncbi.datasets.metadata.genome import get_assembly_metadata_by_taxon

from ncbi.datasets.package import dataset

"""
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

"""

"""

path = "//wsl$/Ubuntu/home/chuhan_duke/refseq/bacteria"
ncbi_id = []
print("Unzipping downloaded data...")
if not os.path.exists("./NCBI_GENOME_unzipped"):
    os.makedirs("./NCBI_GENOME_unzipped")
else:
    pass

for root, directories, files in os.walk(path):
    for i in files:
        if i.endswith(".fna.gz") == True:
            ncbi_id.append(i)
            print('\r' + "Unzipping: >>>>" + i + "<<<<", end='', flush=True)
            with open("./NCBI_GENOME_unzipped/" + i[:-3], "w+") as f:
                unzip = gzip.GzipFile(os.path.join(root,i))
                while True:
                    line = str(unzip.readline())
                    if len(line) <= 3:
                        break
                    else:
                        line = line[2:-3]
                        f.write(line + '\n')
print("\n" + "Unzip completed.")

"""

"""
print("Currently unzipping:")
for i in downloaded_data:
    print('\r' + ">>>>" + i + ".contigs.fa.gz<<<<", end='', flush=True)
    with open("./NCBI_GENOME_unzipped/" + i + ".fa","w+") as f:
        unzip = gzip.GzipFile("./NCBI_GENOME/" + i + ".contigs.fa.gz")
        while True:
            line = str(unzip.readline())
            if len(line) <= 3:
                break
            else:
                line = line[2:-3]
                f.write(line+'\n')
print("\n"+"Unzip completed.")
"""
"""
print("Fetching data from NCBI...")
from selenium import webdriver
from time import sleep

sel_col = '//*[@id="select-columns__open-dialog"]'
check_bio = '//*[@id="chk-col-biosample"]'
apply = '//*[@id="select-columns__dialog__apply"]'
rows = '//*[@id="maincontent"]/div[2]/div/div/div/div[4]/div[3]/div[1]/div[2]/div[1]'
twohun_row = '//*[@id="maincontent"]/div[2]/div/div/div/div[4]/div[3]/div[1]/div[2]/div[2]/ul/li[5]'
next_page = '/html/body/div[3]/main/div[2]/div/div/div/div[4]/div[3]/div[3]/button[2]'

browser = webdriver.Chrome()
browser.maximize_window()
sleep(5)
browser.get("https://www.ncbi.nlm.nih.gov/datasets/genomes/?taxon=210")
sleep(5)
browser.find_element_by_xpath(sel_col).click()
sleep(2)
browser.find_element_by_xpath(check_bio).click()
sleep(2)
browser.find_element_by_xpath(apply).click()
sleep(2)
browser.find_element_by_xpath(rows).click()
sleep(2)
browser.find_element_by_xpath(twohun_row).click()
sleep(5)

NCBI_ID = []
NCBI_ID_2 = []
ENA_ID = []
page = 1
while page <= 27:
    print('\r', 'Fetching Page', page, end='', flush=True)
    if page == 1:
        ID_web = browser.find_element_by_xpath( '//*[@id="DataTables_Table_0"]/tbody/tr[1]/td[3]/span[1]')
        ID = ID_web.text
        NCBI_ID.append(ID)
        ID_web = browser.find_element_by_xpath( '//*[@id="DataTables_Table_0"]/tbody/tr[1]/td[3]/span[3]')
        ID = ID_web.text
        NCBI_ID_2.append(ID)
        ID_web = browser.find_element_by_xpath( '//*[@id="DataTables_Table_0"]/tbody/tr[1]/td[8]')
        ID = ID_web.text
        ENA_ID.append(ID)
        i = 2;
        while i <= 200:
            ID_web = browser.find_element_by_xpath(
                                          '//*[@id="DataTables_Table_0"]/tbody/tr[' + str(i) + ']/td[3]/span[1]')
            ID = ID_web.text
            NCBI_ID.append(ID)
            ID_web = browser.find_element_by_xpath(
                                          '//*[@id="DataTables_Table_0"]/tbody/tr[' + str(i) + ']/td[3]/span[2]')
            ID = ID_web.text
            NCBI_ID_2.append(ID)
            ID_web = browser.find_element_by_xpath('//*[@id="DataTables_Table_0"]/tbody/tr[' + str(i) + ']/td[8]')
            ID = ID_web.text
            ENA_ID.append(ID)
            i += 1
        browser.find_element_by_xpath(next_page).click()
        sleep(3)
        page += 1
    if page == 27:
        i = 1
        while i <= 125:
            ID_web = browser.find_element_by_xpath('//*[@id="DataTables_Table_0"]/tbody/tr[' + str(i) + ']/td[3]/span[1]')
            ID = ID_web.text
            NCBI_ID.append(ID)
            ID_web = browser.find_element_by_xpath(
                                          '//*[@id="DataTables_Table_0"]/tbody/tr[' + str(i) + ']/td[3]/span[2]')
            ID = ID_web.text
            NCBI_ID_2.append(ID)
            ID_web = browser.find_element_by_xpath('//*[@id="DataTables_Table_0"]/tbody/tr[' + str(i) + ']/td[8]')
            ID = ID_web.text
            ENA_ID.append(ID)
            i += 1
        break
    else:
        i = 1;
        while i <= 200:
            ID_web = browser.find_element_by_xpath(
                                          '//*[@id="DataTables_Table_0"]/tbody/tr[' + str(i) + ']/td[3]/span[1]')
            ID = ID_web.text
            NCBI_ID.append(ID)
            ID_web = browser.find_element_by_xpath(
                                          '//*[@id="DataTables_Table_0"]/tbody/tr[' + str(i) + ']/td[3]/span[2]')
            ID = ID_web.text
            NCBI_ID_2.append(ID)
            ID_web = browser.find_element_by_xpath('//*[@id="DataTables_Table_0"]/tbody/tr[' + str(i) + ']/td[8]')
            ID = ID_web.text
            ENA_ID.append(ID)
            i += 1
        browser.find_element_by_xpath(next_page).click()
        sleep(3)
        page += 1
sleep(10)
browser.close()
print("Completed.")

ID_combined = []
for index, value in enumerate(ENA_ID):
    ID_combined.append([value, NCBI_ID[index], NCBI_ID_2[index]])

print('Outputting as csv...')
with open('IDs.csv', 'w+') as output_csv:
    writer = csv.writer(output_csv, dialect="unix")
    for i in ID_combined:
        writer.writerow(i)
print("Completed.")
"""

"""
print("Mapping additional Genome Sequence File...")
path = r'D:\PythonProject_H_pylori_genome\1\NCBI_GENOME_unzipped'
ENA_list_match = []
ID_1_list = []
ID_2_list = []
raw_list = []
processed_list = []
unmatched_counter = 0
with open('IDs.csv', 'r') as f:
    reader = csv.reader(f)
    for i in reader:
        ENA_list_match.append(i[0])
        i_processed_list = i[2].split(': ')
        i_processed = i_processed_list[1]
        ID_2_list.append(i_processed)
        ID_1_list.append(i[1])

for root, directories, files in os.walk(path):
    for i in files:
        raw_list.append(i)
        i_processed_list = i.split('_')
        i_processed = i_processed_list[0]+'_'+i_processed_list[1]
        processed_list.append(i_processed)

with open('ID-path-for-pop.csv', 'w+') as f:
    writer = csv.writer(f, dialect="unix")
    for index, value in enumerate(processed_list):
        if value in ID_2_list:
            writer.writerow([ENA_list_match[ID_2_list.index(value)], raw_list[index]])
        else:
            unmatched_counter += 1
print("Completed with", unmatched_counter, "failure(s).")

print("Checking possible repeats...")
path = r'D:\PythonProject_H_pylori_genome\1\WHOLE_GENOME_SEQUENCE_unzipped'
media = []
media_2 = []
repeated = []
old_re = []
counter = 0
with open('ID-path-for-pop.csv','r') as f:
    reader = csv.reader(f)
    for i in reader:
        media.append(i[0])
        media_2.append(i[1])
for root, directories, files in os.walk(path):
    for i in files:
        i_processed = i.strip('.fa')
        if i_processed in media:
            counter += 1
            repeated.append([i_processed, os.path.join(path, i)])
        else:
            old_re.append([i_processed, i])

print('Completed.', counter, "possible repeat(s). Check repeats.txt.")

print('Comparing fasta data of possible repeats...')
def getMaxmatch(str1, str2, Cap=False):
    str_a = str(str1)
    str_b = str(str2)
    if not str_a or not str_b:
        return {0:[]}
    if len(str_a) > len(str_b):
        str_a, str_b = str_b, str_a
    if Cap:
        str_a, str_b = str_a.lower(), str_b.lower()
    matchDict = {}
    if str_a in str_b:
        matchDict[len(str_a)] = [str_a]
        return matchDict
    shortstrlen = len(str_a)
    matchDict[0] = []
    counter = 0
    for i in range (0, shortstrlen+1):
        if counter>=100:
            break
        counter += 1
        for j in range(0, i-1):
            print('\rMax match length:',max(list(matchDict.keys())), end='', flush=True)
            subStr = str_a[j:i]
            if subStr in str_b:
                if len(subStr) in matchDict.keys():
                    matchDict[len(subStr)].append(subStr)
                else:
                    matchDict[len(subStr)] = [subStr]
    result = {}
    maxlen =max(list(matchDict.keys()))
    result[maxlen] = matchDict[maxlen]
    return maxlen

for i in repeated:
    print('\r'+'Comparing '+i[0]+'...: ', end='',flush=True)
    data_1 = ''
    data_2 = ''
    with open (i[1],'r') as f:
        lines_1 = f.readlines()
    with open (media_2[media.index(i[0])], 'r') as f:
        lines_2 = f.readlines()
    for j in lines_1:
        data_1 = data_1 + j.strip('\n')
    for k in lines_2:
        data_2 = data_2 + k.strip('\n')
    i.append(getMaxmatch(data_1, data_2))
with open('repeats.txt', 'w+') as f:
    for i in repeated:
        f.write(i[0] + '   ' + i[1] + ' ' + str(i[2]))
        f.write('\n')

print("Merging the two...")
path = r'D:\PythonProject_H_pylori_genome\1\WHOLE_GENOME_SEQUENCE_unzipped'
with open('ID-path-for-pop.csv', 'a+') as f:
    writer = csv.writer(f, dialect="unix")
    for i in old_re:
        writer.writerow(i)
print('Completed.')

print("preparing Sample-to-Path text for poppunk...")
media = []
with open('ID-path-for-pop.csv', 'r') as f:
    reader = csv.reader(f)
    for i in reader:
        media.append(i)
with open('ID-path-for-pop.txt','w+') as f:
    for i in media:
        f.write(i[0] + '	' + i[1])
        f.write('\n')
print("Completed.")
"""

# match SampleID with metadata
print("Retrieving related metadata...")
data = xlrd.open_workbook('D:\Python_project\Python_Project\H_pylori_metadata_enterobase.xls')
table = data.sheets()[0]
col = table.col_values(26)
row_header = table.row_values(0)
row_header.insert(0,'path')
row_header.insert(0,'SampleID')
matched_row = []
matchedID = []
unmatchedID = []
id_output_list2 = []
id_output_array2 = []

with open ('D:/PythonProject_H_pylori_genome/1/hello_visul_microreact_clusters.csv', 'r') as f:
    reader = csv.reader(f)
    biosample_id = []
    i = 0
    for row in reader:
        if i == 0:
            i = i + 1
        else:
            biosample_id.append(row[0])

    auto_colour = []
    i = 0
    for row in reader:
        if i == 0:
            i = i + 1
        else:
            auto_colour.append(row[1])

    del_header = []
    i = 0
    for row in reader:
        if i == 0:
            i = i +1
        else:
            del_header.append(row)

workbook = xlrd.open_workbook('D:\Python_project\Python_Project\H_pylori_metadata_enterobase.xls')

sheet = workbook.sheets()[0]
metadata_id = sheet.col_values(26)
header = sheet.row_values(0)
header.insert(0, 'Cluster_Cluster__autocolour')
header.insert(0, 'id')

for ID in biosample_id:
    num = 0
    for i in metadata_id:
        if ID == i:
            matched_row.append([ID,num])
            matchedID.append(ID)
        num += 1

for ID in biosample_id:
    count = 0
    for i in metadata_id:
        if ID == i:
            break
        else:
            count += 1
    if count >= len(metadata_id):
        unmatchedID.append(ID)

for row in del_header:
    id_output_list2 = [row]
    # adding metadata to the list
    count = 0
    for i in matched_row:
        if row[0] == i[0]:
            row_tmp = sheet.row_values(i[1])
            id_output_list2 = id_output_list2 + row_tmp
            break
        else:
            count += 1
    if count >= len(matched_row):
        num = 0
        while num < 44:
            num += 1
            id_output_list2.append("")
    id_output_array2.append(id_output_list2)

print("Outputting sorted data to microreact.csv")
with open('microreact.csv', 'w+') as output_csv:
    writer = csv.writer(output_csv)
    writer.writerow(row_header)
    for i in id_output_array2:
        writer.writerow(i)
