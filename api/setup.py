import os

def replace_line_in_file(file_path, variable_name, new_line):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.startswith(variable_name):
            lines[i] = new_line + '\n'
            break

    with open(file_path, 'w') as file:
        file.writelines(lines)

if __name__ == "__main__":
    user = os.environ.get('DB_USER', 'sevensuiteuser')
    password = os.environ.get('DB_PASSWORD', 'development-sevensuiteapp')
    host = os.environ.get('DB_HOST', 'db')
    database = os.environ.get('DB_NAME', 'sevensuite')

    connection_string = f'mariadb+mariadbconnector://{user}:{password}@{host}/{database}'

    first_file_path = '/app/alembic.ini'
    first_variable_name = 'sqlalchemy.url'
    first_new_line = "sqlalchemy.url = " + connection_string

    second_file_path = '/app/alembic/env.py'
    second_variable_name = 'target_metadata'
    second_new_line = "\n".join([
        "from models.migrate import return_target_metadata",
        "target_metadata = return_target_metadata()"
    ])

    replace_line_in_file(first_file_path, first_variable_name, first_new_line)
    replace_line_in_file(second_file_path, second_variable_name, second_new_line)

    print("Successfully updated the Alembic configuration files.")
