import csv

input_file = 'cowrie_sessions.csv'
output_file = 'cowrie_sessions_20k.csv'

with open(input_file, mode='r', newline='') as infile, open(output_file, mode='w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    for i, row in enumerate(reader):
        if i < 20001:
            writer.writerow(row)
        else:
            break