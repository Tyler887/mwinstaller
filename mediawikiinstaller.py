#!/usr/bin/env python3
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#          MᴇᴅɪᴀWɪᴋɪ Iɴsᴛᴀʟʟᴇʀ Pʀᴏɢʀᴀᴍ               #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Purpose: Helps you instantly and automatically     #
#          install MediaWiki (because Wikimedia      #
#          wouldn't).                                #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# License: GPL-3.0-or-later                          #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# WARNING: I DO NOT PROVIDE ANY WARRANTY FOR         #
# THIS SCRIPT. USE IT AT YOUR OWN RISK.              #
# I always try to fix any bugs, but sometimes it is  #
# impossible. You should inspect the source code     #
# yourself.                                          #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#####################################################
####################### INIT ########################
#####################################################
import os
import sys
import ctypes
import time
import glob

try:
    from colorama import *
except ImportError:
    os.system("python -m pip install colorama")
    from colorama import *
try:
    import inquirer
except:
    os.system("python -m pip install inquirer")
    import inquirer
from pathlib import Path

home = str(Path.home())
import platform
import shutil

os.system("cls" if platform.system() == "Windows" else "clear")
print(
    f"MediaWiki Installer Program (unofficial) developer release"
)
print(
    f"{Fore.RED}Disclaimer:{Style.RESET_ALL} Wikimedia does NOT own this installer. Plus,"
)
print("            MediaWiki is PHP, so it will be installed.")
try:
    import requests
except ImportError:
    os.system("python -m pip install requests")
    import requests
try:
    import questionary
except ImportError:
    os.system("python -m pip install questionary")
    import questionary
sysver = platform.system() + " " + platform.release() + " v" + platform.version()
print(f"Running on: {sysver}")
if os.name == "nt":

    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

