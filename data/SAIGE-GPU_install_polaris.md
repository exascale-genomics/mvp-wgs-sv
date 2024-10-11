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

### Step 1: Create a Conda Environment

Create and activate a new Conda environment for SAIGE:

```bash
conda create -n RSAIGE r-essentials r-base=4.2 python=3.10
conda activate RSAIGE
conda env export > environment-RSAIGE.yml

```

### Step 2: Install Dependencies
SAIGE requires several R packages and additional libraries. Install these with the following commands:


```bash
conda install -c r r-rcpp  r-rcpparmadillo r-data.table r-bh r-matrix
conda install -c conda-forge r-spatest r-rcppeigen r-devtools  r-skat r-rcppparallel r-optparse boost openblas r-rhpcblasctl r-metaskat r-skat r-qlcmatrix r-rsqlite r-matrix
```

Then, install OpenMPI and other dependencies:

```bash
conda install -c conda-forge openmpi
conda install -c anaconda cmake
conda install -c conda-forge gettext lapack
conda install bioconda::savvy
conda install conda-forge::superlu
pip3 install cget click
```


### Step 3: Install Additional Libraries
Install other required libraries, such as Boost and zlib:

```bash
conda install -c conda-forge boost  zlib
```

### Step 4: Clone and Configure SAIGE-GPU
Clone the SAIGE repository and navigate to its directory:

```bash
git clone https://github.com/exascale-genomics/SAIGE-GPU.git
cd SAIGE-GPU
```

### Step 5: Update the ./src/Makevars
Modify the Makevars file to specify the correct paths for OpenMPI. Locate the PKG_LIBS line and update it as follows:

```Makevars
PKG_LIBS += -I$(CONDA_PREFIX)/include -L$(CONDA_PREFIX)/lib -lmpi
```

If you encounter errors related to -lmpi, try replacing it with -lmpi_cxx or -lmpicxx.

In addition, modify the top lines in the Makevars file by commenting out the "showme" commands and adding the "cray" lines:

```Makevars
MPI_CPPFLAGS = $(shell CC --cray-print-opts=cflags)
MPI_LDFLAGS = $(shell CC --cray-print-opts=libs)

#MPI_CPPFLAGS = $(shell mpic++ -showme:compile)
#MPI_LDFLAGS = $(shell mpic++ -showme:link)
```


### Step 6: Compile SAIGE
To compile SAIGE-GPU, first clean any previous builds and then run make:

```bash
make clean
cd ../.
R CMD INSTALL --library=$PWD/SAIGE-GPU SAIGE-GPU
```

If you encounter linking errors, ensure that the PKG_LIBS line in the Makevars file correctly references the MPI library.

### Step 7: Update the paths to the SAIGE library in the step1 and step2 scripts
You will need to update the paths on the scripts for step1 and step2 to your SAIGE library location:

```./extdata/step1_fitNULLGLMM.R
.libPaths(c(.libPaths(), "$PWD/SAIGE-GPU"))
library(SAIGE)
require(pbdMPI)
```

```./extdata/step2_SPAtests.R
.libPaths(c(.libPaths(), "$PWD/SAIGE-GPU"))
library(SAIGE)
```

### Step 8: Verify Installation
Check if the installation was successful by running the following commands:

```bash
./step1_fitNULLGLMM.R --help
./step2_SPAtests.R --help
```

If the help information is displayed for each command, the installation is complete.

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

