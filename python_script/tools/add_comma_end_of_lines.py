def add_comma_end_of_lines(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            stripped_line = line.rstrip()
            if not stripped_line.endswith(','):
                stripped_line += ','
            outfile.write(stripped_line + '\n')

input_file_path = 'fusion_heralding.json'
output_file_path = 'fusion_heraling_coma.json'
add_comma_end_of_lines(input_file_path, output_file_path)