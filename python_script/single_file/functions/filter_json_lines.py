def filter_lines(single_json, single_json_filtered):
    with open(single_json, 'r', encoding='utf-8') as f_entree:
        with open(single_json_filtered, 'w', encoding='utf-8') as f_sortie:
            # Reading the input file line by line
            for ligne in f_entree:
                # Check if line starts with '{'
                if ligne.strip().startswith('{'):
                    # Writing the line to the output file
                    f_sortie.write(ligne)

    print(f"Lines starting with '{{' were written in {single_json_filtered}.")
