#Random wallpaper setter

import argparse
import json
import os
import shutil
import random
import logging ,traceback
import pickle
import urllib , urllib.request , urllib.error
from platform import system

def cust_logger():
    '''logger for file and console'''

    logger = logging.getLogger("mistawall v1.0")

    log_format = logging.Formatter("[%(asctime) s] %(levelname) s [%(filename) s : %(lineno) d] %(message) s")

    # Create a handler
    c_handler = logging.StreamHandler()   # consloe handler
    f_handler = logging.FileHandler("./imp.log")

    # set format 
    c_handler.setFormatter(log_format)
    f_handler.setFormatter(log_format)

    # link handler to logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    # Set new_logger level to the logger
    logger.setLevel(logging.DEBUG) # <-- THIS!


    # test
    logger.debug('This is a debug message')

    return logger

new_logger = cust_logger()

def detect_de():
    
    session = str(os.environ.get('XDG_CURRENT_DESKTOP'))
    if session.lower().startswith("gnome"):
        de = "gnome"
    elif session.lower().startswith("kde"):
        de = "kde"
    elif session.lower().startswith("xfce"):
        de = "xfce"
    elif session.lower().startswith("mate"):
        de = "mate"
    elif session.lower().startswith("lxde"):
        de = "lxde"
    else:
        de = "unknown"

    return de


def system_details(foldername: str ="mistawall") -> tuple:
    """to get the os name and relevant path"""

    if "ANDROID_ROOT" in os.environ:
        path = f"/sdcard/Download/{foldername}"
        return ("android",path)

    elif system() == "Linux":
        path = os.path.expanduser("~") + f"/Downloads/{foldername}"
        return ("linux",path)

    elif os.path.exists("/private/var/mobile"):
        path = "./{foldername}"
        return ("ios",path)

    elif system() == "Darwin":
        path = os.path.expanduser("~") + f"/Downloads/{foldername}"
        return ("macos",path)

    elif system() == "Windows":
        user = os.getlogin()
        path = f"C:/Users/{user}/Downloads/{foldername}"
        return ("windows",path)

    else:
        path = ""

    return ("unknown","")
    
    
def check_internet(timeout:int) -> bool:
    """to check the internet connectivity"""

    try:
        response = urllib.request.urlopen("https://google.com/",timeout=timeout)
        return True

    except urllib.error.URLError or TimeoutError:
        return False

def get_data_file(folderpath: str) -> dict:

    data_path = folderpath+"/data.dat"

    if os.path.exists(data_path):

        file = open(data_path,"rb")
        data = pickle.load(file)
        file.close()

    else:
        # if no data found ---> same as restarting the program
        data = {"temp": 0, "offline": 0,"downloaded": 0}

    new_logger.debug(f"Data accessed : {data}")

    return data

def update_data_file(data: dict ,folderpath: str) -> None:
    
    data_path = folderpath+"/data.dat"

    with open(data_path,"wb") as file:
        pickle.dump(data,file)

        new_logger.debug(f"data updated: {data}\n")


def first_run(data: dict, folderpath: str) -> None:
    """to initilize the process by creating directories"""

    new_logger.info(f"making directories : {folderpath}")

    if (not os.path.exists(folderpath)):
        os.makedirs(folderpath)

    paths = [ folderpath+"/offline" , folderpath+"/temp" , folderpath+"/data.dat" ]
    # it will create two folders offline,temp and data file

    new_logger.info(f"making directory : {paths[0]}")
    os.mkdir(paths[0])
    new_logger.info(f"making directories : {paths[1]}")
    os.mkdir(paths[1])

    with open(paths[2],"wb") as file:
        pickle.dump(data,file)





def image_path(data: dict,folderpath: str,img_type: str) -> str:
    '''get img path plus update into data.dat'''

    img_no = data[img_type] + 1
    image_path = f"{folderpath}/{img_type}/{img_no}.jpeg"
    new_logger.debug(f"img_path: {image_path}\n")
    data[img_type] = img_no
    update_data_file(data,folderpath)

    return image_path



