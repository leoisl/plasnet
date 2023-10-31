# plasnet

Python package for clustering, visualisation and exploration of plasmid networks.

Code under heavy development, not expected to work and not refactored for now.


## Installation

```
pip install git+https://github.com/leoisl/plasnet
```

## Usage

```
Usage: plasnet [OPTIONS] DISTANCES OUTPUT_DIR

Options:
  -d, --distance-threshold FLOAT  Distance threshold
  -b, --bh-connectivity INTEGER   Minimum number of connections a plasmid need
                                  to be considered a blackhole plasmid
  -e, --bh-neighbours-edge-density FLOAT
                                  Maximum number of edge density between
                                  blackhole plasmid neighbours to label the
                                  plasmid as blackhole
  -p, --output-plasmid-graph      Also outputs the full, unsplit, plasmid
                                  graph
  --help                          Show this message and exit.

  Creates and split a plasmid graph into communities.
  The plasmid graph is defined by a plasmid distances file.
  The distances file is a tab-separated file with 3 columns: plasmid_1, plasmid_2, distance.
  plasmid_1 and plasmid_2 are plasmid names, and distance is a float between 0 and 1.
  The distance threshold is the minimum distance value for two plasmids to be considered connected.

  Example of such file:
  plasmid_1       plasmid_2       distance
  AP024796.1      AP024825.1      0.8
  AP024796.1      CP012142.1      0.5
  AP024796.1      CP014494.1      0.3
  AP024796.1      CP019149.1      0.0
  AP024796.1      CP021465.1      0.0
  AP024796.1      CP022675.1      1.0
  AP024796.1      CP024687.1      0.0
  AP024796.1      CP026642.1      0.5
  AP024796.1      CP027485.1      0.8
```