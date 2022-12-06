1. Download the bam (mapped on GRCh37), reference (GRCh37) and vcf files from GIAB server for HG002 (We use the GRCh37 as reference as the SV calls have been made using it as the reference and not GRCh38)\
Link to bam file: https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/AshkenazimTrio/HG002_NA24385_son/NIST_Illumina_2x250bps/novoalign_bams/ \
wget https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/AshkenazimTrio/HG002_NA24385_son/NIST_Illumina_2x250bps/novoalign_bams/HG002.hs37d5.2x250.bam \
Link to reference file: https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/references/GRCh37/ \
Link to VCF file: https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/release/AshkenazimTrio/HG002_NA24385_son/NIST_SV_v0.6/ \
Link to sequence file: N/A \
Parliament2 only requires the bam and the reference files (and optionally, the corresponding index files). So the sequence file is not requires (its information is implicitly present in the bam file) \

2. Run Parliament2 SV callers \
singularity run -B \`pwd\`/input:/home/dnanexus/in:rw -B \`pwd\`/output:/home/dnanexus/out:rw -H /lus/grand/projects/covid-ct/tarak/SVCallers/parliament2_HG002/outputs parliament2_latest.sif --bam HG002.hs37d5.2x250.bam --bai HG002.hs37d5.2x250.bam.bai -r hs37d5.fa --fai hs37d5.fa.fai --prefix lumpy_bd --lumpy --breakdancer 

