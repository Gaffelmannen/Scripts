#!/bin/bash

#URL=www.sunet.se
#URL='https://file-examples-com.github.io/uploads/2017/10/file_example_JPG_1MB.jpg'
URL='https://file-examples.com/wp-content/storage/2017/04/file_example_MP4_1280_10MG.mp4'

if avg_speed=$(curl -qfsS -w '%{speed_download}' -o /dev/null --url "${URL}")
then
  echo "$avg_speed"
fi

#curl -s -o /dev/null -w "%{time_total}\n" ${URL}

#curl -s -w 'Time to connect: {time_connect}'  $URL

#curl -s -w 'Testing Website Response Time for :%{url_effective}\n\nLookup Time:\t\t%{time_namelookup}\nConnect Time:\t\t%{time_connect}\nPre-transfer Time:\t%{time_pretransfer}\nStart-transfer Time:\t%{time_starttransfer}\n\nTotal Time:\t\t%{time_total}\n' -o /dev/null $URL > webspeedtest_"$(date)"
