import csv
import pandas

cluster1_id_list = []
cluster2_id_list = []

def splitword(term):
    return list(term)

def trimword(term, digit):
    return ''.join(list(term[0:(-digit)]))

with open ('geographical_samples/hpSwitzerland_sample.csv', 'r') as input_csv:
    reader = csv.reader(input_csv)
    for row in reader:
        if splitword(row[1])[0] == 'G':
            row[1] = trimword(row[1], 4)
            cluster1_id_list.append(row[1])
        elif splitword(row[1])[0] == 'S':
            row[1] = trimword(row[1], 3)
            cluster1_id_list.append(row[1])
        else:
            pass

with open ('geographical_samples/hpUSA_sample.csv', 'r') as input_csv:
    reader = csv.reader(input_csv)
    for row in reader:
        if splitword(row[1])[0] == 'G':
            row[1] = trimword(row[1], 4)
            cluster2_id_list.append(row[1])
        elif splitword(row[1])[0] == 'S':
            row[1] = trimword(row[1], 3)
            cluster2_id_list.append(row[1])
        elif splitword(row[1])[0] == 'H':
            row[1] = trimword(row[1], 6)
            cluster2_id_list.append(row[1])
        else:
            pass

head = ['Gene', 'Non-unique Gene name', 'Annotation']
edited_cluster1_id = head + cluster1_id_list
edited_cluster2_id = head + cluster2_id_list


hpSwitzerland_gene_array = []
hpUSA_gene_array = []

with open('gene_presence_absence2.csv', 'r', newline='') as file:
    df = pandas.read_csv(file)
    df_new = df[edited_cluster1_id]
    hpSwitzerland_gene_array = df_new.values.tolist()

with open('gene_presence_absence2.csv', 'r', newline='') as file:
    df = pandas.read_csv(file)
    df_new = df[edited_cluster2_id]
    hpUSA_gene_array = df_new.values.tolist()

with open('hpSwitzerland_gene_array.csv', 'w+') as output_csv:
    writer = csv.writer(output_csv, dialect='unix')
    writer.writerow(edited_cluster1_id)
    for row in hpSwitzerland_gene_array:
        writer.writerow(row)

with open('hpUSA_gene_array.csv', 'w+') as output_csv:
    writer = csv.writer(output_csv, dialect='unix')
    writer.writerow(edited_cluster2_id)
    for row in hpUSA_gene_array:
        writer.writerow(row)

header1 = edited_cluster1_id + ['gene_count', 'gene_frequency']
header2 = edited_cluster2_id + ['gene_count', 'gene_frequency']

for row in hpSwitzerland_gene_array:
    counter = 0
    for i in row [3:]:
        if splitword(str(i))[0] != 'n':
            counter += 1
        else:
            pass
    row.append(str(counter))
    row.append(str(counter/60))

for row in hpUSA_gene_array:
    counter = 0
    for i in row [3:]:
        if splitword(str(i))[0] != 'n':
            counter += 1
        else:
            pass
    row.append(str(counter))
    row.append(str(counter/60))

with open('hpSwitzerland_gene_frequency.csv', 'w+') as output_csv:
    writer = csv.writer(output_csv, dialect='unix')
    writer.writerow(header1)
    for row in hpSwitzerland_gene_array:
        writer.writerow(row)

with open('hpUSA_gene_frequency.csv', 'w+') as output_csv:
    writer = csv.writer(output_csv, dialect='unix')
    writer.writerow(header2)
    for row in hpUSA_gene_array:
        writer.writerow(row)

print('All done')