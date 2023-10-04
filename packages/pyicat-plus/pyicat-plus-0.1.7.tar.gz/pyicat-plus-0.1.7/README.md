# PyIcat-Plus

A python client for ICAT+.

## Getting started

Register raw datasets with ICAT

```bash
icat-store-raw --beamline id00 \
    --proposal id002207 \
    --path /data/visitor/path/to/dataset1 \
    --dataset test1 \
    --sample mysample

icat-store-raw --beamline id00 \
    --proposal id002207 \
    --path /data/visitor/path/to/dataset2 \
    --dataset test2 \
    --sample mysample
```

Register processed data with ICAT

```bash
icat-store-processed --beamline id00 \
    --proposal id002207 \
    --path /data/visitor/path/to/processed \
    --dataset testproc \
    --sample mysample \
    --raw /data/visitor/path/to/dataset1 \
    --raw /data/visitor/path/to/dataset2
```

## Test

With threads

```bash
python -m pip install -e .[test]
pytest
```

With gevent

```bash
python -m pip install -e .[test]
python -m pip install gevent
python -m gevent.monkey --module pytest
```

## Documentation

https://pyicat-plus.readthedocs.io/
