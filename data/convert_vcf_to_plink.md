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
