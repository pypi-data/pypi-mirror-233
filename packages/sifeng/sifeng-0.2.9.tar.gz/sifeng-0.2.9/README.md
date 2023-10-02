# Si Feng

Si Feng (思风) is a quant research framework built by our team, SiFeng. It is mainly designed to be used within our team but welcomes public users. Feel free to tell us what features you want to add to this project.

## How to use

The project is posted on [github](https://github.com/zty200489/sifeng). To use this python package, simply install it from [PyPI](https://pypi.org/project/sifeng/) to your local environment with:

```console
pip install sifeng
```

## Features

### Data

Data is always crucial when it comes to quantitive analysis, information IS key. So, we provide simple-to-use access to Chinese stock market data. Using `sifeng.fetcher`, you can get access to daily data with ease.

### Models

Various state-of-the-art deep-learning models are already built-in, you can build, train, and evaluate your own quant model easily by calling `sifeng.dl`. More deep-learning models are on the way alongside many tree-based models as well as simple but always useful mathematical models.

## Updates

### Version 0.2.8

- Added mini-batch scheduler and renamed learn-rate scheduler.

### Version 0.2.7 (Bug fix)

- training loss should pass a Callable rather than a module for better customization

### Version 0.2.6

- Better `MixtureOfExpertsBlock`. (Fast MoE)
- Added reference to each model or module.
- Added mini-batching to `dl_trainer`.

### Version 0.2.5

- More options for the `dl_trainer`, you can now control custom learning rate curves.
- Added `ResidualBlock`.

### Version 0.2.4 (Bug fix)

- Trainer swapping yhat and y with trainset eval.

### Version 0.2.3

- Changed package file structure, now `sifeng.nn` is renamed to `sifeng.dl`.
- Updated the model stat analyzer, and added the sorting option.
- Added model trainer. With configurable optimizers, learning rate, early stopping, and so on.
- Useful deep-learning modules are added, including `MultiheadedSelfAttentionModule`, `AbsolutePositionalEncodingModule`, `FeedForwardLayer`, `TransformerEncoderBlock`, and `MixtureOfExpertsBlock`. 

### Version 0.2.2 (Bug fix)

- Model stat analyzer not outputting correctly with memory usage.

### Version 0.2.1
- Added torch model stat analyzer. Outputs info about model parameters and memory size. Sets the foundation for further analysis.

### Version 0.1.8

- Major update. We gave up the process of maintaining an online database and fetching data every time someone accessed it. Rather, we saved parquest files on Cloud Object Storage and fetched the required parquest files instead. Now, a local duckdb OLAP database will be used to process and fetch the data, allowing for much lower latency and much lower maintenance costs.
- Please note that due to the change in our implementation, previous versions are now deprecated.

### Version 0.1.7 (DEPRECATED)

- Due to limitations on the python version, grequests may have excessive warning logs that are quite annoying. So, we switched to a new implementation of parallel fetching with joblib.

### Version 0.1.6  (Bug fix) (DEPRECATED)

- Swapped processing sequence. Parsing data annually avoids running into forced-aborted connections.
- Ignored index when concating pandas dataframes.

### Version 0.1.5 (DEPRECATED)

- Added partitioned table support. Slicing up requests into year-specific subrequests, speeding up the search.

### Version 0.1.4 (DEPRECATED)

- Thread pooling fetchers based on grequests.
- kline and indicators are updated every day.

