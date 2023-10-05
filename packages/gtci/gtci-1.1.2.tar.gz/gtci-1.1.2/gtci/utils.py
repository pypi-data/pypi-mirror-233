import os
import subprocess
import sys
import time
import shutil
import json
import pip
import threading
import platform
import re
import random
import zipfile
import requests
import urllib.request
from tqdm import tqdm



repository_store = "TWK5XME9V704"
execute = lambda: "3" if (platform.system().lower() == "darwin") else ""
currentpath = os.getcwd()
__version__ = "1.1.2"



def color():
    global black,reset,blue,red,yellow,green,cyan,white,magenta,lightblack,lightblue,lightcyan,lightgreen,lightmagenta,lightred,lightwhite,lightyellow,bold
    if (subprocess.getoutput("printf \"color\"") == "color") :
        bold          = "\033[01m"
        black         = '\033[30m'
        reset         = '\033[39m'
        blue          = '\033[34m'
        red           = '\033[31m'
        if (os.name == "nt"): yellow = '\033[33m'
        else: yellow  = '\033[92m'
        green         = '\033[32m'
        cyan          = '\033[36m'
        white         = '\033[37m'
        magenta       = '\033[35m'
        lightblack    = '\033[90m'
        lightblue     = '\033[94m'
        lightcyan     = '\033[96m'
        lightmagenta  = '\033[95m'
        lightred      = '\033[91m'
        lightwhite    = '\033[97m'
        lightyellow   = '\033[93m'
    else:
        bold, black, reset, blue, red, yellow, green, cyan, white, magenta, lightblack, lightblue, lightcyan, lightgreen, lightmagenta, lightred, lightwhite, lightyellow = "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
color()


def PrimeNum(num):
    if num <= 1: return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0: return False
    return True


