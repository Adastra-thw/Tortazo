****************************************************
Plugin Development in Tortazo
****************************************************

Develop a plugin in Tortazo is a very simple task, which is composed by the following steps:

1. Create a Python file in <TORTAZO_DIR>/plugins/<CATEGORY> where category is the root module which better describes the actions of your plugin (attack, bruteforce, enumeration, infogathering, etc.) In <TORTAZO_DIR>/plugins you’ll see the module “examples” where you can create your Python file to follow this guide.

2. Open the Python file created in the previous step and creates a new class which will extend from the class “core.tortazo.pluginManagement.BasePlugin.BasePlugin”. BasePlugin class defines the elements to integrate Python routines with Tortazo, so every plugin developed in Totazo must be an sub-class of BasePlugin class. Also, you should define a constructor (__init__) with the parameter “torNodes” which will be used by Tortazo to inject the dataset of relays loaded in the execution context; as probably already you know, data are the relays found in the current scan performed by Tortazo or database records from previous scan, depends on the switches used. 
The following script could be a valid example ::
 
    from core.tortazo.pluginManagement.BasePlugin import BasePlugin
    
    class TestPlugin(BasePlugin):
        def __init__(self, torNodes=[]):
            BasePlugin.__init__(self, torNodes, 'examplePlugin')
            self.setPluginDetails('testPlugin', 'Example of a plugin in Tortazo.', '1.0', 'Adastra: @jdaanial')
            self.info("[*] examplePlugin Initialized!")
        def __del__(self):
            self.info("[*]testPlugin Destroyed!")

Note that you should use the function “setPluginDetails” to define the settings for the plugin (name, description, version and author).

3. Your plugin is almost done. Now you need to register it in Tortazo. Edit the file  <TORTAZO_DIR>/pluginsDeployed.py and add your new plugin in the dict structure defined in the script. You need to add the name for your plugin and the class that you’ve defined in the previous step. For example ::

    plugins = {
    #OTHER PLUGINS LOADED IN TORTAZO
    #Now, the definition of your plugin.
    "testingPlugin": plugins.examples.testing.TestPlugin"
    }

Assuming that you’ve created the module “testing” inside the module “plugins.examples”, the class “TestPlugin” will be loaded in Tortazo when you use the switch “-P  /  --use-plugin”. Execute the following command to check if your plugin can be successfully loaded.::

    python Tortazo.py –v –D –P testingPlugin
    
If you can see the IPython interpreter loaded, you’re done. Your simple plugin is now integrated in Tortazo. Please, note that if your python script has compilation errors, the load process will fail, so you should verify that your program don’t have any errors before trying to load it in Tortazo.   


============================
Utilities in Tortazo for Plugin Development.
============================
When you create a plugin, the functions declared in that plugin will require access to  hidden services and TOR relays. You can't access to any hidden service without a connection with TOR and a Socks proxy up and running. The utilities included in Tortazo manages this issues for you and you can create and start your own TOR instance (with a Socks Proxy to browse in the TOR deep web) or indicate to Tortazo that executes an local instance and uses the Socks Proxy settings to connect with any hidden service. The main utility to perform connections to SMB, SSH, HTTP, FTP, and other services in the TOR deep web is the attribute “serviceConnector” defined in the class “BasePlugin”. The class “ServiceConnector” includes some functions to performs connections to services in TOR and uses utilities to manage connections like “socat” and “connect-socks”. The functions declared in “ServiceConnector” are the following:

============================================================================================================   =================================================================================================================================================================================================
Function Name                                                                                                  Description                                                                     
============================================================================================================   =================================================================================================================================================================================================
startLocalSocatTunnel(self, tcpListen,hiddenServiceAddress,hiddenServicePort, socksPort='9150')                Starts a local socat tunnel using the “TCP4-LISTEN” switch. The command executed will have the following format: 
                                                                                                               <TORTAZO_INSTALL>/plugins/utils/socat/socat TCP4-LISTEN:<tcp_port>,reuseaddr,fork SOCKS4A:127.0.0.1:<hidden_service_onion_address>:<hidden_service_onion_port>,socksport=<tor_socksport> &
anonymousFTPAccess(self,host, port)                                                                            Tries to perform an FTP anonymous connection in the host and port specified.
performFTPConnection(self, host, port, user, passwd)                                                           Tries to perform an FTP connection using the user and password specified.
performSSHConnection(self, host, port, user, passwd, brute=False)                                              Tries to perform an SSH connection using the user and password specified. If the parameter "brute" is True, Tortazo will append the connection settings to the tortazo_botnet.bot file.
performSSHConnectionHiddenService(self, onionService, port, user, passwd)                                      Tries to perform an SSH connection using the user and password specified against a hidden service.
performSNMPConnection(self, host, port=161, community='public')                                                Tries to perform an SNMP connection using the community name specified.
performSMBConnection(self, host='127.0.0.1', port=139, user="", passwd="")                                     Tries to perform an SMB connection using the user and password specified. If the connection is successful, lists the shared resources in the server.
performHTTPAuthConnection(self, url, user, passwd)                                                             Tries to perform an HTTP connection using the user and password specified against a protected resource in the server. This function checks if the resource has Basic or Digest authentication.
performHTTPConnectionHiddenService(self, onionUrl, headers={}, method="GET", urlParameters=None, auth=None)    Tries to perform an HTTP connection against a hidden service. The caller of the function could specify headers, url parameters and authentication details as needed.
performHTTPConnection(self, siteUrl, headers, method="GET", urlParameters=None, auth=None)                     Tries to perform a HTTP connection against the web site specified. The caller of the function could specify headers, url parameters and authentication details as needed.
setSocksProxySettings(self, socksHost, socksPort)                                                              Sets the socks proxy settings. Host and Port where the TOR socks proxy is running.
setSocksProxy(self)                                                                                            Enable the socks proxy defined by the function “setSocksProxySettings” and allows to route every connection through the TOR socks proxy.
unsetSocksProxy(self)                                                                                          Disable the socks proxy defined by the function “setSocksProxySettings” and allows to perform every connection directly with the service, without using the TOR socks proxy.
============================================================================================================   =================================================================================================================================================================================================
