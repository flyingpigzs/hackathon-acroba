import os


def install_requirements():
    os.system("apt-get update && apt-get install -y git apt-transport-https ca-certificates curl software-properties-common")
    os.system("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg")
    os.system('echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null')
    os.system('sudo apt update && sudo apt install -y docker-ce')


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


def credential_validation():
    exit_code = os.system('git config --global credential.helper store && git clone git@github.com:ACROBA-Project/ACROBA-Platform.git')
    if exit_code == 0:
        return True
    else:
        return False


def main():
    print("Welcome to ACROBA!")

    # Checking the software requirements
    while True:
        answer = input("First, we will check the requirements. Y(yes) / N(quit) ")
        if answer.lower() == "y":
            meet_requirements = check_requirements()
            break
        elif answer.lower() == "n":
            return

    # Install the requirements
    while not meet_requirements:
        answer = input("We are going to install the requirements. Y(yes) / N(quit) ")
        if answer.lower() == "y":
            install_requirements()
            meet_requirements = check_requirements()
        elif answer.lower() == "n":
            return

    # Asking for credential
    print("Requirements are all meet. We need your credentials to download ACROBA-Platform")
    credential_saved = credential_validation()
    if credential_saved:
        print("Your credential is saved.")
    else:
        print("Your credential is invalid. Please contact ACROBA.")
        return

    # Installing ACROBA-Platform
    print("Downloading ACROBA-Platform...")
    exit_code = os.system('cd ACROBA-Platform && ./make pull TAG=latest')
    if exit_code == 0:
        print("ACROBA-Platform download successful.")
    else:
        print("ACROBA-Platform download failed. Please contact ACROBA.")
        return

    print("Running ACROBA-Platform...")
    exit_code = os.system('make run X11=NO GPU=NO')
    if exit_code == 0:
        print("ACROBA-Platform starts and running.")


if __name__ == '__main__':
    main()