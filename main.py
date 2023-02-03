import logging
import time
from n2yowrapper import *

logger = logging.getLogger()
logger.setLevel(logging.DEBUG) #NOTE: minimum logging level - set this to whatever suits your needs

#config logging
stream_handler = logging.StreamHandler() 
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO) 
file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG) 
logger.addHandler(stream_handler)
logger.addHandler(file_handler)


def tle_example():
    print(tle.satid)
    print(tle.satname)
    print(tle.transactions_count)
    print(tle.two_line_element)


def satallite_position_example():
    ps = n2yo.get_satellite_positions(25544,39.949242, -76.743683, 16, 5)

    print(ps.satid)
    print(ps.satname)
    print(ps.transactions_count)
    for k, v in ps.positions.items():
        print(f'SEC: {k}')
        print(v.sataltitude)
        print(v.satlatitude)
        print(v.azimuth)
        print(v.elevation)
        print(v.ra)
        print(v.dec)


if __name__ == '__main__':
    n2yo = N2yo()
    tle = n2yo.get_tle(25544)
    tle_example()
    satallite_position_example()