import os
from functions.decompress_gz_files import decompress_gz_files
from functions.delete_unused_files import delete_unused_files
from functions.filter_json_lines import filter_lines
from functions.multiple_to_one_file import merge_files
from functions.json_format import fix_json_files

# Cowrie / honeytrap / ciscoasa / dionaea / sentrypeer 
selected_honeypots = ["cowrie", "h0neytr4p", "honeytrap", "ciscoasa", "dionaea", "sentrypeer", "tanner", "heralding","honeyaml"]
#filename_honeypots = ["cowrie.json.", "log.json.", "attacker.log.", "ciscoasa.log.", "dionaea.json.", "sentrypeer.json."]

# Paths
input_directory = '/home/benjamin/tpot_multiple_file/log/data'
output_directory = '/home/benjamin/tpot_multiple_file/log/unzipped'
honeypots_json = ["fusion_attackers.json", "fusion_ciscoasa.json", "fusion_cowrie.json", "fusion_log.json", "fusion_dionaea.json","fusion_log_session.json","fusion_tanner_report.json","fusion_honeyaml.json"]
honeypots_json_filtered = ["fusion_attackers_filtered.json", "fusion_ciscoasa_filtered.json", "fusion_cowrie_filtered.json", "fusion_log_filtered.json", "fusion_dionaea_filtered.json","fusion_log_session_filtered.json","fusion_tanner_report_filtered.json","fusion_honeyaml_filtered.json"]

for honeypot in selected_honeypots:
    log_path = os.path.join(input_directory, honeypot, "log")
    decompress_gz_files(log_path, output_directory)

delete_unused_files(output_directory)
merge_files(output_directory)
filter_lines(honeypots_json)
fix_json_files(honeypots_json)       
    

