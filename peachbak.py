###################################
#    Written by Patrik Nagy :)    #
#                                 #
# GNU General Public License v3.0 #
###################################

import shutil
import configparser
import os
import argparse
import time
from tqdm import tqdm  # pip install tqdm

# ANSI escape kody pre farbičky
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"

# CLI argumenty
# -no alebo --no-print pre vypnutie printovania priebehu
parser = argparse.ArgumentParser(description="Copy files with optional progress display")
parser.add_argument('-no', '--no-print', action='store_true', help="Do not print progress or filenames")
args = parser.parse_args()
silent = args.no_print

# Prečítaj config.ini
if not os.path.exists('config.ini'): # ak subor nejestvuje, vypíš chybu a ukonči toto trápenie
    print(f"{RED}Error: config.ini not found! Please create it first!{RESET}")
    exit(1)
config = configparser.ConfigParser()
config.read('config.ini')

def copy_with_progress(src, dst):
    # Ulož všetky subory na kopirovanie do zoznamu
    if not os.path.exists(src): # Ak zdrojovy priečinok neexistuje, vypíš chybu
        if not silent:
            print(f"{RED}Source directory {src} does not exist! Skipping...{RESET}")
        return
    
    files_to_copy = [] # zoznam suborov na kopirovanie
    for root, dirs, files in os.walk(src): # prejdi priečinok a jeho podpriečinky
        for file in files: # prejdi subory
            files_to_copy.append(os.path.join(root, file)) # pridaj subor do zoznamu
    
    total_files = len(files_to_copy)
    if total_files == 0 and not silent:
        print(f"{RED}No files to copy in {src}{RESET}")
        return

    # Zisti šírku terminálu pre tqdm
    term_width = shutil.get_terminal_size((100, 20)).columns

    # KOPIROVANIEEEEE
    if silent: # ak nechceme vypisovať priebeh:
        for file_path in files_to_copy: # pre každý subor v zozname
            relative_path = os.path.relpath(file_path, src)
            dest_file = os.path.join(dst, relative_path)
            os.makedirs(os.path.dirname(dest_file), exist_ok=True) # vytvor priečinok ak neexistuje
            try:
                shutil.copy2(file_path, dest_file) # skus skopírovať subor
            except Exception as e:
                print(f"Error copying {file_path}: {e}") # ak nie tak nie :( no čo už.
    else:
        with tqdm(total=total_files, desc=f"Copying from {src}", unit="file", ncols=term_width, leave=True) as pbar: # zadefinuj tqdm progress bar 
            for file_path in files_to_copy: # pre každý subor v zozname
                relative_path = os.path.relpath(file_path, src)
                dest_file = os.path.join(dst, relative_path)
                os.makedirs(os.path.dirname(dest_file), exist_ok=True) # vytvor priečinok ak neexistuje
                try:
                    shutil.copy2(file_path, dest_file) # skus skopírovať subor
                    # Vypíš nazov suboru do CLI
                    tqdm.write(f"{GREEN}Copying: {os.path.basename(file_path)}{RESET}")
                except Exception as e:
                    tqdm.write(f"{RED}Error copying: {os.path.basename(file_path)} - {e}{RESET}") # No a niečo sa pokazilo, vypíš chybu
                # Aktualizuj progress bar
                pbar.update(1)

# stopky pre dlžku operácie
start_time = time.time()

# Urob všetko pre každú sekciu v konfigu
for section in config.sections(): # pre každú sekciu v konfigu
    src = config[section]['source']
    dst = config[section]['destination']
    if not silent: # Ak chceme písať priebeh:
        print(f"\n{CYAN}Starting copy for section: {section}{RESET}")
    
    try:
        copy_with_progress(src, dst) # Tak, skúsme teda kopirovať:
        if not silent: # Ak chceme písať priebeh, napíš, že sme skopírovali sekciu
            print(f"{CYAN}Finished copying section: {section}{RESET}\n") 
    except Exception as e: # Ak nastane chyba pri kopírovaní, vypíš ju
        print(f"{RED}Error copying section {section}: {e}{RESET}\n")

# Zaznamenaj čas ukončenia a vypíš trvanie operácie
end_time = time.time()
duration = end_time - start_time
minutes, seconds = divmod(duration, 60)
hours, minutes = divmod(minutes, 60)
if not silent: # Ak chceme písať priebeh, vypíš čas operácie
    print(f"{CYAN}All sections copied successfully!{RESET}")
    if hours > 0: # Ak to bolo hlhšie ako 1 hodina, vypíš aj hodiny
        print(f"{CYAN}Total operation time: {int(hours)}h {int(minutes)}m {int(seconds)}s{RESET}")
    else: # Inak len minuty a sekundy
        print(f"{CYAN}Total operation time: {int(minutes)}m {int(seconds)}s{RESET}")
