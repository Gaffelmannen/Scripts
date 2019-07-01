#!/bin/bash

HOSTNAME=www.sunet.se

while ! ping -c1 $HOSTNAME &>/dev/null
	do echo "No internet connection. - `date`"
	sleep 1
done

echo "Internet connection okay! - `date`";


