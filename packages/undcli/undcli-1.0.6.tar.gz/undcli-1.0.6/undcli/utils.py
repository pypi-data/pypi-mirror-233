import subprocess

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode != 0:
        print(f"Command failed with error: {err}")
    else:
        print(out)

def get_ubuntu_version():
    with open('/etc/lsb-release', 'r') as file:
        for line in file:
            if line.startswith('DISTRIB_RELEASE'):
                return line.split('=')[1].strip().split('.')[0]  # Extracts '22' from '22.04'
    return None  # Returns None if the Ubuntu version can't be determined

def setup_cuda_ubuntu(version):
    if version not in ["20", "22"]:
        print("Unsupported Ubuntu version.")
        return
    
def setup_cuda_ubuntu(version):
    if version not in ["20", "22"]:
        print("Unsupported Ubuntu version.")
        return

    commands = [
        f"wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu{version}04/x86_64/cuda-ubuntu{version}04.pin",
        f"sudo mv cuda-ubuntu{version}04.pin /etc/apt/preferences.d/cuda-repository-pin-600",
        f"wget https://developer.download.nvidia.com/compute/cuda/12.2.2/local_installers/cuda-repo-ubuntu{version}04-12-2-local_12.2.2-535.104.05-1_amd64.deb",
        f"sudo dpkg -i cuda-repo-ubuntu{version}04-12-2-local_12.2.2-535.104.05-1_amd64.deb",
        f"sudo cp /var/cuda-repo-ubuntu{version}04-12-2-local/cuda-*-keyring.gpg /usr/share/keyrings/",
        "sudo apt-get update",
        "sudo apt-get -y install cuda"
    ]

    for command in commands:
        run_command(command)