def image_download(os_name: str,url_list: dict) -> bytes:
    '''tries to download image '''

    
    try:
        if os_name in ["android","ios"]:
            num = random.randint(0, len(url_list["mobile"]) - 1 )
            img_url = url_list["mobile"][num]
        else:
            num = random.randint(0, len(url_list["desktop"]) - 1 )
            img_url = url_list["desktop"][num]
            

        image_data = urllib.request.urlopen(img_url, timeout=120).read()
        new_logger.info("Image downloaded successfully")
        return image_data

    except Exception as e:
        new_logger.info("Image not downloaded")
        new_logger.error(traceback.format_exc())
        new_logger.info(f"error: {e}")

    return b"error"



def update_offline(data : dict ,max_img : int ,folderpath : str ,os_name : str, url_list : dict) -> str:
    """update offline or create images for first time"""

    offline_folder = folderpath+"/offline"
    files_downloaded = data["downloaded"]

    for i in range(max_img-files_downloaded):

        files = len(os.listdir(offline_folder))
        # current no of imaages in folder
        img_path = f"{offline_folder}/{files+1}.jpeg"
        new_logger.info(f"Downloading image no: {files+1}")
        
        value = image_download(os_name , url_list)
        if value != b"error":
            img_data = value
            new_logger.info(f"Downloaded image no: {files+1}")
        else:
            return "error"


        file = open(img_path,"wb")
        file.write(img_data)
        file.close()
        data["downloaded"] = files + 1
        update_data_file(data , folderpath)

    else:
        return "success"

def getWallpaper_windows(folderpath : str) -> bool:
    '''get current wallpaper from windows'''

    import ctypes

    SPI_GETDESKWALLPAPER = 0x0073  # harcoded value to not use win32con library = 115

    ubuf = ctypes.create_unicode_buffer(512)
    ctypes.windll.user32.SystemParametersInfoW(SPI_GETDESKWALLPAPER,len(ubuf),ubuf,0)
    path =  ubuf.value

    new_logger.info(f"original wallpaper path: {path}")
    if (path != None):
        if os.path.isfile(path):
            
            new_logger.info(f"original wallpaper path: {path}")
            shutil.copy(path ,folderpath+"/original.jpeg" )
            new_logger.info(f"original wallpaper copied at : {folderpath+'/original.jpeg'}")
            return True
        else:
            new_logger.info(f"original wallpaper not a file")
            return False
    else:
        new_logger.info(f"original wallpaper not exist")
        return False

def copy_linux_wallpaper(wallpaper_path : str, folderpath : str) -> bool:
    ''' to overcome the issue of file:// or cots '''

    if wallpaper_path == None:
        return False

    if (not os.path.isfile(wallpaper_path)):
        wallpaper_path = wallpaper_path.replace("'","")
        if (not os.path.isfile(wallpaper_path)):
            wallpaper_path = wallpaper_path.replace('"',"")

    if os.path.isfile(wallpaper_path):
            
        new_logger.info(f"original wallpaper path: {wallpaper_path}")
        shutil.copy(wallpaper_path ,folderpath+f"/original.jpeg" )
        new_logger.info(f"original wallpaper copied at : {folderpath+'/original.jpeg'}")
        new_logger.info(f"Wallpaper copied successfully")

        return True
    
    return False

