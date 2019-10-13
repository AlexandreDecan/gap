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
           [--text | --csv | --json | --plot [PLOT]]
           [PATH [PATH ...]]
```

In its simplest form, GAP only requires a path to the git repositories of the software projects that need to be analysed. One or more such repositories can be provided as input, depending on the scope of the analysis. For example, a company may desire to analyse the commit activity of all its paid contributors in the open source projects the company is involved in; a package maintainer may desire to analyse the global activity of all the packages he is maintaining; a package developer may wish to analyse the activity in a project and all its dependents; and so on.

By default, GAP analyses all branches of each repository but the list of branches to analyse can be specified.
Optionally, a list mapping multiple authors into specific identities can be provided. Such mapping files can be used to support identity merging, data anonymization, or to exclude specific authors from the analysis.
Parameters can be provided to set the date of the analysis (current date by default), the number of observations used by the model (20 by default), the list of probability values (0.5, 0.7 and 0.9 by default), and the minimal recency of the last activity (30 days by default).

```
$ gap ./repo --date 2019-05-01 --probs 0.5 0.7 0.9 --mapping anon.csv
  author          last        0.5         0.7         0.9
bots (grouped)  2019-05-01  2019-05-01  2019-05-01  2019-05-02
T. Hall         2019-05-01  2019-05-01  2019-05-02  2019-05-03
R. Cox          2019-04-30  2019-05-02  2019-05-03  2019-05-07
D. Mckinney     2019-04-29  2019-04-30  2019-05-07  2019-05-23
A. Gomez        2019-04-29  2019-05-04  2019-05-05  2019-05-14
C. Jordan       2019-04-29  2019-04-30  2019-05-02  2019-05-06
H. Hawkins      2019-04-27  2019-04-30  2019-05-04  2019-05-19
R. Warren       2019-04-26  2019-04-26  2019-04-27  2019-04-29
R. Martin       2019-04-26  2019-05-03  2019-05-12  2019-08-19
N. Erickson     2019-04-25  2019-04-28  2019-05-04  2019-05-17
W. Brewer       2019-04-25  2019-04-27  2019-05-03  2019-05-24
R. Thompson     2019-04-12  2019-04-13  2019-04-17  2019-05-09
R. Reilly       2019-04-11  2019-05-08  2019-05-24  2019-05-29
```

To ease their reuse by other automated tools, the forecasts can be exported into four different formats: (i) simple text, (ii) comma-separated values (csv), (iii) JSON, and (iv) bar activity charts.
GAP output results can also be used as a basis for a project-level dashboard that visualises the project's past and estimated future commit activities.

