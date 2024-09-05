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

