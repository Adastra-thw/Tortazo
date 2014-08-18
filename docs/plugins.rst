.. _plugins-management-label:

****************************************************
Plugins in Tortazo. Getting started
****************************************************

Tortazo defines a plugin system to execute Python scripts against TOR relays and TOR hidden services. This feature enables to Python developers create code routines that will perform actions in the TOR deep web. This is actually, one of the major features in Tortazo. It’s a bridge between TOR and the Python Hackers.
The plugin’s interpreter is a simple IPython interface and there, the modules and classes defined by the developer will be loaded and could be executed against any target (TOR relay or hidden service). Obviously IPython is a mandatory dependence and the system of plugins depends on this library. 
The default installation of Tortazo contains some interesting plugins to perform pentesting activities and you can get the list of plugins loaded using the switches “-L  /  --list-plugins”. Also, some plugins allows the integration with third-party tools like Nessus, W3AF, Nikto and Metasploit. So, you can execute these tools against TOR!

See the section about plugins development :ref:`plugin_development.rst`
See the section about plugins available in Tortazo :ref:`available_plugins.rst`