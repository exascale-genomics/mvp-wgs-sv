# SVision

[SVision](https://github.com/xjtu-omics/SVision) is a deep learning-based structural variants caller that takes aligned reads or contigs as input. Specially, SVision implements a targeted multi-objects recognition framework, detecting and characterizing both simple and complex structural variants from three-channel similarity images.

This file shows how SVision was installed on Polaris and characteristics of the run on Polaris. We will be downloading the models from the SVision repository and will use them to predict SVs on our data. We will not be building any models. HiFi sequence data is needed for building the models.

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
conda activate svisionenv
python setup.py install

#######
(/soft/datascience/conda/2022-09-08/svisionenv) arodriguez@polaris-login-02:/lus/grand/projects/covid-ct/arodriguez/tools/svision/SVision> SVision --help
usage: SVision [-h] -o OUT_PATH -b BAM_PATH -m MODEL_PATH -g GENOME -n SAMPLE
               [-t THREAD_NUM] [-s MIN_SUPPORT] [-c CHROM] [--hash] [--qname]
               [--graph] [--contig] [--debug] [--min_mapq MIN_MAPQ]
               [--min_sv_size MIN_SV_SIZE] [--max_sv_size MAX_SV_SIZE]
               [--window_size WINDOW_SIZE]
               [--patition_max_distance PATITION_MAX_DISTANCE]
               [--cluster_max_distance CLUSTER_MAX_DISTANCE]
               [--batch_size BATCH_SIZE] [--min_gt_depth MIN_GT_DEPTH]
               [--homo_thresh HOMO_THRESH] [--hete_thresh HETE_THRESH]
               [--k_size K_SIZE] [--min_accept MIN_ACCEPT]
               [--max_hash_len MAX_HASH_LEN]

SVision 1.3.8

Short Usage: SVision [parameters] -o <output path> -b <input bam path> -g <reference> -m <model path>

optional arguments:
  -h, --help            show this help message and exit

Input/Output parameters:
  -o OUT_PATH           Absolute path to output
  -b BAM_PATH           Absolute path to bam file
  -m MODEL_PATH         Absolute path to CNN predict model
  -g GENOME             Absolute path to your reference genome (.fai required
                        in the directory)
  -n SAMPLE             Name of the BAM sample name

Optional parameters:
  -t THREAD_NUM         Thread numbers (default: 1)
  -s MIN_SUPPORT        Minimum support read number required for SV calling
                        (default: 5)
  -c CHROM              Specific region (chr1:xxx-xxx) or chromosome (chr1) to
                        detect
  --hash                Activate local realignment for unmapped sequences
                        (default: False)
  --qname               Report support names for each events (default: False)
  --graph               Report graph for events (default: False)
  --contig              Activate contig mode (default: False)
  --debug               Activate debug mode and keep intermedia outputs
                        (default: False)

Collect parameters:
  --min_mapq MIN_MAPQ   Minimum mapping quality of reads to consider (default:
                        10)
  --min_sv_size MIN_SV_SIZE
                        Minimum SV size to detect (default: 50)
  --max_sv_size MAX_SV_SIZE
                        Maximum SV size to detect (default: 1000000)
  --window_size WINDOW_SIZE
                        The sliding window size in segment collection
                        (default: 10000000)

Cluster parameters:
  --patition_max_distance PATITION_MAX_DISTANCE
                        Maximum distance to partition signatures (default:
                        5000)
  --cluster_max_distance CLUSTER_MAX_DISTANCE
                        Clustering maximum distance for a partition (default:
                        0.3)

Predict parameters:
  --batch_size BATCH_SIZE
                        Batch size for the CNN prediction model (default: 128)

Genotype parameters:
  --min_gt_depth MIN_GT_DEPTH
                        Minimum reads required for genotyping (default: 4)
  --homo_thresh HOMO_THRESH
                        Minimum variant allele frequency to be called as
                        homozygous (default: 0.8)
  --hete_thresh HETE_THRESH
                        Minimum variant allele frequency to be called as
                        heterozygous (default: 0.2)

Hash table parameters:
  --k_size K_SIZE       Size of kmer (default: 10)
  --min_accept MIN_ACCEPT
                        Minimum match length for realignment (default: 50)
  --max_hash_len MAX_HASH_LEN
                        Maximum length of unmapped sequence length for
                        realignment (default: 1000)

#####

# you will manually have to download the model files from https://drive.google.com/drive/folders/1j74IN6kPKEx9hy3aENx3zHYPUnyYWGvj
# download to your computer and then transfer to polaris
# files:
# $ls /lus/grand/projects/covid-ct/arodriguez/tools/svision/SVision/models
# -rw-r--r--  1 arodri7     9420131 Oct 13 17:22 svision-cnn-model.ckpt.meta
# -rw-r--r--  1 arodri7         713 Oct 14 10:27 svision-cnn-model.ckpt.index
# -rw-r--r--  1 arodri7   227554836 Oct 14 10:27 svision-cnn-model.ckpt.data-00000-of-00001

```

We will now be able to submit the SVision job on the 30X HG00138 sample BAM file that was generated with Parabricks:

```
qsub -A covid-ct -I -l select=1 -l walltime=1:00:00 -l filesystems=home:eagle -q debug

module load conda/2022-09-08
conda activate svisionenv

# modify the command line
mkdir /lus/grand/projects/covid-ct/arodriguez/wgs_test/HG00138/output/30x/svision_out
cd /lus/grand/projects/covid-ct/arodriguez/wgs_test/HG00138/output/30x/svision_out
SVision -o /lus/grand/projects/covid-ct/arodriguez/wgs_test/HG00138/output/30x/svision_out -b /lus/grand/projects/covid-ct/arodriguez/wgs_test/HG00138/output/30x/HG00138.bam -m /lus/grand/projects/covid-ct/arodriguez/tools/svision/SVision/models/svision-cnn-model.ckpt -g /lus/grand/projects/covid-ct/arodriguez/wgs_test/reference/GRCh38_CRAM/GRCh38_full_analysis_set_plus_decoy_hla.fa -n HG00138 -s 5 --graph --qname

```
