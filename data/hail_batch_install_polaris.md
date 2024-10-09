# Install HAIL batch on ALCF Polaris

HAIL-Batch will be used to generate synthetic phenotype files for the 1KG whole-genome sequences we processed through the variant calling pipeline.
We will install using Conda environment:

```
  module use /soft/modulefiles
  module load conda
  module load cray-python/3.11.5

  hail_home=/grand/projects/GeomicVar/rodriguez/1kg_proj/data/tools/hail
  mkdir -p $hail_home
  cd $hail_home

  conda create -n hail python'==3.9'
  conda activate hail
  conda install conda-forge/label/cf202003::openjdk # java 11
  conda install anaconda::libopenblas
  pip install hail==0.2.132

```

Try it out!
~~~~~~~~~~~

To try `batch` out, open iPython or a Jupyter notebook and run:


    >>> import hailtop.batch as hb
    >>> b = hb.Batch()
    >>> j = b.new_job(name='hello')
    >>> j.command('echo "hello world"')
    >>> b.run()

## HAIL ldscsim on Polaris
ldscsim does not work on Polaris. We need to take a further look. For now I transferred the 1KG VCF to my  laptop and ran it locally.
