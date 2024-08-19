#!/bin/bash


arch=$(uname -m)

if [ "$arch" == "aarch64" ]
then 
    arch="arm64"
elif [ "$arch" == "aarch32" ]
then
    arch="arm"
fi


declare -a binary_availible_platforms=(
    [0]="arm64"
)

binary_found="false"
download_link="https://github.com/mistabaaz/mistawall/releases/download/1.0/mistawall_linux_$arch.bin"
src_link="https://github.com/mistabaaz/mistawall/raw/master/mistawall.py"

for i in "${binary_availible_platforms[@]}"
do
    if [ "$arch" ==  "$i" ]
    then
        binary_found="true"
    fi
done

if [ "$binary_found" == "true" ]
then
    wget $download_link
    mv "mistawall_linux_$arch.bin" "mistawall"
    chmod +x "mistawall"
    echo "Now you can run mistawall by ./mistawall"
else
    wget $src_link
    output="$(dpkg -s python | grep Status)"
    if [ "$output" == "Status: install ok installed" ]
    then
        echo "Python is already installed :)"
    else
        read -p " Do you want to install python(y/n): " choice
        if [ "$choice" == "y" ] 
        then 
            pkg install python
        else
            echo "install it yourself it is neccessary to run script"
            echo "as binary is not avalible for your achitecture"
        fi
    fi
    echo "Now you can run mistawall by following command:"
    echo "python mistawall.py"
fi
    

    


    


