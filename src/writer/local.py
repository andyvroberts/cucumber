import logging
import configparser
import pathlib

#------------------------------------------------------------------------------
def save_parquet_file(data, file_name):
    """
        write a parquet file within the "home" of the local filesystem.

        Args:
            data: parquet bytes
            save_dir: the local sub-directory under home
            file_name: the parquet file name (without the file extension)
            return: n/a
    """
    log = logging.getLogger("writer.local.save_parquet_file")
    conf = configparser.ConfigParser()
    conf.read('settings.ini')
    save_dir = conf['DATA']['LocalDirectory'] 

    home = pathlib.Path.home()
    save_dir = pathlib.Path.joinpath(home, save_dir)
    save_file = pathlib.Path.joinpath(save_dir, f'{file_name}.parquet')

    with open(save_file, 'wb') as write_it:
        write_it.write(data)

    log.info(f'Saved file: {save_file}')
