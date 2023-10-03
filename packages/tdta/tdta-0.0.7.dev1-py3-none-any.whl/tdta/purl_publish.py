import os
import requests
import subprocess
import logging


#  TODO switch to main repo on release
# PURL_TAXONOMY_FOLDER_URL = 'https://github.com/brain-bican/purl.brain-bican.org/tree/main/config/taxonomy/'
# PURL_REPO = 'brain-bican/purl.brain-bican.org'
PURL_TAXONOMY_FOLDER_URL = 'https://github.com/hkir-dev/purl.brain-bican.org/tree/main/config/taxonomy/'
PURL_REPO = 'hkir-dev/purl.brain-bican.org'


def publish_to_purl(file_path: str) -> str:
    """
    Publishes the given taxonomy to the purl system. First checks if PURL system already has a config for the given
    taxonomy. If not, makes a pull request to create a config.
    :param file_path: path to the project root folder
    :return: url of the created pull request or the url of the existing PURL configuration.
    """
    print("In PURL action 7.")
    work_dir = os.path.abspath(file_path)
    print(work_dir)
    print('>>>>>')
    contents = os.listdir(work_dir)
    for item in contents:
        print(item)
    print('<<<<<<')
    purl_folder = os.path.join(work_dir, "purl")
    print(purl_folder)
    print('>>>>>')
    contents = os.listdir(purl_folder)
    for item in contents:
        print(item)
    print('<<<<<<')
    files = [f for f in os.listdir(os.path.abspath(purl_folder)) if os.path.isfile(f) and str(f).endswith(".yml")]
    purl_config_name = None
    if len(files) == 0:
        raise Exception("PURL config file couldn't be found at project '/purl' folder.")
    else:
        purl_config_name = files[0]

    response = requests.get(PURL_TAXONOMY_FOLDER_URL + purl_config_name)
    if response.status_code == 200:
        print('PURL already exists: ' + (PURL_TAXONOMY_FOLDER_URL + purl_config_name))
    else:
        # check all branches/PRs if file exists

        # create pull request
        create_pull_request(purl_folder, os.path.join(purl_folder, purl_config_name))

    return "DONE"


def create_pull_request(purl_folder, file_path):
    print("INN CPR")
    github_token = os.environ.get('PERSONAL_ACCESS_TOKEN', "").strip()
    runcmd("cd {dir} && gh auth login --with-token {gh_token} && gh repo fork {repo} --clone --default-branch-only".format(gh_token=github_token, dir=purl_folder, repo=PURL_REPO))
    print("OUT CPR")

def runcmd(cmd):
    logging.info("RUNNING: {}".format(cmd))
    p = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    (out, err) = p.communicate()
    logging.info('OUT: {}'.format(out))
    if err:
        logging.error(err)
    if p.returncode != 0:
        raise Exception('Failed: {}'.format(cmd))

