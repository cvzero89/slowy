import shutil
import os
import tarfile
import argparse
from wordpress_assets.installer import WordPress_Site
from wordpress_assets.plugin_list import plugin_list, theme_list

parser = argparse.ArgumentParser(
                    prog='Slowy',
                    description='Sets up a slow WordPress instance to be used for debug/training.',
                    epilog='What are you looking at? I am a short help article.')

parser.add_argument('--mode', type=str, nargs=1, required=True, default='install', choices=['install', 'run'])
args = parser.parse_args()
mode = args.mode[0]

this_path = os.path.dirname(os.path.abspath(__file__))
site = WordPress_Site(mode)
site.folder_check()
site.get_info()
if mode == 'install':
    site.wp_install()

print('Installing plugins...')

total_tasks = len(plugin_list)
def progress_bar(progress):
    percent_complete = int((progress * 100) / total_tasks)
    if percent_complete % 25 == 0 or percent_complete % 3 == 0:
        print(f'{int(percent_complete)}% completed...')
progress = 1
for plugin in plugin_list:
    plugin_name = plugin["name"]
    plugin_version = plugin["version"]
    site.run_command(['wp', 'plugin', 'install', plugin_name, f'--version={plugin_version}', '--force'])
    progress_bar(progress)
    progress += 1

theme_name = theme_list[0]["name"]
theme_version = theme_version = theme_list[0]["version"]
if site.run_command(['wp', 'theme', 'install', theme_name, f'--version={theme_version}']):
    site.run_command(['wp', 'theme', 'activate', theme_name])
else:
    default_theme = 'twentytwentyfour'
    site.run_command(['wp', 'theme', 'activate', default_theme])
    print(f'Activating default theme since {theme_name} could not be installed.')

if not os.path.exists('./.htaccess'):
    print('Copying the .htaccess...')
    htaccess_location = f'{this_path}/wordpress_assets/.htaccess'
    shutil.copy(htaccess_location, './')
    if os.path.exists('./.htaccess'):
        print('Copied.')

def copy_plugins(this_path, plugin):
    plugin_asset = f'{this_path}/wordpress_assets/{plugin}'
    plugin_dir = f'./wp-content/plugins/{plugin}'
    if os.path.isdir(plugin_dir):
        shutil.rmtree(plugin_dir)
    shutil.copytree(plugin_asset, plugin_dir)

def copy_uploads(this_path):
    uploads = tarfile.open(f'{this_path}/wordpress_assets/uploads.tar.gz')
    uploads.extractall(f'{this_path}/wordpress_assets/')
    upload_dir_name = uploads.getnames()[0]
    uploads_asset = f'{this_path}/wordpress_assets/{upload_dir_name}'
    upload_dir = f'./wp-content/uploads'
    if os.path.isdir(upload_dir):
        shutil.rmtree(upload_dir)
    shutil.copytree(uploads_asset, upload_dir)

copy_uploads(this_path)

site.import_db()

zero_plugins = ['flash', 'its-a-me-mario', 'slowy']
for plugin in zero_plugins:
    copy_plugins(this_path, plugin)

site.run_command(['wp', 'plugin', 'activate', '--all'])

print('Done.')
