## NVIDIA Clara Parabricks
First we will try [NVIDIA Clara-Parabricks](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/clara/containers/clara-parabricks). 
The container is distributed via Docker and unfortunately Polaris does not allow usage of Docker. In order to use Parabricks within Polaris we must first create a Singularity container:

```
module use /soft/spack/gcc/0.6.1/install/modulefiles/Core
module load singularityce
mkdir -p /grand/projects/GeomicVar/rodriguez/1kg_proj/data/tools/singularity
cd /grand/projects/GeomicVar/rodriguez/1kg_proj/data/tools/singularity
singularity build --tmpdir ~/. parabricks-4.3 docker://nvcr.io/nvidia/clara/clara-parabricks:4.3.1-1
INFO:    Starting build...
2024/09/05 17:40:26  info unpack layer: sha256:43f89b94cd7df92a2f7e565b8fb1b7f502eff2cd225508cbd7ea2d36a9a3a601
2024/09/05 17:40:39  info unpack layer: sha256:03bb9eb021f579ed871d5fee2344ba68d4509e9fc3b8865cf47fad506fa2f5d7
2024/09/05 17:40:41  info unpack layer: sha256:d1937dd2edf2b94d5f600d1112c804645e3d345cb93bf15444910612534f1f41
2024/09/05 17:40:43  info unpack layer: sha256:89aa5c6f87943c439cf2ceb52a6b13506ea6a1e614d14570b407ae3dfeede332
2024/09/05 17:40:43  info unpack layer: sha256:7d4f0f8effa7864e2b25cac47ecb80e71881841ce2b2a32d9e4c06d5696635b5
2024/09/05 17:40:43  info unpack layer: sha256:2e1379a5fd14b0e684aeb7f7bf34b0b50e80ca7551a6c1a0ace50b1a0149f9e1
2024/09/05 17:40:43  info unpack layer: sha256:40c6e206a72e5e93e0b12922d7228543e2d5648bc6232937b43d203391d3d155
2024/09/05 17:40:44  info unpack layer: sha256:b3c41b60ddb7d609c66bad32d4ee89b59a3984cbe62029a30a1194a8c7caa46f
2024/09/05 17:42:18  info unpack layer: sha256:74f8fe54ba6ab9ac1f9b60686c46313527afa5213bf776cc67b46f43227ffea3
2024/09/05 17:42:25  info unpack layer: sha256:16d5150597159a2ed7d42c7faec7286e0c58f03ff26481e01c2d82798e689d80
2024/09/05 17:42:55  info unpack layer: sha256:f4bde4daf907b776c848514d23aa152734294c5d0f37b3147d4df9989ee6062b
2024/09/05 17:42:55  info unpack layer: sha256:7a555e5e8ddc2f92d649acc07bafa080b9169251582be2a5056368648a218a41
INFO:    Creating SIF file...
INFO:    Build complete: parabricks-4.3
```

Now we can go ahead and test a simple job to see if our Singularity container build was a success.

