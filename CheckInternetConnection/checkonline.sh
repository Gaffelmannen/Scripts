#!/bin/bash

set -e

HOSTNAME=www.sunet.se

while ! ping -c1 $HOSTNAME &>/dev/null
	do echo "No internet connection. - `date`"
	sleep 1
done

echo "Internet connection okay! - `date`";
echo "External IP-Address: `dig @resolver4.opendns.com myip.opendns.com +short -4`";

