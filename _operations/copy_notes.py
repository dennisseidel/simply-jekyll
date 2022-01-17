# This uses the obsidian metadata extractor plugins metadata.json
import argparse
import json
import os
import shutil
import re
from git import Repo
import sys


# global constants
SUPPORTED_EMBEDDED_FILES_ENDINGS = "png|jpg|gif|jpeg|drawio"



def read_json(complete_path_to_file):    
    with open(complete_path_to_file, 'r') as f:
        return json.load(f)

def filter_by_classification_and_path(metadata: list, path: str, classification: str):
    return [x for x in metadata if x.get('frontmatter') and is_public(x.get('frontmatter'), classification) and x.get('relativePath').find(path) == 0]


def is_public(frontmatter: dict, classification: str):
    if frontmatter.get('classification') == classification:
        return True
    return False

def find_linked_files(path):
    with open(path, 'r') as f:
        content = f.read()
        # I python strings I have to escape backslashes https://stackoverflow.com/questions/52335970/how-to-fix-string-deprecationwarning-invalid-escape-sequence-in-python
        pattern = re.compile(r'\[\[.*\.({})\]\]'.format(SUPPORTED_EMBEDDED_FILES_ENDINGS))
        filenames = []
        for match in pattern.finditer(content):
            file_name = match.group(0).replace('[[', '').replace(']]', '')
            filenames.append(file_name)
    return filenames

def copy_file_and_return_embedded_filenames(path: str, filename: str, destination_folder: str, frontmatter: dict):
    if is_public(frontmatter, classification='public'): 
        if is_markdown(filename):
            shutil.copy(path, f"{destination_folder}/_notes/{filename}")
            ## read the file and find the linked files
            return find_linked_files(path)

# I don't have to recursively check each link of a file as we go through all md files, and the script moves all public md files. I only check if the file contains linked non md files I need to move

def copy_notes_and_linked_assets(vault_path: str, metadata_list: dict, destination_path: str, non_md_meta: dict):
    embedded_files = []
    for note_entry in metadata_list:
        frontmatter = note_entry.get('frontmatter')
        source_path_to_file = f'{vault_path}/{note_entry.get("relativePath")}'
        filename = note_entry.get("relativePath").split('/')[-1]
        embedded_files_in_note = copy_file_and_return_embedded_filenames(source_path_to_file, filename, destination_path, frontmatter)
        embedded_files.extend(embedded_files_in_note)
    nonMdFiles = non_md_meta.get('nonMdFiles') or []
    for file_entry in nonMdFiles:
        if file_entry.get('name') in embedded_files:
            complete_path_to_file = f"{vault_path}/{file_entry.get('relativePath')}"
            shutil.copy(complete_path_to_file, f"{destination_path}/assets/files/{file_entry.get('name')}")

def is_markdown(file):
    if file.endswith('.md'):
        return True
    return False

def delete_files_from_folder(folder_path):
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def delete_old_notes_and_assets(path: str):
    delete_files_from_folder(f"{path}/_notes")
    delete_files_from_folder(f"{path}/assets/files")

def setup_git_repo(repo: Repo,branch: str):
    git = repo.git
    git.checkout(branch) 
    return repo

def commit_and_push(git): 
    git.add('-A')
    git.commit('-m', 'feat: update blog files')
    git.push()

def push_to_github(branch: str):
    git = setup_git_repo(branch)
    commit_and_push(git)

def harmonize_embedded_urls_in_notes(path_to_notes_folder: str):
    # read files from folder
    for file in os.listdir(path_to_notes_folder):
        if is_markdown(file):
            file_path = os.path.join(path_to_notes_folder, file)
            with open(file_path, 'r') as f:
                content = f.read()
                pattern = re.compile(r'!?\[\[(.*\/)?(.*)\.({})(\]\])'.format(SUPPORTED_EMBEDDED_FILES_ENDINGS))
                res = replace_in_text(content, pattern, r'![](../assets/files/\g<2>.\g<3>)')
            with open(file_path, 'w') as f:
                f.write(res)

def remove_alttext_from_links(path_to_notes_folder: str):
    for file in os.listdir(path_to_notes_folder):
        if is_markdown(file):
            file_path = os.path.join(path_to_notes_folder, file)
            with open(file_path, 'r') as f:
                content = f.read()
                pattern = re.compile(r'\[\[([^\]]*)\|([^\]]*)\]\]')
                res = replace_in_text(content, pattern, r'[[\g<1>]]')
            with open(file_path, 'w') as f:
                f.write(res)


# replace in text regex
def replace_in_text(text: str, pattern: str, replacement: str):
    return re.sub(pattern, replacement, text)

def parse_args(args):
    parser = argparse.ArgumentParser(description='Publish a digital garden to github')
    parser.add_argument('-v', '--vault', type=str, default="/Users/dennisseidel/OneDrive/notes", help='path to the vault folder')
    parser.add_argument('-b', '--branch', type=str, default='master', help='the branch to publish to')
    parser.add_argument('-p', '--push', default=False, help='indicate to work only locally', action='store_true')
    parser.add_argument('-m', '--metadata', type=str, default='/Users/dennisseidel/workspace/obsidian-plugins-meta/metadata-extractor', help='path to metadata files')
    args = parser.parse_args(args)
    return args


def move_public_files_from_vault_to_blog(vault_path: str, destination_path: str, metadata_path: str = None):
    metadata_path = metadata_path or f'{vault_path}/.obsidian/plugins/metadata-extractor'
    non_md_metadata = read_json(f'{metadata_path}/allExceptMd.json')
    metadata = read_json(f'{metadata_path}/metadata.json')
    public_resources = filter_by_classification_and_path(metadata, path='03_RESOURCES', classification='public')
    copy_notes_and_linked_assets(vault_path, public_resources, destination_path, non_md_meta=non_md_metadata)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    
    SOURCE_PATH = args.vault
    GIT_BRANCH = args.branch
    METADATA_PATH = args.metadata
    DESTIONATION_PATH = f'{os.getcwd()}/..'
    

    repo = Repo(DESTIONATION_PATH)
    setup_git_repo(repo, GIT_BRANCH) 
    delete_old_notes_and_assets(DESTIONATION_PATH)
    move_public_files_from_vault_to_blog(SOURCE_PATH, DESTIONATION_PATH, METADATA_PATH)
    harmonize_embedded_urls_in_notes(f"{DESTIONATION_PATH}/_notes")
    remove_alttext_from_links(f"{DESTIONATION_PATH}/_notes")        
    if args.push:
        push_to_github(GIT_BRANCH)


# vault/.obisian/metadata-extractor/metadata.json ...
# vault/03_RESOURCES/nonpublic_note.md
# vault/03_RESOURCES/public.md
# vault/nonpublic_note.md