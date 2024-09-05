# Overall Test Plan for 1000 Genome Whole Genome PheWAS Analysis on Polaris

We will have access to approximately 10,000 whole genome sequences from the MVP project.
In the past the VA was able to perform mapping and SNP calling using the [Trellis](https://www.nature.com/articles/s41598-021-02569-5) platform. However, SV calling at this scale has not been attempted before.
Performing analysis on the whole genome sequences can be very computational and time intensive. We would like to use ALCF's Polaris machine to perform the workflows for NGS sequence analysis.
We will have the opportunity to perform a population analysis so we can conclude with a Phewas analysis on the results from the whole genome analysis.

Here, we will be testing the workflow analysis plan on a subset of data from 1000 Genome. We will only concentrate on SNP calling and no structural variant (SV) analysis will be performed.
We will be using a subset of data from 1K genomes EUR samples from a [GBR cohort](https://www.internationalgenome.org/data-portal/population/GBR).
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
2. Download [1KG Whole genome GBR datasets](https://www.cell.com/cell/fulltext/S0092-8674(22)00991-6): 
   * 92 GBR samples from 1KG (EUR) datasets [[progress](https://github.com/exascale-genomics/mvp-wgs-sv/blob/main/data/1kg_download_92_samples.MD)] 
   * Reference download and index build for hg38 [[progress](https://github.com/exascale-genomics/mvp-wgs-sv/blob/main/data/download_references.md)]
3. Gather a set of NGS and PheWAS/GWAS tools that will be tested on Polaris. Each tool will most likely encounter its own issues and will have to deal with it appropriately.
  * Alignment
    * [NVIDIA Clara-Parabricks](https://www.nvidia.com/en-us/clara/genomics/)
  * SNP Callers
    * [DeepVariant](https://ai.googleblog.com/search/label/Google%20Genomics) - included within parabricks
    * [GATK HaplotypeCaller]() - included with parabricks
  * Annotations
    * Annotate with [VEP]()
  * Population analysis
    * SAIGE
4. Test each of the tools from the previous set
   * NVIDIA Clara-Parabricks - Succesfully ran workflow on low coverage and 30X whole-genome fastq sequences [[Progress](https://github.com/exascale-genomics/mvp-wgs-sv/blob/main/parabricks_readme.md)]
5. Evaluate outputs - Determine which set of tools are best for our analysis, but be dynamic enough that if new tools come up, we can shift focus.
6. Create/test submission engine (i.e. Parsl, Balsam, etc)
   * Look [here](https://www.alcf.anl.gov/files/uram_workflows_performanceworkshop2018.pdf)
   * [Parsl on Polaris](https://github.com/argonne-lcf/user-guides/blob/workflow-docs/docs/polaris/workflows.md)
7. Create workflow for submitting the genomes
8. Generate statistics on rutime to determine how much our allocation on Polaris should be
9. Start processing 1KG whole-genome through workflow pipeline
10. Convert VCF to PGENs for access to SAIGE
11. Perform post-process analysis on VCFs (i.e QC, annotations, etc)
12. <b>Write paper on how VCFs were generated, what was found (computational and science?)</b>
13. Create simulated phenotype files for 1KG VCF results. [Use link](https://github.com/bambrozio/bioinformatics/blob/master/utils/1k-genomes-phenotype-simulator.ipynb) to create phenotypes
13. Setup SAIGE on Polaris
14. Run SAIGE for 1KG WG PGEN data
15. Perform QC on SAIGE analysis
16. Package up the tools to perform same test on cloud.
17. Compare cloud results with Polaris results
18. Share data
19. <b>Write paper on findings</b>


## References
This is what others are doing:

* Take a look at what the Broad folks are doing [here](https://www.sciencedirect.com/science/article/pii/S0092867422009916?via%3Dihub). They are calling whole genomes using the Broad workflow and SV calling is being done in a consensus manner.
* [Genomics England's very first initiative – sequencing 100,000](https://www.genomicsengland.co.uk/initiatives/100000-genomes-project/documentation)