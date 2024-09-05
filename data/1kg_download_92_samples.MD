# Data Download for Testing
#
We will download data from [1000 Genome Project](https://www.internationalgenome.org) to test our tools on the Polaris Supercomputer.
We will download 92 EUR samples [GBR](https://www.internationalgenome.org/data-portal/population/GBR) 


      Population:           British
      Code:                 GBR
      Description:          British in England and Scotland
      Superpopulation:      European Ancestry
      Superpopulation code: EUR

The project provides both low coverage and 30x coverage data files for each of the samples.
We will be working with 30x coverage files in CRAM format.
We will need to convert from CRAM files to fastq files for our testing.


Copy and paste [text](https://www.internationalgenome.org/api/beta/file/_search/igsr_British%20in%20England%20and%20Scotland_undefined.tsv.tsv) to file `30x-igsr-gbr-seqpaths.tsv`

Download the CRAM and CRAI files using `wget`

      mkdir /grand/projects/GeomicVar/rodriguez/1kg_proj/data/30x
      for i in `cut -f1  30x-igsr-gbr-seqpaths.tsv`; do 
        echo $i; 
        name=`echo $i |cut -d"/" -f8 | cut -f1 -d"."`; 
        echo $name; 
        mkdir $name; 
        cd $name; 
        wget $i; 
        wget $i.crai; 
        cd /grand/projects/GeomicVar/rodriguez/1kg_proj/data/30x; 
      done


Install additional tools for index making

```
mkdir -p /grand/projects/GeomicVar/rodriguez/1kg_proj/tools

# BWA
mkdir -p /grand/projects/GeomicVar/rodriguez/1kg_proj/tools/bwa
cd /grand/projects/GeomicVar/rodriguez/1kg_proj/tools/bwa
git clone https://github.com/lh3/bwa.git
cd bwa
make

# samtools
mkdir -p /grand/projects/GeomicVar/rodriguez/1kg_proj/tools/samtools
cd samtools
wget https://github.com/samtools/samtools/releases/download/1.16.1/samtools-1.16.1.tar.bz2
bunzip2 samtools-1.16.1.tar.bz2
tar xvf samtools-1.16.1.tar
cd samtools-1.16.1/
## configure without htslib as it needs libbzip2 which I cannot find. This will only install samtools
./configure --disable-bz2 --prefix=/lus/grand/projects/covid-ct/arodriguez/wgs_test/tools/samtools/samtools-1.16.1/
make
make install
```

Create the indexed files and also download the reference hg38 file which we will align to:

```
mkdir -p /grand/projects/GeomicVar/rodriguez/1kg_proj/reference/hg38
cd /grand/projects/GeomicVar/rodriguez/1kg_proj/reference/hg38
wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/001/405/GCA_000001405.15_GRCh38/seqs_for_alignment_pipelines.ucsc_ids/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz
## Unzip and index the reference
gunzip GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz

# Also for the CRAM file
mkdir -p /grand/projects/GeomicVar/rodriguez/1kg_proj/reference/GRCh38_CRAM
cd /grand/projects/GeomicVar/rodriguez/1kg_proj/reference/GRCh38_CRAM
wget ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/GRCh38_reference_genome/GRCh38_full_analysis_set_plus_decoy_hla.fa

## Create an FAI index
cd /grand/projects/GeomicVar/rodriguez/1kg_proj/reference/hg38
/grand/projects/GeomicVar/rodriguez/1kg_proj/tools/samtools/samtools-1.16.1/bin/samtools faidx GCA_000001405.15_GRCh38_no_alt_analysis_set.fna

cd /grand/projects/GeomicVar/rodriguez/1kg_proj/reference/GRCh38_CRAM
/grand/projects/GeomicVar/rodriguez/1kg_proj/tools/samtools/samtools-1.16.1/bin/samtools faidx GRCh38_full_analysis_set_plus_decoy_hla.fa

## Create the BWA indices
cd /grand/projects/GeomicVar/rodriguez/1kg_proj/reference/hg38
/grand/projects/GeomicVar/rodriguez/1kg_proj/tools/bwa/bwa/bwa index GCA_000001405.15_GRCh38_no_alt_analysis_set.fna

cd /grand/projects/GeomicVar/rodriguez/1kg_proj/reference/GRCh38_CRAM
/grand/projects/GeomicVar/rodriguez/1kg_proj/tools/bwa/bwa/bwa index GRCh38_full_analysis_set_plus_decoy_hla.fa

```
