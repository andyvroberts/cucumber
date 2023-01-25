import sys
import io
import logging
import requests
import zipfile
import configparser
from collections import defaultdict
from memory_profiler import profile

#------------------------------------------------------------------------------
@profile
def controller():
    log = logging.getLogger("nspl.py")
    url = 'https://www.arcgis.com/sharing/rest/content/items/60484ad9611249b59f3644e92f37476d/data'
    file_count = 0
    pcode_count = 0
    la_dict = dict()
    pc_dict = defaultdict(list)

    conf = configparser.ConfigParser()
    conf.read('nspl_config.ini')
    la_pre = conf['NSPL']['LaNameFileStartsWith']
    pc_pre = conf['NSPL']['PostcodeFileStartsWith']
    file_suff = conf['NSPL']['FileExtension']

    #response_zip = requests.get(url)
    file_path = r'/home/avrob/downloads/nspl.zip'

    #with zipfile.ZipFile(io.BytesIO(response_zip.content)) as zips:
    with zipfile.ZipFile(file_path) as zips:
        la_ua = ([name for name in zips.namelist() if name.startswith(la_pre) and name.endswith(file_suff)][0])
        pcode = ([name for name in zips.namelist() if name.startswith(pc_pre) and name.endswith(file_suff)][0])

        # get the list of local authorities
        with io.TextIOWrapper(zips.open(la_ua), encoding='utf-8') as la_file:
            la_file.readline() # csv header

            for la_line in la_file:
                la_rec = la_line.split(',')
                la_dict[la_rec[0]] = la_rec[1]

        with io.TextIOWrapper(zips.open(pcode), encoding='utf-8') as pc_file:
            pc_file.readline() # csv header

            for pcode_line in pc_file:
                pcode_count += 1
                pc_rec = pcode_line.split(',')
                postcode_col = pc_rec[2]
                laua_col = pc_rec[12]

                if postcode_col in pc_dict:
                    if laua_col not in pc_dict[postcode_col]:
                        pc_dict[postcode_col].append(laua_col)
                        print(pc_dict[postcode_col])
                else:
                    pc_dict[postcode_col].append(laua_col)

            
    print(f'postcode count = {pcode_count}')
    for item in pc_dict:
        print(item)
        break
    




        #     file_count +=1;
        #     print(f'File: {zipinfo.filename} is {round(zipinfo.compress_size/1024/1024,2)} Mb compressed.')


#------------------------------------------------------------------------------
if __name__ == '__main__' :
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)-8s [%(name)s]: %(message)s",
        datefmt='%Y-%m-%d %I:%M:%S',
        handlers = [
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.getLogger("urllib3.connectionpool").setLevel(logging.ERROR)

    controller()