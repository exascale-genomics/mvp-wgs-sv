## Running Parliament2 on hg002 dataset on Polaris with Parabricks assisted pre-processing

1. **Download files from GIAB site**

Download the bam (mapped on GRCh37), reference (GRCh37) and VCF files from GIAB server for hg002 (We use the GRCh37 as reference as the SV calls in GIAB v0.6 truth set have been made using it as the reference and not GRCh38)\
\
Location of 60X bam file: https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/AshkenazimTrio/HG002_NA24385_son/NIST_HiSeq_HG002_Homogeneity-10953946/NHGRI_Illumina300X_AJtrio_novoalign_bams/ \
Download bam file by using ```wget https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/AshkenazimTrio/HG002_NA24385_son/NIST_HiSeq_HG002_Homogeneity-10953946/NHGRI_Illumina300X_AJtrio_novoalign_bams/HG002.GRCh38.60x.1.bam``` \
Note: This bam file was not formatted properly for using directly as input to Parliament2. It was first converted to fastq read files using Parabricks *bam2fq* tool and then a new bam file was created using Parabricks *fq2bam* (add the commands)\
\
Location of reference file: https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/references/GRCh37/ \
Download reference file using: 'wget ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz' \
\
Link to VCF file: https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/NIST_SV_v0.6/ 
>Files in this directory include:
>1. HG002_SVs_Tier1_v0.6.vcf.gz - the calls with PASS in the FILTER field are our highest confidence set of SVs >=50bp.
>2. HG002_SVs_Tier1_v0.6.bed - this defines regions in which HG002_SVs_Tier1_v0.6.vcf.gz should contain close to 100 % of true insertions and deletions >=50bp.
>3. HG002_SVs_Tier2_v0.6.bed - this defines additional regions in which there was strong evidence for an SV, but the sequence and size could not be determined with confidence.  There is some overlap of this with the Tier 1 vcf.
>4. HG002_SVs_Tier1plusTier2_v0.6.1.bed - this defines regions that encompass all of the Tier1 and Tier 2 SV calls, with variants merged into a single region if they are within 1kb.
>5. HG002_SVs_Tier1_v0.6.2.bed - this defines regions in which HG002_SVs_Tier1_v0.6.vcf.gz should contain close to all of true insertions and deletions >=50bp. This is more conservative than HG002_SVs_Tier1_v0.6.bed in that it excludes the VDJ and X and Y.
\

2. **Run Parliament2 SV callers** 
```
singularity run -B \`pwd\`/input:/home/dnanexus/in:rw -B \`pwd\`/output:/home/dnanexus/out:rw -H /lus/grand/projects/covid-ct/tarak/SVCallers/parliament2_HG002/outputs parliament2_latest.sif  [-h] --bam BAM [--bai BAI] -r REF_GENOME [--fai FAI]
                      [--prefix PREFIX] [--filter_short_contigs]
                      [--breakdancer] [--breakseq] [--manta] [--cnvnator]
                      [--lumpy] [--delly_deletion] [--delly_insertion]
                      [--delly_inversion] [--delly_duplication] [--genotype]
                      [--svviz] [--svviz_only_validated_candidates]
```

3. **Computation time**

| Caller          	| Time (mins) 	|
|-----------------	|-------------	|
| Manta           	| 46          	|
| Lumpy           	| 18          	|
| Breakdancer     	| 5           	|
| Breakseq        	| 14          	|
| Delly_insertion 	| 99          	|
| Delly_deletion  	| 171         	|
