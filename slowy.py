import shutil
import os
from wordpress_assets.installer import WordPress_Site
from wordpress_assets.plugin_list import plugin_list, theme_list

site = WordPress_Site()
site.folder_check()
site.get_info()
site.wp_install()

this_path = os.path.dirname(os.path.abspath(__file__))
print('Installing plugins...')

total_tasks = len(plugin_list)
def progress_bar(progress):
    percent_complete = int((progress * 100) / total_tasks)
    if percent_complete % 25 == 0 or percent_complete % 3 == 0:
        print(f'{int(percent_complete)} completed...')
progress = 1
for plugin in plugin_list:
    plugin_name = plugin["name"]
    plugin_version = plugin["version"]
    site.run_command(['wp', 'plugin', 'install', plugin_name, f'--version={plugin_version}', '--force'])
    progress_bar(progress)
    progress += 1

def copy_plugins(this_path, plugin):
    plugin_asset = f'{this_path}/slowy/wordpress_assets/{plugin}'
    plugin_dir = f'./wp-content/plugins/{plugin}'
    if os.path.isdir(plugin_dir):
        shutil.rmtree(plugin_dir)
    shutil.copytree(plugin_asset, plugin_dir)

site.import_db()

zero_plugins = ['flash', 'its-a-me-mario', 'slowy']
for plugin in zero_plugins:
    copy_plugins(this_path, plugin)

site.run_command(['wp', 'plugin', 'activate', '--all'])
theme_name = theme_list[0]["name"]
theme_version = theme_version = theme_list[0]["version"]
if site.run_command(['wp', 'theme', 'install', theme_name, f'--version={theme_version}']):
    site.run_command(['wp', 'theme', 'activate', theme_name])
print('Done.')
