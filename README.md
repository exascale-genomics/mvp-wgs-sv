# Project Plan for MVP Whole Genome Structural Variant and PheWAS Analysis on Polaris

We will have access to approximately 10,000 whole genome sequences from the MVP community.
In the past the VA was able to perform mapping and SNP calling using the [Trellis](https://www.nature.com/articles/s41598-021-02569-5) platform. However, SV calling can be expensive to to perform.
Performing analysis on the whole genome sequences can be very computational and time intensive. We would like to use ALCF's Polaris machine to perform the workflows for NGS sequence analysis.
We will have the opportunity to perform a population analysis so we can conclude with a Phewas analysis on the results from the whole genome analysis.

Below is a draft of what steps are needed to achieve the goals on this project. Please modify appropriately.

1. Get familiar with Polaris
   * Get user accounts
   * Login
   * Submit interactive and script jobs
2. Gather a set of NGS and PheWAS/GWAS tools that will be tested on Polaris. Each tool will most likely encounter its own issues and will have to deal with it appropriately.
   * NVIDIA Clara-Parabricks - Create Singularity container [[progress](https://github.com/exascale-genomics/mvp-wgs-sv/blob/main/parabricks_readme.md)]
   * [SVision](https://github.com/xjtu-omics/SVision)
   * [AstraZeneca tools](https://github.com/AstraZeneca)
   * SAIGE
   * ...
3. Test each of the tools from the previous set
4. Evaluate outputs - Determine which set of tools are best for our analysis, but be dynamic enough that if new tools come up, we can shift focus.
6. Download 1KG Whole genome datasets [Progress](https://github.com/exascale-genomics/mvp-wgs-sv/blob/main/data/1kg_download.txt)
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
19. Perform QC on SAIGE analysis
20. Post-process analysis - Will need Anurag and Jenny for this
    * What is different compared to gwPhewas analysis?
    * Novel SNPs, SVs (quantitities)
21. Share data
22. <b>Write paper on findings</b>
