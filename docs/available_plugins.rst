.. _available_plugins:

****************************************************
Available Plugins in Tortazo
****************************************************

There’s some plugins integrated in Tortazo and you can use them immediately just by loading the plugin in the interpreter using the switch “-P  / --use-plugin”. 

=================
Plugins to Gather Information and enumeration of hidden services and TOR relays
=================

infoGathering. TODO IN 1.2!
###################

   *Plugin Name: infoGathering*

   *Definition: plugins.infogathering.infoGatheringPlugin.infoGatheringPlugin*

   *Description:*		

   Plugin with some functions to gather information about the relays located in the plugin's context. The source of the information could be from the last scan performed by Tortazo or from Database records stored in previous scans.

====================================   ==========================================================================     ==========================================================================================================
Function Name                          Description                                                                    Usage Example     
====================================   ==========================================================================     ==========================================================================================================
help                                   Shows the banner help.                                                         self.help()
====================================   ==========================================================================     ==========================================================================================================

infoGathering Plugin example
=================
Interaction Example::

    sudo python Tortazo.py -v -D -P infoGathering -U -T config/config-example/torrc-example
    

stemming
###########

    *Plugin Name: stemming*
    *Definition: plugins.enumeration.deepWebStemmingPlugin.deepWebStemmingPlugin*
    *Description:*
    
    Basic tasks  of stemming module against hidden services in the TOR network. Uses IRL library to find terms in hidden services in the TOR network.

====================================   ============================================================================     ==========================================================================================================
Function Name                          Description                                                                      Usage Example     
====================================   ============================================================================     ==========================================================================================================
help                                   Shows the banner help.                                                           self.help()
simpleStemmingAllRelays                Stemming with the specified terms along the relays loaded in the plugin.         self.simpleStemmingAllRelays("drugs kill killer hitman")
                                       Searches in websites against common ports, 
                                       like 80,8080,443 or in an specific port.                                       
stemmingHiddenService                  Stemming with the specified terms in the onion address defined.                  self.stemmingWebSite("http://torlinkbgs6aabns.onion/", "drugs kill killer")                          
====================================   ============================================================================     ==========================================================================================================

stemming Plugin example
=================

Interaction Example::

    sudo python Tortazo.py -v -D -P stemming -U -T config/config-example/torrc-example


crawler
###########

    *Plugin Name:  crawler*

    *Definition:   plugins.enumeration. deepWebCrawlerPlugin.deepWebCrawlerPlugin*

    *Description:*

    This plugin uses Scrapy Framework to crawl a hidden service in TOR network. By default, the rules used follow every link in the specified website and downloads the contents found, however the user could overwrite this behavior specifying custom XPATH rules. The first action performed by the plugin is create a new Socat tunnel in the local machine in the port 8765 by default. The endpoint will be the hidden service specified by the user, but the crawler will performs the requests directly against the local machine through the Socat tunnel created. This is very useful to route the requests from the local machine to the TOR network transparently. Also, the user could specify arguments to overwrite the XPATH rules for content extraction and the pages that the crawler should visit before to start the process.
The website structure will be stored in database and the contents will be downloaded in local file system in the path "<TORTAZO_DIR>/onionSites/<hiddenServiceName>/"


====================================   ==========================================================================     ==========================================================================================================
Function Name                          Description                                                                    Usage Example     
====================================   ==========================================================================     ==========================================================================================================
help                                   Shows the banner help.                                                         self.help()
setExtractorRulesAllow                 Sets the XPATH rules to specify the allowed pages to visit and analyse.        self.setExtractorRulesAllow("index\.php| index\.jsp")
                                       This value will be passed to the "allow" attribute of the class:               
                                       "scrapy.contrib.linkextractors.LinkExtractor"
setExtractorRulesDeny                  Sets the XPATH rules to specify the disallowed pages to visit and analyze.     self.setExtractorRulesDeny("index\.php| index\.jsp")
                                       This value will be passed to the “deny” attribute of the class:
                                       “scrapy.contrib.linkextractors.LinkExtractor”                                       
setCrawlRulesLinks                     Sets the XPath rules to extract links from every webpage analyzed.             self.setCrawlRulesLinks('//a[contains(@href, "confidential")]/@href')
                                       Default value should be enough to almost every case, 
                                       however you can use this function to overwrite this value.
                                       Default: '//a/@href' 
