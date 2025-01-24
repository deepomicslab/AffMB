from affmb import affmb
import subprocess

outdir = 'test_paired'
subprocess.call('mkdir -p '+outdir,shell=True)
vdj_file = 'example.filtered_contig.annotation.csv'
affmb.paired_repertoire_analysis(vdj_file,outdir,depth_filter=2)

outdir = 'test_bulk'
subprocess.call('mkdir -p '+outdir,shell=True)
vdj_file = 'bulk_contig13m.annotation.csv'
affmb.IGH_repertoire_analysis(vdj_file,outdir,depth_filter=2)
