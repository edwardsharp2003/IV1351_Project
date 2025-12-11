# IV1351 Project
Instructions for project task 3 [further down](#task-3)

## Scripts

To run the scripts, follow the installation proccess of the required dependencies inside of an venv

### Python Configuration
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
sudo pacman -S python3
# or whatever package manager you use
```

2. Create the virtual environment
```
python3 -m venv venv 
```

3. Run the venv script to start it 
```
# For z-shell/bash 
source ./venv/bin/activate
# For fish-shell 
source ./venv/bin/activate.fish
# maybe for windows powershell?
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

## Task 2

### Manual method

Follow this method to setup the database manually with inserts into the sql cli.

1. Create and connect to the database (Do this in project root directory, IV1351_Project)
```
psql postgres
```
```
CREATE DATABASE iv1351t2;
```
```
\c iv1351t2;
```
2. Insert appropriate sql scripts
```
\i seminar_2/task_submissions/create_db.sql;
```
```
\i seminar_2/task_submissions/insert_data.sql;
```
3. Run queries, for example:
```
\i seminar_2/task_submissions/query-4.sql;
```


## Task 3
Everything needed to replicate our results from task 3 <br>
You will need python in order to run the app, since everything is done in python. <br>
Follow [Python Configuration](#python-configuration) in case you dont have any python version installed.

### 3.1 Create Database
**Create DB from files in [db_scripts](seminar_3/task_submission/db_scripts)**
```
CREATE DATABASE iv1351t3;
\c iv1351t3;
\i seminar_3/task_submission/db_scripts/create_db.sql;
\i seminar_3/task_submission/db_scripts/insert_data.sql;
```

### 3.2 Dotfiles and Venv setup
**Make a copy of [env.example.](seminar_3/task_submission/env.example), name it ".env" (dotenv) and fill with your specific information.** <br>
Most noteworthy, this means changing "DB_USER=postgres" to whatever username you use for your database, and <br>
"DB_PASSWORD=your_postgres_password_here" to contain your database password

**Activate venv, go to project root for task 3**
```
cd IV1351_Project/seminar_3/task_submission
```
**Download requirements**<br>
<sub>(Need to be in same directory as requirements.txt for this, otherwise add path)</sub>
```
pip install -r requirements.txt
```

### 3.3 Run it
if you're in source root [task_submission](seminar_3/task_submission/):
```
python3 main.py
```
if you're in project root [IV1351_Project]():
```
python3 seminar_3/task_submission/main.py
```
