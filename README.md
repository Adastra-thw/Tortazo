# Tortazo

Stem is a powerful library written in Python to perform various operations against TOR Clients and Directory Authorities. The information gathered using Stem could be very useful to an attacker to get information about the relays available in the TOR network

Tortazo is an open source Python Script to gather information about ExitNodes in the TOR Network, perform bruteforce attacks against services like FTP or SSH and create a Botnet with the compromised ExitNodes over SSH.

* **Use Shodan** - Using a valid Shodan Key, you can gather information about an ExitNode stored in the Shodan Database.
* **Use Nmap** - Using python-nmap, Tortazo is able to perform NMap scans against a list of ExitNodes

## Dependencies
To use the script, you'll need the following dependencies:

* Paramiko
* Python-Nmap
* Python-shodan
* Stem
* Plumbum
* zlib

   

## Examples
*All examples assume you have already setup the dependencies!*

##Gather Information

* **Show the available Options
```
python Tortazo.py -h
```

* **Connect to the Directory Authorities using the mirrors servers (-d)
    Enable the "verbose" mode (-v)
    Scan ExitNodes which operative system is Windows (-m windows)
```
python Tortazo.py -d -v -m windows
```

* **Connect to the Directory Authorities directly
    Enable the "verbose" mode (-v)
    Scan ExitNodes which operative system is Linux (-m linux)
```
python Tortazo.py -d -v -m linux
