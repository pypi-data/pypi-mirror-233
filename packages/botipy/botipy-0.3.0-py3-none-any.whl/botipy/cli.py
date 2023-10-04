import argparse
import os
import shutil

def create_project(args):
    project_name = args.project_name

    project_dir = os.path.join(os.getcwd(), project_name)
    os.makedirs(project_dir, exist_ok=True)

    src_dir = os.path.join(project_dir, 'src')
    os.makedirs(src_dir)

    cog_dir = os.path.join(src_dir, 'cog')
    os.makedirs(cog_dir)
    with open(os.path.join(cog_dir, '__init__.py'), 'w') as init_file:
        pass

    template_dir = os.path.join(os.path.dirname(__file__), 'src')
    files_to_copy = ['app.py', 'bot.py', 'Makefile', 'Procfile', 'requirements.txt']

    for file_name in files_to_copy:
        source_file = os.path.join(template_dir, file_name)
        destination_file = os.path.join(src_dir, file_name)
        shutil.copy(source_file, destination_file)

    print(f"Project '{project_name}' has been created in '{project_dir}'.")

def main():
    parser = argparse.ArgumentParser(description='Create a new project.')
    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')

    start_parser = subparsers.add_parser('start', help='Create a new project.')
    start_parser.add_argument('project_name', help='Name of the project')

    args = parser.parse_args()

    if args.subcommand == 'start':
        create_project(args)

if __name__ == '__main__':
    main()