def getWallpaper_linux(folderpath : str) -> bool:
    '''get current wallpaper from linux'''

    import subprocess

    de = detect_de()
    new_logger.info(f"desktop enviornment : {de}")

    if de == "kde":

        try:
            kde_cmd = "kreadconfig5 --group Wallpaper --key Image plasma-org.kde.plasma.desktop"
            result = subprocess.run(kde_cmd,capture_output=True, text = True,check=True)
            wallpaper_path = result.stdout.strip().replace("file://","")

            value = copy_linux_wallpaper(wallpaper_path,folderpath)

            return value

        except subprocess.CalledProcessError:
            new_logger.info("error while copying original wallpaper!")
            new_logger.error(traceback.format_exc())
            return False

    elif de == "gnome":

        try:
            gnome_cmd = f"gsettings get org.gnome.desktop.background picture-uri"
            result = subprocess.run(gnome_cmd,capture_output=True, text = True,check=True)
            wallpaper_path = result.stdout.strip().replace("file://","")

            value = copy_linux_wallpaper(wallpaper_path,folderpath)
            
            return value

        except subprocess.CalledProcessError:
            new_logger.info("error while copying original wallpaper!")
            new_logger.error(traceback.format_exc())
            return False

    elif de == "xfce":

        try:
            xfce_cmd = f''' i = 0
            xfconf-query --channel xfce4-desktop --list | grep last-image | while read path;
            do
                img_path=$(xfconf-query --channel xfce4-desktop --property $path --get)
                cp "$img_path" "{folderpath}/original_{{i}}.jpeg"
                ((i++))
            done''' 

            subprocess.run(xfce_cmd, check=True)
            new_logger.info(f"Wallpaper copied successfully")
            return True

        except subprocess.CalledProcessError:
            new_logger.info("error while copying wallpaper wallpaper!")
            new_logger.error(traceback.format_exc())
            return False

    elif de == "lxde":

        try:
            lxde_cmd = f'pcmanfm --get-wallpaper'
            result = subprocess.run(lxde_cmd, check=True,capture_output=True)
            wallpaper_path = result.stdout.strip().replace("file://","")

            value = copy_linux_wallpaper(wallpaper_path,folderpath)

            return value

        except subprocess.CalledProcessError:
            new_logger.info("error while coping wallpaper!")
            new_logger.error(traceback.format_exc())
            return False

    elif de == "mate":

        try:
            mate_cmd = f"gsettings get org.gnome.desktop.background picture-filename"
            result = subprocess.run(mate_cmd, check = True,text = True,capture_output = True)
            wallpaper_path = result.stdout.strip().replace("file://","")

            value = copy_linux_wallpaper(wallpaper_path,folderpath)

            return value
            
        except subprocess.CalledProcessError:
            new_logger.info("error while coping wallpaper!")
            new_logger.error(traceback.format_exc())
            return False

    else:
        
        new_logger.info("error while copying wallpaper!")
        return False

def getWallpaper_macos(folderpath: str) -> bool:
    '''set wallpaper to macos'''

    import subprocess
    script = f'''
        tell application "Finder"
            to get POSIX path of (get desktop picture as alias);
        end tell
    '''
    try:
        result = subprocess.run(["osascript", "-e", script], text = True, check=True , capture_output= True) 
        wallpaper_path = result.stdout.strip().replace("file://","")

        value = copy_linux_wallpaper(wallpaper_path,folderpath)

        return value
        
    except subprocess.CalledProcessError:
        new_logger.info("error while copying wallpaper!")
        new_logger.error(traceback.format_exc())
        return False

def setWallpaper_windows(img_path: str) -> bool:
    '''set wallpaper to windows'''

    # importing windows needed library
    import ctypes
    from platform import architecture

    '''
    SPI_SETDESKWALLPAPER = 0x0014  # SPI_SETDESKWALLPAPER = 20 actullay comes from win32con
    SPIF_UPDATEINIFILE = 1 # SPIF_UPDATEINIFILE = 1 from 
    # win32con its not builtin library thats why using direct values
    SPIF_SENDCHANGE = 2 # comes from win32con or u can say windows api in c

    # win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE  
    # combining these two with bitwise or is = 3 
    # SPIF_UPDATEINIFILE is used for persist the change after reboot
    '''

    arch = architecture()[0]

    new_logger.info(f"arch: {arch}")

    # the above code dosen't work for me :(
    sys_parameter = ctypes.windll.user32.SystemParametersInfoW
    set_wall = sys_parameter(20,0,img_path,3)

    if set_wall:
        print("Wallpaper appplied successfully")
        new_logger.info(f"Wallpaper appplied successfully")
        return True
    else:
        new_logger.debug(f"error: {ctypes.WinError()}")
        new_logger.info("error while setting wallpaper!")
        return False

