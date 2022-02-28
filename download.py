import os
import io
import time
import numpy as np
import argparse

from PIL import Image
from datetime import datetime
from dataclasses import dataclass

from meteomatics.api import query_api


URL = 'https://api.meteomatics.com'

STRFTIME = '%Y-%m-%dT%H:%M:%SZ'

IMAGE_W = 800
IMAGE_H = 600

REGIONS = {
    'north_america': {
        'lat_0': 60,
        'lon_0': -120,
        'lat_1': 30,
        'lon_1': -85,
    },
    'central_europe': {
        'lat_0': 65,
        'lon_0': -15,
        'lat_1': 35,
        'lon_1': 20,
    },
    'mexico': {
        'lat_0': 27.8417,
        'lon_0': -112.1654,
        'lat_1': 10.4812,
        'lon_1': -76.1187,
    }
}


@dataclass
class QueryParams:
    """TODO

    """
    image_w: int
    image_h: int
    lat_0: int
    lon_0: int
    lat_1: int
    lon_1: int
    timestamp: int

    def _to_url(self, base_url: str, type: str):
        """TODO

        """
        url = base_url
        url += f'/{datetime.utcfromtimestamp(self.timestamp).strftime(STRFTIME)}'
        url += f'/{type}'
        url += f'/{self.lat_0},{self.lon_0}_{self.lat_1},{self.lon_1}'
        if type == 'lifted_index:K':
            url += f':{self.image_w}x{self.image_h}/csv'
        else:
            url += f':{self.image_w}x{self.image_h}/png'
        return url.strip(' ')

    def sat_ir_108_url(self, base_url: str):
        """TODO: docstring """
        return self._to_url(base_url, 'sat_ir_108:K')

    def sat_ir_062_url(self, base_url: str):
        """TODO: docstring """
        return self._to_url(base_url, 'sat_ir_062:K')

    def lifted_index_url(self, base_url: str):
        """TODO: docstring """
        return self._to_url(base_url, 'lifted_index:K')

    def precip_5min_url(self, base_url: str):
        """TODO: docstring """
        return self._to_url(base_url, 'precip_5min:mm')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('user', type=str)
    parser.add_argument('pwd', type=str)
    parser.add_argument('--data', type=str, default='/datasets/meteomatics')
    args = parser.parse_args()

    now = time.time() - 60 * 60 # go 60 minutes back to make sure data exists

    for region, corners in REGIONS.items():

        print(f'{now} | Downloading data for region: {region}')
        
        params = QueryParams(
            IMAGE_W,
            IMAGE_H,
            corners['lat_0'],
            corners['lon_0'],
            corners['lat_1'],
            corners['lon_1'],
            now,
        )

        base_path = os.path.join(args.data, region)

        # get and save sat_ir_108
        path = os.path.join(base_path, 'sat_ir_108')
        os.makedirs(path, exist_ok=True)
        try:
            print(params.sat_ir_108_url(URL))
            response = query_api(params.sat_ir_108_url(URL), args.user, args.pwd)
        except Exception as e:
            print(f'ERROR: {e}')
            continue
        image = Image.open(io.BytesIO(response._content))
        image.save(os.path.join(path, str(int(now))) + '.png')

        # get and save sat_ir_062
        path = os.path.join(base_path, 'sat_ir_062')
        os.makedirs(path, exist_ok=True)
        try:
            response = query_api(params.sat_ir_062_url(URL), args.user, args.pwd)
        except Exception as e:
            print(f'ERROR: {e}')
            continue
        image = Image.open(io.BytesIO(response._content))
        image.save(os.path.join(path, str(int(now))) + '.png')

        # get and save sat_ir_108
        path = os.path.join(base_path, 'lifted_index')
        os.makedirs(path, exist_ok=True)
        try:
            response = query_api(params.lifted_index_url(URL), args.user, args.pwd)
        except Exception as e:
            print(f'ERROR: {e}')
            continue
        with open(os.path.join(path, str(int(now))) + '.csv', "wb") as binary_file:
            binary_file.write(response._content)

        # get and save sat_ir_108
        path = os.path.join(base_path, 'precip_5min:mm')
        os.makedirs(path, exist_ok=True)
        try:
            response = query_api(params.precip_5min_url(URL), args.user, args.pwd)
        except Exception as e:
            print(f'ERROR: {e}')
            continue
        image = Image.open(io.BytesIO(response._content))
        image.save(os.path.join(path, str(int(now))) + '.png')
