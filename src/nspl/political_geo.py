import sys
import io
import logging
import requests
import zipfile
import configparser
from collections import defaultdict
#from memory_profiler import profile

#------------------------------------------------------------------------------
def read_zip_data():
    """
        download the zip file and extract
        1. the postcode file
        2. the laua file

        Args:
            Return: a tuple (postcode dict, laua dict)
    """
    log = logging.getLogger("nspl.political_geo.read_zip_data")
    logging.getLogger("urllib3.connectionpool").setLevel(logging.ERROR)

    pcode_count = 0
    la_dict = dict()
    pc_dict = defaultdict(list)

    conf = configparser.ConfigParser()
    conf.read('settings.ini')
    url = conf['ArcGisUrl']['NsplUsed']
    la_pre = conf['NSPL']['LaNameFileStartsWith']
    pc_pre = conf['NSPL']['PostcodeFileStartsWith']
    file_suff = conf['NSPL']['FileExtension']

    #response_zip = requests.get(url)
    file_path = r'/home/avr/downloads/nspl1.zip'

    #with zipfile.ZipFile(io.BytesIO(response_zip.content)) as zips:
    with zipfile.ZipFile(file_path) as zip_files:
        la_ua = ([name for name in zip_files.namelist() if name.startswith(la_pre) and name.endswith(file_suff)][0])
        pcode = ([name for name in zip_files.namelist() if name.startswith(pc_pre) and name.endswith(file_suff)][0])

        # get the list of local authorities
        with io.TextIOWrapper(zip_files.open(la_ua), encoding='utf-8') as la_file:
            la_file.readline() # csv header

            for la_line in la_file:
                la_rec = la_line.split(',')
                la_dict[la_rec[0]] = la_rec[1]

        with io.TextIOWrapper(zip_files.open(pcode), encoding='utf-8') as pc_file:
            pc_file.readline() # csv header

            for pcode_line in pc_file:
                pcode_count += 1
                pc_rec = pcode_line.split(',')
                postcode_col = pc_rec[2].strip('"')
                laua_col = pc_rec[12].strip('"')

                # create a dictionary, k = postcode, v = list of local authorities
                if postcode_col in pc_dict:
                    if laua_col not in pc_dict[postcode_col]:
                        pc_dict[postcode_col].append(laua_col)
                        print(pc_dict[postcode_col])
                else:
                    pc_dict[postcode_col].append(laua_col)


    log.info(f'postcode count = {pcode_count}')
    return la_dict, pc_dict


#------------------------------------------------------------------------------
def postcode_local_authority_map():
    """
        for each postcode in the main nspl file, create a tuple with the 
        postcode and its local authority name.

        Args:
            Return: a list of tuples, aprrox. 2.2 million postcodes
    """
    log = logging.getLogger("nspl.political_geo.postcode_local_authority_map")

    la_dict, pc_dict = read_zip_data() 

    # prepare the output to be returned.
    postcodes = []
    for entry in pc_dict:
        postcode = ()   # tuple = (postcode, LA count, LA List of Names)
        authorities = []
        cntr = len(pc_dict[entry])
        
        for la_code in pc_dict[entry]:
            if len(la_code) > 0:
                try:
                    auth_name = la_dict[la_code]
                except KeyError:
                    auth_name = la_code

                authorities.append(auth_name)
        postcode = (entry, cntr, authorities)
        postcodes.append(postcode)
    
    return postcodes

#------------------------------------------------------------------------------
def postcode_local_authority_search(postcode_list):
    """
        for each postcode in search list, create a dict with the postcode and 
        its local authority name.

        Args:
            Return: a list dicts - postcode with its local authority name
    """
    log = logging.getLogger("nspl.political_geo.postcode_local_authority_search")

    la_dict, pc_dict = read_zip_data() 

    # prepare the output to be returned.
    postcodes = []
    for entry in postcode_list:
        postcode = {}   # dict = (postcode: LA Name)
        cntr = len(pc_dict[entry])
        
        for la_code in pc_dict[entry]:
            if len(la_code) > 0:
                try:
                    auth_name = la_dict[la_code]
                except KeyError:
                    auth_name = la_code
                
                postcode[entry] = auth_name

        postcodes.append(postcode)
    
    return postcodes