def setWallpaper_linux(img_path: str) -> bool:
    '''set wallpaper to linux'''

    import subprocess

    de = detect_de()
    new_logger.info(f"desktop enviornment : {de}")

    if de == "kde":

        try:
            kde_cmd = '''qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript \'
    var allDesktops = desktops();
    for (i=0;i<allDesktops.length;i++) {{{{
        d = allDesktops[i];
        d.wallpaperPlugin = \"org.kde.image\";
        d.currentConfigGroup = Array(\"Wallpaper\",\"org.kde.image\","General");
        d.writeConfig(\"Image",\"\'file://{path}\'\")
    }}}}\' '''.format(path=img_path)

            subprocess.run(kde_cmd,check=True)
            new_logger.info(f"Wallpaper appplied successfully")
            return True

        except subprocess.CalledProcessError:
            new_logger.info("error while setting wallpaper!")
            new_logger.error(traceback.format_exc())
            return False

    elif de == "gnome":

        try:
            gnome_cmd = f"gsettings set org.gnome.desktop.background picture-uri file://{img_path}"
            subprocess.run(gnome_cmd, check=True)
            new_logger.info(f"Wallpaper appplied successfully")
            return True

        except subprocess.CalledProcessError:
            new_logger.info("error while setting wallpaper!")
            new_logger.error(traceback.format_exc())
            return False

    elif de == "xfce":

        try:
            xfce_cmd = f'''xfconf-query --channel xfce4-desktop --list | grep last-image | while read path;
            do
                xfconf-query --channel xfce4-desktop --property $path --set \"{img_path}\"
            done'''

            subprocess.run(xfce_cmd, check=True)
            new_logger.info(f"Wallpaper appplied successfully")
            return True

        except subprocess.CalledProcessError:
            new_logger.info("error while setting wallpaper!")
            new_logger.error(traceback.format_exc())
            return False

    elif de == "lxde":

        try:
            lxde_cmd = f'pcmanfm --set-wallpaper="{img_path}"'
            subprocess.run(lxde_cmd, check=True)
            new_logger.info(f"Wallpaper appplied successfully")
            return True

        except subprocess.CalledProcessError:
            new_logger.info("error while setting wallpaper!")
            new_logger.error(traceback.format_exc())
            return False

    elif de == "mate":

        try:
            # mate_cmd = f"dconf write /org/mate/desktop/background/picture-filename \"\'{img_path}\'\""
            mate_cmd = f"gsettings set org.gnome.desktop.background picture-filename \"\'{img_path}\'\""
            subprocess.run(mate_cmd, check=True)
            new_logger.info(f"Wallpaper appplied successfully")
            return True
            
        except subprocess.CalledProcessError:
            new_logger.info("error while setting wallpaper!")
            new_logger.error(traceback.format_exc())
            return False

    else:
        
        new_logger.info("error while setting wallpaper!")
        return False

def setWallpaper_macos(img_path: str) -> bool:
    '''set wallpaper to macos'''

    import subprocess
    script = f'''
        tell application "Finder"
            set desktop picture to POSIX file "{image_path}";
        end tell
    '''
    try:
        subprocess.run(["osascript", "-e", script], check=True)
        new_logger.info(f"Wallpaper appplied successfully")
        return True
    except subprocess.CalledProcessError:
        new_logger.info("error while setting wallpaper!")
        new_logger.error(traceback.format_exc())
        return False

def setWallpaper_android(img_path: str) -> bool:
    '''set wallpaper to android using termux'''

    import subprocess
    
    termux_path = os.path.exists('/data/data/com.termux/')
    termux_api_path = os.path.exists('/data/data/com.termux.api/')
    termux_api_pkg_path = os.path.exists('/data/data/com.termux/files/usr/bin/termux-wallpaper')
    
    while True:

        if ("TERMUX_VERSION" in os.environ) and (termux_api_pkg_path):

            new_logger.info("Termux is already installed :) ")
            new_logger.info("and Termux api is also installed :) ")
            if termux_api_path:
                new_logger.info("and Termux api app is also installed :) ")
                try:
                    command = ["termux-wallpaper", "-f", img_path]
                    subprocess.run(command,check=True)
                    new_logger.info(f"Wallpaper appplied successfully")
                    return True
                except:
                    new_logger.info(f"error while setting wallpaper !")
                    new_logger.error(traceback.format_exc())
                    return False

            else:
                new_logger.info("please install termux-api app to work :( ")
                return False

        elif (not (termux_api_pkg_path)) and ("TERMUX_VERSION" in os.environ) :
            try:
                new_logger.info(f"termux-api package not installed")
                ans = input("do you want to install termux-api(y/n): ")

                if (ans.lower() == "y"):

                    new_logger.info(f"termux api installing")
                    command = ["pkg","install","termux-api"]
                    subprocess.run(command,check=True)
                    new_logger.info(f"termux api installed successfully")
                    return False

                
            except:
                new_logger.info(f"error occured !")
                new_logger.error(traceback.format_exc())
                return False
        
        else:
            new_logger.info(f"Install Termux and termux-api (app & pkg both) to work!")
            return False
            
        
