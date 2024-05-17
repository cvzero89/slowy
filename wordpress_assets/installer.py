import subprocess
import getpass
import time
import os
import random
import tarfile

class WordPress_Site():
	"""
	Setting up a class to handle all info, commands in a better way.
	"""
	def __init__(self, mode):
		self.mode = mode.lower()
		if self.mode == 'install':
			print('WordPress Installer...')
		elif self.mode == 'run':
			print('WordPress install skipped...')
		else:
			print('Unknown mode.')
			exit()
	
	"""
	If the script is executed from a subfolder it will move to the home directory.
	If executed from the user directory it will exit.
	"""
	def folder_check(self):
		directory = list(filter(None, os.getcwd().split('/')))
		if len(directory) <= 2:
			print(f'This script cannot be run on the user directory or lower. Current path is {os.getcwd()}\nBye!')
			exit()
		elif len(directory) > 3:
			move_backwards = ''
			directory_size = len(directory) - 3
			for size in range(directory_size):
				move_backwards = move_backwards + '../'
			os.chdir(move_backwards)
			directory = os.getcwd()
			return directory

	"""
	All WP commands will be handled with this function.
	Capturing the output to prevent it from outputing to console, only printed if considered necessary.
	"""
	def run_command(self, cmd):
		try:
			if 'import' not in cmd:
				cmd.extend(['--skip-plugins', '--skip-themes'])

			#print(cmd)
			process = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
			return process.stdout.strip()
		except subprocess.CalledProcessError as e:
			print(f'WP-CLI command failed with error:\n{e}')
			return None

	"""
	User input to install WordPress.
	Domain name can be added with protocol since it is removed.
	Password is not shown in console.
	"""
	def get_info(self):
		if self.mode == 'install':
			try:
				self.site_name = input('Enter the domain name: ').replace('http://', '').replace('https://', '')
				self.database_name = input('Enter the database name: ')
				self.user_name = input('Enter the database usermame: ')
				self.database_host = input('Enter the database hostname: ')
				self.db_pass = getpass.getpass('Enter the database password: ')
			except KeyboardInterrupt:
				print('Action cancelled.')
				exit()
		elif self.mode == 'run':
			self.site_name = self.run_command(['wp', 
									 'option', 
									 'get', 
									 'siteurl']).replace('http://', '').replace('https://', '')
			
	
	"""
	WordPress downloader, creates config file and setups the automatic install.
	time.sleep() is used to make sure the subprocess runs are exiting without any problems before starting the new process.
	"""
	def wp_install(self):
		"""
		Installing WordPress, if wp-settings.php exists with a non-read permission it will remove it. Not doing this affects re-runs.
		Command stdout is shown since it does not disrupt the exercise goal.
		"""
		if os.path.exists('./wp-settings.php') and not os.access('./wp-settings.php', os.R_OK):
			os.remove('./wp-settings.php')
		print('Setting up WordPress:')
		download_wp = ['wp', 'core', 'download', '--force']
		install_out = self.run_command(download_wp)
		if install_out:
			print(install_out)
		time.sleep(2)

		"""
		Set up config. If wp-config.php is found renames it to prevent problems from previous runs.
		Also checks for .maintenance in case it exists to make sure the first display of the site will be correct.
		If there's info on the database it will clear it.
		"""
		print('Creating config file and basic setup.')
		if os.path.exists('./wp-config.php'):
			print('Old wp-config.php found, renaming...')
			os.rename('wp-config.php', 'wp-config.old')
		config_create = [
			'wp', 'config', 'create', 
			f'--dbname={self.database_name}', 
			f'--dbuser={self.user_name}',
			f'--dbhost={self.database_host}', 
			f'--dbpass={self.db_pass}']
		self.run_command(config_create)
		time.sleep(2)
		if os.path.exists('./.maintenance'):
			os.remove('./.maintenance')
		clear_db = ['wp', 'db', 'reset', '--yes']
		self.run_command(clear_db)

		"""
		Install WordPress with fixed values. These are not really important.
		"""
		install_wp = [
			'wp', 'core', 'install', 
			f'--url={self.site_name}',
			'--title=\"WPS Test Site\"',
			'--admin_user=cvzero89',
			'--admin_email=test@wpstesting.com']
		self.run_command(install_wp)
		time.sleep(2)

	"""
	Creating a WordPress page to set up as the main page to see.
	Information is stored as self.page_id to reference on the tasks.
	"""
	def create_wp_post(self, title, content):

		set_up_post = ['wp', 'post', 'create',
				'--porcelain', 
				'--post_type=page', 
				'--post_status=publish', 
				f'--post_title={title}', 
				f'--post_content={content}']

		self.page_id = self.run_command(set_up_post)
		if self.page_id:
			page = ['wp', 'option', 'update', 'show_on_front', 'page']
			self.run_command(page)
			page_update = ['wp', 'option', 'update', 'page_on_front', self.page_id]
			self.run_command(page_update)
			print('Custom setup completed.')
	
	def random_post(self):
		page = ['wp', 'option', 'update', 'show_on_front', 'page']
		self.page_id = self.run_command(['wp', 'option', 'get', 'page_on_front'])
		self.run_command(page)
		get_random_list = self.run_command([
			'wp', 'post', 'list', 
			'--post_type=page', 
			'--format=ids'])
		if get_random_list:
			page_ids = [id_str for id_str in get_random_list.split() if id_str != self.page_id]
		if page_ids:
			random_page_id = random.choice(page_ids)
			self.run_command(['wp', 'option', 'update', 'page_on_front', random_page_id])
	
	def import_db(self):
		print('Importing the database...')
		this_path = os.path.dirname(__file__)
		database = tarfile.open(f'{this_path}/database.tar.gz')
		database.extractall(f'{this_path}/')
		database_name = database.getnames()[0]
		database.close()
		self.run_command(['wp', 'db', 'import', f'{this_path}/{database_name}'])
		self.run_command(['wp', 'search-replace', 'https://wpsupport.dream.press', f'https://{self.site_name}'])
