import csv
import random
import os

hpWAfrica_id = []
hpEAsia_id = []
hpWAfrica_random_sample = []
hpEAsia_random_sample = []

#list all IDs from two geographically seperate regions
with open('visuala_microreact_clusters.csv', 'r') as input_csv:
    reader = csv.reader(input_csv)
    for row in reader:
        if row[1] == '1':
            hpWAfrica_id.append([row[0], row[1]])
        elif row[1] == '2':
            hpEAsia_id.append([row[0], row[1]])
        else:
            pass

#randomly pick 100 IDs from each list as sample pools
hpWAfrica_random_sample = random.sample(hpWAfrica_id, 100)
hpEAsia_random_sample = random.sample(hpEAsia_id, 100)

with open('ID-path-for-pop.csv', 'r') as path_csv:
    reader = csv.reader(path_csv)
    for path in reader:
        for sample1 in hpWAfrica_random_sample:
            if sample1[0] == path[0]:
                sample1.append(path[1])

with open('ID-path-for-pop.csv', 'r') as path_csv:
    reader = csv.reader(path_csv)
    for path in reader:
        for sample2 in hpEAsia_random_sample:
            if sample2[0] == path[0]:
                sample2.append(path[1])

with open('visuala_microreact_clusters.csv', 'r') as input_csv:
    reader = csv.reader(input_csv)
    for row in reader:
        for sample1 in hpWAfrica_random_sample:
            if sample1[0] == row[0]:
                sample1 += row[2:18]

with open('visuala_microreact_clusters.csv', 'r') as input_csv:
    reader = csv.reader(input_csv)
    for row in reader:
        for sample2 in hpEAsia_random_sample:
            if sample2[0] == row[0]:
                sample2 += row[2:18]
                
with open ('hpWAfrica_sample_metadata.csv', 'w+') as output:
    writer = csv.writer(output, dialect="unix")
    for i in hpWAfrica_random_sample:
        writer.writerow(i)

with open ('hpEAsia_sample_metadata.csv', 'w+') as output:
    writer = csv.writer(output, dialect="unix")
    for i in hpEAsia_random_sample:
        writer.writerow(i)

print("All done")