def getWallpaper(os_name: str , folderpath : str) -> bool:
    '''get wallpaper from different os'''        

    if os_name == "windows":

        path = getWallpaper_windows(folderpath)
        return path

    elif os_name == "linux":

        path = getWallpaper_linux(folderpath)
        return path
        
    elif os_name == "macos":

        path = getWallpaper_macos(folderpath)
        return path

    elif os_name == "android":

        new_logger.info("getting wallpaper on android is not possible right now")
        return False

    elif os_name == "ios":
        new_logger.info("os not supported!")
        return False
    else:
        new_logger.info("os not supported!")
        return False

def setWallpaper(img_path: str,os_name: str) -> bool:
    '''set wallpaper to different os'''

    new_logger.info(f"img path: {img_path}")

    if os_name == "windows":

        value = setWallpaper_windows(img_path)
        return value

    elif os_name == "linux":

        value = setWallpaper_linux(img_path)
        return value
        
    elif os_name == "macos":

        value = setWallpaper_macos(img_path)
        return value

    elif os_name == "android":

        value = setWallpaper_android(img_path)
        return value

    elif os_name == "ios":
        new_logger.info("os not supported!")
        return False
    else:
        new_logger.info("os not supported!")
        return False

def log_copy(src : str , dst : str) -> bool:
    '''copy log file'''

    try:
        file1 = open(src, "r")
        file2 = open(dst, "a")
        content = file1.read()
        file2.write(content)
        file1.close()
        file2.close()
        return True

    except OSError:
        return False

def parser():
    '''comand line utility arguments parser'''

    parser = argparse.ArgumentParser(description="mistawall 1.0 command line utility to set random wallpaper")
    parser.add_argument('-c','--config',type= str, help="path to your own config.json file",default=None)
    parser.add_argument('-n','--no-store',action="store_true",help= "don't store any file (no folder created)",default=None)
    parser.add_argument('-max','--max-cache',type= int,help= "how many max images is to be cached for offline use",default=None)
    parser.add_argument('-url','--image-url',type= str,help="add your own random image url",default=None)
    parser.add_argument('-d','--delete',action="store_true" ,help="deletes the software directory",default=None)
    parser.add_argument('-o','--offline',action="store_true",help= "cache the random image for offline use",default=None)
    parser.add_argument('-t','--timeout',type= int,help= "how much time in seconds for cheking internet",default=None)
    parser.add_argument('-f','--foldername',type= str,help= "foldername for program directory (where offline images stored)",default=None)
    parser.add_argument('-p','--path',type= str,help= "path for program directory (where offline images stored)  # preffered over foldername",default=None)
    parser.add_argument('-g','--get-wallpaper',action="store_true",help= "copy current wallpaper to current dir",default=None)

    return parser.parse_args()
    
def config_path(parser_arguments) -> str:
    '''load user config file if any'''

    config_path = parser_arguments.config
    config_not_none = (config_path != None)
    if (config_not_none):
        config_exists = os.path.isfile(config_path)
    else:
        config_exists = False
    
    # --config is preffered over config file
    if (config_exists):
        return config_path
        
    else:
        cwd = os.getcwd() # current directory in which program is running
        default_paths = (cwd+"/mista.json",cwd+"/mista_config.json",cwd+"/config.json",cwd+"/conf.json",cwd+"/mconfig.json",cwd+"/mconf.json")

        for config_file in default_paths:
            if os.path.isfile(config_file):
                config_file = config_file.replace("\\","/")
                new_logger.info(f"config path : {config_file}")
                return config_file