setCrawlRulesImages                    Sets the XPath rules to extract images from every webpage analyzed.            self.setCrawlRulesImages('//a[contains(@href, "image")]/@href')
                                       Default value should be enough to almost every case, 
                                       however you can use this function to overwrite this value.
                                       Default: ' //img/@src'
compareWebSiteWithHiddenWebSite        Compares the contents of a website in clear web with the contents              self.compareWebSiteWithHiddenWebSite("http://exit-relay-found.com/", "http://gai12dase4sw3f5a.onion/")
                                       of a web site in TOR’s deep web. 
                                       The return value will be a percent of similitude between both sites.                                       
compareRelaysWithHiddenWebSite         This function will perform an HTTP connection against every relay found.       self.compareRelaysWithHiddenWebSite("http://gai12dase4sw3f5a.onion/")
                                       If the response is a HTTP 200 status code, 
                                       performs an HTTP connection against the hidden service specified 
                                       and compares the contents of both responses.  
                                       The return value will be a percent of similitude between both sites.
crawlOnionWebSite                      This function executes a crawler against the specified hidden service.         *	self.crawlOnionWebSite("http://gai12dase4sw3f5a.onion/")    
                                       The following parameters allow to control the behaviour of the crawler:        * self.crawlOnionWebSite("http://gai12dase4sw3f5a.onion/", hiddenWebSitePort=8080, crawlImages=False)
                                       hiddenWebSite: The hidden site to crawl. This is a mandatory parameter.        * self.crawlOnionWebSite("http://gai12dase4sw3f5a.onion/", crawlFormData=False)
                                       hiddenWebSitePort: Port for the hidden site to crawl. Default value: 80
                                       socatTcpListenPort: Port for the Socat proxy. Default value: 8765
                                       crawlImages: Search and download the images from every page.
                                       Default value: True.
                                       crawlLinks: Search and visit the links found in every page.
                                       Default value: True.
                                       crawlContents: Download and save in local file system the 
                                       contents of every page found. 
                                       crawlFormData: Search the forms in every page and store 
                                       that structure in database.
                                       deepLinks: Number of Links that the crawler will visit in deep. 
                                       useRandomUserAgents: Use a random list of User-Agents 
                                       in every HTTP connection performed by the crawler. 
                                       FuzzDB project is used to get a list of User-Agents reading the file 
                                       fuzzdb/attack-payloads/http-protocol/user-agents.txt
                                       bruterOnProtectedResource: If true, when the spider found an 
                                       HTTP protected resource, tries to execute an bruteforce attack 
                                       using the specified dict file or FuzzDB.
====================================   ==========================================================================     ==========================================================================================================

crawler Plugin example
=================

Interaction Example::

    sudo python Tortazo.py -v -D -P crawler -U -T config/config-example/torrc-example


shodan
############

    *Plugin Name: shodan*

    *Definition: plugins.infogathering.shodanPlugin.shodanPlugin*

    *Description:*

    Plugin used to perform tests against Shodan service using the information gathered by Tortazo. This plugin is much more flexible that the switch “-s  /  --use-shodan”.

====================================   ==========================================================================     ==========================================================================================================
Function Name                          Description                                                                    Usage Example     
====================================   ==========================================================================     ==========================================================================================================
help                                   Shows the banner help.                                                         self.help()
setApiKey                              Sets the API Key string.                                                       self.setApiKey("XXXXXXXXXXXX")
setApiKeyFile                          Sets the API Key file.                                                         self.setApiKeyFile("/home/apiKeyFile")
                                       Reads the first line of the file and then sets the API Key string. 
basicSearchQuery                       Performs a basic search with Shodan.                                           self.basicSearchQuery("OpenSSL 1.0.1", 15)
                                       By default prints the 10 first results                                       
basicSearchAllRelays                   Performs a basic search with Shodan against all TOR relays.                    self.basicSearchAllRelays("OpenSSL 1.0.1")
                                       Uses the "net" filter.                                       
