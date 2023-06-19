# ========================================
# FileName: show_config.py
# Date: 25 mai 2023 - 18:52
# Author: Ammar Mian
# Email: ammar.mian@univ-smb.fr
# GitHub: https://github.com/ammarmian
# Brief: See config file used for a run
# Take into account the commit_sha at
# the time of the run
# =========================================

import os
import git
import argparse
import yaml
import rich


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
            description='Show config file used for a run')
    parser.add_argument('--storage_path',
                        type=str, help='Path to the storage folder')
    args = parser.parse_args()

    # Check if the storage_path is named group_*
    if os.path.basename(args.storage_path).startswith('group_'):
        info_file_path = os.path.join(args.storage_path, '../info.yaml')
        group_id = int(os.path.basename(args.storage_path).split('_')[1])
    else:
        info_file_path = os.path.join(args.storage_path, 'info.yaml')
        group_id = 0

        # Check that there aren't multiple groups
        for f in os.listdir(args.storage_path):
            if f.startswith('group_'):
                raise ValueError('Multiple groups in the storage folder:'
                                 'please specify the group no')

    # Load info file
    with open(info_file_path, 'r') as info_file:
        info = yaml.safe_load(info_file)
    commit_sha = info['commit_sha']

    # Get the config file path from the commands
    command = info['commands'][group_id]

    # Look for the config file: only thing in the
    # command that ends with .py besides execute
    # script.
    config_file_path = None
    for c in command[2:]:
        if c.endswith('.py'):
            config_file_path = c
            break

    if config_file_path is None:
        raise ValueError('Sorry no config file found in the commands...')

    rich.print('Config file path: {}'.format(config_file_path))
    rich.print('Commit sha: {}'.format(commit_sha))

    # Get the config file at the time of the commit
    repo = git.Repo(os.getcwd())
    config = repo.git.show('{}:{}'.format(commit_sha, config_file_path))
    rich.print('Config file content:')
    rich.print(config)
