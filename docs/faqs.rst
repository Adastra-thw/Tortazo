.. _faqs_tortazo:

****************************************************
GENERAL FAQs
****************************************************

=================
¿What is this?
=================
Please, read the gentle introduction of Tortazo. :ref:`gentle_introduction`


=================
I have problems when I run "Tortazo.py" script.
=================
Please, check the dependencies and verify that your environment satisfy them all.


=================
¿This is free?
=================
Yes, free as the air you breathe. This project is licensed under GNU/GPLv2

.. _contact_adastra
=================
¿How can I help you?
=================
Great! if you want to help, read the documentation and find errors, test the framework, report bugs and if you can, write code.
You can write me an email to debiadastra [at] gmail.com

****************************************************
SPECIFIC FAQs
****************************************************
=================
I get "Import Errors" when I run the Tortazo.py script.
=================
Please, check the dependencies of Tortazo and install the Python libraries needed :ref:`dependencies-label` or use the binary distributed.

.. _problems_tor_socks_port:
=================
I have problems running the onion repository mode and some plugins which perform connections against hidden services in TOR, ¿what am I doing wrong?
=================
Every connection against the Deep web, must to use a SOCKS proxy to route the traffic through a TOR circuit. To do that, you must start a local instance of TOR and setting the "SockPort" property in the configuration file "torrc" used to start TOR.
On other hand, the default value for that port in Tortazo is "9150" and you can change that value manually editing property "socksPort" in the configuration file "config/config.py" (If you're using the development version, you can't change that value using the executable distributed). Also, if you want to start automatically a new instance of TOR when you're executing Tortazo, just specify the switches -T / --tor-localinstance and -U / --use-localinstance. 
Check the switches available in Tortazo :ref:`supported_options`

=================
I get an error when try to loading a Plugin
=================
Check two things:
1. The user that runs the command must read and write over the structure directories where Tortazo runs. Check the permissions of your user.
2. The argument passed to the switch -P / --use-plugin must include a valid plugin registered in the application. To see the modules enabled in Tortazo, check the configuration file "pluginsDeployed.py"

=================
Oh man, the onion repository mode has been running for the last "n" hours and I don't have any result ¿Am I doing something wrong?
=================
Well, this could be something normal. Please, check the onion repository mode documentation :ref:`repository-mode-label`
Also, you must have a TOR local instance up and running with the SocksPort property enabled. Check: :ref:`problems_tor_socks_port`

=================
When I run the crawler plugin twice I get the error "ReactorNotRestartable".
=================
The crawler plugin uses Scrapy Framework (http://scrapy.org/) which uses Twisted for every connection and network process. Twisted have an element called "reactor" which is designed to not be "restartable", so if you run the function "crawlOnionWebSite" from the crawler plugin twice, you'll get that error. You should exit from the plugin interpreter and run the plugin again.

=================
I'm trying to use shodan to gather information about the relays found, but I get errors
=================
To use Shodan, you'll need a valid Shodan Key, which you can get if created a new Shodan account. http://www.shodanhq.com/ 
Also, the shodan key must be included in a plain-text file (in just one line) and use the switch -k / --shodan-key
If you use the Shodan plugin available, you'll have another extended options to perform searches against shodan. :ref`supported_options`

=================
I get an strange error... ¿What can I do?
=================
Well, this is very ambiguous, don't you think? If after read the documentation  :ref:`getting_started` and read this FAQ :ref:`faqs_tortazo`` you can not solve it, please contact me :ref:`contact_adastra`
