#!/bin/bash

# Function to navigate to specific script labels
function goto {
    label=$1
    cmd=$(sed -n "/^:[[:blank:]][[:blank:]]*${label}/{:a;n;p;ba};" $0 | grep -v ':$')
    eval "$cmd"
    exit
}

# Get the ngrok token from user input
read -p "Paste Ngrok Authtoken: " CRP

# Download and execute the ngrok script
wget -O ng.sh https://github.com/kmille36/Docker-Ubuntu-Desktop-NoMachine/raw/main/ngrok.sh > /dev/null 2>&1
chmod +x ng.sh
./ng.sh

# Configure ngrok with the provided token
./ngrok config add-authtoken "$CRP"

: ngrok
clear
echo "Repo: https://github.com/kmille36/Docker-Ubuntu-Desktop-NoMachine"
echo "======================="
echo "Choose ngrok region (for better connection)."
echo "======================="
echo "us - United States (Ohio)"
echo "eu - Europe (Frankfurt)"
echo "ap - Asia/Pacific (Singapore)"
echo "au - Australia (Sydney)"
echo "sa - South America (Sao Paulo)"
echo "jp - Japan (Tokyo)"
echo "in - India (Mumbai)"
read -p "Choose ngrok region: " CRP
./ngrok tcp --region "$CRP" 4000 &>/dev/null &
sleep 1

# Check ngrok tunnel status
if curl --silent --show-error http://127.0.0.1:4040/api/tunnels > /dev/null 2>&1; then
    echo "OK"
else
    echo "Ngrok Error! Please try again!"
    sleep 1
    goto ngrok
fi

# Run Docker container for NoMachine without privileged options
docker run --rm -d --network host --name nomachine-mate -e PASSWORD=123456 -e USER=user --shm-size=1g thuonghai2711/nomachine-ubuntu-desktop:mate
clear

# Display NoMachine connection information
echo "NoMachine: https://www.nomachine.com/download"
echo "Done! NoMachine Information:"
echo "IP Address:"
curl --silent --show-error http://127.0.0.1:4040/api/tunnels | sed -nE 's/.*public_url":"tcp:..([^"]*).*/\1/p'
echo "User: user"
echo "Passwd: 123456"
echo "VM can't connect? Restart Cloud Shell then Re-run script."

# Progress indicator loop
seq 1 43200 | while read -r i; do 
    for dots in . .. ... .... .....; do 
        echo -en "\r Running $dots $i s /43200 s"
        sleep 0.1
    done
done
