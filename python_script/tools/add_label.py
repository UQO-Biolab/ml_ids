def add_label(input_file, output_file, string_to_add=',1'):
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                # Remove trailing whitespace (like newlines)
                stripped_line = line.rstrip()
                # Add the specified string at the end of the line
                new_line = f"{stripped_line}{string_to_add}\n"
                # Write the new line to the output file
                outfile.write(new_line)
        print(f"Modifications have been saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_file_path = 'ssh_legitimate_20000_shortid.csv'
output_file_path = 'ssh_legitimate_20000_label.csv'
add_label(input_file_path, output_file_path)
