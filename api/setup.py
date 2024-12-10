def replace_line_in_file(file_path, variable_name, new_line):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.startswith(variable_name):
            lines[i] = new_line + '\n'
            break

    with open(file_path, 'w') as file:
        file.writelines(lines)