```
arodriguez@x3004c0s13b1n0:~> qsub -A geomicVar -I -l select=1 -l walltime=1:00:00 -l filesystems=home:eagle -q debug
qsub: waiting for job 2082735.polaris-pbs-01.hsn.cm.polaris.alcf.anl.gov to start
qsub: job 2082735.polaris-pbs-01.hsn.cm.polaris.alcf.anl.gov ready

module use /soft/spack/gcc/0.6.1/install/modulefiles/Core
module load singularityce
cd /grand/projects/GeomicVar/rodriguez/1kg_proj/data/tools/singularity
arodriguez@x3004c0s13b1n0:~> singularity exec  --bind /grand/projects/GeomicVar/rodriguez:/grand/projects/GeomicVar/rodriguez ./parabricks-4.3 pbrun -h
INFO:    Converting SIF file to temporary sandbox...
Please visit https://docs.nvidia.com/clara/#parabricks for detailed documentation

usage: pbrun <command> [<args>]
Help: pbrun -h

command can be a TOOL or FULL PIPELINE. Example:
pbrun fq2bam --ref genome.fa --in-fq sample_1.fq.gz sample_2.fq.gz --out-bam sample.bam
pbrun germline --ref genome.fa --in-fq sample_1.fq.gz sample_2.fq.gz --out-bam sample.bam --out-variants sample.vcf

command options for standalone TOOL

applybqsr               - Apply BQSR report to a BAM file and generate a new BAM file
bam2fq                  - Convert a BAM file to FASTQ
bammetrics              - Collect WGS Metrics on a BAM file
bamsort                 - Sort a BAM file
bqsr                    - Collect BQSR report on a BAM file
collectmultiplemetrics  - Collect multiple classes of metrics on a BAM file
dbsnp                   - Annotate variants based on a dbsnp
deepsomatic             - Run GPU-DeepSomatic for calling somatic variants
deepvariant             - Run GPU-DeepVariant for calling germline variants
fq2bam                  - Run bwa mem, co-ordinate sorting, marking duplicates, and Base Quality Score Recalibration
fq2bam_meth             - Run GPU-accelerated bwa-meth compatible alignment, co-ordinate sorting, marking duplicates, and Base Quality Score Recalibration
fq2bamfast              - Run newly optimized version of bwa mem, co-ordinate sorting, marking duplicates, and Base Quality Score Recalibration
genotypegvcf            - Convert a GVCF to VCF
haplotypecaller         - Run GPU-HaplotypeCaller for calling germline variants
indexgvcf               - Index a GVCF file
markdup                 - Identifies duplicate reads
minimap2                - Align long read sequences against a large reference database to convert FASTQ to BAM/CRAM
mutectcaller            - Run GPU-Mutect2 for tumor-normal analysis
postpon                 - Generate the final VCF output of doing mutect pon
prepon                  - Build an index for PON file, which is the prerequisite to performing mutect pon
rna_fq2bam              - Run RNA-seq data through the fq2bam pipeline
starfusion              - Identify candidate fusion transcripts supported by Illumina reads

command options for commonly used FULL PIPELINES

deepvariant_germline    - Run the germline pipeline from FASTQ to VCF using a deep neural network analysis
pacbio_germline         - Run the germline pipeline from FASTQ to VCF by aligning long read sequences with minimap2 and using a deep neural network analysis
germline                - Run the germline pipeline from FASTQ to VCF
somatic                 - Run the somatic pipeline from FASTQ to VCF

Information about the software
version                 - Current version of Parabricks

Please visit https://docs.nvidia.com/clara/#parabricks for detailed documentation

positional arguments:
  command     The pipeline or tool to run.

options:
  -h, --help  show this help message and exit
INFO:    Cleaning up image...
```

