# ========================================
# FileName: dodo.py
# Date: 26 mai 2023 - 14:09
# Author: Ammar Mian
# Email: ammar.mian@univ-smb.fr
# GitHub: https://github.com/ammarmian
# Brief: Project task definition in
#        pydoit (https://pydoit.org/)
#        format.
# =========================================
import os
import yaml

DOIT_CONFIG = {
    'default_tasks': ['show_info'],
    'verbosity': 2
}


def task_show_info():
    """Show information"""

    def show_info():
        print("Utility script for creating Qanat project: ")
        print("Multivariate Gaussian")
        print("Author: Ammar Mian")

    return {
        'basename': 'show_info',
        'actions': [show_info],
        'verbosity': 2
    }


def task_init_qanat():
    """Creates the directory structure for a Qanat project"""

    return {
        'basename': 'init_qanat',
        'actions': [['qanat', 'init', '.', '-y']],
        'targets': ['.qanat/config.yaml',
                    '.qanat/database.db',
                    '.qanat/cache'],
    }


def task_add_experiments():
    """Add experiments to the project"""

    # Find all experiments_details.yml files
    # in the experiments directory
    experiments_details = []
    name_list = []
    for root, dirs, files in os.walk('experiments'):
        if 'experiment_details.yaml' in files:
            experiments_details.append(os.path.join(root,
                                                    'experiment_details.yaml'))
            with open(os.path.join(root, 'experiment_details.yaml')) as f:
                name_list.append(yaml.load(f, Loader=yaml.FullLoader)['name'])

    for experiment_file, name in zip(experiments_details, name_list):
        yield {
            'name': name,
            'actions': [['qanat', 'experiment',
                        'new', '--file',
                         experiment_file]],
            'verbosity': 2,
            'doc': 'Add experiment {}'.format(name),
            'task_dep': ['init_qanat']
        }


def task_add_documents():
    """Add documents to the project"""

    # Find all the document_details.yaml files in doucments/*/
    documents_details = []
    name_list = []
    for root, dirs, files in os.walk('documents'):
        if 'document_details.yaml' in files:
            documents_details.append(os.path.join(root,
                                                  'document_details.yaml'))
            with open(os.path.join(root, 'document_details.yaml')) as f:
                name_list.append(yaml.load(f, Loader=yaml.FullLoader)['name'])

    for document_file, name in zip(documents_details, name_list):
        yield {
            'name': name,
            'actions': [['qanat', 'document',
                        'new', document_file]],
            'verbosity': 2,
            'doc': 'Add document {}'.format(name),
            'task_dep': ['init_qanat', 'add_experiments']
        }


def task_delet_qanat():
    """Delete the Qanat project"""

    def delete_qanat():
        os.system('qanat cache clean')
        os.system('rm -rf .qanat')
        os.system('rm -rf results/**')

    return {
        'basename': 'delete_qanat',
        'actions': [delete_qanat],
        'verbosity': 2,
    }
