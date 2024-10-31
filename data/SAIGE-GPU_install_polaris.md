# Installing SAIGE on Polaris using Conda

This guide provides steps to install SAIGE on the ALCF Polaris system using Conda. It includes necessary dependencies, configuration details, and troubleshooting tips.

## Prerequisites

1. **Access to Polaris**: Ensure you have access to the Polaris system.
2. **Conda**: Conda should be available on Polaris.

```bash
module use /soft/modulefiles/
module load conda/2024-04-29
```

## Installation Steps

### Step 1: Create directory and clone the SAIGE-DOE GitHub repository

Create and activate a new Conda environment for SAIGE:

```bash
mkdir SAIGE-GPU
cd SAIGE-GPU
git clone https://github.com/exascale-genomics/SAIGE-DOE.git
cd SAIGE-DOE/
git pull origin SAIGE-step1GPU-step2Wei-openmpi
```

### Step 2: Create a Conda Environment

Create and activate a new Conda environment for SAIGE. We will be using the existing YML file from the repository.
In this example I am naming my environment `RSAIGE_GPU_V2`, you can replace with your desired name. 
In addition, due to the size of the conda environment and packages, I will be installing the environment in a different mount where I have more space. You can create your environment either in your home directory if you have enough space, or your project space.

```bash
conda env create  --file=./conda_env/environment-RSAIGE.yml -p /grand/projects/GeomicVar/rodriguez/conda_envs/RSAIGE_GPU_V2
conda activate /grand/projects/GeomicVar/rodriguez/conda_envs/RSAIGE_GPU_V2
```

### Step 3: Install Dependencies
SAIGE requires several packages and libraries. Install these with the following commands:


```bash
pip3 install cget click
conda install cuda -c nvidia/label/cuda-11.4.3
```

You need to install openMPI version `4.1.5`. This is difficult to perform within Conda, so we will install separately, but then include it in our Conda environment:

```bash
cd /grand/projects/GeomicVar/rodriguez/conda_envs/pkgs
wget https://download.open-mpi.org/release/open-mpi/v4.1/openmpi-4.1.5.tar.gz tar -xzf openmpi-4.1.5.tar.gz
cd openmpi-4.1.5
./configure --prefix=/grand/projects/GeomicVar/rodriguez/conda_envs/RSAIGE_GPU_V2/opt/openmpi
make -j4
make install
export PATH=/grand/projects/GeomicVar/rodriguez/conda_envs/RSAIGE_GPU_V2/opt/openmpi/bin:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/grand/projects/GeomicVar/rodriguez/conda_envs/RSAIGE_GPU_V2/opt/openmpi/lib

mkdir -p $CONDA_PREFIX/etc/conda/activate.d
mkdir -p $CONDA_PREFIX/etc/conda/deactivate.d
echo 'export PATH=$CONDA_PREFIX/opt/openmpi/bin:$PATH' > $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
echo 'export LD_LIBRARY_PATH=$CONDA_PREFIX/opt/openmpi/lib:$LD_LIBRARY_PATH' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
```

Install other required libraries, such as pbdMPI, savvy, superlu:

```bash
Rscript -e 'install.packages("pbdMPI", repos=c("https://cloud.r-project.org"))'
conda install -c conda-forge -c bioconda savvy
conda install conda-forge::superlu
```

### Step 4: Compile SAIGE
To compile SAIGE-GPU, first clean any previous builds and then run make:

```bash
cd ~/SAIGE-GPU
R CMD INSTALL SAIGE-DOE
```

If you encounter linking errors, ensure that the PKG_LIBS line in the Makevars file correctly references the MPI library.

### Step 5: Verify Installation
Check if the installation was successful by running the following commands where the output should be the list of parameter options:

```bash
path_to_saige=~/SAIGE-GPU_3/SAIGE-DOE
Rscript $path_to_saige/extdata/step1_fitNULLGLMM.R --help
```

If the help information is displayed for each command, the installation is complete.

You can also run a test with the provided test input files. You can replace `mpirun -n 4` in the command below with the appropriate number of GPUs you have available.

```bash
# ask for a node
qsub -A geomicVar -I -l select=1 -l walltime=1:00:00 -l filesystems=home:eagle -q debug

# once the node is provided
module use /soft/modulefiles/
module load conda
conda activate /grand/projects/GeomicVar/rodriguez/conda_envs/RSAIGE_GPU_V2

path_to_saige=~/SAIGE-GPU_3/SAIGE-DOE
mpirun -n 4 Rscript $path_to_saige/extdata/step1_fitNULLGLMM.R \
--plinkFile=$path_to_saige/extdata/input/plinkforGRM_1000samples_10kMarkers \
--phenoFile=$path_to_saige/extdata/input/pheno_1000samples.txt \
--invNormalize=FALSE \
--phenoCol=y \
--covarColList=x1,x2 \
--sampleIDColinphenoFile=IID \
--traitType=binary \
--outputPrefix=./GPU_step1_output \
--minMAFforGRM 0.01 \
--LOCO  \
 --IsOverwriteVarianceRatioFile=TRUE \
--nThreads=1
```

You should see a succesful run where all GPUs are used. The log should provide the IDs of the GPUs used.

## Troubleshooting

- **Library Not Found Error (`-lmp` not found)**:
  - Ensure the correct MPI library is referenced in the Makefile:
    - Check if you should use `-lmpi`, `-lmpi_cxx`, or `-lmpicxx`.
  
- **Missing Headers or Libraries**:
  - Verify that all dependencies are installed:
    - Ensure you followed the installation steps for all required packages.
  - Confirm that paths in the `PKG_LIBS` line point to the correct directories:
    - Update the Makefile to reflect the paths from your Conda environment.
  
- **Compilation Errors**:
  - If you encounter errors during compilation, try cleaning the build and recompiling:
    ```bash
    make clean
    make
    ```
  - Check for additional error messages that may indicate missing dependencies.

- **R Package Issues**:
  - If you experience problems with R packages, ensure that they are installed in the correct Conda environment.
  - You can check the installed R packages with:
    ```bash
    Rscript -e "installed.packages()"
    ```

## Conclusion

By following these steps, you should have SAIGE installed and ready to use on Polaris with Conda. Make sure to adjust environment variables and paths as needed based on your setup.

