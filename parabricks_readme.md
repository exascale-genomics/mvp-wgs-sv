# polaris-wgs
Running tests for NGS analysis on [Polaris ALCF](https://www.alcf.anl.gov/polaris)

I will be testing several NGS tools for fast throughput analysis of WGS on Polaris focusing on the SV callers.

## NVIDIA Clara Parabricks
First we will try [NVIDIA Clara-Parabricks](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/clara/containers/clara-parabricks). 
The container is distributed via Docker and unfortunately Polaris does not allow usage of Docker. In order to use Parabricks within Polaris we must first create a Singularity container:
```
$module load singularity/3.8.7
$mkdir -p /lus/grand/projects/covid-ct/arodriguez/tools/singularity
$cd /lus/grand/projects/covid-ct/arodriguez/tools/singularity
$singularity  build parabricks-4.0 docker://nvcr.io/nvidia/clara/clara-parabricks:4.0.0-1
INFO:    Starting build...
Getting image source signatures
Copying blob d7bfe07ed847 done
Copying blob bbbbd451a669 done
Copying blob 773163705c35 done
Copying blob d6949fcf1aef done
Copying blob 3eb73064088b done
Copying blob a3ac3ab0ee35 done
Copying blob 8d88682a5e1d done
Copying config 41b997ec10 done
Writing manifest to image destination
Storing signatures
2022/09/28 19:08:34  info unpack layer: sha256:d7bfe07ed8476565a440c2113cc64d7c0409dba8ef761fb3ec019d7e6b5952df
2022/09/28 19:08:34  warn xattr{etc/gshadow} ignoring ENOTSUP on setxattr "user.rootlesscontainers"
2022/09/28 19:08:34  warn xattr{/tmp/build-temp-256462640/rootfs/etc/gshadow} destination filesystem does not support xattrs, further warnings will be suppressed
2022/09/28 19:08:35  info unpack layer: sha256:bbbbd451a669065c9ef688d0d43e47f20ae334efda40dfc323d82fd342763976
2022/09/28 19:08:35  warn xattr{var/log/apt/term.log} ignoring ENOTSUP on setxattr "user.rootlesscontainers"
2022/09/28 19:08:35  warn xattr{/tmp/build-temp-256462640/rootfs/var/log/apt/term.log} destination filesystem does not support xattrs, further warnings will be suppressed
2022/09/28 19:08:35  info unpack layer: sha256:773163705c35e00e6c9cdb84e4e8db9079b8777f8f3f62839ec2008af668f939
2022/09/28 19:08:36  warn xattr{var/log/apt/term.log} ignoring ENOTSUP on setxattr "user.rootlesscontainers"
2022/09/28 19:08:36  warn xattr{/tmp/build-temp-256462640/rootfs/var/log/apt/term.log} destination filesystem does not support xattrs, further warnings will be suppressed
2022/09/28 19:08:36  info unpack layer: sha256:d6949fcf1aef0c0e95826220c5f2731c2909492c994d70707d8c93eb4c815b99
2022/09/28 19:08:36  info unpack layer: sha256:3eb73064088b62826e9ea4b1bcbd9b10270f134e45f6436214db7c8ebed6052b
2022/09/28 19:08:36  info unpack layer: sha256:a3ac3ab0ee351d7e137a83615b01acb272d3b091c745163fb506cdf7b96c077b
2022/09/28 19:08:37  warn xattr{usr/local/lib/python3.8} ignoring ENOTSUP on setxattr "user.rootlesscontainers"
2022/09/28 19:08:37  warn xattr{/tmp/build-temp-256462640/rootfs/usr/local/lib/python3.8} destination filesystem does not support xattrs, further warnings will be suppressed
2022/09/28 19:09:23  info unpack layer: sha256:8d88682a5e1dfc9375ea4a4834e5aff43e780f2c6e82ddbec89eabbd5a9800fa
2022/09/28 19:09:23  warn xattr{var/cache/apt/archives/partial} ignoring ENOTSUP on setxattr "user.rootlesscontainers"
2022/09/28 19:09:23  warn xattr{/tmp/build-temp-256462640/rootfs/var/cache/apt/archives/partial} destination filesystem does not support xattrs, further warnings will be suppressed
INFO:    Creating SIF file...
INFO:    Build complete: parabricks-4.0
```

Now we can go ahead and test a simple job to see if our Singularity container build was a success.

```
arodriguez@polaris-login-02:~> qsub -A covid-ct -I -l select=1 -l walltime=1:00:00 -l filesystems=home:eagle -q debug
qsub: waiting for job 333796.polaris-pbs-01.hsn.cm.polaris.alcf.anl.gov to start

arodriguez@x3107c0s19b0n0:~> singularity exec  --bind /lus/grand/projects/covid-ct/arodriguez:/lus/grand/projects/covid-ct/arodriguez ./parabricks-4.0 pbrun -h
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
deepvariant             - Run GPU-DeepVariant for calling germline variants
fq2bam                  - Run bwa mem, co-ordinate sorting, marking duplicates, and Base Quality Score Recalibration
genotypegvcf            - Convert a GVCF to VCF
haplotypecaller         - Run GPU-HaplotypeCaller for calling germline variants
indexgvcf               - Index a GVCF file
mutectcaller            - Run GPU-Mutect2 for tumor-normal analysis
postpon                 - Generate the final VCF output of doing mutect pon
prepon                  - Build an index for PON file, which is the prerequisite to performing mutect pon
rna_fq2bam              - Run RNA-seq data through the fq2bam pipeline
starfusion              - Identify candidate fusion transcripts supported by Illumina reads

command options for commonly used FULL PIPELINES
germline                - Run the germline pipeline from FASTQ to VCF
deepvariant_germline    - Run the germline pipeline from FASTQ to VCF using a deep neural network analysis
somatic                 - Run the somatic pipeline from FASTQ to VCF

Information about the software
version                 - Current version of Parabricks

Please visit https://docs.nvidia.com/clara/#parabricks for detailed documentation

positional arguments:
  command     The pipeline or tool to run.

optional arguments:
  -h, --help  show this help message and exit
```

## Sequence and Reference data
Several files for testing will be downloaded. The description and steps taken can be seen [here](https://github.com/exascale-genomics/mvp-wgs-sv/blob/main/data/1kg_download.txt) and the [source of the data](https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/analysisSet/).

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
module load singularity/3.8.7

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
module load singularity/3.8.7

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
|  Parabricks accelerated Genomics Pipeline | BWA-mem Sorting Phase-I    |  4.0.0-1 | - |  X |
|  Parabricks accelerated Genomics Pipeline | Sorting Phase-II   |  4.0.0-1 | - |  X |
|  Parabricks accelerated Genomics Pipeline |  Marking Duplicates, BQSR   |  4.0.0-1 | - |  X |
|  Parabricks accelerated Genomics Pipeline |  deepvariant   |  4.0.0-1 | - |  X |
| |  |  <b>Total</b> | <b>- seconds = - minutes</b> |   |
