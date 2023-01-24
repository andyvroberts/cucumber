import sys
import io
import logging
import requests
import zipfile

#------------------------------------------------------------------------------
def controller():
    log = logging.getLogger("nspl.py")
    url = 'https://www.arcgis.com/sharing/rest/content/items/60484ad9611249b59f3644e92f37476d/data'
    file_count = 0

    response_zip = requests.get(url)

    with zipfile.ZipFile(io.BytesIO(response_zip.content)) as zips:
        la_ua = [name for name in zips.namelist() if name.startswith('Documents/LA_UA names and codes UK') and name.endswith('.csv')]
        print(la_ua)
        # for zipinfo in zips.infolist():
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

    controller()