#!/usr/bin/env bash

sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update && sudo apt upgrade -y

sudo apt install -y python3.6 python3.6-dev python3.6-venv virtualenv
wget -nc https://bootstrap.pypa.io/get-pip.py && sudo python3.6 get-pip.py

sudo apt install -y redis-tools redis-server
sudo apt install -y nginx nginx-extras

sudo apt install -y libpq-dev postgresql postgresql-contrib

virtualenv --python=python3.6 --always-copy ~/venv
~/venv/bin/pip install git+git://github.com/mverteuil/pytest-ipdb.git

sudo apt-get install curl python-software-properties
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -

sudo apt-get install nodejs

curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list

sudo apt-get update && sudo apt-get install yarn