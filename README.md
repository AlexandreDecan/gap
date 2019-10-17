# GAP: Forecasting Commit Activity in git Projects

This repository contains the GAP tool used in our paper *GAP: Forecasting Commit Activity in git Projects*. A link to the paper will be added to this README as soon as the paper is available.


## Abstract

Abandonment of active developers poses a significant risk for many open source software projects. This risk can be reduced by forecasting the future activity of contributors involved in such projects.

Focusing on the commit activity of individuals involved in git repositories, we proposes a practical probabilistic forecasting model based on the statistical technique of survival analysis.

The model is empirically validated on a wide variety of projects accounting for 7,528 git repositories and 5,947 active contributors.

This model is implemented as part of an open source tool, called gap, that predicts future commit activity.


## The GAP tool

GAP makes it possible to analyse and forecast developer activity in the form of git commits.
The tool is available at the root of this repository (*gap.py*). The tool can be downloaded and used as a Python script (the usual way) or installed through pip (`pip install git+https://github.com/AlexandreDecan/gap`). The dependencies will be automatically installed.
Gap is released under LGPL3.

```
$ gap -h
usage: gap [-h] [--date DATE] [--obs OBS]
           [--probs [PROB [PROB ...]]]
           [--limit LIMIT] [--mapping [MAPPING]]
           [--branches [BRANCH [BRANCH ...]]]
           [--as-dates]
           [--text | --csv | --json | --plot [PLOT]]
           [PATH [PATH ...]]
```

In its simplest form, GAP only requires a path to the git repositories of the software projects that need to be analysed. One or more such repositories can be provided as input, depending on the scope of the analysis. For example, a company may desire to analyse the commit activity of all its paid contributors in the open source projects the company is involved in; a package maintainer may desire to analyse the global activity of all the packages he is maintaining; a package developer may wish to analyse the activity in a project and all its dependents; and so on.

By default, GAP analyses all branches of each repository but the list of branches to analyse can be specified.
Optionally, a list mapping multiple authors into specific identities can be provided. Such mapping files can be used to support identity merging, data anonymization, or to exclude specific authors from the analysis.
Parameters can be provided to set the date of the analysis (current date by default), the number of observations used by the model (20 by default), the list of probability values (0.5, 0.6, 0.7, 0.8 and 0.9 by default), and the minimal recency of the last activity (30 days by default).
Predictions can be expressed either as dates or as relative time differences (by default).


```
$ gap ./repo --date 2019-05-16 --probs 0.5 0.7 0.9 --mapping anon.csv
               last  0.5  0.6 0.7 0.8  0.9
author
D. Young          0    1    1   2   3    4
Z. Andrews        0    4    5   8  10   23
D. Johnson        0    2    3   4   4    8
J. Berry          0    3    6   7  29  131
B. Rodriguez      0    1    1   3   3    6
bots (grouped)    0    1    1   1   1    2
M. Johnston       0    3    3   4   6    7
L. Owen          -1    3    7   7  17   22
S. Allen         -2    3    7  12  25   38
J. Schultz       -4    5   10  13  23   38
J. Smith         -4    0    3   6   7   21
M. Fry           -9   -6   -3   0   8   21
J. Lopez        -17  -11  -11  -9  -6   -1
S. Lewis        -20  -12  -10  -3  50   96
```

The output shows, for each recently active contributor (first column), the time difference in days since the last known commit activity (second column), and the expected number of days until the next predicted day of activity according to a certain probability threshold ranging between $0.5$ and $0.9$ (remaining columns).
The names shown in the output are anonymised and replaced by auto-generated names based on the input mapping file *anon.csv* that we have created for that purpose.

To ease their reuse by other automated tools, the forecasts can be exported into four different formats: (i) simple text, (ii) comma-separated values (csv), (iii) JSON, and (iv) bar activity charts.
GAP output results can also be used as a basis for a project-level dashboard that visualises the project's past and estimated future commit activities.

