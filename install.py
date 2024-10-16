import os,sys


def install_nvidia_toolkit(is_wls):
    if is_wls:
        pass
    else:
        os.system("curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list")
        os.system("apt-get update && apt-get install -y nvidia-container-toolkit")


def install_requirements():
    os.system("apt-get update && apt-get install -y git apt-transport-https ca-certificates curl software-properties-common make")
    os.system("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg")
    os.system('echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null')
    os.system('apt update && sudo apt install -y docker-ce')


def check_git():
    exit_code = os.system('git --version >nul 2>&1')
    return exit_code


def check_make():
    exit_code = os.system('make --version >nul 2>&1')
    return exit_code


def check_docker():
    exit_code = os.system('make --version >nul 2>&1')
    return exit_code


def check_requirements():
    meet_requirements = True
    if check_git() == 0:
        print("Checking for git: Installed")
    else:
        print("Checking for git: Not Installed")
        meet_requirements = False
    if check_make() == 0:
        print("Checking for make: Installed")
    else:
        print("Checking for make: Not Installed")
        meet_requirements = False
    if check_docker() == 0:
        print("Checking for docker: Installed")
    else:
        print("Checking for docker: Not Installed")
        meet_requirements = False
    return meet_requirements


# def credential_validation():
#     exit_code = os.system('git config --global credential.helper store && git clone git@github.com:ACROBA-Project/ACROBA-Platform.git')
#     if exit_code == 0:
#         return True
#     else:
#         return False


def main():
    print("Welcome to ACROBA!")
    print("\n")
    print("We'll need the root privilege to install ACROBA-Platform.")
    if os.geteuid() == 0:
        print("You are running this program as root.")
    else:
        print("You are not running this program as root. Maybe you forget sudo?")
        return

    # Checking the system information
    print("Checking system information...")
    sys_info = os.popen('cat /proc/version').read()
    pci_info = os.popen('lspci').read()
    if 'WSL' in sys_info:
        print("The system is running under WSL.")
        is_wls = True
    else:
        print("The system is not running under WSL.")
        is_wls = False
    if 'NVIDIA' in pci_info:
        print("You have NVIDIA GPU(s).")
        has_nvidia = True
    else:
        print("You don't have a NVIDIA GPU.")
        has_nvidia = False

    # Checking the software requirements
    print("\n")
    while True:
        answer = input("Start to check the software requirements. Y(yes) / N(quit) ")
        if answer.lower() == "y":
            meet_requirements = check_requirements()
            break
        elif answer.lower() == "n":
            return

    # Install the requirements
    while not meet_requirements:
        answer = input("We are going to install the software requirements. Y(yes) / N(quit) ")
        if answer.lower() == "y":
            install_requirements()
            meet_requirements = check_requirements()
        elif answer.lower() == "n":
            return

    # Install Nvidia Toolkit for linux
    if has_nvidia and not is_wls:
        print("You have NVIDIA GPU(s), we're going to install the NVIDIA toolkit.")
        install_nvidia_toolkit(is_wls)

    # Asking for credential
    # print("Requirements are all meet. We need your credentials to download ACROBA-Platform")
    # credential_saved = credential_validation()
    # if credential_saved:
    #     print("Your credential is saved.")
    # else:
    #     print("Your credential is invalid. Please contact ACROBA.")
    #     return

    # Installing ACROBA-Platform
    print("Downloading ACROBA-Platform...")
    exit_code = os.system('git clone https://github.com/acroba-hackathon/setup.git && cd setup && ./setup.sh --clean-code')
    if exit_code == 0:
        print("ACROBA-Platform download successful.")
    else:
        print("ACROBA-Platform download failed. Please contact ACROBA.")
        return
    os.system('')

    print("Running ACROBA-Platform...")
    exit_code = os.system('cd setup/code/platform && make run')
    if exit_code == 0:
        print("ACROBA-Platform starts and running.")


if __name__ == '__main__':
    with open('output.log', 'w') as f:
        # sys.stdout = f
        # sys.stderr = f
        main()
