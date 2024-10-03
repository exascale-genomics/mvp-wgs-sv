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

  conda create -n hail
  conda activate hail
  pip install hail

  # also need to install openjdk
  conda install -c conda-forge openjdk
```

Try it out!
~~~~~~~~~~~

To try `batch` out, open iPython or a Jupyter notebook and run:


    >>> import hailtop.batch as hb
    >>> b = hb.Batch()
    >>> j = b.new_job(name='hello')
    >>> j.command('echo "hello world"')
    >>> b.run()
