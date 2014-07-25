.. _botnet-mode-label:

***************
Botnet mode in Tortazo.
***************

The botnet mode is specified with the option -z/--zombie and depends on the tortazo_botnet.bot file. In this mode, Tortazo will read that file and then, tries to perform SSH Connections using the hosts and credentials defined in that file. 
Every line in "tortazo_botnet.bot" have the next format: ::

    host:user:passwd:port:nickname

The python library Fabric is used to connect with the SSH servers and execute commands across a set of SSH Servers. 
When you specify the -z/--zombie option, Tortazo will not download or parse descriptors from Tor authorities, just reads the tortazo_botnet.bot file and then tries to open a shell on the specified bot (-o/--open-shell switch) or run a command (-r/--run-command switch). 
In this mode, you must specify the nicknames that will be excluded from the botnet (comma separated) or the keyword "all" to include all bots from tortazo_botnet.bot file.

Botnet mode examples.   
=============================
Using this mode is very simple, but the file located in <TORTAZO_DIR>/tortazo_botnet.bot must have a list of bots with the connection details of every bot for each line.

**Execute commands across the entirely botnet**
Runs the commands id; uname -a; uptime::

    python Tortazo.py -v -z all -r "id; uname -a; uptime; w"
    python Tortazo.py --verbose --threads 10 --zombie-mode all --run-command "id; uname -a; uptime; w"


**Open a shell in the specified bot**
Entering the shell identifier to open a new console in the specified host.::

    python Tortazo.py -v -z all -o
    python Tortazo.py --verbose --zombie-mode all --open-shell
    
   
.. NOTE::
   KEEP IN MIND:

   Obviously, the credentials in the tortazo_botnet.bot file should be valid for every host registered. If the credentials are not valid, Fabric will resolve the authentication method (password or public key) and will require that you enter the password or passphase.
