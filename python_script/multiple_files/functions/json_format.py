def fix_json_files(honeypots_json):
    prefixe="/home/benjamin/tpot_multiple_file/log/unzipped/"
    honeypots_json_pref = [prefixe + element for element in honeypots_json]
    
    for input_path in honeypots_json_pref:
        with open(input_path, 'r') as file:
            lines = file.readlines()

        # Add a comma to the end of each line except the last one
        fixed_lines = [line.strip() + ',' for line in lines[:-1]]
        fixed_lines.append(lines[-1].strip())

        # Join lines into a single string
        fixed_json = '[' + '\n'.join(fixed_lines) + ']'

        # Set the output path for the corrected file
        output_path = input_path.replace('.json', '_coma.json')

        with open(output_path, 'w') as file:
            file.write(fixed_json)
