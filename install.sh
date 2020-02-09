#!/usr/bin/env sh

DIR_PMAIL='/opt/pmail';

echo "Creating folder $DIR_PMAIL";

if [ ! -d $DIR_PMAIL ]; then
    sudo mkdir $DIR_PMAIL
fi;

echo "Copy file...";

sudo cp './pmail.py' $DIR_PMAIL;
sudo chmod +x "$DIR_PMAIL/pmail.py";

echo "Making symbolic link in /usr/bin";

cd /usr/bin;

if [ -f './pmail' ]; then
    sudo rm './pmail';
fi;

sudo ln -s "$DIR_PMAIL/pmail.py" 'pmail';

echo "\e[0;32mInstallation complete!";