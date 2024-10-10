# Installing SAIGE on Polaris using Conda

This guide provides steps to install SAIGE on the ALCF Polaris system using Conda. It includes necessary dependencies, configuration details, and troubleshooting tips.

## Prerequisites

1. **Access to Polaris**: Ensure you have access to the Polaris system.
2. **Conda**: Conda should be available on Polaris. If not, load or install Conda manually.

## Installation Steps

### Step 1: Create a Conda Environment

Create and activate a new Conda environment for SAIGE:

```bash
conda create -n saige-env -c conda-forge python=3.9
conda activate saige-env
```

### Step 2: Install Dependencies
SAIGE requires several R packages and additional libraries. Install these with the following commands:


```bash
conda install -c conda-forge r-base=4.2 r-essentials
conda install -c conda-forge r-optparse r-rcpp r-rcpparmadillo r-matrix r-data.table r-littler
```

Then, install OpenMPI:

```bash
conda install -c conda-forge openmpi
```

### Step 3: Install the GMP Library
Install the GMP library, required for multi-precision arithmetic operations:

```bash
conda install -c conda-forge gmp
```

### Step 4: Install Additional Libraries
Install other required libraries, such as Boost, CMake, and zlib:

```bash
conda install -c conda-forge boost cmake zlib
```

### Step 5: Clone and Configure SAIGE
Clone the SAIGE repository and navigate to its directory:

```bash
git clone https://github.com/weizhouUMICH/SAIGE.git
cd SAIGE
```

### Step 6: Update the Makefile
Modify the Makefile to specify the correct paths for OpenMPI. Locate the PKG_LIBS line and update it as follows:

```makefile
PKG_LIBS += -I$(CONDA_PREFIX)/include -L$(CONDA_PREFIX)/lib -lmpi
```

If you encounter errors related to -lmpi, try replacing it with -lmpi_cxx or -lmpicxx.

### Step 7: Compile SAIGE
To compile SAIGE, first clean any previous builds and then run make:

```bash
make clean
make
```

If you encounter linking errors, ensure that the PKG_LIBS line in the Makefile correctly references the MPI library.

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

