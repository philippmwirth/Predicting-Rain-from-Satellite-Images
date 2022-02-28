import os

from PIL import Image
import numpy as np
import argparse


WIDTH: int = 800
HEIGHT: int = 600
CHANNELS: int = 3


import csv
def read_csv(path):
    X = np.zeros((600, 800))
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        a = next(reader)
        b = next(reader)
        b = next(reader)
        for i, row in enumerate(reader):
            for j, val in enumerate(row[1:]):
                X[i, j] = float(val)
    return X


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('region', type=str,
                        help='One of "central_europe", "north_america", "mexico"')
    parser.add_argument('--mode', type=str, default='',
                        help='One of "", "stratiform", "convective"')
    parser.add_argument('--data', type=str, default='/datasets/meteomatics')
    args = parser.parse_args()

    # define some folder paths
    ir062_dir = f'{args.data}/{args.region}/sat_ir_062'
    ir108_dir = f'{args.data}/{args.region}/sat_ir_108'
    li_dir = f'{args.data}/{args.region}/lifted_index'
    target_dir = f'{args.data}/{args.region}/precip_5min:mm'
    output_dir_data = f'{args.data}/{args.region}/sat_ir'
    output_dir_target = f'{args.data}/{args.region}/target'
    os.makedirs(output_dir_data, exist_ok=True)
    os.makedirs(output_dir_target, exist_ok=True)

    # get input filenames
    ir062 = sorted(os.listdir(ir062_dir))
    for filename in ir062:

        print(f'Processing: {filename}')
        ir_array = np.zeros((HEIGHT, WIDTH, CHANNELS)).astype(np.uint8)

        # load ir062 to first color channel
        with Image.open(os.path.join(ir062_dir, filename)) as img:
            arr = np.asarray(img).astype(np.uint8)
            ir_array[:, :, 0] += arr[:, :, 0]

        # load ir108 to second color channel
        with Image.open(os.path.join(ir108_dir, filename)) as img:
            arr = np.asarray(img).astype(np.uint8)
            ir_array[:, :, 1] += arr[:, :, 0]

        # load target
        with Image.open(os.path.join(target_dir, filename)) as img:
            target_array = np.asarray(img).astype(np.uint8)

        if args.mode in ['stratiform', 'convective']:
            # load lifted index
            li = read_csv(
                os.path.join(li_dir, os.path.splitext(filename)[0] + '.csv')
            )
            # mask based on lifted index
            if args.mode == 'stratiform':
                mask = (li >= 0).astype(np.uint8)[:, :, None]
            else:
                mask = (li <= 0).astype(np.uint8)[:, :, None]
            ir_array *= mask
            target_array *= mask    

        # save to disk
        ir_img = Image.fromarray(ir_array)
        ir_img.save(os.path.join(output_dir_data, filename))

        target_img = Image.fromarray(target_array)
        target_img.save(os.path.join(output_dir_target, filename))
