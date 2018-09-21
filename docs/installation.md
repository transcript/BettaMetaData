## BettaMetadata Installation

### Dependencies

* Linux system
* [Conda](https://conda.io/docs/user-guide/install/linux.html)

#### Conda method

The way I install conda:

```
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
conda config --set always_yes yes
conda update -q conda
```

The easiest way to install BettaMetadata is to install the conda package

```
conda create -n metadata_validator python=3.5
source activate metadata_validator
conda install -c adamkoziol bettametadata
```

### Testing

[Unit tests](tests.md)