def minstall():
    global validComp1
    validComp1 = 0
    if os.path.isfile(f"{home}/ComposerPhar.txt"):
      validComp1 = 1
      with open(f'{home}/ComposerPhar.txt') as f: composer = f.read()
    else:
      while not validComp1:
        composer = questionary.path("What's the path to Composer 1? This will be saved.").ask()
        if composer.endswith("composer.phar") and os.path.exists(composer):
          validComp1 = 1
          with open(f"{home}/ComposerPhar.txt", "w") as f:
            f.write(composer)
        else:
         if os.path.exists(composer):
          if os.path.isdir(composer):
            print("Searching in folder for composer.phar via globbing... If the submitted prompt appears again, this folder has no\ncomposer.phar.")
            for i in glob.glob(f"{composer}/*"):
                if os.name == "nt":
                  print(f"{Fore.RED}Error:{Style.RESET_ALL} After testing, you cannot set the path as a folder on Windows.\nInstead, just drop the composer.phar into this window or manually type the path to it\nand add 'composer.phar' (without adding spaces) to the end.")
                  break
                if i == f"{composer}/composer.phar":
                  composer = i
                  validComp1 = 1
                  with open(f"{home}/ComposerPhar.txt", "w") as f:
                    f.write(composer)
                  break
          else:
           print(f"{Fore.RED}Error:{Style.RESET_ALL} To prevent PHP errors, file must be named 'composer.phar'")
         else:
          print(f"{Fore.RED}Error:{Style.RESET_ALL} File doesn't exist")
    if not Path(f"{home}/MediaWiki").is_dir() or not len(os.listdir(f'{home}/MediaWiki')) >= 1:
      if not Path(f"{home}/MediaWiki").is_dir():
        os.makedirs(f"{home}/MediaWiki")
    else:
            print(
                f"{Fore.YELLOW}Warning:{Style.RESET_ALL} MediaWiki is already installed! Trying to install MediaWiki again after installing it may\n{Fore.RED}clear your wiki{Style.RESET_ALL}. Proceed with caution.\n    > If upgrading, don't reinstall! Instead, see https://www.mediawiki.org/wiki/Manual:Upgrading."
            )
            questions = [
                inquirer.Confirm(
                    "confirm",
                    message="Are you sure you want to reinstall MediaWiki?",
                    default=False,
                ),
            ]
            rianswer = inquirer.prompt(questions)
            if str(rianswer) == str("{'confirm': True}"):
                file_path = f"{home}/MediaWiki"
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    if os.name == "nt":
                        os.system("scoop reset apache php/php7.4 sqlite")
                except Exception as e:
                    print("Failed to delete %s. Reason: %s" % (file_path, e))
                    exit(1)
            else:
                exit()
    if os.name == "nt":
      print("These will be installed:")
      print("    1: Database (SQLite)")
      print("    2: MediaWiki")
      print("    3: Server (Apache)")
      print("    4: PHP")
      print("    5: Dependencies of MW")
    version = questionary.select(
      "Which version do you want to install?",
      choices=[
          "1.37.1 (current version)",
          "1.36.3 (legacy 'LTS' version)",
          "1.35.5 (legacy version)"
    ]).ask()  # returns value of selection
    version = version[:6] # Each version consists of 6 unicode characters
    sver = version[:4]
    print(f"    > Actual/short version: {sver}")
    if os.name == "nt":
      os.system("powershell -c Set-ExecutionPolicy RemoteSigned -scope CurrentUser")
      os.system(
        "powershell -c Invoke-Expression (New-Object System.Net.WebClient).DownloadString('https://get.scoop.sh')"
      )
    if os.name == "nt":
      os.system("scoop bucket add php")
      if is_admin():
        print("> scoop bucket add extras")
        os.system("scoop bucket add extras")
        print("> scoop install php/php7.4 sqlite apache extras/vcredist2019")
        os.system("scoop install php/php7.4 sqlite apache extras/vcredist2019")
      else:
        print("> scoop install php/php7.4 sqlite apache")
        os.system("scoop install php/php7.4 sqlite apache")
    if os.name != "nt":
        print(
            "See the MediaWiki documentation for the MediaWiki installation requirements.\n    > Docs: https://mediawiki.org/wiki/Special:MyLanguage/Manual:Installation_requirements"
        )
    link = f"https://releases.wikimedia.org/mediawiki/{sver}/mediawiki-{version}.zip"
    file_name = f"{home}/mediawiki.zip"
    with open(file_name, "wb") as f:
        print("Downloading MediaWiki...")
        response = requests.get(link, stream=True)
        total_length = response.headers.get("content-length")
        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % (f"{Fore.LIGHTGREEN_EX}#{Style.RESET_ALL}" * done, f"{Fore.RED}#{Style.RESET_ALL}" * (50 - done)))
                sys.stdout.flush()
    new = f"{home}/MediaWiki"
    print(" Done!\n")
    import zipfile

    with zipfile.ZipFile(f"{home}/mediawiki.zip", "r") as zip_ref:
        zip_ref.extractall(new)
    os.unlink(file_name)
    if os.name == "nt":
        print("Configuring Apache HTTP Server...")
        with open(f"{home}\MediaWiki\httpd.conf", "w") as f:
            f.write(f"Include {home}\MediaWiki\mediawiki-{version}\*.php")
        print(f"Start the server by running: httpd -f {home}\MediaWiki\httpd.conf")
    print("Please wait...")
    os.system(f"php {composer} config -g -- disable-tls true")
    os.system(f"php {composer} i -d {home}/MediaWiki/mediawiki-{version}")
    os.system(f"php {composer} config -g -- disable-tls false")



