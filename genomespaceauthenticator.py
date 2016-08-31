from tornado import gen
from IPython.utils.traitlets import Dict
from jupyterhub.auth import Authenticator, LocalAuthenticator
import requests
import urllib
import os
from notebook.services.config import ConfigManager
from jupyterhub.app import JupyterHub 
from traitlets import Unicode

class GenomeSpaceAuthenticator(Authenticator):
	user_dir_path = Unicode('/home/ubuntu/userdirs2/', help='Directory path that holds the user notebooks, mounted to the docker containers with <username> appended. Creates the <username> directory there.').tag(config=True)
      
	@gen.coroutine
	def authenticate(self, handler, data):
		print("user dir is ", self.user_dir_path)

		username = urllib.parse.quote(data['username'])
		password = urllib.parse.quote(data['password'])

		url = "https://"+username + ":" + password + "@identity.genomespace.org/identityServer/selfmanagement/user"
		response = requests.get(url)
		
		if (response.status_code == 200):
			userInfo = response.json()
			username2 = userInfo['username']
			directory = self.user_dir_path +username2
			if not os.path.exists(directory):
				os.makedirs(directory)
				os.chmod(directory,0o775)
			return username2


class LocalGenomeSpaceAuthenticator(LocalAuthenticator, GenomeSpaceAuthenticator):
    """A version that mixes in local system user creation"""
    pass




