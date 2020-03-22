#!/bin/bash
  
COMPANY=$1
#PASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)
PASSWORD=$2
ENCRYPTED=$(openssl passwd $PASSWORD)

if [ `sudo /bin/egrep  -i "^${COMPANY}:" /etc/passwd` ]; then
        echo "User $COMPANY exists in /etc/passwd" >> /home/FTPscript/user.txt
else
        echo "User $COMPANY now added to /etc/passwd" >> /home/FTPscript/user.txt
	
        sudo useradd -d /home/FTPserver/$COMPANY/ -m $COMPANY -p $ENCRYPTED
#       sudo usermod -d /home/FTPserver/$COMPANY/ $COMPANY
        sudo mkdir -p /home/FTPserver/$COMPANY
        sudo chown -R $COMPANY:$COMPANY /home/FTPserver/$COMPANY
        sudo chmod 770 /home/FTPserver/$COMPANY
        echo -e "${PASSWORD}\n${PASSWORD}" | passwd $COMPANY
        echo Username: $COMPANY and Password: $PASSWORD >> /home/FTPscript/pass.txt
fi
