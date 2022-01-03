# This uses the obsidian metadata extractor plugins metadata.json

import json
import os
import shutil
import re
from git import Repo


def read_json(complete_path_to_file):    
    with open(complete_path_to_file, 'r') as f:
        return json.load(f)

def filter_by_classification_and_path(metadata_list, path):
    return [x for x in metadata_list if x.get('frontmatter') and is_public(x.get('frontmatter')) and x.get('relativePath').find(path) == 0]


def is_public(frontmatter):
    if frontmatter.get('classification') == 'public':
        return True
    return False

def find_linked_files(path):
    with open(path, 'r') as f:
        content = f.read()
        pattern = re.compile(f'\[\[.*\.({SUPPORTED_EMBEDDED_FILES_ENDINGS})\]\]')
        filenames = []
        for match in pattern.finditer(content):
            file_name = match.group(0).replace('[[', '').replace(']]', '')
            filenames.append(file_name)
    return filenames

def copy_file_and_return_embedded_filenames(path: str, filename: str, destination_folder: str, frontmatter: dict):
    if is_public(frontmatter): 
        if is_markdown(filename):
            shutil.copy(path, f"{destination_folder}/_notes/{filename}")
            ## read the file and find the linked files
            return find_linked_files(path)

    else:
        print('not public')

# I don't have to recursively check each link of a file as we go through all md files, and the script moves all public md files. I only check if the file contains linked non md files I need to move

def copy_files(metadata_list: dict, destination_path: str):
    embedded_files = []
    for note_entry in metadata_list:
        frontmatter = note_entry.get('frontmatter')
        source_path_to_file = f'{SOURCE_PATH}/{note_entry.get("relativePath")}'
        filename = note_entry.get("relativePath").split('/')[-1]
        embedded_files_in_note = copy_file_and_return_embedded_filenames(source_path_to_file, filename, destination_path, frontmatter)
        embedded_files.extend(embedded_files_in_note)
    non_md_meta = read_json('allExceptMd.json')
    for file_entry in non_md_meta.get('nonMdFiles'):
        if file_entry.get('name') in embedded_files:
            complete_path_to_file = f"{SOURCE_PATH}/{file_entry.get('relativePath')}"
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


def setup_git_repo(branch: str):
    repo = Repo(DESTIONATION_PATH)
    #origin = repo.remotes.origin
    # try: 
    #     origin.pull()
    # except:
    #     print('could not pull')
    git = repo.git
    git.checkout(branch) 
    return git

def commit_and_push(git): 
    git.add('-A')
    git.commit('-m', 'feat: update blog files')
    git.push()

def push_to_github(branch: str):
    git = setup_git_repo(branch)
    commit_and_push(git)

def copy_meta_files(path: str):
    shutil.copy(f'{path}/allExceptMd.json', './')
    shutil.copy(f'{path}/metadata.json', './')

def harmonize_embedded_urls(path_to_notes_folder: str):
    # read files from folder
    for file in os.listdir(path_to_notes_folder):
        if is_markdown(file):
            file_path = os.path.join(path_to_notes_folder, file)
            with open(file_path, 'r') as f:
                content = f.read()
                pattern = re.compile(f'!?\[\[(.*\/)?(.*)\.({SUPPORTED_EMBEDDED_FILES_ENDINGS})(\]\])')
                res = replace_in_text(content, pattern, '![](../assets/files/\g<2>.\g<3>)')
            with open(file_path, 'w') as f:
                f.write(res)

def fix_links_with_alt_text(path_to_notes_folder: str):
    for file in os.listdir(path_to_notes_folder):
        if is_markdown(file):
            file_path = os.path.join(path_to_notes_folder, file)
            with open(file_path, 'r') as f:
                content = f.read()
                pattern = re.compile(f'\[\[([^\]]*)\|([^\]]*)\]\]')
                res = replace_in_text(content, pattern, '[[\g<1>]]')
            with open(file_path, 'w') as f:
                f.write(res)


# replace in text regex
def replace_in_text(text: str, pattern: str, replacement: str):
    return re.sub(pattern, replacement, text)


# setup argparse
import argparse
parser = argparse.ArgumentParser(description='Publish a digital garden to github')
parser.add_argument('-v', '--vault', type=str, default="/Users/dennisseidel/OneDrive/notes", help='path to the vault folder')
parser.add_argument('-b', '--branch', type=str, default='master', help='the branch to publish to')
parser.add_argument('-p', '--push', default=False, help='indicate to work only locally', action='store_true')
parser.add_argument('-m', '--metadata', type=str, default='/Users/dennisseidel/workspace/obsidian-plugins-meta/metadata-extractor', help='path to metadata files')
args = parser.parse_args()


SOURCE_PATH = args.vault
GIT_BRANCH = args.branch
METADATA_PATH = args.metadata
DESTIONATION_PATH = f'{os.getcwd()}/..'
SUPPORTED_EMBEDDED_FILES_ENDINGS = "png|jpg|gif|jpeg|drawio"


setup_git_repo(GIT_BRANCH)
delete_files_from_folder(f"{DESTIONATION_PATH}/_notes")
delete_files_from_folder(f"{DESTIONATION_PATH}/assets/files")
copy_meta_files(path=METADATA_PATH)
metadata = read_json('metadata.json')
public_resources = filter_by_classification_and_path(metadata, '03_RESOURCES')
copy_files(public_resources, DESTIONATION_PATH)
harmonize_embedded_urls(f"{DESTIONATION_PATH}/_notes")
fix_links_with_alt_text(f"{DESTIONATION_PATH}/_notes")
if args.push:
    push_to_github(GIT_BRANCH)