basicSearchByRelay                     Performs a basic search with Shodan against the specified TOR relay.           self.basicSearchByRelay("OpenSSL 1.0.1", "80.80.80.80")
basicSearchByNickname                  Performs a basic search with Shodan against the specified TOR NickName.        self.basicSearchByNickname("OpenSSL 1.0.1", "TORNickName")                                        
====================================   ==========================================================================     ==========================================================================================================

shodan Plugin example
=================

Interaction Example::

    sudo python Tortazo.py -v -D -P shodan -U -T config/config-example/torrc-example


=================
Plugins to Pentesting and attack hidden services and TOR relays
=================

bruter
###############
    *Plugin Name: bruter*

    *Definition: plugins.bruteforce.bruterPlugin.bruterPlugin*

    *Description:*

    This plugin is used to perform dictionary attacks against TOR relays and hidden services. Supports brute forcing against services like SSH, FTP, SNMP and SMB.

====================================   ==========================================================================     ===================================================================================================================
Function Name                          Description                                                                    Usage Example     
====================================   ==========================================================================     ===================================================================================================================
help                                   Shows the banner help.                                                         self.help()
setDictSeparator                       Sets an separator for the dictionary file.                                         self.setDictSeparator(":")
                                       Every line en the file must contain <user><separator><passwd>.
sshBruterOnRelay                       Bruteforce attack against an SSH Server in the relay entered.                  self.sshBruterOnRelay('37.213.43.122', dictFile='/home/user/dict')
                                       Uses FuzzDB if the dictFile is not specified.                                        
sshBruterOnAllRelays                   Bruteforce attack against an SSH Server in the relays founded.                 self.sshBruterOnAllRelays(dictFile='/home/user/dict')
                                       Uses FuzzDB if the dictFile is not specified.                                       
sshBruterOnHiddenService               Bruteforce attack against an SSH Server in the onion address entered.          self.sshBruterOnHiddenService("5bsk3oj5jufsuii6.onion", dictFile="/home/user/dict")
                                       Uses FuzzDB if the dictFile is not specified.
ftpBruterOnRelay                       Bruteforce attack against an FTP Server in the relay entered.                  self.ftpBruterOnRelay("37.213.43.122", dictFile="/home/user/dict")
                                       Uses FuzzDB if the dictFile is not specified.        
ftpBruterOnAllRelays                   Bruteforce attack against an FTP Server in the relays founded.                 self.ftpBruterOnAllRelays(dictFile="/home/user/dict")
                                       Uses FuzzDB if the dictFile is not specified.                                  
ftpBruterOnHiddenService               Bruteforce attack against an FTP Server in the onion address entered.          self.ftpBruterOnHiddenService("5bsk3oj5jufsuii6.onion", dictFile="/home/user/dict")
                                       Uses FuzzDB if the dictFile is not specified.
smbBruterOnRelay                       Bruteforce attack against an SMB Server in the relay entered.                  self.smbBruterOnRelay("37.213.43.122", dictFile="/home/user/dict")
                                       Uses FuzzDB if the dictFile is not specified.
smbBruterOnAllRelays                   Bruteforce attack against an SMB Server in the relays founded.                 self.smbBruterOnAllRelays(dictFile="/home/user/dict")
                                       Uses FuzzDB if the dictFile is not specified.                                       
smbBruterOnHiddenService               Bruteforce attack against an SMB Server in the onion address entered.          self.smbBruterOnHiddenService("5bsk3oj5jufsuii6.onion", servicePort=139, localPort=139, dictFile="/home/user/dict")
                                       This function uses socat to create a local Socks proxy and 
                                       route the requests from the local machine to the hidden service.                                       
snmpBruterOnRelay                      Bruteforce attack against an SNMP Server in the relay entered.                 self.snmpBruterOnRelay("37.213.43.122", dictFile="/home/user/dict")
                                       Uses FuzzDB if the dictFile is not specified.
snmpBruterOnAllRelays                  Bruteforce attack against an SNMP Server in the relays founded.                self.snmpBruterOnAllRelays(dictFile="/home/user/dict")
                                       Uses FuzzDB if the dictFile is not specified.                         
httpBruterOnSite                       Bruteforce attack against a web site.                                          self.httpBruterOnSite("http://eviltorrelay.com/auth/", dictFile="/home/user/dict")       
                                       Uses FuzzDB if the dictFile is not specified.                         
