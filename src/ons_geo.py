import sys
import time
import logging
import argparse
from nspl import political_geo
from writer import local

#------------------------------------------------------------------------------
def controller(args):
    log = logging.getLogger("postcodes.py")
    start_exec = time.time()

    if args.mapping == 'laua':
        if args.searched is not None:
            arg_split = args.searched.upper().split(',')
            sl = [x for x in arg_split]
            pc_la_map = political_geo.postcode_local_authority_search(sl)
            print(pc_la_map)
        else:
            pc_la_map = political_geo.postcode_local_authority_map()
            print(pc_la_map[1])


    end_exec = time.time()
    duration = end_exec - start_exec
    hours, hrem = divmod(duration, 3600)
    mins, secs = divmod(hrem, 60)
    log.info(f"Finished process: {hours}:{mins}:{round(secs, 2)}.")

#------------------------------------------------------------------------------
def parse_command_line():
    """
        The ons_geo module can initiate a variety of geographic data mappings.
        1. Postcode processes:
            i.  LA Name to Postcode Mapping
        2. Health Authority processes:
            i.  County to Health Authority Mapping

        Args:
            Return: the parsed results of the command line arguments.
    """
    par = argparse.ArgumentParser(prog='ONSGeo')
    subpars = par.add_subparsers(help='sub command help')

    par_pcode = subpars.add_parser('postcode', help='postcode processing')
    par_pcode.add_argument('mapping', choices=["laua"], help='type of mapping to apply to postcodes')
    par_pcode.add_argument('searched', type=str, nargs='?', help='a list of postcodes to search for within the mapping')

    par_health = subpars.add_parser('health', help='health authority processing')
    par_health.add_argument('mapping', choices=["county"], help='type of mapping to apply to health authorities')

    args = par.parse_args()
    return args

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
    args = parse_command_line()
    controller(args)