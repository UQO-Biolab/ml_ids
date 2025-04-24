## 🚀 Use

These tools were built to assist with data cleansing and dataset creation:

| Script Name                     | Description                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| `add_comma_end_of_lines.py`      | Add commas to the end of lines in JSONL dictionary files (fixing format)   |
| `check_port_range.py`            | Check the port range in a Honeytrap JSON file to validate entries           |
| `correlation_suricata.py`        | Correlate Suricata logs with Honeytrap logs for labeling                    |
| `json_to_csv_cowrie.py`          | Convert Cowrie JSON logs to CSV and compute useful fields                   |
| `json_to_pcap.py`                | Convert a Honeytrap JSON file to a PCAP file for Suricata/Wireshark analysis|
| `keep_20k_lines_only.py`         | Parse a file and retain only 20k lines for dataset creation                 |
| `merge_and_shuffle_rows.py`      | Merge two CSV files and shuffle the rows (used for mixing labeled data)    |
| `add_string_to_each_line.py`     | Append a specific string (e.g., `,1`) to every line of a file (labeling)    |
| `update_login_success.py`        | Set `login_success` to 0 for rows where the label is 1, useful for cleaning and aligning labels before model training |
| `total_login_equal_to_login_failed.py` | Set `login_failed` equal to `total_connexion` when the label is 1, useful for cleaning the dataset before model training |
