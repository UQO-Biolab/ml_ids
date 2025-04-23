def filter_lines(liste):
    prefix="/home/benjamin/tpot_multiple_file/log/unzipped/"
    newlist= [prefix + element for element in liste]
    print(newlist)

    for file in newlist:
        file_filter = file.replace(".json", "_filtered.json")

        with open(file, 'r', encoding='utf-8') as f_entree:
            with open(file_filter, 'w', encoding='utf-8') as f_output:
                for ligne in f_entree:
                    if ligne.strip().startswith('{'):
                        f_output.write(ligne)

        print(f"Lines starting with '{{' have been written to {file_filter}.")