def config_laoder(filepath : str , urlList : dict) -> dict:
    '''load dictionary data from config file'''

    # If some value is not given by user
    default_values = {"no-store" : False, "max-cache" : 5, "image-url" : urlList, "delete" : False,"offline" : False, "timeout" : 20 , "foldername" : "mistawall", "path" : system_details()[1] , "get-wallpaper" : False}

    if filepath == None:
        new_logger.info(f"config filepath not found !")
        return default_values

    new_logger.info("config file found!")
    config_data = {}
    file = open(filepath)
    data = json.load(file)

    for key in default_values:
        if (data.get(key) != None):
            config_data[key] = data[key]
        else:
            config_data[key] = default_values[key]

    file.close()
    return config_data

def args_loader(parser_arguments , urlList : dict) -> dict:
    '''load arguments into dictionatry file'''

    # to match value with args
    configs = {"config" : "config" ,"no-store" : "no_store", "max-cache" : "max_cache", "image-url" : "image_url", "delete" : "delete","offline" : "offline", "timeout" : "timeout" , "foldername" : "foldername", "path" : "path" ,"get-wallpaper" : "get_wallpaper"}

    # If some value is not given by user
    default_values = {"config" : None, "no-store" : False, "max-cache" : 5, "image-url" : urlList, "delete" : False,"offline" : False, "timeout" : 20 , "foldername" : "mistawall","path" : system_details()[1] , "get-wallpaper" : False}

    args_data = {}

    for key in default_values:
        value = configs[key]
        arg_value = getattr(parser_arguments,value)  # calling args."arg_name"
        if (arg_value != None):
            args_data[key] = arg_value
        else:
            args_data[key] = default_values[key]

    return args_data

def main_loader(config_data : dict , args_data : dict, urlList : dict) -> dict:
    '''arguments preffered over config file'''

    # If some value is not given by user
    default_values = {"config" : None, "no-store" : False, "max-cache" : 5, "image-url" : urlList, "delete" : False,"offline" : False, "timeout" : 20 , "foldername" : "mistawall" ,"path" : system_details()[1] , "get-wallpaper" : False}

    
    loader_data = {}

    for key in default_values:
        if (args_data[key] != default_values[key]):
            loader_data[key] = args_data[key]
        elif (config_data.get(key) != default_values[key]):
            loader_data[key] = config_data.get(key)
        else:
            loader_data[key] = default_values[key]

    return loader_data

def work_actully_exist(workpath : str) -> bool:
    '''check all directories inside workpath'''

    dirs = [workpath,f"{workpath}/offline",f"{workpath}/temp",f"{workpath}/data.dat"]
    for dir in dirs:
        if not (os.path.exists(dir) or os.path.isfile(dir)):
            return False

    return True

def img_url_list(main_data : dict ,urls : dict) -> dict:
    '''create a dictionary format of urls'''

    if (main_data["image-url"]) and ( isinstance( main_data["image-url"] , str) ) :
        # user specified his/her own url for random image
        new_logger.info("# user specified his/her own url for random image")
        main_data["image-url"] = {"mobile": [ main_data["image-url"] ] ,"desktop": [ main_data["image-url"] ] }
    elif (main_data["image-url"]) and ( isinstance( main_data["image-url"] , list) ) :
        # user specified his/her own url for random image
        new_logger.info("# user specified multiples urls for random image")
        main_data["image-url"] = {"mobile": main_data["image-url"] ,"desktop": main_data["image-url"] }
    
    
    # elif (main_data["image-url"]) and ( isinstance( main_data["image-url"] , dict) ) :
    #     # user specified his/her own url for random image
    #     new_logger.info("# user specified multiples urls in dictionry form for random image")
    #     pass # same value is returnd as it is dictionary form
    

    else:
        main_data["image-url"] = urls
    
    return main_data["image-url"]

