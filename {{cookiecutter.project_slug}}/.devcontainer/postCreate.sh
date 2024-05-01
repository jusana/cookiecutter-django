#!/bin/bash
git init --initial-branch=main
pre-commit install
sudo ln -sf /usr/share/zoneinfo/Europe/Paris /etc/localtime
bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)" --unattended
cat .devcontainer/bashrc.override.sh >> ~/.bashrc
sed -i 's/\#\[\[ -z ${AG_NO_HIST+x} ]]/[[ -z ${AG_NO_HIST+x} ]]/g' ~/.oh-my-bash/themes/agnoster/agnoster.theme.sh
sed -i 's/OSH_THEME="font"/OSH_THEME="agnoster"/g' ~/.bashrc
sed -i 's/composer/django/g' ~/.bashrc
source ~/.bashrc
