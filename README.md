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
The examples below, will generate a file named "nmapScan.txt" with the nmap scan results for every single Exit Node in the Directory Authorities or in the local TOR Client storage. (Depending on the options used).
I put various combinations to explain how to use the script and the effect of use some options.
On other hand, is much, much faster to use the local descriptors than to connect with the directory authorities (directly or using mirrors, both connection types are very slow sometimes) also depending on the number of users connected, sometimes the servers are busy and the connections with the directory authorities will fail or will be unstable. Anyways, you can use any method to gather information, but the fact is that the directory authorities always have a lot of information about new relays available and the local descriptors have a short set of exit nodes. So... choose your weapon!

*KEEP IN MIND:*
- In the new versions of the TOR Client, by default the microdescriptors will be dowloaded to compose the circuits. This is good because the circuit construction is much faster, but the information about the relays is very limited. So, if you plan to gather information using the TOR Client, you need to set the "UseMicrodescriptors" option to "0" in your torrc file.
- If you want to use the TOR Client to gather information, you need to open the Control Port to use the Stem Controller (and set a password for security issues) to connect with the local instance and get the server descriptors. Please, check your torrc file.
- The connections with the Directory Authorities could be slow and sometimes unstable.
- You can use all the features included in Nmap (including NSE Scripts) using the option "-a/--scan-arguments"
- If you want to use Shodan, you'll need a valid developer key. That value should be writen into a file in a single line and use the options "--use-shodan" and "--shodan-key"
- The bruteforce mode needs a dictionary to perform the attack against the open ports

*Show the available Options*
```
python Tortazo.py -h
```

*Connect to the Directory Authorities using the mirrors servers (-d)
    Enable the "verbose" mode (-v)
    Scan ExitNodes which operative system is Windows (-m windows)*
```
Short opts:
python Tortazo.py -d -v -m windows

Long opts:
python Tortazo.py --use-mirrors --verbose --mode windows
```

*Connect to the Directory Authorities directly
    Enable the "verbose" mode (-v)
    Scan ExitNodes which operative system is Linux (-m linux)*
```
Short opts:
python Tortazo.py -d -v -m linux

Long opts:
python Tortazo.py --use-mirrors --verbose --mode linux
```

*Connect to the Directory Authorities directly
    Enable the "verbose" mode (-v)
    Scan ExitNodes which operative system is Linux (-m linux)*
```
Short opts:
python Tortazo.py -v -m linux

Long opts:
python Tortazo.py --verbose --mode windows
```

*Connect to the Directory Authorities directly
    Enable the "verbose" mode (-v)
    Scan ExitNodes which operative system is Linux (-m linux)
    Just recover the first 30 nodes from the list of exit nodes found (this value by default is very short: 10)*
```
Short opts:
python Tortazo.py -n 30 -v -m linux

Long opts:
python Tortazo.py --servers-to-attack 30 --verbose --mode linux
```

*Connect to the Directory Authorities directly
    Enable the "verbose" mode (-v)
    Scan ExitNodes which operative system is Linux (-m linux)
    Just recover the first 30 nodes from the list of exit nodes found (this value by default is very short: 10)
    Create 10 threads to process the list of exit nodes which match with the criteria specified*
```
Short opts:
python Tortazo.py -t 10 -n 30 -v -m linux

Long opts:
python Tortazo.py --threads 10 --servers-to-attack 30 --verbose --mode linux
```

*Connect to the Directory Authorities directly
    Enable the "verbose" mode (-v)
    Scan ExitNodes which operative system is Linux (-m linux)
    Just recover the first 30 nodes from the list of exit nodes found (this value by default is very short: 10)
    Create 10 threads to process the list of exit nodes which match with the criteria specified
    Perform the Nmap scan with the specified options "-sSV -A -n"*
```
Short opts:
python Tortazo.py -t 10 -n 30 -v -m linux -a "-sSV -A -n"

Long opts:
python Tortazo.py --threads 10 --servers-to-attack 30 --verbose --mode linux --scan-arguments "-sSV -A -n"
```


*Connect to the Local instance of TOR and use the ExitNodes stored in the local descriptors.
    Enable the "verbose" mode (-v)
    Scan ExitNodes which operative system is Linux (-m linux)*

```
Short opts:
python Tortazo.py -v -m linux -c

Long opts:
python Tortazo.py --verbose --mode linux --use-circuit-nodes
```

*Connect to the Directory Authorities directly
    Enable the "verbose" mode (-v)
    Scan ExitNodes which operative system is Linux (-m linux)
    Just recover the first 30 nodes from the list of exit nodes found (this value by default is very short: 10)
    Create 10 threads to process the list of exit nodes which match with the criteria specified
    Perform the Nmap scan with the specified options "-sSV -A -n"
    Filter by FingerPrint*
```
Short opts:
python Tortazo.py -t 10 -n 30 -v -m linux -a "-sSV -A -n" -e FergieRossendorf3

Long opts:
python Tortazo.py --threads 10 --servers-to-attack 30 --verbose --mode linux --scan-arguments "-sSV -A -n" --exit-node-fingerprint FergieRossendorf3
```