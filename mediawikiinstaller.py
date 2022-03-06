#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#          MᴇᴅɪᴀWɪᴋɪ Iɴsᴛᴀʟʟᴇʀ Pʀᴏɢʀᴀᴍ               #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Purpose: Helps you instantly and automatically     #
#          install MediaWiki (because Wikimedia      #
#          wouldn't).                                #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# License: GPL-3.0-or-later                          #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# 𝗪𝗔𝗥𝗡𝗜𝗡𝗚: 𝗜 𝗗𝗢 𝗡𝗢𝗧 𝗣𝗥𝗢𝗩𝗜𝗗𝗘 𝗔𝗡𝗬 𝗪𝗔𝗥𝗥𝗔𝗡𝗧𝗬 𝗙𝗢𝗥    #
# 𝗧𝗛𝗜𝗦 𝗦𝗖𝗥𝗜𝗣𝗧. 𝗨𝗦𝗘 𝗜𝗧 𝗔𝗧 𝗬𝗢𝗨𝗥 𝗢𝗪𝗡 𝗥𝗜𝗦𝗞.             #
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
backtoinst = "N"
print(
    f"{Fore.GREEN}MediaWiki installer{Style.RESET_ALL} (unofficial) developer release"
)
print(
    f"{Fore.RED}Disclaimer:{Style.RESET_ALL} Wikimedia does NOT own this installer. Plus,"
)
print("            MediaWiki is PHP, so it will be installed.")
import platform
import shutil

try:
    import requests
except ImportError:
    os.system("python -m pip install requests")
    import requests
sysver = platform.system() + " " + platform.release() + " v" + platform.version()
print(f"Running on: {sysver}")
if os.name == "nt":

    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False


def minstall():
    if not Path(f"{home}/MediaWiki").is_dir():
        os.makedirs(f"{home}/MediaWiki")
    else:
            print(
                f"{Fore.YELLOW}Warning:{Style.RESET_ALL} MediaWiki is already installed! Trying to install MediaWiki again after installing it may\n{Fore.RED}clear your wiki{Style.RESET_ALL}. Proceed with caution."
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
                        os.system("scoop reset apache php/php7.4 sqlite composer")
                except Exception as e:
                    print("Failed to delete %s. Reason: %s" % (file_path, e))
                    exit(1)
            else:
                exit()
    print("These will be installed:")
    print("    1: Database (SQLite)")
    print("    2: MediaWiki")
    print("    3: Server (Apache)")
    print("    4: PHP")
    print("This includes what you need to use MW. We need Composer (this IS NOT Docker-related but PHP-related, see\nhttps://www.mediawiki.org/wiki/Composer).")
    os.system("powershell -c Set-ExecutionPolicy RemoteSigned -scope CurrentUser")
    os.system(
        "powershell -c Invoke-Expression (New-Object System.Net.WebClient).DownloadString('https://get.scoop.sh')"
    )
    os.system("scoop bucket add php")
    if is_admin():
        print("> scoop bucket add extras")
        os.system("scoop bucket add extras")
        print("> scoop install php/php7.4 sqlite apache extras/vcredist2019 composer")
        os.system("scoop install php/php7.4 sqlite apache extras/vcredist2019 composer")
    else:
        print("> scoop install php/php7.4 sqlite apache composer")
        os.system("scoop install php/php7.4 sqlite apache composer")
    if os.name != "nt":
        print(
            "See the MediaWiki documentation for the MediaWiki installation requirements:\nhttps://www.mediawiki.org/wiki/Special:MyLanguage/Manual:Installation_requirements"
        )
    link = "https://releases.wikimedia.org/mediawiki/1.37/mediawiki-1.37.1.zip"
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
                sys.stdout.write("\r[%s%s]" % (f"{Fore.GREEN}#{Style.RESET_ALL}" * done, f"{Fore.RED}#{Style.RESET_ALL}" * (50 - done)))
                sys.stdout.flush()
    new = f"{home}/MediaWiki"
    print(" Done!\n")
    import zipfile

    with zipfile.ZipFile(file_name, "r") as zip_ref:
        zip_ref.extractall(new)
    os.unlink(file_name)
    if os.name == "nt":
        print("Please wait...")
        os.system("composer i openssl")
        os.system(f"composer i -d {home}\MediaWiki\mediawiki-1.37.1")
        httpdfile = f"{home}\httpd.conf"
        print("Configuring Apache HTTP Server...")
        with open(f"{home}\MediaWiki\httpd.conf", "w") as f:
            f.write(f"Include {home}\MediaWiki\mediawiki-1.37.1\*.php")
        print(f"Start the server by running: httpd -f {home}\MediaWiki\httpd.conf")
        time.sleep(2)


def byemw():
    if os.path.exists(f"{home}/MediaWiki"):
        try:
            file_path = f"{home}/MediaWiki"
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
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))
            exit(1)
    else:
        print("MediaWiki is not installed.")
        exit(1)


print("Choose a mode:")
print(
    f"    1: {Fore.GREEN}Install{Style.RESET_ALL} MediaWiki 1.37 and the required software"
)
print(f"    2: {Fore.RED}Uninstall{Style.RESET_ALL} the current MediaWiki")
print("Or, type 'q' to quit")
### Choose Mode ##
try:
    while True:
        mode = "0"
        mode = input("\nChoose mode: ")
        if mode == "1":
            minstall()
        elif mode == "2":
            byemw()
        elif mode == "q":
            exit()
        else:
            print(f"Invalid input: {mode}. Please choose 1 or 2. Or, type 'q' to quit.")
except KeyboardInterrupt:
  exit()
