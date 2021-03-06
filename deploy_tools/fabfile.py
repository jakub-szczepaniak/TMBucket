#! python2

from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/jakub-szczepaniak/TMBucket.git'

def deploy():
    site_folder = '/home/{}/sites/{}'.format(env.user, env.host)
    source_folder = site_folder + '/source'

    _create_directory_structure(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_venv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

def  _create_directory_structure(site_folder):
    for subfolder in ('database', 'static', 'venv', 'source'):
        run('mkdir -p {}/{}'.format(site_folder, subfolder))

def _get_latest_source(source_folder):
    if exists (source_folder + '/.git'):
        run('cd {} && git fetch'.format(source_folder))
    else:
        run('git clone {} {}'.format(REPO_URL, source_folder))
        current_commit = local('git log -n 1 --format=%H', capture=True)
        run('cd {} && git reset --hard {}'.format(source_folder,current_commit))

def _update_settings(source_folder, host):

    settings_path = source_folder + '/TMBucket/settings.py'
    sed(settings_path, "DEBUG=True", "DEBUG=False")
    sed(settings_path,
        'ALLOWED_HOSTS=.+$',
        'ALLOWED_HOSTS=["{}"]'.format(host))
    secret_key_file = source_folder + '/TMBucket/secret_key_file.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnoprqstuwxyz0123456789!@#$%^&*()-=_+'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, 'SECRET_KEY="{}"'.format(key))
    append(settings_path, '\nfrom .secret_key_file import SECRET_KEY')

def _update_venv(source_folder):
    venv_folder = source_folder + '/../venv'
    if not exists(venv_folder + '/bin/pip'):
        run('virtualenv python=python3 {}'.format(venv_folder))
    run('{}/bin/pip install -r {}/requirements.txt'.format(
        venv_folder,
        source_folder))
def _update_static_files(source_folder):
    run('cd {} && ../venv/bin/python manage.py collectstatic --noinput'.format(
        source_folder))
def _update_database(source_folder):
    run('cd {} && ../venv/bin/python manage.py migrate --noinput'.format(
        source_folder))
