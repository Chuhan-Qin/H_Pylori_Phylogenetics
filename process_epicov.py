#! python

import os
import sys
import subprocess
import Bio
from Bio import SeqIO
import pandas as pd
import geopandas as gpd
import numpy as np

# data
# load spatial data
countries_url = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_10m_admin_0_label_points.geojson"
countries_df = gpd.read_file(countries_url)
regions_url = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_10m_admin_1_label_points.geojson"
regions_df = gpd.read_file(regions_url)

usa_states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}

australia_states = {
    'NSW': 'New South Wales',
    'QLD': 'Queensland',
    'SA': 'South Australia',
    'TAS': 'Tasmania',
    'VIC': 'Victoria',
    'WA': 'Western Australia'
}

canada_states = {
    'AB': 'Alberta',
    'BC': 'British Columbia',
    'MB': 'Manitoba',
    'NB': 'New Brunswick',
    'NL': 'Newfoundland and Labrador',
    'NT': 'Northwest Territories',
    'NS': 'Nova Scotia',
    'NU': 'Nunavut',
    'ON': 'Ontario',
    'PE': 'Prince Edward Island',
    'QC': 'Quebec',
    'SK': 'Saskatchewan',
    'YT': 'Yukon'
}

uk_capitals = {
    'England': 'Westminster',
    'Wales': 'Cardiff',
    'Scotland': 'Edinburgh',
    'Northern Ireland': 'Belfast'
}

china_regions = {
    'Hangzhou': 'Zhejiang',
    'Foshan': 'Guangdong',
    'Guangzhou': 'Guangdong',
    'Wuhan-Hu-1': 'Hubei',
    'Wuhan': 'Hubei',
    'Nanchang': 'Jiangxi',
    'Shangrao': 'Jiangxi',
    'Jiujiang': 'Jiangxi',
    'Shenzhen': 'Guangdong',
    'NanChang': 'Jiangxi',
    'bat': 'Yunnan',
    'Ganzhou': 'Jiangxi',
    'Xinyu': 'Jiangxi',
    'Pingxiang': 'Jiangxi',
    'Jian': 'Jiangxi',
    'Tianmen': 'Hubei',
    'Hefei': 'Anhui',
    'Jingzhou': 'Hubei'
}

# functions
def get_coordinates(location = None, info_region = None, info_country = None, name = None):
    # initialise
    country = ""
    region = ""
    longitude = ""
    latitude = ""
    location = location.replace('_',' ')
    # special cases
    if location == "USA":
        location = "United States of America"
        country = "United States of America"
        state_code = name[:2]
        if state_code in usa_states:
            location = usa_states[state_code]
    elif location == "Canada":
        country = "Canada"
        state_code = name[:2]
        if state_code in canada_states:
            location = canada_states[state_code]
    elif location == "Australia":
        state_code = name[:2]
        if state_code in australia_states:
            location = australia_states[state_code]
        else:
            state_code = name[:3]
        if state_code in australia_states:
            location = australia_states[state_code]
    elif location in ("England","Wales","Scotland","Northern Ireland"):
        country = "United Kingdom"
        region = location
        location = uk_capitals[location]
    elif location == "Korea" or location == "South Korea":
        location = "Seoul"
        country = "South Korea"
    elif location in china_regions:
        location = china_regions[location]
    elif location == "Hong Kong":
        region = "Hong Kong"
        country = "China"
    # get coordinates
    if location in info_region.name.values:
        longitude = str(info_region.loc[info_region.name==location].geometry.values.y[0])
        latitude = str(info_region.loc[info_region.name==location].geometry.values.x[0])
        if country != "United Kingdom": # as using capitals as proxy
            region = location
            country = str(info_region.loc[info_region.name==location].admin.values[0])
    elif location in info_country.sr_subunit.values:
        country = location
        longitudes = info_country.loc[info_country.sr_subunit==country].geometry.values.y
        latitudes = info_country.loc[info_country.sr_subunit==country].geometry.values.x
        longitude = str(np.median(longitudes))
        latitude = str(np.median(latitudes))
