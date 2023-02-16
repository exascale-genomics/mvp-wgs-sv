## Running Parliament2 on hg002 dataset on Polaris with Parabricks assisted pre-processing

1. **Download files from GIAB site**

Download the bam (mapped on GRCh37), reference (GRCh37) and VCF files from GIAB server for hg002 (We use the GRCh37 as reference as the SV calls in GIAB v0.6 truth set have been made using it as the reference and not GRCh38)\
\
Location of 60X BAM file: https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/AshkenazimTrio/HG002_NA24385_son/NIST_HiSeq_HG002_Homogeneity-10953946/NHGRI_Illumina300X_AJtrio_novoalign_bams/ \
Download BAM file using ```wget https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/AshkenazimTrio/HG002_NA24385_son/NIST_HiSeq_HG002_Homogeneity-10953946/NHGRI_Illumina300X_AJtrio_novoalign_bams/HG002.GRCh38.60x.1.bam``` \
Note: This BAM file was not formatted properly for using directly as input to Parliament2. It was first converted to FASTQ read files using Parabricks *bam2fq* tool and the reads were converted to a new BAM file (hg002_60X_fq2bam.bam) using Parabricks *fq2bam*. To maintain consistency with the MVP dataset, this BAM file was downsampled by a factor of 2 to create a BAM file that corresponds to 30X data (samtools view -s 0.5 -b hg002_60X_fq2bam.bam > hg002_30X_fq2bam.bam) \
\
Location of reference file: https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/references/GRCh37/ \
Download reference file using: ```wget ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/technical/reference/phase2_reference_assembly_sequence/hs37d5.fa.gz``` \
\
Link to VCF file: https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/NIST_SV_v0.6/ 
>Files in this directory include:
>1. HG002_SVs_Tier1_v0.6.vcf.gz - the calls with PASS in the FILTER field are our highest confidence set of SVs >=50bp.
>2. HG002_SVs_Tier1_v0.6.bed - this defines regions in which HG002_SVs_Tier1_v0.6.vcf.gz should contain close to 100 % of true insertions and deletions >=50bp.
>3. HG002_SVs_Tier2_v0.6.bed - this defines additional regions in which there was strong evidence for an SV, but the sequence and size could not be determined with confidence.  There is some overlap of this with the Tier 1 vcf.
>4. HG002_SVs_Tier1plusTier2_v0.6.1.bed - this defines regions that encompass all of the Tier1 and Tier 2 SV calls, with variants merged into a single region if they are within 1kb.
>5. HG002_SVs_Tier1_v0.6.2.bed - this defines regions in which HG002_SVs_Tier1_v0.6.vcf.gz should contain close to all of true insertions and deletions >=50bp. This is more conservative than HG002_SVs_Tier1_v0.6.bed in that it excludes the VDJ and X and Y.
\

Note: 
>Known and Likely Limitations of this callset:
>1. Although many of the Tier 1 calls are challenging (e.g., in long tandem repeats), it likely only includes 50% or less of the total SVs in the genome, and is likely biased towards easier SVs. 
>2. The predicted sequence change is not always accurate.  If multiple methods predicted the same sequence change, we select it, but this is not the case for all sites, and biases can cause the same incorrect sequence change to be predicted.
>3. The consensus genotype may be inaccurate in some cases, particularly if the predicted sequence change is inaccurate.  The fraction of Mendelian errors for sites genotyped in all 3 members of the trio was ~2%, and more sites were heterozygous in all individuals than expected.

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

***Preprocessing*** (Note: these figures correspond to 60X reads)

| Parabricks tool 	| Time (mins) 	|
|-----------------	|-------------	|
| bam2fq          	| 56          	|
| fq2bam          	| 58          	|

***SV calling*** (30X reads)
| Caller          	| Time (mins) 	|
|-----------------	|-------------	|
| Manta           	| 12          	|
| Lumpy           	|           	|
| Breakdancer     	| 3           	|
| Breakseq        	| 7          	|
| Delly_insertion 	| 16          	|
| Delly_deletion  	| 25         	|
| Delly_inversion  	| 14         	|
| Delly_duplication  	| 13         	|
| Combined(all above)  	| 55         	|

#Note: SV calling carried out using the Delly v1.1.6 singularity file (https://github.com/dellytools/delly/releases/) took 58 mins for SV calling, and 20 mins for annotation + genotyping
## Running Parliament2 on synthetic genomes on Polaris with Parabricks assisted pre-processing

1. **Generation of synthetic data**

