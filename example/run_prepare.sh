export PATH=$PATH:/mnt/Downloads/ncbi-igblast-1.18.0/bin
export IGDATA=/mnt/Downloads/ncbi-igblast-1.18.0

igblastn -germline_db_V $IGDATA/airr_c_human/airr_c_human_ig.V -germline_db_J $IGDATA/airr_c_human/airr_c_human_ig.J -germline_db_D $IGDATA/airr_c_human/airr_c_human_igh.D -c_region_db $IGDATA/database/ncbi_human_c_genes -organism human -auxiliary_data $IGDATA/optional_file/human_gl.aux -query example.filtered_contig.fasta -ig_seqtype Ig -outfmt 19 > example.filtered_contig.igblast.airr.tsv
python igblast_parser.py example.filtered_contig.igblast.airr.tsv example.filtered_contig.annotation.csv

igblastn -germline_db_V $IGDATA/airr_c_human/airr_c_human_ig.V -germline_db_J $IGDATA/airr_c_human/airr_c_human_ig.J -germline_db_D $IGDATA/airr_c_human/airr_c_human_igh.D -c_region_db $IGDATA/database/ncbi_human_c_genes -organism human -auxiliary_data $IGDATA/optional_file/human_gl.aux -query bulk_contig13m.fasta -ig_seqtype Ig -outfmt 19 > bulk_contig13m.igblast.airr.tsv
python igblast_parser.py bulk_contig13m.igblast.airr.tsv bulk_contig13m.annotation.csv