def no_store(system_name : str ,main_data : dict ,urls : dict) :
    '''this should be the code if no extra features included'''

    main_data["image-url"] = img_url_list(main_data,urls)
    
    work_path = os.getcwd().replace("\\","/")
    if not os.path.exists(f"{work_path}/original.jpeg"):

        value = getWallpaper(system_name,work_path)
        if (value == False) or (value == "error"):
                new_logger.info("current Wallpaper not copied!")
                ans = input("current wallpaper not copied do still want to apply random image : (y/n) ")
                if (ans.lower() == "y") or (ans.lower() == "yes"):
                    pass
                else:
                    return
        else:
        
            new_logger.info("original wallpaper already copied :)")

    new_logger.info(f"Downloading image...")
    img_data = image_download(system_name,main_data["image-url"])
    if img_data != b"error":
        new_logger.info(f"Downloaded image ")
    else:
        new_logger.info("error in downloading image!")
        return "error"

    path = f"{work_path}/temp.jpeg"
    file = open(path,"wb")
    file.write(img_data)
    file.close()
    value = setWallpaper(path,system_name)
    if value:
        new_logger.info(f"Wallpaper appplied successfully")
        return 
    else:
        new_logger.error(f"error while applying image ! ")
        return "error"


def main():

         # url for random image
    urls = {"mobile": ["https://picsum.photos/1440/3168"], "desktop" : ["https://picsum.photos/3840/2160"]}

    args = parser()
    config_file = config_path(args)
    config_data = config_laoder(filepath = config_file, urlList = urls)
    args_data = args_loader(parser_arguments = args,urlList = urls)
    main_data = main_loader(config_data,args_data,urls)

    system_name , work_path = system_details(foldername=main_data["foldername"])  # like windows linux etc
       # where program store important data


    # log file for checking what and where     
    # the wrong thing happens

    if main_data["get-wallpaper"]:
        new_logger.info("# user specified only to get wallpaper")
        value = getWallpaper(os_name = system_name, folderpath = os.getcwd())
        if (value != False) or (value != "error"):
            new_logger.info("current wallpaper copied successfully ")
        else:
            new_logger.info("current Wallpaper not copied!")
        return value

    if main_data["no-store"]:
        new_logger.info("# user specified no features to use")
        value = no_store(system_name , main_data , urls)
        return value

    if (main_data["path"] != work_path) and (main_data["path"] != system_details()[1]):
        new_logger.info("# user specified his/her own path")
        new_logger.info("# path preffered over foldername")

        if main_data["path"] == ".":
            #as image setting need full path not relative
            main_data["path"] = os.getcwd()

        work_path = main_data["path"]        

    # max_image = args.max-cache  #how much to store image for offline use


    # timeout = args.timeout   # for checking user is online or not timeout for website to load
    

   
    if (main_data["delete"]) and (os.path.exists(work_path)):
        #user want to delete directory and program created directoroy exists as well
        shutil.rmtree(work_path)
        new_logger.info(f"directory deleted \n")

    main_data["image-url"] = img_url_list(main_data,urls)
    
    


    while True:

        online = check_internet(main_data["timeout"])
        work_path_exist = work_actully_exist(workpath = work_path)

        if (not work_path_exist) and (not online):

            # for first time runnning and have no internet

            new_logger.info(f"No internet and path doesn't exist\n")

            print("please connect to the internet for first time")
            input("\nenter any key to exit: ")
            break

        elif (not work_path_exist):

            # for first time runnning but have internet connection
            # so now we can proceed to create folder

            new_logger.info(f"have internet but path doesn't exist\n")

            data = get_data_file(folderpath = work_path)
            first_run(data = data , folderpath = work_path)

            # good place to store original wallpaper 
            value = getWallpaper(os_name = system_name, folderpath = work_path)
            if (value == False) or (value == "error"):
                new_logger.info("current Wallpaper not copied!")
                ans = input("current wallpaper not copied do still want to apply random image : (y/n) ")
                if (ans.lower() == "y") or (ans.lower() == "yes"):
                    pass
                else:
                    shutil.rmtree(work_path)
                    break

            if (main_data["offline"]):
                #if user speciefied offline it will store image cache
                
                new_logger.info(f" installing offlline as you specified --offline\n")
                value = update_offline(data = data , max_img = main_data["max-cache"] ,folderpath = work_path,os_name = system_name, url_list= main_data["image-url"])
                if value == "error":
                    break

            continue
                

        elif (not online) and (main_data["offline"]):

            # if no internet is there it will apply offline images
            # or check if all are already applied then update

            new_logger.info(f"have not internet but path exist and also specified --offline\n")
            data = get_data_file(folderpath = work_path)
            update_exist = os.path.exists(work_path+"/update.txt")
            all_img_used = (data["offline"] >= data["downloaded"])
            new_logger.info(f"update_exist : {update_exist}\n")

            if (not all_img_used) and (not update_exist):

                new_logger.info(f"image can be set no update is there\n")
                img_path = image_path(data = data, folderpath = work_path,img_type = "offline")
                
                
            elif update_exist:

                new_logger.info(f"Please connect to internet to update offlines\n")
                input("\nenter any key to exit: ")
                break

            else:

                new_logger.info(f"settting mode to update offline\n")
                data["offline"] = 0
                data["downloaded"] = 0
                shutil.rmtree(work_path+"/offline")
                os.mkdir(work_path+"/offline")
                update_data_file(data = data , folderpath = work_path)
                
                with open(work_path+"/update.txt","w") as file:
                    file.write("update")
                continue
        
        elif (not online):

            new_logger.info(f"No internet and not specified offline\n")

            print("please connect to the internet or use --offline")

            break

        else: 

            # it will download image from internet

            data = get_data_file(folderpath= work_path)

            new_logger.info(f"Everything is in favour\n")
            update_exist = os.path.exists(work_path+"/update.txt")
            new_logger.info(f"update exist : {update_exist}")

            if (update_exist) and (main_data["offline"]):
                # update_offline()
                new_logger.info(f"Updating the offline folder\n")

                value = update_offline(data = data , max_img = main_data["max-cache"] ,folderpath = work_path,os_name = system_name, url_list= main_data["image-url"])
                
                if value == "error":
                    break
                os.remove(work_path+"/update.txt")

            else:
                new_logger.info(f"not updating as you not specified --offline\n")
                
                
            
        
            #write_image()
            img_no = data["temp"] + 1

            new_logger.info(f"Downloading image no: {img_no}")
            value = image_download(os_name = system_name, url_list = main_data["image-url"])
            if value != "error":
                new_logger.info(f"downloaded image no: {img_no}")
                img_data = value
            else:
                break
            
            img_path = image_path(data = data, folderpath = work_path,img_type = "temp")
            file = open(img_path,"wb")
            file.write(img_data)
            file.close()
            new_logger.debug(f"temp img saved success\n")

        # after above code we will get the image path 
        # then we can set it as wallpaper
        if os.path.isfile(img_path):
            value = setWallpaper(img_path,system_name)
            if value:
                new_logger.info(f"Wallpaper appplied successfully")
                break
            else:
                new_logger.error(f"error while applying image ! ")

        else:
            new_logger.error(f"image dosen't exist :( ")
        

 
