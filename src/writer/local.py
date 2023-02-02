import logging
import pathlib

#------------------------------------------------------------------------------
def save_parquet_file(data, save_dir, file_name):
    """
        write a parquet file within the "home" of the local filesystem.

        Args:
            data: parquet bytes
            save_dir: the local sub-directory under home
            file_name: the parquet file name (without the file extension)
            return: n/a
    """
    log = logging.getLogger("writer.local.save_parquet_file")
    home = pathlib.Path.home()
    save_dir = pathlib.Path.joinpath(home, save_dir)
    save_file = pathlib.Path.joinpath(save_dir, f'{file_name}.parquet')

    

    log.info(f'Saving file: {save_file}')
