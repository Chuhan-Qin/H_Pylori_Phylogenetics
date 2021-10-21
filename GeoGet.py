from urllib import request
import ssl
import csv



location_list=[]
coordinates_list_raw=[]
coordinates_list_query=[]
coordinates_list = []
coordinates_list_cache_name = []
coordinates_list_cache_data = []


with open(r'D:\PythonProject_H_pylori_genome\1\poppunk files\Upload to Microreact\input_microreact.csv', 'r') as f:
    reader = csv.reader(f)
    for i in reader:
        location_list.append(i[2])

location_list_query = location_list[1:]

ssl._create_default_https_context = ssl._create_unverified_context

counter = 0
for location_name in location_list_query:

    if location_name != '':
        location_name = location_name.replace(' ','_')
        if location_name in coordinates_list_cache_name:
            coordinates_list_query.append(coordinates_list_cache_data[coordinates_list_cache_name.index(location_name)][1])
        else:
            print('\r' + str(counter) + ' getting coordinates of: ' + location_name, end='', flush=True)
            latitude = ''
            longitude = ''
            wiki = request.urlopen("http://en.wikipedia.org/wiki/"+ location_name)
            left = 0
            right = 0
            num = 0
            html = str(wiki.read(), encoding='utf-8')
            x = html.index('class="latitude"')
            y = html.index('class="longitude"')
            while True:
                if html[x+num]=='>':
                    left = x+num
                if html[x+num]=='<':
                    right = x+num
                    break
                num += 1
            num = left + 1
            while num < right:
                latitude = latitude + html[num]
                num += 1

            num = 0
            while True:
                if html[y+num]=='>':
                    left = y+num
                if html[y+num]=='<':
                    right = y+num
                    break
                num += 1
            num = left + 1
            while num < right:
                longitude = longitude + html[num]
                num += 1

            coordinates_list_raw.append([latitude,longitude])

            if latitude[-1] == 'S':
                latitude = '-'+latitude[:-1].split('°')[0]
            else:
                latitude = latitude[:-1].split('°')[0]

            if longitude[-1] == 'W':
                longitude = '-'+longitude[:-1].split('°')[0]
            else:
                longitude = longitude[:-1].split('°')[0]


            coordinates_list_query.append([latitude,longitude])
            coordinates_list_cache_name.append(location_name)
            coordinates_list_cache_data.append([location_name, [latitude, longitude]])
    else:
        coordinates_list_query.append(['', ''])
    counter += 1

coordinates_list = coordinates_list_query
coordinates_list.insert(0,['Latitude','Longitude'])

media=[]

with open(r'D:\PythonProject_H_pylori_genome\1\poppunk files\Upload to Microreact\input_microreact.csv', 'r') as f1:
    reader = csv.reader(f1)
    for index, i in enumerate(reader):
        i[6] = coordinates_list[index][0]
        i[7] = coordinates_list[index][1]
        media.append(i)

with open(r'D:\PythonProject_H_pylori_genome\1\input_microreact_cor.csv', 'w+') as f:
    writer = csv.writer(f, dialect='unix')
    for i in media:
        writer.writerow(i)