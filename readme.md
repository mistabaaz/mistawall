A command line utility for applying random wallpaper to your os

# Requirements
Desktop : Nothing just run `mistawall.exe` (Windows)

Linux *[if you are using linux then you already know how to run binaries 😎]*

Android : hmm, this requires a bit more work 

- You should have Termux and Termux:API installed 
- also the termux-api package in termux 
- by running following command in terminal (termux) `pkg install termux-api`

<details>
<summary> Click here for detailed android guide</summary> <br>

1. Install Termux:API app from F-Droid (link below)

```https://f-droid.org/repo/com.termux.api_51.apk```

2. Install Termux app from F-Droid (link below)

```https://f-droid.org/repo/com.termux_118.apk```

3. Now Open `Termux` and run following commands

```pkg update && pkg upgrade```

4. install wget to download mistawall script

```pkg install wget```

5. Now run below command to download mistawall (in termux)

```wget "https://github.com/mistabaaz/mistawall/raw/master/android.sh" && bash android.sh```

6. Now you can run mistawall on android

```./mistawall```

or with some arguments

```./mistawall --offline --foldername "hello" ```

</details>

# Installation

## From binaries

[1]: https://github.com/mistabaaz/mistawall/releases/download/1.0/mistawall_windows_x86.exe
[2]: https://github.com/mistabaaz/mistawall/releases/download/1.0/mistawall_linux_arm64.bin
[3]: https://github.com/mistabaaz/mistawall/archive/refs/tags/1.0.zip

| Opreating System       | Download Link         | Tested         | 
| :----------------------| :-------------------: | :------------: |
| windows 32bit (x86)    | [Download][1]         | ✅ bY mista   |
| windows 64bit (x86_64) | [Run from Source][3]  | ❌            |
| linux 32bit (x86)      | [Run from Source][3]  | ❌            |
| linux 64bit (x86_64)   | [Run from Source][3]  | ❔             |
| android 32bit (arm)    | [Run from Source][3]  | ❌            |
| android 64bit (arm64)  | [Download][2]         | ✅ bY mista   |
| macOS                  | [Run from Source][3]  | ❌            |

### Linux Testing
| Desktop Enviornment    | Tested           | architecture |
| :----------------------| :--------------: | :----------: |
| kde                    |  ❌              | ❌          |
| gnome                  |  ❌              | ❌          |
| xfce                   |  ❌              | ❌          |
| mate                   |  ❌              | ❌          |
| lxde                   |  ✅ by nexus     | x86_64      |
| other de               |  Not implemented | ❌          |
        


## From Source

1. Make sure you have python installed
2. now just run `mistawall.py` and all set!

# Demo
<details>
<summary> Windows </summary> 

![windows](https://github.com/mistabaaz/mistawall/blob/master/demo/windows.gif)

</details>

<details>
<summary> Android </summary> 

![android](https://github.com/mistabaaz/mistawall/blob/master/demo/android.gif)

</details>

# Features

- NO external library used so can be directly without any extra setup
- Cross Platform (Windows, lInux , macOS, android)
- Easily and heavily customizable
- No user intreaction required

## Customizability
 
### from config file

- you can create your own `config.json` file 
- program will auto detect config file if present in same directory of program
- else you can also specify the path by --config flag

#### structure of `config.json` file :

```json
{
    "no-store" : false,
    "max-cache" : 5,
    "image-url" : "wallpaper link",
    "delete" : false,
    "offline" : false,
    "timeout" : 20,
    "foldername" : "mistawall",
    "path" : null,
    "get-wallpaper" : false
}
```

#### Explaination of each flag

**no-store** {default_value = false} : does not store any data on downloads folder *[ just creates `temp.jpeg` and `original.jpeg` in current directory ]*, usually program store its content in downloads folder.

**max-cache** {default_value = 5}: program stores wallpapers for  offline use *[only if user specified --offline flag or "offline" : true" in config file]*

**image-url** : user can specify his/her own url for wallpaper *[also user can pass list of urls to download random wallpaper from them]*

```json
{
    "image-url" : ["url1", "url2", "url3"]
}
```

**delete** {default_value = false} : this deletes the directory of program *[you can delete it manually this is just in case if you don't know where files are stored]*

**offline** {default_value = false} : if you want to store some images for offline use *[when there is no internet this can help]*

**timeout** {default_value = 20} : this is used for detecting your interent if your internet is slow and not detected by program increase the time *[maybe 120 seconds]*

**foldername** {default_value = "mistawall"} : if you want to use your own folder name for storing program contents *[usually program create mistawall directory in downloads folder]*

**path** : specify the full path where you wan to store all program data 
```json
{
    "path" : "path/to/your/folder/"
}
```

**get-wallpaper** {default_value = false} : make this true if you only want to get current wallpaper, this will copy current wallpaper to current directory namely `original.jpeg` *[usually program only get wallpaper for first time]*

## Notes
- if you want to use default value of any flag you can use `null` in `config.json` file or just don't use that flag
```json
{
    "image-url" : null,
    "offline" : null
}
```
- you can also specify these flags via passing as arguments 
```
mistawall.exe --no-store --image-url "url" 
```

- just remeber **no-store, delete, offline, get-wallpaper** *[in these case you just have to use that flag not specify its value it will automatically set to true]*
```
mistawall.exe --no-store 
```
is same as writing true in `config.json` file
```json
{
    "no-store" : true
}
```

- default path of storing data is : "c:/users/"your_user_name"/downloads/mistawall/"  *[check your downloads folder]*
- in android this looks like : "/sdcard/downloads/mistawall/"

# Limitations

Nothing is prefect :) this program also have some limitations

- iOS not supported *[ reason : i don't know how the ios filesystem works bec i don't have ios :( and also i don't think this is possible unless you make a complete ios application and i don't want to dig into that right now :( ]*
- Android program does not work without having termux and its api *[no workaround till now as accessing android apis requires a android app and i could not make a standalone app right now as i don't know android dev, will learn it soon :) ]*
- Also i don't think making an android/ios app is a good idea for a just random wallpaper setter it is good if only used as CLI 
- On Linux this uses some system commands that may not be availible to all users and also i could not able to add all desktop enviornment support till now *[it will take time]*
- cannot get current wallpaper on android *[as termux-api only supports to set wallpaper]*

**Only works better in windows (now i think why many people use windows )**

# TODO

<details>
<summary> Code Refactoring </summary>

    [] by using classes instead of functions
    [] adding comments for good readability

</details>

### Features Implementation

[x] get current wallpaper  <br>
[] colored logging <br>
[] retries for downloading an image <br>
[] concurrent downloading for offline images <br>
[] adding support for other linux de <br>


# Credits

- Lorem Picsum : for random wallpaper api

