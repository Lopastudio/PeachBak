# PeachBak - File Copy & Config Generator  

![PeachBak Logo](peachbak-logo.png)

**Written by Patrik Nagy**  
**Licensed under:** GNU General Public License v3.0  

---

## Overview

**PeachBak** is a simple python utility written to simplify backups!
You simply create a config file `config.ini` with my *fancy* GUI tool `gen-config.py`, or manually and run the peachbak.py script. It uses the `shutil` library, so it should be pretty fast.
You can then run the script manually and it will backup all your data, or make a schedule with windows's `task scheduler` or on linux, you can use `Crontab`.

---

## Installation

1. Install python 3, and if you are running this script on windows, make sure to check the "Add Python to enviroment variables" checkbox.
2. Install dependencies:  
`pip install tqdm configparser argparse`
If your system did not recognise this command on windows, you didn't check the checkbox from the first step

3. Download the gen-config.py and set up your folders you would like to copy along with their destinations.

4. Copy the generated config.ini into the same directory as `peachbak.py`

5. RUN IT! It should copy all your files according to the config without any issuess :>
