import hail as hl
# Follow: https://github.com/nikbaya/ldscsim/tree/master

# Initialize hl and adjust the number of cores based on your laptop's capabilities
hl.init(local='local[4]')  

# pheno table containing the samples' gender.
pheno_table = hl.import_table("/Users/b54328/Desktop/1kg.British.pheno.txt", delimiter='\t', key='Samplename', types={'Samplename': hl.tstr, 'Sex': hl.tstr, 'Gender' : hl.tint32, 'BiosampleID': hl.tstr})
pheno_table2 = pheno_table.annotate(sc= pheno_table.Gender -1)

# Import the VCF that was created in Polaris from whole-genome seqs
vcf_file = '/Users/b54328/Desktop/merged.anno.vcf.bgz'
mt = hl.import_vcf(vcf_file, reference_genome="GRCh38", array_elements_required=False)
n_samples = 91
h2=0.5

# Create the simulated phenotype
mt1 = mt.annotate_rows(a1 = hl.rand_bool(p=0.01),
                          a2 = hl.rand_bool(p=0.05),
                          a3 = hl.rand_norm())
mt2 = hl.experimental.ldscsim.agg_fields(tb=mt1, str_expr='a', axis='rows') #
coef_dict = {'a1':0.3, 'a2':0.1, 'a3':0.4}
mt2 = hl.experimental.ldscsim.agg_fields(tb=mt1, coef_dict=coef_dict, axis='rows')
sim = hl.experimental.ldscsim.simulate_phenotypes(mt=mt2, genotype=mt2.GT, h2=0.1)
sim_binarize = hl.experimental.ldscsim.binarize(mt=sim, y=sim.y, K=0.2, exact=True)

# merge the pheno_table2 with the sim_binarize table
phenogeno_sim = sim_binarize.annotate_cols(**pheno_table2[sim_binarize.s])

# print the table
phenogeno_sim.cols().show(100)

# print to file to transfer back to Polaris to run GWAS
# We should also run GWAS using HAIL
# use: https://laderast.github.io/best_practices_dnanexus/hail-gwas.html

phenogeno_sim.cols().export("/Users/b54328/Desktop/pheno.tsv")



