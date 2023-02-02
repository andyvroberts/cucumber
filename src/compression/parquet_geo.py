import logging
import pyarrow

#------------------------------------------------------------------------------
def postcode_local_authority_map(data):
    """
        accept the list of tuples (postcode, la count, la name list) and 
        compress into a parquet file format.

        Args:
            data: a list of tuples, aprrox. 2.2 million postcodes
            return: a compressed parquet table
    """
    log = logging.getLogger("parpostcode_local_authority_map")
    

    return None