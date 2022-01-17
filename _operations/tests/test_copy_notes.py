import os
import shutil
import pytest
from git import Repo
from py._path.local import LocalPath


import copy_notes

@pytest.fixture(name="repo")
def repo_(tmpdir: LocalPath) -> Repo:
    """Create a git repository with fake data and history.

    Args:
        tmpdir: Pytest fixture that creates a temporal directory
    """
    # Copy the content from `tests/assets/test_data`.
    repo_path = tmpdir / "test_repo"
    shutil.copytree("tests/fixtures/repo", repo_path)

    # Initializes the git repository.
    repo = Repo.init(repo_path)
    repo.git.add(all=True)
    repo.index.commit("Initial commit")

    # add branch 
    repo.git.checkout("-b", "newbranch")
    return repo

@pytest.fixture(name="folder")
def folder_(tmpdir: LocalPath) -> LocalPath:
    """Create a temporal directory with a subfolder.

    Args:
        tmpdir: Pytest fixture that creates a temporal directory
    """
    # Create a temporal directory with a subfolder.
    folder = tmpdir / "test_folder"
    shutil.copytree("tests/fixtures/repo", folder)
    return folder

@pytest.fixture(name="vault")
def vault_(tmpdir: LocalPath) -> LocalPath:
    """Create a temporal directory with a subfolder.

    Args:
        tmpdir: Pytest fixture that creates a temporal directory
    """
    # Create a temporal directory with a subfolder.
    vault = tmpdir / "test_vault"
    shutil.copytree("tests/fixtures/vault", vault)
    return vault

def get_path_to_this_file():
    return os.path.dirname(os.path.abspath(__file__))

def test_read_json(folder):
    path_to_sample_json = folder / 'assets/files/sample.json'
    read_json = copy_notes.read_json(path_to_sample_json)
    assert read_json == {'some': 'data'}

def test_parse_args():
    sys_args = ['./copy_notes.py', '--vault', '/Users/maxman/test/folder', '--branch', 'newbranch', '--push', '--metadata', '/Users/maxman/workspace/obsidian-plugins-meta/metadata-extractor']
    parsed_args = copy_notes.parse_args(sys_args[1:])
    assert parsed_args.vault == '/Users/maxman/test/folder'
    assert parsed_args.branch == 'newbranch'
    assert parsed_args.push == True
    assert parsed_args.metadata == '/Users/maxman/workspace/obsidian-plugins-meta/metadata-extractor'

def test_setup_git_repo(repo):
    branch = 'newbranch'
    repo = copy_notes.setup_git_repo(repo, branch)
    assert repo.active_branch.name == branch

def test_delete_old_notes_and_assets(folder):
    path_to_repo = f'{folder}'
    copy_notes.delete_old_notes_and_assets(path_to_repo)
    assets = os.listdir(f'{path_to_repo}/assets/files')
    notes = os.listdir(f'{path_to_repo}/_notes')
    assert len(assets) == 0
    assert len(notes) == 0

def test_is_markdown_png():
    result = copy_notes.is_markdown("image.png")
    assert result == False

def test_is_markdown_md():
    result = copy_notes.is_markdown("test.md")
    assert result == True

def test_move_public_files_from_vault_to_blog(vault, folder):
    print (vault)
    # delete notes in repo and assets
    copy_notes.delete_old_notes_and_assets(f'{folder}')
    copy_notes.move_public_files_from_vault_to_blog(vault, folder)
    assets = os.listdir(f'{folder}/assets/files')
    notes = os.listdir(f'{folder}/_notes')
    assert len(notes) == 1
    assert len(assets) == 1

def test_find_linked_files(vault):
    linked_files = copy_notes.find_linked_files(vault/'03_RESOURCES/public_resources.md')
    assert linked_files == ['netlify-blog-setup.png']

def test_harmonize_embedded_urls(folder):
    notes_folder = folder/'_notes' 
    copy_notes.harmonize_embedded_urls_in_notes(notes_folder)
    # read file
    note_with_single_link = notes_folder/'single_link.md'
    with open(note_with_single_link, 'r') as f:
        contentNew = f.read()
        print (contentNew)
    assert contentNew == '![](../assets/files/netlify-blog-setup.png)'


def test_remove_alttext_from_links(folder):
    notes_folder = folder/'_notes' 
    note_with_single_link = notes_folder/'alt_text.md'
    with open(note_with_single_link, 'r') as f:
        contentOld = f.read()
        print (contentOld)
    copy_notes.remove_alttext_from_links(notes_folder)
    # read file
    with open(note_with_single_link, 'r') as f:
        contentNew = f.read()
        print (contentNew)
    assert contentNew == '[[testname]]'
