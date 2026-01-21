#!/bin/bash

set +e

# Fundamenta
hostname=www.sunet.se
speed_check_url='https://file-examples.com/wp-content/storage/2017/04/file_example_MP4_1920_18MG.mp4'

# Check connection
while ! ping -c1 $hostname &>/dev/null
	do echo "No internet connection. - `date`"
	sleep 1
done

# Get information from ipinfo
data=`curl -s ipinfo.io`

# Get system type
unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    MSYS_NT*)   machine=MSys;;
    *)          machine="UNKNOWN:${unameOut}"
esac

# Get local IP
if [ $machine == "Mac" ]; then
    local_ip=$(ipconfig getifaddr en0)
    if [ "$local_ip" = "" ]; then
    	local_ip=$(ipconfig getifaddr en1)
    fi
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    local_ip=$(/sbin/ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1)
fi

# Try to check speed
if [ "$(curl -sL -w '%{http_code}' ${speed_check_url} -o /dev/null)" = "200" ]; then
	avg_speed=$(curl -qfsS -w '%{speed_download}' -o /dev/null --url "${speed_check_url}l")
	avg_speed_output=$((($avg_speed/1024)*10))
else
	avg_speed_output="-- "
fi

# Present it
echo "Internet connection okay! - `date`";
echo ""
echo "Internal IP:         `echo $local_ip`";
echo "External IP:         `dig @resolver4.opendns.com myip.opendns.com +short -4`";
echo "City:                `echo $data | jq -r '.city'`";
echo "Country:             `echo $data | jq -r '.country'`";
echo "Timezone:            `echo $data | jq -r '.timezone'`";
echo "Organization:        `echo $data | jq -r '.org'`";
echo "Location:            `echo $data | jq -r '.loc'`";
echo "Speed:               `echo `$avg_speed_output` echo Mbps`";
