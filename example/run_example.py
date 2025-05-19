import subprocess,affmb

# paired (single-cell) data
igblast_wd = '/mnt/Software/ncbi-igblast-1.22.0'
infile = 'example.filtered_contig.fasta'
affmb.run_igblast(infile=infile,outfile='example.filtered_contig.airr.tsv',igblast_wd=igblast_wd)

outdir = 'test_paired'
subprocess.run('mkdir -p '+outdir, shell=True)
sample_name = 'example'
affmb.paired_repertoire_analysis('example.filtered_contig.airr.tsv',sample_name,outdir,depth_filter=2)
affmb.paired_repertoire_analysis('example.filtered_contig.airr.tsv',sample_name,outdir,clonotype='cdrs',depth_filter=2)

# bulk data
infile = 'example.filtered_contig.fasta'
affmb.run_igblast(infile='bulk_contig13m.fasta',outfile='bulk_contig13m.igblast.airr.tsv',igblast_wd=igblast_wd)

outdir = 'test_bulk'
subprocess.run('mkdir -p '+outdir, shell=True)
sample_name = 'bulk'
affmb.IGH_repertoire_analysis('bulk_contig13m.igblast.airr.tsv',sample_name,outdir,clonotype='cdrs',depth_filter=2)