.. _gathering-information-label:

******************
Gather Information mode.
******************

=================
Gather information about exit relays in TOR
=================
This is the simplest mode of execution in Tortazo. In this mode, Tortazo always performs an Nmap scan and the results for every exit node in the Directory Authorities or in the local TOR instance will be stored in the local database used by Tortazo. Below you’ll see various switches to explain how to use the script Tortazo.py. On other hand, is much, much faster to use the local descriptors than to connect with the directory authorities (directly or using mirrors, both connection types are very slow sometimes) also depending on the number of users connected, sometimes the servers are busy and the connections with the directory authorities will fail or will be unstable. Anyways, you can use any method to gather information, but the fact is that the directory authorities have a lot of information about new relays available and the local descriptors have a short set of exit nodes. So, choose wisely your weapon!

.. NOTE::
   KEEP IN MIND:
* In the new versions of the TOR Client, by default the microdescriptors will be downloaded to compose the circuits. This is good because the circuit construction is much faster, but the information about the relays is very limited. So, if you plan to gather information with Tortazo using the TOR Client, you need to set the "UseMicrodescriptors" switch to "0" in your torrc file.
* If you want to use the TOR Client to gather information, you'll need to open the Control Port to use the Stem Controller (and set a password for security issues) to connect with the local instance and get the server descriptors. Please, check your torrc file.
* The connections with the TOR Authorities could be slow and sometimes unstable.
* You can use all the features included in Nmap, NSE Scripts even, just by using the switch "-a/--scan-arguments"
* If you want to use Shodan, you'll need a valid developer key. That value should be written into a file in a single line and use the switches "--use-shodan" and "--shodan-key"
* In botnet mode, Tortazo will not perform connections against TOR (neither local nor remote)

Gather information examples.   
=============================
Ok, now lets see some examples about the use of Tortazo in this execution mode.

**Show the available Options**

Shows the help banner of Tortazo::

    python Tortazo.py -h  


    
**Connecting to the Mirror servers of TOR**

- Connect to the TOR Authorities using the mirrors servers (-d / --use-mirrors). 
- Enable the "verbose" mode (-v / --verbose). 
- Scan ExitNodes which operative system is Windows (-m / --mode windows)::

    python Tortazo.py -d -v -m windows
    python Tortazo.py --use-mirrors --verbose --mode windows

    

**Connecting to the TOR servers (authorities)**    

- Connect to the TOR Authorities directly.
- Enable the "verbose" mode (-v / --verbose) 
- Scan ExitNodes which operative system is Linux (-m / --mode linux)::
    
    python Tortazo.py -v -m linux
    python Tortazo.py --verbose --mode linux



**Specify the number of relays to fetch from the descriptors downloaded**

- Connect to the TOR Authorities directly.
- Enable the "verbose" mode (-v / --verbose).
- Scan ExitNodes which operative system is Linux (-m / --mode linux) 
- Fetch the first 30 nodes from the list of exit nodes found (this value by default is very short: 10)::
    
    python Tortazo.py -n 30 -v -m linux
    python Tortazo.py --servers-to-attack 30 --verbose --mode linux



**Custom Nmap scan**

- Connect to the TOR Authorities directly.
- Enable the "verbose" mode (-v / --verbose) 
- Scan ExitNodes which operative system is Linux (-m / --mode linux) 
- Fetch the first 30 nodes from the list of exit nodes found 
- Perform the Nmap scan with the specified options "-sSV -A -n"::

    python Tortazo.py -n 30 -v -m linux -a "-sSV -A -n"
    python Tortazo.py --servers-to-attack 30 --verbose --mode linux --scan-arguments "-sSV -A -n"



**Connect with an Local instance of TOR.**

- Connect to the Local instance of TOR and use the ExitNodes stored in the local descriptors (-c / --use-circuit-nodes)
- Enable the "verbose" mode (-v / --verbose) 
- Scan ExitNodes which operative system is Linux (-m / --mode linux)::
    
    python Tortazo.py -v -m linux -c
    python Tortazo.py --verbose --mode linux --use-circuit-nodes



**Specify an relay's fingerprint to filter**    

- Connect to the TOR Authorities directly.
- Enable the "verbose" mode (-v / --verbose) 
- Scan ExitNodes which operative system is Linux (-m / --mode linux) 
- Fetch the first 30 nodes from the list of exit nodes found 
- Perform the Nmap scan with the specified options "-sSV -A -n" 
- Filter by FingerPrint (-e / --exit-node-fingerprint)::

    python Tortazo.py -n 30 -v -m linux -a "-sSV -A -n" -e FFAC0F4C85052F696EBB9517DD6E2E8B830835DD
    python Tortazo.py --servers-to-attack 30 --verbose --mode linux --scan-arguments "-sSV -A -n" --exit-node-fingerprint FFAC0F4C85052F696EBB9517DD6E2E8B830835DD



**Using Shodan to Gather information about the relays found**

- Connect to the TOR Authorities directly.
- Enable the "verbose" mode (-v / --verbose) 
- Scan ExitNodes which operative system is Linux (-m / --mode linux) 
- Fetch the first 30 nodes from the list of exit nodes found 
- Perform the Nmap scan with the specified options "-sSV -A -n" 
- Use Shodan (-s  / --use-shodan) with the specified developer key (-k  /  --shodan-key). The key must be stored in a text file in a single line::

    python Tortazo.py -n 30 -v -m linux -a "-sSV -A -n" -s -k /home/developer/shodanKeyFile
    python Tortazo.py --servers-to-attack 30 --verbose --mode linux --scan-arguments "-sSV -A -n" --use-shodan --shodan-key /home/developer/shodanKeyFile


