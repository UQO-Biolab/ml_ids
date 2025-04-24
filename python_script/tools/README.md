## 🚀 Use

These tools were built to assist with data cleansing and dataset creation:

| Script Name                           | Description                                                                 |
|---------------------------------------|-----------------------------------------------------------------------------|
| `add_comma_end_of_lines.py`           | Add commas to the end of lines in JSONL dictionary files (fixing format)   |
| `check_port_range.py`                 | Check the port range in a Honeytrap JSON file to validate entries (Honeytrap) |
| `correlation_suricata.py`             | Correlate Suricata logs with Honeytrap logs for labeling                    |
| `json_to_csv_cowrie.py`               | Convert Cowrie JSON logs to CSV and compute useful fields                   |
| `json_to_pcap.py`                     | Convert a Honeytrap JSON file to a PCAP file for Suricata/Wireshark analysis|
| `keep_20k_lines_only.py`              | Parse a file and retain only 20k lines for dataset creation                 |
| `merge_and_shuffle_rows.py`           | Merge two CSV files and shuffle the rows (used for mixing labeled data)    |
| `add_string_to_each_line.py`          | Append a specific string (e.g., `,1`) to every line of a file (labeling)    |
| `total_login_equal_to_login_failed.py`| Set `login_failed` equal to `total_connexion` when the label is 1 (Cowrie) |
| `correct_avg_failed_login.py`         | Calculate and assign the average time between failed logins when conditions are met (Cowrie) |
| `login_success_to_0.py`               | Set `login_success` to 0 when the label is 1 (Cowrie)                       |
