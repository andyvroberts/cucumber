import sys
import io
import logging
import requests
import zipfile
import configparser
import memory_profiler

#------------------------------------------------------------------------------
@memory_profiler
def controller():
    log = logging.getLogger("nspl.py")
    url = 'https://www.arcgis.com/sharing/rest/content/items/60484ad9611249b59f3644e92f37476d/data'
    file_count = 0
    la_dict = dict()

    conf = configparser.ConfigParser()
    conf.read('nspl_config.ini')
    la_pre = conf['NSPL']['LaNameFileStartsWith']
    pc_pre = conf['NSPL']['PostcodeFileStartsWith']
    file_suff = conf['NSPL']['FileExtension']

    response_zip = requests.get(url)
    file_path = r'/home/avr/downloads/nspl.zip'

    #with zipfile.ZipFile(io.BytesIO(response_zip.content)) as zips:
    with zipfile.ZipFile(file_path) as zips:
        la_ua = ([name for name in zips.namelist() if name.startswith(la_pre) and name.endswith(file_suff)][0])
        pcode = ([name for name in zips.namelist() if name.startswith(pc_pre) and name.endswith(file_suff)][0])

        # get the list of local authorities
        with io.TextIOWrapper(zips.open(la_ua), encoding='utf-8') as la_file:
            la_file.readline() # csv header

            for data_line in la_file:
                rec = data_line.split(',')
                la_dict[rec[0]] = rec[1]

        print(la_dict)


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