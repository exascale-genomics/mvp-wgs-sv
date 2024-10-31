# SAIGE-GPU Running Instructions on Polaris

This README provides step-by-step instructions on how to run SAIGE-GPU on the Polaris system at the ALCF. The instructions cover requesting a compute node, loading the necessary modules, activating a Conda environment, and running the SAIGE step 1 script.

## Prerequisites

1. **SAIGE-GPU Installed:** Ensure SAIGE-GPU and dependencies are installed within your Conda environment.
2. **Files Available:** Make sure you have your phenotype file, plink files, and any other necessary data available on the system.

## Step-by-Step Instructions

### 1. Request a Compute Node

Use the following command to request an interactive compute node:

```bash
qsub -A geomicVar -I -l select=1 -l walltime=1:00:00 -l filesystems=home:eagle -q debug
```

This command will request a node under the `geomicVar` project with a walltime of 1 hour and access to the `home` and `eagle` filesystems. The `-q debug` option requests a debug queue for testing.

### 2. Load Module Files
Load the module files for Conda and any other necessary dependencies:

```bash
module use /soft/modulefiles/
module load conda
```

### 3. Activate the Conda Environment
Activate your Conda environment where SAIGE-GPU is installed. For example:

```bash
conda activate /grand/projects/GeomicVar/rodriguez/conda_envs/RSAIGE_GPU_V2
```

### 4. Run SAIGE Step 1: Fit NULL GLMM
Use the `mpiexec` command to run the SAIGE step 1 script, `step1_fitNULLGLMM.R`, with your desired parameters. Adjust the paths and options according to your files and analysis requirements:

```bash
path_to_saige=~/SAIGE-GPU_3/SAIGE-DOE
output_path="/grand/projects/GeomicVar/rodriguez/1kg_proj/output"
mpiexec -n 4 Rscript $path_to_saige/extdata/step1_fitNULLGLMM.R \
  --plinkFile=$output_path/merged/merged.anno.geno.hwe.maf.pruned \
  --phenoFile=$output_path/sim_phenotype/pheno.tsv \
  --invNormalize=FALSE \
  --phenoCol=y_binarized \
  --covarColList=sc \
  --sampleIDColinphenoFile=s \
  --traitType=binary \
  --outputPrefix=$output_path/SAIGE_test/sim_test \
  --minMAFforGRM 0.01 \
  --LOCO FALSE \
  --IsOverwriteVarianceRatioFile=TRUE \
  --nThreads=1 \
  --memoryChunk 2
```

Replace `$path_to_saige` with the path where SAIGE-GPU is installed on your system. Modify the file paths and parameters based on your data and specific analysis needs.

## Troubleshooting

- `Error in barrier(comm = 0) : could not find function "barrier"`: Ensure the `pbdMPI` package is installed in your R environment. You may need to load MPI libraries or reinstall `pbdMPI` if issues persist.

## Additional Information

- Ensure that your phenotype file is formatted correctly and that all specified columns (e.g., `--phenoCol`, `--covarColList`, `--sampleIDColinphenoFile`) are present in the file.
- Ensure that your Plink input bim file does not have chromosomes with textual form (i.e. `X`, `Y`). Replace with `23` and `24` respectively if they appear.
- For larger data sets, consider adjusting the `memoryChunk` value to better accommodate your system's available memory.

By following these instructions, you should be able to successfully run SAIGE-GPU on Polaris. Adjust the parameters as necessary for your specific analysis needs.
