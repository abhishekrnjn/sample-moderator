# Install tools
## Execution Environment
- The program is executed on a virtual machine created using VirtualBox 7.0.14.
- Host OS: Windows 11 Pro
- Guest OS: Ubuntu Desktop 22.04.4 LTS

# Setup
## Python
#### Python Installation (Preparation)
- Refer to this [link](https://www.python.jp/install/ubuntu/index.html) for Python installation.

## Poetry
#### Poetry Installation (Preparation)
- Refer to this [link](https://python-poetry.org/docs/#installing-with-pipx) for Poetry installation.
- Install pipx using this [link](https://pipx.pypa.io/stable/#on-linux).
- Run the following commands:
```
sudo apt install python3-pip python3-venv
python3 -m pip install --user pipx
python3 -m pipx ensurepath
python3 -m pip install --user --upgrade pipx
```

### Pip
- Run the following commands:
```
pip install -U git+https://github.com/FujitsuResearch/atproto-python.git
pip install -U langchain langchain-openai
```

### Docker
#### Docker Installation (Preparation)
- Refer to this [link](https://docs.docker.com/engine/install/ubuntu/) for Docker installation.
- Run the following commands:
```
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755-d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
$(. /etc/os-release &&echo"$UBUNTU_CODENAME") stable"|\
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
