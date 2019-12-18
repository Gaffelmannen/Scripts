run:
sudo -H install -r requirements.txt

if windows:
    install xming
    cmd > export DISPLAY=:0

linux:
    chmod +x generate.py

app:
./generate.py
