# SVision

[SVision](https://github.com/xjtu-omics/SVision) is a deep learning-based structural variants caller that takes aligned reads or contigs as input. Especially, SVision implements a targeted multi-objects recognition framework, detecting and characterizing both simple and complex structural variants from three-channel similarity images.

This file shows how SVision was installed on Polaris and characteristics of the run on Polaris.

```
# build SVision on Polaris
module load conda/2022-09-08
mkdir -p /lus/grand/projects/covid-ct/arodriguez/tools/svision
cd /lus/grand/projects/covid-ct/arodriguez/tools/svision

# download latest from Git repo
git clone https://github.com/xjtu-omics/SVision.git
cd SVision

## Create conda environment and install SVision 
conda env create -f environment.yml
python setup.py install

```
