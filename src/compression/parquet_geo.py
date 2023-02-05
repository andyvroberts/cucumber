import logging
import pyarrow as pa
import pyarrow.parquet as pq

#------------------------------------------------------------------------------
def postcode_local_authority_map(nspl_tuple, writer):
    """
        accept the list of tuples (postcode, la count, la name list) and 
        compress into a parquet file format.

        Args:
            data: a list of tuples, aprrox. 2.2 million postcodes
            writer: the write module specifies where to save the parquet file
            return: n/a
    """
    log = logging.getLogger("compression.parquet_geo.postcode_local_authority_map")

    # construct the parquet table
    parq_arr = {
        'Postcode': pa.array([col[0] for col in nspl_tuple], type='string'),
        'Count': pa.array([col[1] for col in nspl_tuple], type=pa.int32()),
        'Authorities': pa.array([col[2] for col in nspl_tuple], type=pa.list_(pa.string()))
    }
    table = pa.Table.from_pydict(parq_arr)
    buf = pa.BufferOutputStream()
    pq.write_table(table, buf)

    # send the buffer stream to the writer function
    writer.save_parquet_file(buf.getvalue().to_pybytes(), 'PostcodeToLA')