def Box(text, left, right, raw, area, ct="", crt="", clt="", align="center"):
    area = area - 4
    if not PrimeNum(len(text)): text += " "
    if not PrimeNum(area): area -= 1
    LenOfTxt = len(text)
    len_txt_area = (area // 2) - (LenOfTxt // 2)
    finaltxt = clt + left
    if align == "right": finaltxt += ct + text
    for i in range(len_txt_area+1): finaltxt += raw
    if align == "center": finaltxt += ct + text
    for i in range(int(str(len_txt_area + LenOfTxt - area).replace("-",""))+1): finaltxt += raw
    if align == "left": finaltxt += ct + text
    finaltxt += crt + right
    return finaltxt


def space(num, a= " "):
    return "".join([a for i in range(num)])


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    i = 0
    while size_bytes >= 1024 and i < len(suffixes) - 1:
        size_bytes /= 1024
        i += 1
    size = "{:.2f}".format(size_bytes)
    return f"{size} {suffixes[i]}"


def anim_load(text):
    try:
        for handlechar in "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏":
            sys.stdout.write(f"\r {white}{handlechar} {reset}{text}")
            sys.stdout.flush()
            time.sleep(0.04)
    except KeyboardInterrupt:
        print(f"\n\n{bold}{magenta}[{red}!{magenta}] {white}Program Interrupted...{yellow}!!{reset}")
        exit()


def uninstall(repository_name):
    os.chdir(pip.__path__[0])
    os.chdir("..")
    try:
        os.chdir(repository_store)
        RM = None
        for repo in os.listdir():
            if (repo == repository_name): RM = True ; break
            else: RM = False
        if not (RM): print(f"{bold}{magenta}[{white}!{magenta}] {white}'{blue}{repository_name}{white}' aren't installed.{reset}")
        else:
            print(f"{bold}{magenta}[{white}!{magenta}] {white}Found existing installed program '{blue}{repository_name}{white}'{reset}")
            action = input(f"{bold}{magenta}[{white}?{magenta}] {white}Do you want's uninstall {red}( {white}Y{red}/{white}n {red}) {green}: {yellow}").lower()
            if (action == "y") or (action == "yes") :
                for repo in os.listdir():
                    if (repo == repository_name): shutil.rmtree(repository_name)
                    else: pass
                print(f"\n{bold}{magenta}[{white}+{magenta}] {blue}'{red}{repository_name}{blue}'{white} sucessfully uninstalled.{reset}")
            elif (action == "n") or (action == "no") :
                print(f"\n{bold}{magenta}[{white}+{magenta}] {blue}'{red}{repository_name}{blue}'{white} unsucessfull to uninstall.{reset}")
            else: print(f"\n{bold}{magenta}[{white}!{magenta}] {white}Invalid option.{reset}")
    except KeyboardInterrupt:
        print(f"\n\n{bold}{magenta}[{red}!{magenta}] {white}Program Interrupted...{yellow}!!{reset}")
        exit()
    except FileNotFoundError: print(f"{bold}{magenta}[{white}!{magenta}] {white}There aren't any repositories installed.{reset}")


def help():
    print(f"""{bold}
{magenta}[{white}-{magenta}] {yellow}Usage: {blue}gtci {white}<{red}command{white}> {white}[{red}options{white}]

{magenta}[{white}+{magenta}] {cyan}Commands {white} ~
    {yellow}install, clone     {white}Install programs.
    {yellow}run, start         {white}Iaunch a program.
    {yellow}uninstall, remove  {white}Remove or uninstall previously installed programs.
    {yellow}download           {white}Download the file in zip format to the current working directory.
    {yellow}list               {white}Display a list of all installed programs.
    {yellow}version            {white}Display the current version of the "gtci" tool itself.
    {yellow}help               {white}Display information about the available commands and options.
{magenta}[{white}+{magenta}] {cyan}General Options {white} ~
    {yellow}-i, -install       {white}Install programs.
    {yellow}-r, -run           {white}Iaunch a program.
    {yellow}-d, -download      {white}Download the file in zip format to the current working directory.
    {yellow}-l, -list          {white}Display a list of all installed programs.
    {yellow}-v, -version       {white}Display the current version of the "gtci" tool itself.
    {yellow}-h, -help          {white}Display information about the available commands and options.
{magenta}[{white}+{magenta}] {cyan}Here some examples {white}~
    {bold}{blue}gtci {yellow}install{red} tool_name_here   {magenta}>> {reset}{white}Install A Program From GreyTechno.
    {bold}{blue}gtci {yellow}run{red} tool_name_here       {magenta}>> {reset}{white}Launch A Installed Program.
    {bold}{blue}gtci {yellow}uninstall{red} tool_name_here {magenta}>> {reset}{white}Remove Or Uninstall Previously Installed Programs.
    {bold}{blue}gtci {yellow}list                     {magenta}>> {reset}{white}Display A List Of All Installed Programs.{bold}

{magenta}[{white}+{magenta}] {white}For get tools form GreyTechno so, visit {blue}https://github.com/GreyTechno/gtci
    {reset}""")


def run(reponame, Arguments):
    arguments = ""
    for args in Arguments: arguments += args + " "
    root_path = pip.__path__[0]
    os.chdir(root_path)
    os.chdir("..")
    try:
        os.chdir(repository_store)
        run = ""
        for repo in os.listdir():
            if (repo[0] == "."): continue
            elif (repo == reponame): 
                try:
                    os.chdir(reponame)
                    with open(".info") as file : run = json.loads(file.read())["main"]
                except : pass
            else: pass
        if not (run):
            Repository = os.listdir()
            DID = False
            for repo in Repository:
                if (repo[0] == "."): continue
                else:
                    if (re.search(reponame.lower(), repo.lower()) == None): pass
                    else: DID = True
            print(f"{bold}{magenta}[{red}!{magenta}] {white}Program not found '{blue}{reponame}{white}'{reset}")
            if (DID): print(f"{bold}{magenta}[{white}+{magenta}] {white}Did you mean,")
            for repo in Repository:
                if (repo[0] == "."): continue
                else:
                    if (re.search(reponame.lower(), repo.lower()) == None): pass
                    else: print(f"{bold}{magenta}[{white}-{magenta}] {yellow}{repo}{reset}")
        else: os.system(f"python{execute()} {run} {arguments}"), exit()
    except KeyboardInterrupt:
        print(f"\n\n{bold}{magenta}[{red}!{magenta}] {white}Program Interrupted...{yellow}!!{reset}")
        exit()
    except FileNotFoundError: print(f"{bold}{magenta}[{white}!{magenta}] {white}There aren't any repositories installed.{reset}")


def version():
    print(f"{bold}{magenta}[{white}+{magenta}] {white}The gtci current version is {red}{__version__} {white}and it includes several new features and bug fixes.{reset}")


def list():
    RepoLen = []
    VersionLen = []
    root_path = pip.__path__[0]
    os.chdir(root_path)
    os.chdir("..")
    try:
        os.chdir(repository_store)
        RepoLen, VersionLen = [], []
        [(
            RepoLen.append(len(repo)),
            VersionLen.append(len(json.loads(open(repo+"/.info").read())["version"]))
        ) for repo in os.listdir() if repo[0] != "."]

        if (max(RepoLen) < 10): RepoLen.append(10)
        if (max(VersionLen) < 7): VersionLen.append(7)
        if (PrimeNum(max(RepoLen))): MaxLenOfRepo = max(RepoLen) + 1
        else: MaxLenOfRepo = max(RepoLen)
        if (PrimeNum(max(VersionLen))): MaxLenOfVersion = max(VersionLen) + 1
        else: MaxLenOfVersion = max(VersionLen)
        print()
        print(bold + white + "Programs{}   Version{}".format(space(MaxLenOfRepo - 8), space(MaxLenOfVersion - 7)))
        print(bold + red + space(MaxLenOfRepo, "-") + "   " +space(MaxLenOfVersion, "-"))
        for repo in os.listdir():
            if (repo[0] == "."): continue
            else:
                with open(repo+"/.info") as file : version = json.loads(file.read())["version"]
                LenRepo, LenVersion = (MaxLenOfRepo - len(repo)), (MaxLenOfVersion - len(version))
                print(f"{bold}{yellow}{repo+space(LenRepo)}   {reset}{cyan}{version}{space(MaxLenOfVersion+3)}{reset}")
    except KeyboardInterrupt:
        print(f"\n\n{bold}{magenta}[{red}!{magenta}] {white}Program Interrupted...{yellow}!!{reset}")
        exit()
    except FileNotFoundError: print(f"{bold}{magenta}[{white}!{magenta}] {white}There aren't any repositories installed.{reset}")


def install(repository_name):
    try:
        repository_list = requests.get("https://raw.githubusercontent.com/GreyTechno/gtci/main/programs/.programs").json()
        root_path = pip.__path__[0]
        os.chdir(root_path)
        os.chdir("..")
        try:os.chdir(repository_store)
        except FileNotFoundError:
            os.mkdir(repository_store)
            with open(".info", "w") as file : file.write("")
            os.chdir(repository_store)
        if not (repository_name in repository_list):
            DID = False
            for repo in repository_list:
                if (repo[0] != "."):
                    if (re.search(repository_name.lower(), repo.lower()) == None): pass
                    else: DID = True
            print(f"{bold}{magenta}[{red}!{magenta}] {white}Program not found '{blue}{repository_name}{white}'{reset}")
            if (DID): print(f"{bold}{magenta}[{white}+{magenta}] {white}Did you mean,")
            for repo in repository_list:
                if (repo[0] != "."):
                    if (re.search(repository_name.lower(), repo.lower()) != None):
                        print(f"{bold}{magenta}[{white}-{magenta}] {yellow}{repo}{reset}")
        else:
            url = repository_list[repository_name]['zipurl'] + "?raw=true"
            supported_platforms = repository_list[repository_name]['platforms']['supported_platforms']
            dependencies = repository_list[repository_name]['dependencies']
            rname = "".join(random.sample("abcdefghijklmnopqrstuvwxyz", 7))
            zipname = url.split("/")[4] +"$"+ url.split("/")[-1].split(".")[0]
            toolname = zipname.split("$")[0]
            block_size = 1024
            if (repository_name in os.listdir()):
                print(f"{bold}{magenta}[{red}!{magenta}] {green}'{repository_name}{green}'{white}already installed.{reset}")
                print(f"{bold}{magenta}[{yellow}+{magenta}]  {white}See {green}'{blue}gtci -h{green}' {white}for more information.{reset}")
            else:
                response = requests.get(url, stream=True)
                E = True
                for i in range(15):
                    try: E, total_size = True, int(urllib.request.urlopen(urllib.request.Request(url, method='HEAD')).headers['Content-Length']) ; break
                    except TypeError: E = False
                if not (E): print(f"{bold}{magenta}[{red}!{magenta}] {white}Something went's wrong try again later.{reset}")
                else:
                    print(f"{bold}{magenta}[{yellow}-{magenta}] {white}File Size {yellow}{convert_size(total_size)}")
                    action = input(f"{bold}{magenta}[{yellow}*{magenta}] {white}Do you want's continue {red}({white}Y{red}/{white}n{red}){magenta}[{cyan}Default {green}: {blue}Y{magenta}] {green}: {yellow}").lower()
                    if (action == "n") or (action == "no"): print(reset)
                    else:
                        START = True
                        print()
                        if (supported_platforms != "os_independent"):
                            supported_os = repository_list[repository_name]['platforms']["supported_os"]
                            print(f"{bold}{magenta}[{red}!{magenta}] {white}Supported OS {green}: {cyan}{supported_os}{reset}")
                            action = input(f"{bold}{magenta}[{yellow}*{magenta}] {white}Do you want's continue {red}({white}Y{red}/{white}n{red}){magenta}[{cyan}Default {green}: {blue}Y{magenta}] {green}: {yellow}").lower()
                            if (action == "n") or (action == "no"): START = False, print(reset)
                            else: START = True
                        print()
                        print(f"{bold}{magenta}[{yellow}-{magenta}] {white}Tool Name {yellow}{repository_name}")
                        print(f"{bold}{magenta}[{yellow}-{magenta}] {white}Total Dependencies {yellow}{str(len(dependencies))}")
                        print(f"{bold}{magenta}[{yellow}-{magenta}] {white}File Size {yellow}{convert_size(total_size)}")
                        print()
                        with open(f"{rname}.zip", 'wb') as f:
                            for data in tqdm(iterable = response.iter_content(chunk_size = block_size),total = total_size/block_size, unit = ' KB', desc=f"{bold}{magenta}[{yellow}+{magenta}] {white}Downloading "):
                                f.write(data)
                        with zipfile.ZipFile(f"{rname}.zip", "r") as zip: zip.extractall(f"{rname}")
                        os.remove(f"{rname}.zip")
                        os.chdir(rname)
                        subfolder_path = os.path.join(rname, os.listdir()[0])
                        os.chdir("..")
                        for item in os.listdir(rname):
                            item_path = os.path.join(rname, item)
                            shutil.move(item_path, os.path.join(os.path.dirname(rname), item))
                        os.rmdir(rname)
                        os.rename(os.listdir()[0], toolname)
                        Dependencies = lambda: [subprocess.getoutput(f"pip{execute()} install {i}") for i in dependencies]
                        DEPENDENCIES = threading.Thread(target=Dependencies)
                        DEPENDENCIES.start()
                        while DEPENDENCIES.is_alive(): anim_load(f"{yellow}  Installing Building Dependencies...")
                        DEPENDENCIES.join()
                        sys.stdout.write(f"\r{bold}{magenta}[{white}*{magenta}] {white}Installtion Completed.             \n")
                        print(f"\n{bold}{magenta}[{yellow}+{magenta}] {white}For start {green}: {white}'{yellow}gtci {red}run {blue}{toolname}{white}'")
                        print(f"{bold}{magenta}[{yellow}+{magenta}] {white}See {green}'{blue}gtci -h{green}' {white}for more information.{reset}")
    except KeyboardInterrupt:
        print(f"\n\n{bold}{magenta}[{red}!{magenta}] {white}Program Interrupted...{yellow}!!{reset}")
        exit()


def download(repository_name):
    try:
        repository_list = requests.get("https://raw.githubusercontent.com/GreyTechno/gtci/main/programs/.programs").json()
        root_path = pip.__path__[0]
        os.chdir(root_path)
        os.chdir("..")
        try:os.chdir(repository_store)
        except FileNotFoundError:
            os.mkdir(repository_store)
            with open(".info", "w") as file : file.write("")
            os.chdir(repository_store)
        if not (repository_name in repository_list):
            DID = False
            for repo in repository_list:
                if (repo[0] != "."):
                    if (re.search(repository_name.lower(), repo.lower()) == None): pass
                    else: DID = True
            print(f"{bold}{magenta}[{red}!{magenta}] {white}Program not found '{blue}{repository_name}{white}'{reset}")
            if (DID): print(f"{bold}{magenta}[{white}+{magenta}] {white}Did you mean,")
            for repo in repository_list:
                if (repo[0] != "."):
                    if (re.search(repository_name.lower(), repo.lower()) != None):
                        print(f"{bold}{magenta}[{white}-{magenta}] {yellow}{repo}{reset}")
        else:
            os.chdir(currentpath)
            url = repository_list[repository_name]['zipurl'] + "?raw=true"
            rname = "".join(random.sample("abcdefghijklmnopqrstuvwxyz", 7))
            zipname = url.split("/")[4] +"$"+ url.split("/")[-1].split(".")[0]
            toolname = zipname.split("$")[0]
            block_size = 1024
            response = requests.get(url, stream=True)
            E = True
            for i in range(15):
                try: E, total_size = True, int(urllib.request.urlopen(urllib.request.Request(url, method='HEAD')).headers['Content-Length']) ; break
                except TypeError: E = False
            if not (E): print(f"{bold}{magenta}[{red}!{magenta}] {white}Something went's wrong try again later.")
            else:
                
                print(f"{bold}{magenta}[{yellow}-{magenta}] {white}Tool Name {yellow}{repository_name}")
                print(f"{bold}{magenta}[{yellow}-{magenta}] {white}File Size {yellow}{convert_size(total_size)}")
                action = input(f"{bold}{magenta}[{yellow}*{magenta}] {white}Do you want's continue {red}({white}Y{red}/{white}n{red}){magenta}[{cyan}Default {green}: {blue}Y{magenta}] {green}: {yellow}").lower()
                if (action == "n") or (action == "no"): print(reset)
                else:
                    print()
                    with open(f"{rname}.zip", 'wb') as f:
                        for data in tqdm(iterable = response.iter_content(chunk_size = block_size),total = total_size/block_size, unit = ' KB', desc=f"{bold}{magenta}[{yellow}+{magenta}] {white}Downloading "):
                            f.write(data)
                    with zipfile.ZipFile(f"{rname}.zip", "r") as zip: zip.extractall(f"{rname}")
                    os.remove(f"{rname}.zip")
                    os.chdir(rname)
                    subfolder_path = os.path.join(rname, os.listdir()[0])
                    os.chdir("..")
                    for item in os.listdir(rname):
                        item_path = os.path.join(rname, item)
                        shutil.move(item_path, os.path.join(os.path.dirname(rname), item))
                    os.rmdir(rname)
                    os.rename(os.listdir()[0], toolname)
                    with zipfile.ZipFile(toolname + ".zip", 'w', zipfile.ZIP_DEFLATED) as zip_obj:
                        for foldername, subfolders, filenames in os.walk(toolname):
                            for filename in filenames:
                                file_path = os.path.join(foldername, filename)
                                zip_obj.write(file_path)
                    shutil.rmtree(toolname)
                    print(f"{bold}{magenta}[{yellow}+{magenta}] {white}Sucessfully Download.")
                    print(f"\n{bold}{magenta}[{yellow}-{magenta}] {white}Downloaded Path,")
                    print(f"{bold}{magenta}[{yellow}-{magenta}] {cyan}{currentpath}\{toolname}.zip")
                    print(f"\n{bold}{magenta}[{yellow}+{magenta}] {white}See {green}'{blue}gtci -h{green}' {white}for more information.{reset}")
    except KeyboardInterrupt:
        print(f"\n\n{bold}{magenta}[{red}!{magenta}] {white}Program Interrupted...{yellow}!!{reset}")
        exit()


def internet():
    try:requests.get("https://google.com") ; return True
    except: return False



