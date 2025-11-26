# IV1351\_Project

## Scripts

To run the scripts, follow the installation proccess of the required dependencies inside of an venv

### Python configuration
This is only needed for the script [create_db.sh](seminar_2/scripts/create_db.sh) <br>
All other scripts can be run without setting up python

1. Install python3 on your machine (if you don't already have it)
```
brew install python3
# or
sudo apt-get install python3
# or 
sudo dnf install python3
# or 
sudo pacman -S python
# or whatever package manager you use
```

2. Create the virtual environment
```
python3 -m venv venv 
```

3. Run the venv script to start it 
```
# For regular zsh terminal
source ./venv/bin/activate
# For the fish terminal 
source ./venv/bin/activate.fish
# maybe for windows?
venv/scripts/activate
```

4. install the faker dependency
```
python -m pip install faker 
```

5. exit the venv 
```
deactivate
```

### Running scripts
To run the scripts, you first need to give yourself permission to do so. In the project root directory you can enter this command to give permission to all the scripts:
```
find . -type f -name "*.sh" -exec chmod 755 {} \;
```
Alternatively `chmod +x filename.sh` to give permission to one script at a time.

Then you can run them by simply `./path/to/script/folder/script.sh`
