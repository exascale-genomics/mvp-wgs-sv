# Overall Plan for MVP Whole Genome Structural Variant and PheWAS Analysis on Polaris and Frontier

We will have access to approximately 10,000 whole genome sequences from the MVP project.
In the past the VA was able to perform mapping and SNP calling using the [Trellis](https://www.nature.com/articles/s41598-021-02569-5) platform. However, SV calling at this scale has not been attempted before.
Performing analysis on the whole genome sequences can be very computational and time intensive. We would like to use ALCF's Polaris machine to perform the workflows for NGS sequence analysis.
We will have the opportunity to perform a population analysis so we can conclude with a Phewas analysis on the results from the whole genome analysis.

Below is a draft of what steps are needed to achieve the goals on this project. Please modify appropriately.

1. Get familiar with Polaris
   * Get user accounts
   * Login
     ```
     ssh arodriguez@polaris.alcf.anl.gov
     ```
   * Submit interactive and script jobs
     ```
     qsub -A covid-ct -I -l select=1 -l walltime=1:00:00 -l filesystems=home:eagle -q debug
     ```
2. Download data [[progress](https://github.com/exascale-genomics/mvp-wgs-sv/blob/main/data/1kg_download.txt)]: 
   * [1KG Whole genome datasets](https://www.cell.com/cell/fulltext/S0092-8674(22)00991-6) 
   * Reference [hg38](ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/001/405/GCA_000001405.15_GRCh38/seqs_for_alignment_pipelines.ucsc_ids/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz)
3. Gather a set of NGS and PheWAS/GWAS tools that will be tested on Polaris. Each tool will most likely encounter its own issues and will have to deal with it appropriately.
  * Alignment
    * [NVIDIA Clara-Parabricks](https://www.nvidia.com/en-us/clara/genomics/)
  * SNP Callers
    * [DeepVariant](https://ai.googleblog.com/search/label/Google%20Genomics) - included within parabricks
    * [GATK HaplotypeCaller]() - included with parabricks
  * SV Callers
    * [SVision](https://github.com/xjtu-omics/SVision) - This tool is meant to be used with long read sequencers (i.e. PacBio, OxfordNanopore) for building the models which they already provide. We can test with the BAM file we generate from Parabricks.
    * [AstraZeneca tools](https://github.com/AstraZeneca)
    * [GATK-sv](https://github.com/broadinstitute/gatk-sv)
    * [DeepSV](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3299-y)
    * [MANTA](https://github.com/Illumina/manta) - consider modifications made [here](https://www.nature.com/articles/s41525-021-00267-9)
    * [DeepSVFilter](https://github.com/yongzhuang/DeepSVFilter) - Tool used to filter SV calls from other SV callers (i.e. Delly, Lumpy, Manta)
    * [Cue](https://www.broadinstitute.org/talks/cue-framework-cross-platform-structural-variant-calling-and-genotyping-deep-learning)
    * [Delly]()
    * [svtools]()
    * [Absynthe]()
    * [Breakdancer]()
    * [BreakSeq]()
    * [CNVNator]()
    * [Lumpy]()
    * [Manta]()
    * [Smoove]()
    * [Tardis]()
    * [Whaning]()
    * [Graphtyper]()
    * [PAV](https://github.com/EichlerLab/pav)
    * [ConsensusSV](https://github.com/MateuszChilinski/ConsensuSV)
    * [Parliament2](https://github.com/dnanexus/parliament2)
  * Annotations
    * Annotate with [VEP]()
  * Population analysis
    * SAIGE
4. Test each of the tools from the previous set
   * NVIDIA Clara-Parabricks - Succesfully ran workflow on low coverage and 30X whole-genome fastq sequences [[Progress](https://github.com/exascale-genomics/mvp-wgs-sv/blob/main/parabricks_readme.md)]
   * SVision - Build tool and test on 30X whole-genome BAM file [[Progress](https://github.com/exascale-genomics/mvp-wgs-sv/blob/main/svision_readme.md)].
6. Evaluate outputs - Determine which set of tools are best for our analysis, but be dynamic enough that if new tools come up, we can shift focus.
7. Create/test submission engine (i.e. Parsl, Balsam, etc)
   * Look [here](https://www.alcf.anl.gov/files/uram_workflows_performanceworkshop2018.pdf)
   * [Parsl on Polaris](https://github.com/argonne-lcf/user-guides/blob/workflow-docs/docs/polaris/workflows.md)
9. Create workflow for submitting the genomes
10. Generate statistics on rutime to determine how much our allocation on Polaris should be
11. Start process to move MVP whole-genome data
12. Start processing MVP whole-genome through workflow pipeline
13. Convert VCF to PGENs for access to SAIGE
14. Share VCFs as results become available
15. Perform post-process analysis on VCFs (i.e QC, annotations, etc)
16. <b>Write paper on how VCFs were generated, what was found (computational and science?)</b>
17. Setup SAIGE on Polaris
18. Run SAIGE for MVP WG PGEN data
    * [Use link](https://github.com/bambrozio/bioinformatics/blob/master/utils/1k-genomes-phenotype-simulator.ipynb) to create phenotypes
19. Perform QC on SAIGE analysis
20. Post-process analysis - Will need Anurag and Jenny for this
    * What is different compared to gwPhewas analysis?
    * Novel SNPs, SVs (quantitities)
21. Share data
22. <b>Write paper on findings</b>

## Summary of SV callers


| Caller/web link  | Types of SVs | AI based? | Actively developed? | Prg Env | GPU acceleration? | 
| ------------- | ------------- | ------------- | ---------------| ------------------|-----------------------------|
| [Breakdancer<sup>\*</sup>](https://github.com/genome/breakdancer)  | Deletions, insertions, inversions, <br /> intra-chromosomal, <br /> inter-chromosomal translocations  | N | N | C++| N |
| [BreakSeq](https://github.com/bioinform/breakseq2)  | Insertions, deletions, <br /> translocations, inversions, <br /> duplications  |  N | N | Python | N | 
| [ClipCrop](https://github.com/shinout/clipcrop)  | Insertions, deletions, <br /> translocations, inversions, <br /> duplications  |  N | N | Node.js | N | 
| [CREST](https://www.stjude.org/research/labs/zhang-lab/crest.html)  | Insertions, deletions, <br /> translocations, inversions, <br /> duplications  |  N | N | Perl | N | 
| [DELLY](https://github.com/dellytools/delly)  | Deletions, inversions, duplications, <br /> interchromosomal translocations  |  N | Y | C++ | N | 
| [GRIDSS](https://github.com/PapenfussLab/gridss)  | Insertions, deletions, translocations, inversions, duplications  |  N | N | Java/R | N | 
| [Gustaf](https://github.com/seqan/seqan/tree/master/apps/gustaf)  | Deletions, inversions, duplications, translocation  | N | N | C++ | N | 
| [LUMPY](https://github.com/arq5x/lumpy-sv)  | Deletions, duplications, inversions, translocations  |  N | Y (June 2022) | C++ | N | 
| [Manta](https://github.com/Illumina/manta)  | Insertions, deletions, translocations, inversions, duplications  |  N | N | C++ | N | 
| [Meerkat](http://compbio.med.harvard.edu/Meerkat/meerkat_download_page.php)  |  Insertions, deletions, translocations, inversions, duplications  |  N | N | Perl | N | 
| [Pindel](https://github.com/genome/pindel)  | Insertions, deletions, translocations, inversions, duplications  |  N | N | C++ | N | 
| [TARDIS](https://github.com/BilkentCompGen/tardis)  | Tandem and interspersed segmental duplications  |  N | N | C | N | 
| [TIGRA](https://bitbucket.org/xianfan/tigra/src/master/)  | Insertions and deletions  |  N | N | C++ | N | 
| [Ulysses](https://github.com/gillet/ulysses)  |  Insertions, deletions, translocations, inversions, duplications  |  N | N | Python/R | N | 
| [SvABA](https://github.com/walaj/svaba)  |  Insertion, deletions, somatic rearrangments  |  N | N | C++/R | N | 
| [Socrates](https://github.com/PapenfussLab/socrates)  |    |  N | N | Java | N | 
| [SVSeq2](https://sites.google.com/site/jinzhangwebsite/svseq2)  |    |  N | N | - | N | 
| [Cue](https://github.com/PopicLab/cue)  |  Deletions, tandem duplication, inversions, deletion-flanked inversions, inverted duplications larger than 5kbp  |  Y | Y | Python | Y | 
| [Strvctvre](https://github.com/andrewSharo/StrVCTVRE)  | Deletions and duplications   |  Y | N | Python | - | 
| [Dysgu](https://github.com/kcleal/dysgu)  |    |  Y | Y | Python | - | 
| [CNNgeno](https://github.com/BRF123/Cnngeno)  | Deletions   |  Y | N | Python | Y | 
| [DeepSV](https://github.com/CSuperlei/DeepSV)  | Deletions   |  Y | N | Python | Y | 
| [sv-channels](https://github.com/GooglingTheCancerGenome/sv-channels)  | Deletions  |  Y | Y | Python/R | Y | 

<sup>\*</sup> BreakDancer has two modes, BreakDancerMax and BreakDancerMini. While the former is for large SVs, the latter is designed for calling small indels (of 10-100 base pairs) using normally mapped read pairs.

## References
This is what others are doing:

* Take a look at what the Broad folks are doing [here](https://www.sciencedirect.com/science/article/pii/S0092867422009916?via%3Dihub). They are calling whole genomes using the Broad workflow and SV calling is being done in a consensus manner.
* [Genomics England's very first initiative – sequencing 100,000](https://www.genomicsengland.co.uk/initiatives/100000-genomes-project/documentation)
