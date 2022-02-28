# Predicting Rain from Satellite Images

How to train a neural network to predict precipitation based on satellite images pulled from the Meteomatics API.

## Usage

### Download Data
In order to download data from the [Meteomatics API](https://meteomatics.com), you need to have a `user` and `password`. Then, you can simply use the `download.py` script:
```
usage: download.py [-h] [--data DATA] user pwd
```
This script will download a single input/output pair for each of the three predefined regions (Central Europe, North America, and Mexico) at the current timestamp. In order to use this data for training, it needs to be processed first, see [Process Data](#process-data).


### Process Data
TODO: Show how to pre-process data.

### Train
To train a model on the downloaded data, use the following commands:
```
cd Pytorch-ENet
python main.py \
    --save-dir ./save/ \
    --dataset meteomatics \
    --dataset-dir PATH/TO/YOUR/DATASET \
    --with-unlabeled \
    --weighing mfb
cd ..
```

### Test
To test a model, use:
```
cd Pytorch-ENet
python main.py \
    -m test  \
    --save-dir ./save/ \
    --dataset meteomatics \
    --dataset-dir PATH/TO/YOUR/DATASET \
    --with-unlabeled \
    --imshow-batch
cd ..
```

## Links
 - [Part 1](https://www.lightly.ai/post/predicting-rain-from-satellite-images-part-1)
 - [Part 2](https://www.lightly.ai/post/predicting-rain-from-satellite-images-part-2)
 - [Towards Data Science](https://towardsdatascience.com/predicting-rain-from-satellite-images-c9fec24c3dd1)
 - [Lightly](https://www.lightly.ai/)
 - [Meteomatics](https://www.meteomatics.com)