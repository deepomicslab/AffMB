# AffMB
Affinity Maturation of B-cell receptors (AffMB)

## Requirements
python>=3.8 \
pandas, numpy, matplotlib, levenshtein, biopython, logomaker, networkx, python-igraph>=0.10.4, cairocffi \
Users are recommended to use **conda install \<package\>** and **pip3 install \<package\>** shown below to install these dependencies.
```
conda install pandas numpy matplotlib biopython logomaker "python-igraph>=0.10.4" cairocffi -c conda-forge -c bioconda
pip3 install levenshtein networkx
```
## Installation
After installing the above requirements, use pip3 to install AffMB:
```
pip3 install -i https://test.pypi.org/simple/ affmb
```
## Input
AffMB accepts two types of input: (i) raw contig file in FASTA format, or (ii) processed AIRR rearrangement file in TSV format. 

The AIRR-format TSV file must at least contain the following necessary fields: sequence_id, sequence, productive, locus, v_call, j_call, sequence_alignment, germline_alignment, fwr1, fwr1_aa, cdr1, cdr1_aa, fwr2, fwr2_aa, cdr2, cdr2_aa, fwr3, fwr3_aa, cdr3, cdr3_aa, fwr4, fwr4_aa.

For a raw input in FASTA format, AffMB calls an external V(D)J annotation tool IgBLAST to generate the AIRR rearrangement file in TSV format. 

### Use of IgBLAST
AffMB offwes an API function for calling IgBLAST on raw contig.fasta input to generate an AIRR rearrangement TSV file. 

The AIRR rearrangement file is a widely used format in immune sequencing. IgBLAST is one of the most popular tools that can generate the required AIRR-format TSV files. Simple instrctions are provided here to install IgBLAST: 

Download and uncompress the pre-compiled IgBLAST program at https://ftp.ncbi.nih.gov/blast/executables/igblast/release/LATEST/ \
Then go to the working directory of IgBLAST:
```
# the code below assumes linux environment; please select the suitable one to download. For further instructions see https://ncbi.github.io/igblast/cook/How-to-set-up.html
wget https://ftp.ncbi.nih.gov/blast/executables/igblast/release/LATEST/ncbi-igblast-1.22.0-x64-linux.tar.gz
tar -xvzf ncbi-igblast-1.22.0-x64-linux.tar.gz
cd ncbi-igblast-1.22.0
```
The **working directory** of IgBLAST should contain the following file structure:
```
bin
internal_data
optional_file 
```
**At the working directory**, download the human vdj and c gene databases for igblast that are used in the prepare python script: 
```
# run under igblast working directory
wget https://ftp.ncbi.nih.gov/blast/executables/igblast/release/database/airr/airr_c_human.tar
mkdir -p airr_c_human
tar -xvf airr_c_human.tar -C airr_c_human/

wget https://ftp.ncbi.nih.gov/blast/executables/igblast/release/database/ncbi_human_c_genes.tar
mkdir -p database/
tar -xvf ncbi_human_c_genes.tar -C database/
```

## Quick Start
### With raw contig.fasta input:
AffMB offers an API function run_igblast() that calls IgBLAST to generate the required AIRR-tsv input, note the path to the **IgBLAST working directory** must be specified to the **igblast_wd** parameter:
```
import affmb
affmb.run_igblast(infile='example/example.filtered_contig.fasta',outfile='example/example.filtered_contig.airr.tsv',igblast_wd='/mnt/Software/ncbi-igblast-1.22.0')
affmb.run_igblast(infile='example/bulk_contig13m.fasta',outfile='example/bulk_contig13m.igblast.airr.tsv',igblast_wd='/mnt/Software/ncbi-igblast-1.22.0')
```

