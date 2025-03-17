import os
from functions.decompress_gz_files import decompress_gz_files
from functions.delete_unused_files import delete_unused_files
from functions.filter_json_lines import filtrer_lignes
from functions.multiple_to_one_file import fusionner_fichiers
from functions.json_tester import tester_fichier_json

# Cowrie / honeytrap / ciscoasa / dionaea / sentrypeer 
selected_honeypots = ["cowrie", "h0neytr4p", "honeytrap", "ciscoasa", "dionaea", "sentrypeer"]
#filename_honeypots = ["cowrie.json.", "log.json.", "attacker.log.", "ciscoasa.log.", "dionaea.json.", "sentrypeer.json."]

# Paths
input_directory = '/home/benjamin/tpot/log/data'
output_directory = '/home/benjamin/tpot/log/unzipped'
single_json = '/home/benjamin/tpot/log/final_result'
single_json_filtered = '/home/benjamin/tpot/log/final_result_filtered'

for honeypot in selected_honeypots:
    log_path = os.path.join(input_directory, honeypot, "log")
    decompress_gz_files(log_path, output_directory)

delete_unused_files(output_directory)
fusionner_fichiers(output_directory, single_json)
filtrer_lignes(single_json, single_json_filtered)
tester_fichier_json(single_json_filtered)
       
    