def byemw():
    global childrenfiles
    childrenfiles = 0
    if os.path.exists(f"{home}/MediaWiki") and len(os.listdir(f'{home}/MediaWiki')) >= 1:
            if os.name == "nt":
                print("Telling Apache to shutdown the wiki server...")
                os.system("httpd -k shutdown")
                print("Uninstalling software...")
                if is_admin():
                    os.system(
                        "scoop uninstall php/php7.4 sqlite apache extras/vcredist2019"
                    )
                else:
                    os.system("scoop uninstall php/php7.4 sqlite apache")
            files = glob.glob(f"{home}/MediaWiki/mediawiki-*/*")
            print("The following files will be DELETED:")
            for i in files:
              if os.path.isfile(i):
                print(f"    {i}")
              time.sleep(0.1)
            print("The following folders will ALSO be deleted:")
            for i in files:
              if os.path.isdir(i):
                for i in glob.glob(f"{i}/*"):
                  childrenfiles=childrenfiles+1
                print(f"    {i}\n        {Back.BLUE}(i){Style.RESET_ALL} This folder has {str(childrenfiles)} files.")
                childrenfiles = 0
              time.sleep(0.1)
            print(f"This is {Fore.RED}permanent{Style.RESET_ALL} and cannot be undone. Backup your wiki first.")
            confirmuninst = input("To continue, type 'Yes, do as I say!': ")
            if confirmuninst == "Yes, do as I say!":
               print("Uninstalling...")
               for i in glob.glob(f"{home}/MediaWiki/mediawiki-*/*"):
                 file_path = i
                 if os.path.isfile(file_path) or os.path.islink(file_path):
                   os.unlink(file_path)
                 elif os.path.isdir(file_path):
                   shutil.rmtree(i)
               if os.path.isfile(f"{home}/MediaWiki/httpd.conf"):
                 os.unlink(f"{home}/MediaWiki/httpd.conf")
               if os.path.isdir(f"{home}/MediaWiki"):
                 shutil.rmtree(f"{home}/MediaWiki")
            else:
              print("Abort.")
          
    else:
        os.system("cls" if platform.system() == "Windows" else "clear")
        print(f"         {Back.BLUE}             MediaWiki is not installed. Choose another option to install it.             ", end="")
        print(Style.RESET_ALL)
        print(
             f"MediaWiki Installer Program (unofficial) developer release"
        )
        print(
             f"{Fore.RED}Disclaimer:{Style.RESET_ALL} Wikimedia does NOT own this installer. Plus,"
        )
        print("            MediaWiki is PHP, so it will be installed.")
        print(f"Running on: {sysver}")

def mwtest():
  print(f"{Fore.RED}ACCORDING TO THE GPLV2 AND GPLV3, WIKIMEDIA PROVIDES TEST RELEASES ON AN AS-IS BASIS!{Style.RESET_ALL} Install\nthis version at your own risk.")
  questions = [
                inquirer.Confirm(
                    "confirm",
                    message="Are you sure you want to install MediaWiki from GIT?",
                    default=False,
                ),
  ]
  rianswer = inquirer.prompt(questions)
  if str(rianswer) == str("{'confirm': True}"):
            if os.path.exists(f"{home}/MediaWiki") and len(os.listdir(f'{home}/MediaWiki')) >= 1:
                file_path = f"{home}/MediaWiki"
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print("Failed to delete %s. Reason: %s" % (file_path, e))
                    exit(1)
            print("If this fails, make sure Git is installed. Some GNU/Linux distros like Ubuntu have Git\npreinstalled.")
            os.system(f"git clone --depth 1 https://gerrit.wikimedia.org/r/mediawiki/core {home}/MediaWiki/mediawiki-gitmain")
  else:
   exit()

### Choose Mode ##
while True:
  mode = questionary.select(
      "What do you want to do?",
      choices=[
          'Install MediaWiki from Wikimedia Download',
          'Install MediaWiki from Wikimedia Gerrit (Git)',
          'Uninstall MediaWiki',
          'Exit'
      ]).ask()  # returns value of selection
  if mode == "Install MediaWiki from Wikimedia Download":
    minstall()
  elif mode == "Uninstall MediaWiki":
    byemw()
  elif mode == "Install MediaWiki from Wikimedia Gerrit (Git)": # Git installation is new to this app
    mwtest()
  elif mode == "Exit":
    exit()
