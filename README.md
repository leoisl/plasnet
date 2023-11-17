# plasnet

Python package for clustering, typing, visualisation and exploration of plasmid networks.

[![Python CI](https://github.com/leoisl/plasnet/actions/workflows/ci.yaml/badge.svg)](https://github.com/leoisl/plasnet/actions/workflows/ci.yaml/badge.svg)
![coverage badge](./coverage.svg)
[![PyPI](https://img.shields.io/pypi/v/plasnet)](https://pypi.org/project/plasnet/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/plasnet)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## TLDR

`plasnet` allows you to cluster, type and visualise plasmids given their evolutionary distance, computed upstream.

### split

The first `plasnet` command is `split`. It creates a plasmid graph given a list of plasmids and their pairwise distances.
It then splits this graph into communities. Communities are groups of plasmids that roughly connected to each other.
This command allows you to view the full plasmids graph and also the isolated communities.

[Click here to view an example of the full plasmid graph from the latest version on an example dataset](https://leoisl.github.io/plasnet/split_out/visualisations/single_graph/single_graph.html)

[Click here to view an example of the isolated communities from the latest version on an example dataset](https://leoisl.github.io/plasnet/split_out/visualisations/communities/index.html)

### type

This command allows you to refine the communities defined in the `split` command into types or subcommunities.
The idea is that you can use a more precise distance function to type the communities than the one used to split the graph.
The different types or subcommunities will have different colours in the visualisation.

[Click here to view an example of the typed communities from the latest version on an example dataset](https://leoisl.github.io/plasnet/type_out/visualisations/communities/index.html)

[Click here to view an example of the typed isolated subcommunities from the latest version on an example dataset](https://leoisl.github.io/plasnet/type_out/visualisations/subcommunities/index.html)

### add-sample-hits

This command allows you to add sample hits annotations on top of previously identified subcommunities or types
in the `type` command. With this command you can explore the subcommunities several different samples hit in more
details and check if they are, for example, sharing plasmids.

[Click here to view an example of two samples hitting a subcommunity](https://leoisl.github.io/plasnet/add_sample_hits_out/visualisations/sample_graphs/graphs/community_1_subcommunity_40.html/)


## Installation

```
pip install plasnet
```

## Usage

### General usage

```
Usage: plasnet [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  split  Creates and split a plasmid graph into communities
  type   Type the communities of a previously split plasmid graph into...
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

### add-sample-hits subcommand

```
Usage: plasnet add-sample-hits [OPTIONS] SUBCOMMUNITIES_PICKLE SAMPLE_HITS
                               OUTPUT_DIR

  Add sample hits annotations on top of previously identified subcommunities
  or types

Options:
  --help  Show this message and exit.

  Add sample hits annotations on top of previously identified subcommunities or types.

  The first file, describing the subcommunities, is a pickle file (.pkl) that can be found in <type_out_dir>/objects/subcommunities.pkl,
  where <type_out_dir> is the output dir of the type command.

  The sample-hits file is a tab-separated file with 2 columns: sample, plasmid.
  These columns are self-explanatory and identifies the plasmids present in each sample.
  Example of such file:
  sample              plasmid
  cpe001_trim_ill     NZ_CP006799.1
  cpe001_trim_ill     NZ_CP028929.1
  cpe002_trim_ill     NZ_CP079159.1
  cpe005_trim_ill     NZ_CP006799.1
  cpe005_trim_ill     NZ_CP079676.1
  cpe010_trim_ill     NZ_CP028929.1
  cpe020_trim_ill     NZ_CP006799.1
  cpe020_trim_ill     NZ_CP079676.1
  cpe021_trim_ill     NZ_CP006799.1
```