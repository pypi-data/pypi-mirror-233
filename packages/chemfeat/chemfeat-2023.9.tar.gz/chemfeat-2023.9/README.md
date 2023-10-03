---
title: README
author: Jan-Michael Rye
---

![ChemFeat logo](https://gitlab.inria.fr/jrye/chemfeat/-/raw/main/img/chemfeat_logo.svg)

# Synopsis

Generate molecular feature vectors for machine- and deep-learning models using cheminformatics software packages. A configuration file is used to select and configure different feature sets for inclusion in the full feature vector. The full list of available feature sets is available [here](https://jrye.gitlabpages.inria.fr/chemfeat/gen_features.html). The results of feature set calculations are cached in an [SQLite](https://www.sqlite.org/index.html) database to avoid the overhead of redundant calculations when feature sets are re-used.

The following packages are currently used to calculate chemical features:

* [RDKit](https://pypi.org/project/rdkit/)
* [PaDEL-pywrapper](https://pypi.org/project/PaDEL-pywrapper/)


# Links

* [GitLab](https://gitlab.inria.fr/jrye/chemfeat)
* [Documentation](https://jrye.gitlabpages.inria.fr/chemfeat/)
* [Python Package](https://pypi.org/project/chemfeat/)



# Installation

The package can be installed from the [Python Package Index](https://pypi.org/project/chemfeat/) with any compatible Python package manager, e.g.

~~~
pip install chemfeat
~~~

To install from source, clone the Git repository and install the package directly:

~~~
git clone https://gitlab.inria.fr/jrye/chemfeat.git
pip install ./chemfeat
~~~


# Usage

## Command-Line

The package provides the `chemfeat` command-line tool to generated CSV files of feature vectors from lists of InChi strings. It can also be used to generate a template feature-set configuration file and a markdown document describing all of the feature sets. The command's various help messages can be found [here](https://jrye.gitlabpages.inria.fr/chemfeat/gen_command_help.html).

### Usage Example

Given a feature set configuration file ("feature_sets.yaml") and a CSV file with a column of InChi strings ("inchis.csv"), a CSV file out features ("features.csv") can be generated with the following command:

~~~sh
chemfeat calc feature_sets.yaml inchis.csv features.csv
~~~

The following sections contain example contents for the input files and the output file that they produce.

#### feature_sets.yaml

Example feature set configuration file. Note that the feature sets are specified as a list, which allows the same feature set to be use multiple times with different parameters. For the full list of features, see the [feature descriptions](https://jrye.gitlabpages.inria.fr/chemfeat/gen_features.html) and the [configuration file template](https://jrye.gitlabpages.inria.fr/chemfeat/gen_feature_set_configuration.html).

~~~yaml
# QED feature calculator.
- name: qed

# RDK descriptor feature calculator.
- name: rdkdesc
~~~

#### inchis.csv

Example CSV input file with a column containing InChi values. The name of the InChi column is configurable and defaults to "InChi".

~~~
InChi,name
"InChI=1S/C8H9NO2/c1-6(10)9-7-2-4-8(11)5-3-7/h2-5,11H,1H3,(H,9,10)","paracetamol"
"InChI=1S/C13H18O2/c1-9(2)8-11-4-6-12(7-5-11)10(3)13(14)15/h4-7,9-10H,8H2,1-3H3,(H,14,15)","ibuprofen"
~~~

#### featurs.csv

The CSV feature file that results from the example input files above.

~~~
InChi,qed__ALERTS,qed__ALOGP,qed__AROM,qed__HBA,qed__HBD,qed__MW,qed__PSA,qed__ROTB,rdkdesc__FpDensityMorgan1,rdkdesc__FpDensityMorgan2,rdkdesc__FpDensityMorgan3,rdkdesc__MaxAbsPartialCharge,rdkdesc__MaxPartialCharge,rdkdesc__MinAbsPartialCharge,rdkdesc__MinPartialCharge,rdkdesc__NumRadicalElectrons,rdkdesc__NumValenceElectrons
"InChI=1S/C8H9NO2/c1-6(10)9-7-2-4-8(11)5-3-7/h2-5,11H,1H3,(H,9,10)",2,2.0000999999999998,1,2,2,151.16500000000002,52.82000000000001,1,1.2727272727272727,1.8181818181818181,2.272727272727273,0.5079642937129114,0.18214293782620056,0.18214293782620056,-0.5079642937129114,0,58
"InChI=1S/C13H18O2/c1-9(2)8-11-4-6-12(7-5-11)10(3)13(14)15/h4-7,9-10H,8H2,1-3H3,(H,14,15)",0,3.073200000000001,1,2,1,206.28499999999997,37.3,4,1.2,1.7333333333333334,2.1333333333333333,0.4807885019257389,0.3101853515323108,0.3101853515323108,-0.4807885019257389,0,82
~~~


## Python API

~~~python
from chemfeat.database import FeatureDatabase
from chemfeat.features.manager import FeatureManager

# Here we assume that the following variables have already been defined:
# 
# feat_specs:
#   A list of feature specifications as returned by loading a YAML feature-set
#   configuration file.
#
# inchis:
#   An iterable of InChi strings representing the molecules for which the
#   features should be calculated.


# Create the database object.
feat_db = FeatureDatabase('features.sqlite')

# Create the feature manager object.
feat_man = FeatureManager(feat_db, feat_specs)

# Calculate the features and retrieve them as a Pandas dataframe.
feat_dataframe = feat_man.calculate_features(inchis, return_dataframe=True)
~~~