httpBruterOnHiddenService              Bruteforce attack against an onion site (hidden site in TOR's deep web).       self.httpBruterOnHiddenService("http://5bsk3oj5jufsuii6.onion/auth/", dictFile="/home/user/dict")
                                       Uses FuzzDB if the dictFile is not specified.
====================================   ==========================================================================     ===================================================================================================================


bruter Plugin example
=================

Interaction Example::

    sudo python Tortazo.py -v -D -P bruter -U -T config/config-example/torrc-example


heartBleed
#############

    *Plugin Name: heartBleed*
    
    *Definition: plugins.attack.heartBleedPlugin.heartBleedPlugin*

    *Description: *
    
    Perform HearthBleed Extension vulnerability tests. This plugin allows to discovery TOR relays with this vulnerability.


====================================   ==========================================================================     ==========================================================================================================
Function Name                          Description                                                                    Usage Example     
====================================   ==========================================================================     ==========================================================================================================
help                                   Shows the banner help.                                                         self.help()
setTarget                              Set the relay for the HeartBleed attack.                                       self.setTarget("1.2.3.4")
                                       Check the targets using the function "printRelaysFound". 
                                       Default port: 443.
setTargetWithPort                      Set the relay and port for the HeartBleed attack.                              self.setTarget("1.2.3.4", "8443")
                                       Check the targets using the function "printRelaysFound".                                       
startAttack                            Starts the HeartBleed attack against the specified target.                     self.startAttack()
startAttackAllRelays                   Starts the HeartBleed attack against all relays loaded in the plugin.          self.startAttackAllRelays()
                                       Default port: 443                                                                              
====================================   ==========================================================================     ==========================================================================================================

heartBleed Plugin example
=================

Interaction Example::

    sudo python Tortazo.py -v -D -P heartBleed -U -T config/config-example/torrc-example


=================
Plugins for integration with Third-Party tools
=================

w3af
#######
 
    *Plugin Name: w3af*
    
    *Definition:   plugins.thirdparty.w3afPlugin.w3afPlugin*
 
    *Description:*

    W3AF is a powerful scanner focused on discovering vulnerabilities and attack in 
web applications. As is written in Python and has a GNU/GPL license, you can use the classes and utilities from any script in Python. In this case, the plugin does not 
only covers the features included in w3af, but also allows the execution 
of audits in web applications that are hosted in the deep web. In the official release of W3AF, you can’t use any site on the deep web whose target address is an ONION TLD. Using this plugin, allows you to do that.

====================================   ==========================================================================     ==========================================================================================================
Function Name                          Description                                                                    Usage Example     
====================================   ==========================================================================     ==========================================================================================================
help                                   Shows the banner help.                                                         self.help()
showPluginsByType                      List of available plugins filtered by type.                                    self.showPluginsByType("audit")
showPluginTypes                        List of available plugin types.                                                self.showPluginTypes()
getEnabledPluginsByType                Enabled plugins by types.                                                      self.getEnabledPluginsByType("audit")
getPluginTypeDescription               Description for the plugin type specified.                                     self.getPluginTypeDescription("audit")
getAllEnabledPlugins                   List of enabled plugins.                                                       self.getAllEnabledPlugins()
enablePlugin                           Enable a plugin.                                                               self.enablePlugin("blind_sqli","audit")
disablePlugin                          Disable a plugin.                                                              self.disablePlugin("blind_sqli","audit")
enableAllPlugins                       Enable all plugins.                                                            self.enableAllPlugins("audit")
disableAllPlugins                      Disable all plugins.                                                           self.disableAllPlugins("audit")
getPluginOptions                       Get Options for the plugin specified.                                          self.getPluginOptions("audit","blind_sqli")
setPluginOptions                       Set Options for the plugin specified.                                          self.setPluginOptions("audit","eval","boolean","use_time_delay","False")
getPluginStatus                        Check if the specified plugin is enabled.                                      self.getPluginStatus("audit","eval")
setTarget                              Sets the target for the attack (clear web).                                    self.setTarget("http://www.target.com")
setTargetDeepWeb                       Sets the target in the Deep eb of TOR.                                         self.setTarget("http://torlongonionpath.onion")
startAttack                            Starts the attack.                                                             self.startAttack()
listMiscConfigs                        List of Misc Settings.                                                         self.listMiscConfigs()
setMiscConfig                          Sets a Misc Setting.                                                           self.setMiscConfig("msf_location","/opt/msf")
listProfiles                           List of Profiles.                                                              self.listProfiles()
useProfile                             Use a Profile.                                                                 self.useProfile("profileName")
createProfileWithCurrentConfig         Creates a new Profile with the current settings.                               self.createProfileWithCurrentConfig("profileName", "Profile Description")
modifyProfileWithCurrentConfig         Modifies an existing profile with the current settings.                        self.modifyProfileWithCurrentConfig("profileName", "Profile Description")
removeProfile                          Removes an existing profile.                                                   self.removeProfile("profileName")
listShells                             List of Shells.                                                                self.listShells()
executeCommand                         Executes a command in the specified shell.                                     self.executeCommand(1,"lsp")
listAttackPlugins                      List of attack plugins.                                                        self.listAttackPlugins()
listInfos                              List of Infos in the Knowledge Base of W3AF.                                   self.listInfos()
listVulnerabilities                    List of Vulns in the Knowledge Base of W3AF.                                   self.listVulnerabilities()
exploitAllVulns                        Exploits all vulns in the Knowledge Base of W3AF.                              self.exploitVulns("sqli")
exploitVuln                            Exploits the specified Vuln in the Knowledge Base of W3AF.                     self.exploitVulns("sqli",18)
====================================   ==========================================================================     ==========================================================================================================

w3af Plugin example
=================

Interaction Example::

    sudo python Tortazo.py -v -D -P w3af -U -T config/config-example/torrc-example -A


nessus
###########
    *Plugin Name:  nessus*
    
    *Definition: plugins.thirdparty.nessusPlugin.nessusPlugin*
    
    *Description:*

    This plugin is responsible for executing the authentication process against a Nessus instance and allows you to use the full features of the Nessus engine against the repeaters 
analyzed by Tortazo. It has the functions necessary to list the available plugins, 
manage policies, users, create specific scans, scheduled scans and query 
reports generated by Nessus. To carry out the interaction between 
Tortazo and Nessus, the pynessus-rest library is used; which has been developed 
primarily to meet the needs of this plugin and directly uses the functions 
available in the latest version of Nessus REST API. In this way, you can run the 
same tasks that are available from the web interface enabled on Nessus. Connection and authentication must be declared in the properties file
located in <TORTAZO_DIR>/config.py, which should specify the details for the connection to the server; these details include the address and port of the Nessus server and the credentials required to access. On other hand, if you want overwrite the configuration values without change the properties file, you can use the switch "-A  /  --plugin-arguments" with the special keywords "nessusHost", "nessusPort", "nessusUser", "nessusPassword".


====================================   ===============================================================================     ==========================================================================================================
Function Name                          Description                                                                         Usage Example     
====================================   ===============================================================================     ==========================================================================================================
help                                   Shows the banner help.                                                              self.help()
serverLoad                             Shows details about the load of the server.                                         self.serverLoad()
                                       Number of opened sessions and memory usage, etc.
feed                                   Return the Nessus Feed.                                                             self.feed()
serverSecureSettingsList               List of Server Secure Settings.                                                     self.serverSecureSettingsList()
serverRegister                         Registers the Nessus server with Tenable Network Security.                          self.serverRegister('FEED_CODE')
serverLoad                             Server Load and Platform Type.                                                      self.serverLoad()
serverUuid                             Server UUID.                                                                        self.serverUuid()
userAdd                                Create a new user.                                                                  self.userAdd('adastra','adastra',0)
                                       The third parameter defines the user as administrator (1) or regular user (0).      
userEdit                               Edit the user specified.                                                            self.userEdit('adastra','new_password',1)
                                       The third parameter defines the user as administrator (1) or regular user (0).                                       
userDelete                             Delete the user specified.                                                          self.userDelete('adastra')
                                       The third parameter defines the user as administrator (1) or regular user (0).                                
userChpasswd                           Change the password for the user specified.                                         self.userChpasswd('adastra','new_password')
                                       The third parameter defines the user as administrator (1) or regular user (0).                                     
usersList                              List of users.                                                                      self.usersList()
pluginsList                            List of plugins.                                                                    self.pluginsList()
pluginAttributesList                   List of plugins attributes for plugin filtering.                                    self.pluginListsFamily('AIX Local Security Checks')
pluginDescription                      Returns the entire description of a given plugin.                                   self.pluginDescription('ping_host.nasl')
pluginsAttributesFamilySearch          Filters against the family of plugins.                                              self.pluginsAttributesFamilySearch('match','or','modicon','description')
pluginsAttributesPluginSearch          Returns the plugins in a family that match a given filter criteria.                 self.pluginsAttributesPluginSearch('match','or','modicon','description','FTP')
                                       Check the Nessus documentation to see filter criteria.
pluginsMd5                             List of plugin file names and corresponding MD5 hashes.                             self.pluginsMd5()
policyList                             List of available policies, policy settings and default values.                     self.policyList()
policyDelete                           Delete the policy specified.                                                        self.policyDelete(POLICY_ID)
policyCopy                             Copies an existing policy to a new policy.                                          self.policyCopy(POLICY_ID)
policyDownload                         Download the policy from the server to the local system.                            self.policyDownload(POLICY_ID, /home/user/policy.nessus)
scanAllRelays                          Create a new scan with all relays loaded.                                           self.scanAllRelays(<POLICY_ID>, 'newScan')
scanByRelay                            Create a new scan with the specified relay.                                         self.scanAllRelays(<POLICY_ID>, 'newScan', <IP_OR_NICKNAME>)
scanStop                               Stops the specified started scan.                                                   self.scanStop(<SCAN_UUID>)
scanResume                             Resumes the specified paused scan.                                                  self.scanResume(<SCAN_UUID>)
scanPause                              Pauses the specified actived scan.                                                  self.scanPause(<SCAN_UUID>)
scanList                               List of scans.                                                                      self.scanList()
scanTemplateAllRelays                  Create a new scan template (scheduled) with all relays loaded.                      self.scanTemplateAllRelays(<POLICY_ID>,<TEMPLATE_NAME>)
scanTemplateByRelay                    Create a new scan template (scheduled) with the specified relay.                    self.scanTemplateByRelay(<POLICY_ID>,<TEMPLATE_NEW_NAME>,<IP_OR_NICKNAME>)
scanTemplateEditAllRelays              Edit the scan template specified with all relays loaded.                            self.scanTemplateEditAllRelays(<POLICY_ID>,<TEMPLATE_NEW_NAME>)
scanTemplateEditByRelay                Edit the scan template specified with the specified relay.                          self.scanTemplateEditByRelay(<TEMPLATE_UUID>,<TEMPLATE_NEW_NAME>,<POLICY_ID>,<IP_OR_NICKNAME>)
scanTemplateDelete                     Delete the scan template specified.                                                 self.scanTemplateDelete(<TEMPLATE_UUID>)
scanTemplateLaunch                     Launch the scan template specified.                                                 self.scanTemplateLaunch(<TEMPLATE_UUID>)
reportList                             List of available scan reports.                                                     self.reportList()
reportDelete                           Delete the specified report.                                                        self.reportDelete(<REPORT_UUID>)
reportHosts                            List of hosts contained in a specified report.                                      self.reportHosts(<REPORT_UUID>)
reportPorts                            List of ports and the number of findings on each port.                              self.reportPorts(<REPORT_UUID>,<HOSTNAME>)
reportDetails                          Details of a scan for a given host.                                                 self.reportDetails(<REPORT_UUID>,<HOSTNAME>,<PORT>,<PROTOCOL>)
reportTags                             Tags of a scan for a given host.                                                    self.reportTags(<REPORT_UUID>, <HOSTNAME>)
reportAttributesList                   List of filter attributes associated with a given report.                           self.reportAttributesList(<REPORT_UUID>)                                         
====================================   ===============================================================================     ==========================================================================================================

nessus Plugin example
=================

Interaction Example::

    sudo python Tortazo.py -v -D -P nessus -U -T config/config-example/torrc-example
    sudo python Tortazo.py -v -D -P nessus -U -T config/config-example/torrc-example -A nessusHost=192.168.1.20,nessusPort=8834,nessusUser=adastra,nessusPassword=adastra