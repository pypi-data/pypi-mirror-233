import os, mystring
from dataclasses import dataclass, field
from sdock.util import cur_dir, getPort


@dataclass
class dock:
	"""Class for keeping track of an item in inventory."""
	docker: str = "docker"
	image: str = "frantzme/pythondev:lite"
	ports: list = field(default_factory=list)
	cmd: str = None
	network:str = None
	dind: bool = False
	shared: bool = False
	detach: bool = False
	sudo: bool = False
	remove: bool = True
	mountto: str = "/sync"
	mountfrom: str = None
	name: str = None
	login: bool = False
	loggout: bool = False
	logg: bool = False
	macaddress: str = None
	postClean: bool = False
	preClean: bool = False
	extra: str = None
	raw: str = None
	save_host_dir: bool = False
	docker_username:str="frantzme"
	docker_id:str=None

	@staticmethod
	def install_docker(save_file:bool=False):
		#https://docs.docker.com/engine/install/ubuntu/
		for string in [
			"curl -fsSL https://get.docker.com -o get-docker.sh",
			"sudo sh ./get-docker.sh --dry-run",
			'echo "Done"' if save_file else "echo \"Done\" && rm get-docker.sh"
		]:
			try:
				mystring.string(string).exec()
			except: pass

	@staticmethod
	def is_docker():
		path = '/proc/self/cgroup'
		return (os.path.exists('/.dockerenv') or os.path.isfile(path) and
				any('docker' in line for line in open(path)))

	@staticmethod
	def dockerImage(string, usebaredocker=False, docker_username="frantzme"):
		if not usebaredocker and "/" not in string:
			use_lite = ":lite" in string
			if "pydev" in string:
				output = f"{docker_username}/pythondev:latest"
			elif "pytest" in string:
				output = f"{docker_username}/pythontesting:latest"
			else:
				output = f"{docker_username}/{string}:latest"
			if use_lite:
				output = output.replace(':latest','') + ":lite"
			output = output.replace(':latest:latest',':latest').replace(':lite:lite',':lite')

			if usebaredocker:
				output = output.replace("{}/".format(docker_username),"")

			return ':'.join(output.split(":")[0:2]) #Fixes a problem where there's an output of :ui:latest
		else:
			return string

	def clean(self):
		return "; ".join([
			"{0} kill $({0} ps -a -q)".format(self.docker),
			"{0} kill $({0} ps -q)".format(self.docker),
			"{0} rm $({0} ps -a -q)".format(self.docker),
			"{0} rmi $({0} images -q)".format(self.docker),
			"{0} volume rm $({0} volume ls -q)".format(self.docker),
			"{0} image prune -f".format(self.docker),
			"{0} container prune -f".format(self.docker),
			"{0} builder prune -f -a".format(self.docker)
		])

	def stop_container(self):
		if self.name:
			base = mystring.string("{0} container ls -q --filter name={1}".format(self.docker,self.name))
		elif self.image:
			base = mystring.string("{0} container ls -q --filter ancestor={1}".format(self.docker,self.image))
		else:
			return False

		self.docker_id = base.exec().strip()
		mystring.string("{0} container stop {1}".format(self.docker, self.docker_id)).exec().strip()
		return True

	def stop_volume(self):
		if self.name:
			base = mystring.string("{0} container ls -q --filter name={1}".format(self.docker,self.name))
		elif self.image:
			base = mystring.string("{0} container ls -q --filter ancestor={1}".format(self.docker,self.image))
		else:
			return False

		self.docker_id = base.exec().strip()
		mystring.string("{0} rm -v {1}".format(self.docker, self.docker_id)).exec().strip()
		return True

	def stop_image(self):
		if True:
			images = []
			for image_line in mystring.string("{0} images -a".format("docker")).exec(lines=True):
				if not image_line.empty and "REPOSITORY" not in image_line:
					image_break = mystring.lyst(image_line.split(" ")).trims(lambda x:mystring.string(x).empty)
					images += [{
						"repo":image_break[0],
						"tag":image_break[1],
						"id":image_break[2],
					}]

			to_kill = []
			for image_info in images:
				if self.name:
					print("Not supported yet")
				elif self.image:
					tag = None
					if ":" in self.image:
						image, tag = self.image.split(":")
					if image == image_info['repo'] and (not tag or tag == image_info['tag']):
						to_kill += [image_info['id']]

			for kill in to_kill:
				mystring.string("{0} rmi {1}".format("docker", kill)).exec()
		else:
			if self.docker_id is None:
				self.stop_container()

			mystring.string("{0} rmi {1}".format("docker", self.docker_id)).exec()

		return True

	def kill(self):
		"""
		https://stackoverflow.com/questions/29406871/how-to-filter-docker-process-based-on-image
		https://docs.docker.com/engine/reference/commandline/image_rm/
		https://docs.docker.com/engine/reference/commandline/rmi/
		https://docs.docker.com/engine/reference/commandline/stop/
		https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes
		https://contabo.com/blog/how-to-remove-docker-volumes-images-and-containers/
		https://www.ibm.com/docs/en/coss/3.15.4?topic=container-stopping-running
		https://nickjanetakis.com/blog/docker-tip-83-stop-docker-containers-by-name-pattern
		"""
		self.stop_container()
		self.stop_volume()
		self.stop_image()

	def string(self):
		if self.dind or self.shared:
			import platform
			if False and platform.system().lower() == "darwin":  # Mac
				dockerInDocker = "--privileged=true -v /private/var/run/docker.sock:/var/run/docker.sock"
			else:  # if platform.system().lower() == "linux":
				dockerInDocker = "--privileged=true -v /var/run/docker.sock:/var/run/docker.sock"
		else:
			dockerInDocker = ""

		if self.shared:
			exchanged = "-e EXCHANGE_PATH=" + os.path.abspath(os.curdir)
		else:
			exchanged = ""

		no_mount = (self.mountto is None or self.mountto.strip() == '') and (self.mountfrom is None or self.mountfrom.strip() == '')
		dir = cur_dir()
		use_dir = "$EXCHANGE_PATH" if self.shared else (self.mountfrom if self.mountfrom and self.mountfrom != ':!' else dir)

		if self.cmd:
			if isinstance(self.cmd, list):
				cmd = ' '.join(self.cmd)
			else:
				cmd = self.cmd 
		else:
			cmd = '/bin/bash'

		network = ""
		if self.network:
			if self.network.strip().lower() == "none":
				network = "--network=\"none\"" #https://docs.docker.com/network/none/
			elif self.network.strip().lower() == "~":
				network = "--network=\"host\""
			else:
				network = "--network=\"" + self.network + "\""

		my_save_host_dir = ''
		if self.save_host_dir:
			if 'HOSTDIR' in os.environ:
				past_dir,current_dir = os.environ['HOSTDIR'], os.path.abspath(os.curdir).replace('/sync/','')
				my_save_host_dir = '--env="HOSTDIR={0}/{1}"'.format(past_dir,current_dir)
			else:
				my_save_host_dir = '--env="HOSTDIR={0}"'.format(dir)

		raw_input = ''
		if self.raw:
			if isinstance(self.raw, list):
				raw_input = ' '.join(self.raw)
			else:
				raw_input = self.raw

		return str(self.clean()+";" if self.preClean else "") + "{0} run ".format(self.docker) + " ".join([
			dockerInDocker,
			'--rm' if self.remove else '',
			'-d' if self.detach else '-it',
			'' if no_mount else '-v "{0}:{1}"'.format(use_dir, self.mountto),
			exchanged,
			network,
			getPort(self.ports),
			'--mac-address ' + str(self.macaddress) if self.macaddress else '',
			self.extra if self.extra else '',
			my_save_host_dir,
			raw_input,
			self.image,
			cmd
		]) + str(self.clean()+";" if self.postClean else "")

	def __str__(self):
		return self.string()
	
	def compose(self, output_file:str=""):
		#https://docs.docker.com/compose/gettingstarted/
		return

