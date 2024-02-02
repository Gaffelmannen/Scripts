#!/bin/bash

set -e

HOSTNAME=www.sunet.se

while ! ping -c1 $HOSTNAME &>/dev/null
	do echo "No internet connection. - `date`"
	sleep 1
done

DATA=`curl -s ipinfo.io`

echo "Internet connection okay! - `date`";
echo "External IP-Address: `dig @resolver4.opendns.com myip.opendns.com +short -4`";
echo "City:                `echo $DATA | jq -r '.city'`";
echo "Country:             `echo $DATA | jq -r '.country'`";
echo "Timezone:            `echo $DATA | jq -r '.timezone'`";
echo "Organization:        `echo $DATA | jq -r '.org'`";
echo "Location:            `echo $DATA | jq -r '.loc'`";