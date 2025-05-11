import sys
import pandas as pd
import Levenshtein

infile=sys.argv[1] # airr tsv format
outfile=sys.argv[2] # output annotation file as input for AffMB

df = pd.read_csv(infile,sep='\t',low_memory=False); df.dropna(subset=['productive'],inplace=True)
df = df[df['productive']=='T']
df['barcode'] = df['sequence_id'].str.split('_',expand=True)[0]
seq = df['sequence_alignment'].tolist(); germ = df['germline_alignment'].tolist()
df['shm'] = [Levenshtein.hamming(germ[i],seq[i])/len(seq[i]) for i in range(len(seq))]
#df.to_csv(outfile,index=False)
#output a subset of columns to reduce the output file size
df.to_csv(outfile,columns=['barcode','sequence_id','sequence','locus','v_call','j_call','c_call','sequence_alignment','germline_alignment','sequence_alignment_aa','germline_alignment_aa','c_sequence_alignment','c_sequence_alignment_aa','c_germline_alignment','c_germline_alignment_aa','fwr1','fwr1_aa','cdr1','cdr1_aa','fwr2','fwr2_aa','cdr2','cdr2_aa','fwr3','fwr3_aa','cdr3','cdr3_aa','fwr4','fwr4_aa','shm','v_identity','j_identity'],index=False)
