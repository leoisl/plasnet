# plasnet

Python package for clustering, typing, visualisation and exploration of plasmid networks.

Code under heavy development, not expected to work and not refactored for now.


## Installation

```
pip install git+https://github.com/leoisl/plasnet
```

## Usage

### General usage

```
Usage: plasnet [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  split  Creates and split a plasmid graph into communities
  type   Type a previously split plasmid graph into subcommunities or types

```

### split subcommand

```
Usage: plasnet split [OPTIONS] PLASMIDS DISTANCES OUTPUT_DIR

  Creates and split a plasmid graph into communities

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
  The plasmid graph is defined by plasmid and distance files.

  The plasmid file is a tab-separated file with one column describing all plasmids in the dataset.
  Example of such file:
  plasmid
  AP024796.1
  AP024825.1
  CP012142.1
  CP014494.1
  CP019149.1
  CP021465.1
  CP022675.1
  CP024687.1
  CP026642.1
  CP027485.1

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

### type subcommand

```
Usage: plasnet type [OPTIONS] COMMUNITIES_PICKLE DISTANCES OUTPUT_DIR

  Type the communities of a previously split plasmid graph into subcommunities
  or types

Options:
  -d, --distance-threshold FLOAT  Distance threshold
  --small-subcommunity-size-threshold INTEGER
                                  Subcommunities with size up to this
                                  parameter will be joined to neighbouring
                                  larger subcommunities
  --help                          Show this message and exit.

  Type the communities of a previously split plasmid graph into subcommunities or types.
  This typing is based on running an asynchronous label propagation algorithm on the previously identified communities.
  This algorithm is implemented in the networkx library, and relies on a given distance file.
  This distance file should be a more precise and careful distance function than the one used to split the graph into communities.
  For example, you could use gene jaccard distance to split the graph and the DCJ-indel distance to type the communities.
  See https://github.com/iqbal-lab-org/pling for a tool to compute gene jaccard and DCJ-indel distances. 

  The first file, describing the communities, is a pickle file (.pkl) that can be found in <split_out_dir>/objects/communities.pkl,
  where <split_out_dir> is the output dir of the split command.

  The distances file is a tab-separated file with 3 columns: plasmid_1, plasmid_2, distance.
  plasmid_1 and plasmid_2 are plasmid names, and distance is a float number.
  The distance threshold is the minimum distance value for two plasmids to be considered connected.
  Example of such file:
  plasmid_1       plasmid_2       distance
  AP024796.1      AP024825.1      4
  AP024796.1      CP012142.1      10
  AP024796.1      CP014494.1      20
  AP024796.1      CP019149.1      1
  AP024796.1      CP021465.1      0
  AP024796.1      CP022675.1      50
  AP024796.1      CP024687.1      1000
  AP024796.1      CP026642.1      20
  AP024796.1      CP027485.1      1
```