### With processed AIRR-tsv input:
For single-cell input:
```
import subprocess
outdir = 'test_paired'
subprocess.run('mkdir -p '+outdir, shell=True)
infile = 'example/example.filtered_contig.airr.tsv'
sample_name = 'example'
affmb.paired_repertoire_analysis(infile,sample_name,outdir,depth_filter=2)

#Alternatively, if you want to analyze and visualize only the IGH chain in the single-cell data
#affmb.IGH_repertoire_analysis(infile,sample_name,outdir,depth_filter=2)
```
For bulk input:
```
# bulk (IGH) input
outdir = 'test_bulk'
subprocess.run('mkdir -p '+outdir, shell=True)
infile = 'example/bulk_contig13m.igblast.airr.tsv'
sample_name = 'bulk'
affmb.IGH_repertoire_analysis(infile,sample_name,outdir,depth_filter=2)
```
## Parameters
```
affmb.paired_repertoire_analysis(infile,sample_name,outdir,contig_id='sequence_id',cell_id=None,id_split='_contig',chain='locus',v_gene='v_call',j_gene='j_call',c_gene='c_call',clonotype='seq',shm='infer',sep='\t',grouping='stringent',depth_filter=2,method='inheritance',cdr1_nt='cdr1',cdr2_nt='cdr2',cdr3_nt='cdr3',fwr1_nt='fwr1',fwr2_nt='fwr2',fwr3_nt='fwr3',fwr4_nt='fwr4',logo=True,logo_dist_cutoff=0.1,logo_depth_cutoff=2,logo_thres=5,vertex_color='red')
affmb.IGH_repertoire_analysis(infile,sample_name,outdir,sequence_id='sequence_id',chain='locus',v_gene='v_call',j_gene='j_call',c_gene='c_call',clonotype='seq',shm='infer',sep='\t',grouping='stringent',depth_filter=2,method='inheritance',cdr1_nt='cdr1',cdr2_nt='cdr2',cdr3_nt='cdr3',fwr1_nt='fwr1',fwr2_nt='fwr2',fwr3_nt='fwr3',fwr4_nt='fwr4',logo=True,logo_dist_cutoff=0.1,logo_depth_cutoff=2,logo_thres=5,vertex_color='red')
```
>**infile**: input annotation file name \
**sample_name**: sample name, used as prefix for all output files \
**outdir**: output directory name, must be an existing directory \
**sequence_id**: the column name for the sequence ID in bulk data \[default: 'sequence_id'\] \
**contig_id**: the column name for the contig ID in paired (single-cell) data \[default: 'sequence_id'\] \
**cell_id**: the column name for the cell ID in paired (single-cell) data; if None, infer cell_id from contig_id by splitting the contig_id with a keyword specified by \`id_split\` \[default: None \] \
**id_split**: the keyword used to split contig_id to get cell_id. The cell_id will be anything on the left of the id_split. For example, the contig_id 'AAACCTGAGTACGACG-1_contig_1' with an id_split '_contig' will result in a cell_id 'AAACCTGAGTACGACG-1'. \[default: '_contig'\] \
**chain**: the column name for the chain type (IGH/IGL/IGK) information \[default: 'locus'\] \
**v_gene**: the column name for the V gene \[default: 'v_call'\] \
**j_gene**: the column name for the J gene \[default: 'j_call'\] \
**c_gene**: the column name for the C gene \[default: 'c_call'\] \
**clonotype**: definition of clonotype, either the full V region ('seq') or the combination of all CDR regions ('cdrs') \[default: 'seq'\] \
**shm**: the column name for the SHM rate; set shm='v_identity' if you want to approximate SHM rate with 'v_identity' \[default: 'shm'\] \
**sep**: delimiter of the input file \[default: '\t'\] \
**grouping**: determines whether or not to allow indels at CDR regions in a lineage. Choose 'stringent' to keep identical CDR lengths in a lineage, choose 'loose' to allow CDR indels (up to 3bp in total) in a lineage. \[default: 'stringent'\] \
**depth_filter**: lineage depth threshold under which lineage trees will not be plot, reduces the number of generated tree figures; set depth_filter=0 to stop the filter \[default: 2\] \
**method**: algorithms for tree construction, choose within {'inheritance','prims'} \[default: 'inheritance'\] \
**fwr1_nt**: the column name for the fwr1 nucleotide (nt) sequence \[default: 'fwr1'\] \
**cdr1_nt**: the column name for the cdr1 nucleotide (nt) sequence \[default: 'cdr1'\] \
**fwr2_nt**: the column name for the fwr2 nucleotide (nt) sequence \[default: 'fwr2'\] \
**cdr2_nt**: the column name for the cdr2 nucleotide (nt) sequence \[default: 'cdr2'\] \
**fwr3_nt**: the column name for the fwr3 nucleotide (nt) sequence \[default: 'fwr3'\] \
**cdr3_nt**: the column name for the cdr3 nucleotide (nt) sequence \[default: 'cdr3'\] \
**fwr4_nt**: the column name for the fwr4 nucleotide (nt) sequence \[default: 'fwr4'\] \
**logo**: whether to detect branches of interest and generate logo plots \[default: True\] \
**logo_dist_cutoff**: determines the largest possible pairwise edit distance between nodes in a branch of interest \[default: 0.1\] \
**logo_depth_cutoff**: determines the minimal depth of a branch of interest \[default: 2\] \
**logo_thres**: determines the minimal size of a branch of interest \[default: 5\] \
**vertex_color**: the color of the nodes in the lineage tree figures \[default: 'red'\]

## Output
The figure below is a graphical summary of AffMB output.
![fig1 affmb_example_output](https://github.com/user-attachments/assets/cdddf94c-14f2-46af-9c29-9fea7081cc75)
The output of running AffMB on the example.filtered_contig.annotation.csv is shown in the [test_paired](test_paired) folder. A typical AffMB output directory contains multiple lineage tree figures (one tree per figure) with depth_filter applied (in this example depth_filter=2 is applied) and a csv table file which provides cell-to-node mapping to the lineage tree figures. If branches of interest are detected, logo plots at amino acid and nucleotide levels will also be generated. A summary plot of lineage statistics are also generated for the depth of the lineages, the dominated Ig type of the lineages, the extent of clonal expansion of the lineages, and the lineage size (i.e., number of unique genotypes in lineage).