if __name__ == "__main__":

         # url for random image
    urls = {"mobile": ["https://picsum.photos/1440/3168"], "desktop" : ["https://picsum.photos/3840/2160"]}

    args = parser()
    config_file = config_path(args)
    config_data = config_laoder(filepath = config_file, urlList = urls)
    args_data = args_loader(parser_arguments = args,urlList = urls)
    main_data = main_loader(config_data,args_data,urls)

    system_name , work_path = system_details(foldername=main_data["foldername"])  # like windows linux etc
       # where program store important data

    # system_name , work_path = system_details()
    system_supported = ["windows","linux","macos","android"]



    try:

        if system_name in system_supported:
            main()
        else:
            print("Your system is not supported !")

    except Exception as e:

        new_logger.info(f"no there is some error check it\n")
        new_logger.error(traceback.format_exc())
        new_logger.debug(f"error: \n{e}\n")

        print("something went wrong!")
        print("let me check send the log file from:")
        print(f"\n {os.getcwd()+'/imp.log'}")
    
        

    finally:

        #copying the log file at the end of program 

        value = log_copy("./imp.log",work_path+"/imp.log")
        if value:
            new_logger.info("log copy success")

        input("enter any key to exit: ")


# finally i am able to complete this project 
# i know its just a simple project but
# takes much more time than what i expected (took 20 days)
# but also a great journey (i learned many things from this project)
# happines :) first time i wrote 900 lines of code