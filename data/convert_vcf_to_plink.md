# Converting VCF to PLINK Binary Format (BED/BIM/FAM)

This guide explains how to convert a VCF file to PLINK's binary format (BED/BIM/FAM) while filtering out multiallelic variants.
We use PLINK's `--biallelic-only` option to handle multiallelic sites, which are not supported in PLINK's binary format.

## Requirements

- [PLINK](https://www.cog-genomics.org/plink/2.0/) (Version 1.9 or later)
- Input VCF file (`input.vcf`)

## Steps

### Step 1: Install PLINK

If you don't have PLINK installed, follow these steps to install it.

#### On Linux or macOS:
1. Download PLINK:

    ```bash
    wget https://s3.amazonaws.com/plink1-assets/plink_linux_x86_64.zip -O plink.zip
    ```

2. Unzip the package:

    ```bash
    unzip plink.zip
    ```

3. Move the `plink` binary to a directory in your PATH (e.g., `/usr/local/bin`):

    ```bash
    sudo mv plink /usr/local/bin
    ```

4. Verify the installation by checking the PLINK version:

    ```bash
    plink --version
    ```

### Step 2: Convert VCF to PLINK Format with Biallelic Filter

1. Use the following command to convert your VCF file while filtering out multiallelic variants:

    ```bash
    plink --vcf input.vcf --biallelic-only strict --make-bed --out output_file
    ```

    - Replace `input.vcf` with the path to your VCF file.
    - Replace `output_file` with the desired prefix for the output files.

2. This command will generate three output files:
   - `output_file.bed`: The binary genotype file.
   - `output_file.bim`: The extended MAP file.
   - `output_file.fam`: The extended pedigree file.

## Explanation of Options

- `--vcf input.vcf`: Specifies the input VCF file.
- `--biallelic-only strict`: Filters out multiallelic variants, ensuring only biallelic sites are included.
- `--make-bed`: Converts the data to PLINK binary format (BED/BIM/FAM).
- `--out output_file`: Specifies the output file prefix.

## Troubleshooting

### Error: `cannot contain multiallelic variants`
If you encounter this error, make sure that the `--biallelic-only strict` option is included in your PLINK command. This option filters out any variants with more than two alleles.

## Additional Information

- PLINK documentation: [https://www.cog-genomics.org/plink/1.9/](https://www.cog-genomics.org/plink/1.9/)
  
By following these instructions, you should be able to successfully convert your VCF file to PLINK binary format while filtering out any multiallelic variants.

# PLINK Filtering and Pruning Workflow

This section describes the steps to filter and prune PLINK BED files to remove low-quality variants and ensure unique variant IDs.

## Requirements

- [PLINK 2.0](https://www.cog-genomics.org/plink/2.0/) installed and available in your environment.
- Input PLINK files in BED format (`.bed`, `.bim`, `.fam`).

## Steps

### Step 1: Filter Variants

Filter variants based on:
- Minor Allele Frequency (MAF) threshold of 0.01
- Hardy-Weinberg Equilibrium (HWE) threshold of 0.0001
- Missing genotype rate threshold of 0.1

```bash
./plink2/plink2 --bfile ../../output/merged/merged.anno \
  --maf 0.01 \
  --hwe 0.0001 \
  --geno 0.1 \
  --make-bed \
  --out ../../output/merged/merged.anno.geno.hwe.maf
```

This command will generate a new set of files with only the variants passing these filters:

- `merged.anno.geno.hwe.maf.bed`
- `merged.anno.geno.hwe.maf.bim`
- `merged.anno.geno.hwe.maf.fam`

### Step 2: Prune Variants

After filtering, prune the variants to remove those in linkage disequilibrium (LD). This step also ensures all variant IDs are unique.

```bash
./plink2/plink2 --bfile ../../output/merged/merged.anno.geno.hwe.maf \
  --indep-pairwise 50 5 0.2 \
  --make-bed \
  --set-all-var-ids @:#:$r:$a \
  --out ../../output/merged/merged.anno.geno.hwe.maf.pruned \
  --new-id-max-allele-len 507
```

- `--indep-pairwise 50 5 0.2`: This performs LD pruning based on a window of 50 SNPs, moving by 5 SNPs at a time, with an r² threshold of 0.2.
- `--set-all-var-ids @:#:$r:$a`: This sets each variant ID to a unique format including chromosome, position, reference allele, and alternate allele.
- `--new-id-max-allele-len 507`: Ensures the new variant IDs comply with length requirements.

This will produce a new set of pruned PLINK files:

- `merged.anno.geno.hwe.maf.pruned.bed`
- `merged.anno.geno.hwe.maf.pruned.bim`
- `merged.anno.geno.hwe.maf.pruned.fam`

## Output Files

- **Filtered files (`merged.anno.geno.hwe.maf.*`)**: These files include variants passing MAF, HWE, and missing genotype rate thresholds.
- **Pruned files (`merged.anno.geno.hwe.maf.pruned.*`)**: These files contain a subset of variants, pruned for LD and assigned unique variant IDs.

## Additional Information

- If any errors are encountered with non-unique variant IDs, ensure to use the `--set-all-var-ids` option with unique format parameters as shown.
- For more advanced filtering and pruning options, refer to the [PLINK 2.0 documentation](https://www.cog-genomics.org/plink/2.0/).

## Troubleshooting

- **Error: `cannot contain multiallelic variants`** - Ensure input files contain only biallelic variants. You may need to pre-process the files to remove multiallelic variants.
- **Error: `non-unique variant IDs`** - Use the `--set-all-var-ids` option as demonstrated to create unique IDs.

## Notes
- Variant Filtrations:
Variants were combined across the Wellderly and ITMI cohorts via GenomeComb and filtered using metrics based on optimized features selected based on concordance between monozygotic twins (Reumers et al., 2011) and refined based on observed GWAS genomic inflation. These filters excluded variants that were (1) labeled as VQLOW in all individuals, (2) clustered in >10% of individuals from either cohort, (3) variants missing in >10% of either cohort, 4) with median coverage <10 or >100 in either cohort, 5) in simple repeats, homopolymer repeats ≥6 bp, segmental duplications, microsatellite repeats, or low-complexity repeats, (5) out of the Hardy-Weinberg Equilibrium (p value < 1 × 10−5), and (6) in non-unique 36-mers (Derrien et al., 2012). VQLOW genotypes were set to missing. For common variant analyses, an additional filter for variants <5% minor allele frequency in either cohort was applied. For rare variant analyses, an additional filter for variants >1% minor allele frequency in either cohort was applied, as well as a minimum allele depth filter, where if 20% of individuals with a rare variant alternate allele call had a minimum alternate allele depth of <25% of total reads or fewer than three supporting reads, the variant was considered a false positive and removed.