#        longitude = str(info_country.loc[info_country.sr_subunit==country].geometry.values.y[0])
#        latitude = str(info_country.loc[info_country.sr_subunit==country].geometry.values.x[0])
    elif location == "Japan":
        country = "Japan"
        longitude = str(info_country.loc[info_country.sr_su_a3=="JPX"].geometry.values.y[0])
        latitude = str(info_country.loc[info_country.sr_su_a3=="JPX"].geometry.values.x[0])
    elif location == "Belgium":
        country = "Belgium"
        longitude = str(info_country.loc[info_country.sr_su_a3=="BCR"].geometry.values.y[0])
        latitude = str(info_country.loc[info_country.sr_su_a3=="BCR"].geometry.values.x[0])
    elif location == "Congo":
        country = "Congo"
        longitude = str(info_country.loc[info_country.sr_subunit=="Congo (Brazzaville)"].geometry.values.y[0])
        latitude = str(info_country.loc[info_country.sr_subunit=="Congo (Brazzaville)"].geometry.values.x[0])
    elif country == "United States of America":
        longitude = str(info_country.loc[info_country.sr_subunit=="U.S.A."].geometry.values.y[0])
        latitude = str(info_country.loc[info_country.sr_subunit=="U.S.A."].geometry.values.x[0])
    elif location == "New Zealand": # code NZL
        country = "New Zealand"
        longitude = str(info_country.loc[info_country.sr_subunit=="South I."].geometry.values.y[0])
        latitude = str(info_country.loc[info_country.sr_subunit=="South I."].geometry.values.x[0])
    elif location == "Czech Republic":
        longitude = str(info_country.loc[info_country.sr_subunit=="Czech Rep."].geometry.values.y[0])
        latitude = str(info_country.loc[info_country.sr_subunit=="Czech Rep."].geometry.values.x[0])

    
    # check for missed entries
    if latitude == "NA":
        sys.stderr.write('Cannot find ' + location + ' for ' + name + '\n')
    # return
    return region, country, latitude, longitude

def print_info(info = None, n_count = 0, seq_length = 0, name = None, file = None, regions = None, countries = None):
    epidata_string = None
    if name in info.keys():
        epidata_string = info[name]
    else:
        sys.stderr.write('No information stored for ' + name)
        exit(2)
    epidata = epidata_string.split('|')
    basic_info = epidata[0].split('/')
    country = basic_info[1]
    isolate = basic_info[2]
    date_info = epidata[2].split('-')
    if len(date_info) < 3:
        sys.stderr.write('Insufficient date precision: ' + str(date_info) + '\n')
        return 1
    region, country, latitude, longitude = get_coordinates(location = country, info_region = regions, info_country = countries, name = isolate)
    if latitude == "NA":
        return 2
    o_list = [
        name,
        isolate,
        region,
        country,
        latitude,
        longitude,
        date_info[0],
        date_info[1],
        date_info[2],
        str(n_count),
        str(seq_length)
    ]
    print(','.join(o_list), file = file)
    return 0

def create_seq_dir(d):
    if os.path.exists(d):
        subprocess.call('rm -rf ' + d, shell = True)
    subprocess.call('mkdir '+ d, shell = True)

# file
seq_fn = sys.argv[1]
output_csv_fn = sys.argv[2] + '_input.csv'
epi_csv_fn = sys.argv[2] + '_info.csv'
output_seq_dir = 'epicov_sequences'

# remove spaces in input file
cmd_array = ['tr','" "','"_"','<',seq_fn,'>','tmp.'+seq_fn]
try:
    subprocess.check_call(' '.join(cmd_array), stderr = subprocess.STDOUT, shell = True)
except:
    sys.stderr.write('Cannot replace spaces in input file ' + seq_fn + ' with command ' + ' '.join(cmd_array) + '\n')
    exit(1)

# data structures
epi_data = {}
contigs_data = {}
genome_name = None
lower_length_threshold = 28000
upper_length_threshold = 32000

# iterate through sequences
create_seq_dir(output_seq_dir)
seq_dict = Bio.SeqIO.index('tmp.'+seq_fn,"fasta")
info_dict = {}
for d in seq_dict.keys():
    info = d.split('|')
    if len(info) == 3:
        info_dict[info[1]] = d
    else:
        sys.stderr.write("Missing information for entry " + d + "\nSplit into: " + str(info) + "\n")
with open(output_csv_fn, 'w') as output_csv:
    with open(epi_csv_fn, 'w') as info_csv:
        print('Id,Isolate,Region,Country__autocolour,longitude,latitude,year,month,day,Ambiguous bases,Length', file = info_csv)
        for genome_name in info_dict.keys():
            seq_fn = output_seq_dir + '/' + genome_name + '.fa'
            #Bio.SeqIO.write(seq_dict[info_dict[genome_name]],seq_fn,"fasta")
            #print(genome_name + '\t' + seq_fn, file = output_csv)
            n_count = seq_dict[info_dict[genome_name]].seq.count("N") + seq_dict[info_dict[genome_name]].seq.count("n")
            seq_length = len(seq_dict[info_dict[genome_name]].seq)
            if print_info(info = info_dict,
                        n_count = n_count,
                        seq_length = seq_length,
                        name = genome_name,
                        file = info_csv,
                        regions = regions_df,
                        countries = countries_df) == 0:
                Bio.SeqIO.write(seq_dict[info_dict[genome_name]],seq_fn,"fasta")
                print(genome_name + '\t' + seq_fn, file = output_csv)

