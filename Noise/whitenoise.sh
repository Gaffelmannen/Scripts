#!/bin/bash

set -e

cat /dev/urandom | sox -traw -r44100 -b16 -e unsigned-integer - -tcoreaudio

