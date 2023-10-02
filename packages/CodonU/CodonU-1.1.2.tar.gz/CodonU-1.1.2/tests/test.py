from CodonU.vizualizer import *

handle = '/home/souro/Projects/CodonU/tests/results/prot.fasta'
organism = 'Staphylococcus aureus subsp. aureus str. Newman'
folder_path = '/home/souro/Projects/CodonU/tests/results'

plot_ca_aa_freq_gene(handle, 11, scale='gravy', organism_name=organism, folder_path=folder_path, save_image=True)