## Testing
NVIDIA Clara-Parabricks provides multiple [tools](https://docs.nvidia.com/clara/parabricks/4.0.0/index.html#software-overview) and [workflows](https://docs.nvidia.com/clara/parabricks/4.0.0/index.html#parabricks-pipelines). We will be testing the tools specified in the link above as well as the workflows for germline variant detection using both low-coverage and 30X whole-genome samples. 

The reference data used is [GRCh38](https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/analysisSet/) and the directions on how to download this were taken from [here](https://docs.nvidia.com/clara/parabricks/4.0.0/How-Tos/WholeGenomeGermlineSmallVariants.html#downloading-and-indexing-a-reference-genome-and-known-sites).

The [deepvariant-germline workflow](https://docs.nvidia.com/clara/parabricks/4.0.0/Documentation/ToolDocs/man_deepvariant_germline.html#deepvariant-germline) runs through multiple tools such as bwa-mem, mark duplicates, and deepVariant. The workflow requires fastq files as input and provides an alignment BAM file and VCF as outputs. These versions of the tools take advantage of Polaris's GPU framework by accelerating the analysis. 

### Low-Coverage Whole-genome Analysis
The following was used to execute the analysis interactively on a Polaris node:

```
# Ask for an interactive node on Polaris and wait until this is provided
qsub -A covid-ct -I -l select=1 -l walltime=1:00:00 -l filesystems=home:eagle -q debug

# load the required modules
module use /soft/spack/gcc/0.6.1/install/modulefiles/Core
module load singularityce

# run the deepvariant-germline workflow using the low-coverage sequences
singularity run  --bind /lus/grand/projects/covid-ct/arodriguez:/lus/grand/projects/covid-ct/arodriguez --nv  /lus/grand/projects/covid-ct/arodriguez/tools/singularity/parabricks-4.0 pbrun deepvariant_germline  --ref /lus/grand/projects/covid-ct/arodriguez/wgs_test/reference/hg38/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna  --in-fq /lus/grand/projects/covid-ct/arodriguez/wgs_test/HG00138/low_cov/ERR016162_1.fastq.gz /lus/grand/projects/covid-ct/arodriguez/wgs_test/HG00138/low_cov/ERR016162_2.fastq.gz --out-variants /lus/grand/projects/covid-ct/arodriguez/wgs_test/HG00138/output/low_cov --out-bam  /lus/grand/projects/covid-ct/arodriguez/wgs_test/HG00138/output/low_cov/HG00138.bam --out-variants /lus/grand/projects/covid-ct/arodriguez/wgs_test/HG00138/output/low_cov/HG00138.vcf

```

The log file of the run can be reached [here](https://github.com/exascale-genomics/mvp-wgs-sv/blob/main/data/pb_deepvariant_germline_wf_low_coverage_log.txt).

The execution times can be seen in the table below:

| Tools | Description | Version | Execution Time (seconds) | GPU Usage |
| :-: | :-----: |  :-----: | :-----: |  :-----: |
|  Parabricks accelerated Genomics Pipeline | BWA-mem Sorting Phase-I    |  4.0.0-1 | 105 |  X |
|  Parabricks accelerated Genomics Pipeline | Sorting Phase-II   |  4.0.0-1 | 10 |  X |
|  Parabricks accelerated Genomics Pipeline |  Marking Duplicates, BQSR   |  4.0.0-1 | 20 |  X |
|  Parabricks accelerated Genomics Pipeline |  deepvariant   |  4.0.0-1 | 337 |  X |
| |  |  <b>Total</b> | <b>472 seconds = 7.9 minutes</b> |   |


### 30X Coverage Whole-genome Analysis
The input data for the 30X sequences are in CRAM format. Since the Parabricks pipeline requires fastq as input, we will need to run the Parabricks tool [bam2fq](https://docs.nvidia.com/clara/parabricks/4.0.0/Documentation/ToolDocs/man_bam2fq.html#man-bam2fq) before running the pipeline.

The following was used to execute the analysis interactively on a Polaris node:

```
# Ask for an interactive node on Polaris and wait until this is provided
qsub -A covid-ct -I -l select=1 -l walltime=1:00:00 -l filesystems=home:eagle -q debug

# load the required modules
module use /soft/spack/gcc/0.6.1/install/modulefiles/Core
module load singularityce

# convert from CRAM to fq
# singularity command needs to have the -W and -H parameters so it can write any tmp files to the specified path instead of the home directory
# home directory can fill up and kill the job
singularity run -H /lus/grand/projects/covid-ct/arodriguez -W /lus/grand/projects/covid-ct/arodriguez/tmp --bind /lus/grand/projects/covid-ct/arodriguez:/lus/grand/projects/covid-ct/arodriguez --nv  /lus/grand/projects/covid-ct/arodriguez/tools/singularity/parabricks-4.0 pbrun bam2fq --in-bam /lus/grand/projects/covid-ct/arodriguez/wgs_test/HG00138/30x_cov/HG00138.final.cram  --out-prefix /lus/grand/projects/covid-ct/arodriguez/wgs_test/HG00138/30x_cov/HG00138_30x_2.fastq --ref  /lus/grand/projects/covid-ct/arodriguez/wgs_test/reference/GRCh38_CRAM/GRCh38_full_analysis_set_plus_decoy_hla.fa

# run the deepvariant-germline workflow using the low-coverage sequences
singularity run -H /lus/grand/projects/covid-ct/arodriguez -W /lus/grand/projects/covid-ct/arodriguez/tmp --bind /lus/grand/projects/covid-ct/arodriguez:/lus/grand/projects/covid-ct/arodriguez --nv  /lus/grand/projects/covid-ct/arodriguez/tools/singularity/parabricks-4.0 pbrun deepvariant_germline  --ref /lus/grand/projects/covid-ct/arodriguez/wgs_test/reference/GRCh38_CRAM/GRCh38_full_analysis_set_plus_decoy_hla.fa  --in-fq /lus/grand/projects/covid-ct/arodriguez/wgs_test/HG00138/30x_cov/HG00138_30x_2.fastq_1.fastq.gz /lus/grand/projects/covid-ct/arodriguez/wgs_test/HG00138/30x_cov/HG00138_30x_2.fastq_2.fastq.gz --out-bam  /lus/grand/projects/covid-ct/arodriguez/wgs_test/HG00138/output/30x/HG00138.bam --out-variants  /lus/grand/projects/covid-ct/arodriguez/wgs_test/HG00138/output/30x/HG00138.vcf

```

The log file of the run can be reached [here](https://github.com/exascale-genomics/mvp-wgs-sv/blob/main/data/pb_deepvariant_germline_wf_30x_coverage_log.txt).

Below are the execution times:

| Tools | Description | Version | Execution Time (seconds) | GPU Usage |
| :-: | :-----: |  :-----: | :-----: |  :-----: |
|  Parabricks accelerated Genomics Pipeline | bam2fq    |  4.0.0-1 | 1015 |  X |
|  Parabricks accelerated Genomics Pipeline | BWA-mem Sorting Phase-I    |  4.0.0-1 | 1689 |  X |
|  Parabricks accelerated Genomics Pipeline | Sorting Phase-II   |  4.0.0-1 | 50 |  X |
|  Parabricks accelerated Genomics Pipeline |  Marking Duplicates, BQSR   |  4.0.0-1 | 100 |  X |
|  Parabricks accelerated Genomics Pipeline |  deepvariant   |  4.0.0-1 | 1094 |  X |
| |  |  <b>Total</b> | <b>3948 seconds = 66 minutes</b> |   |
