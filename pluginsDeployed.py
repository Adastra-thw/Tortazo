####
####          PLUGINS DEPLOYED IN TORTAZO. NAME AND MODULE.
####
plugins = {
                   #EXAMPLE PLUGINS. IF YOU ARE A DEVELOPER, THIS IS A GOOD STARTING POINT :-)
                   "example"       : "plugins.examples.examplePlugin.examplePlugin",

                   #THIRDPARTY PLUGINS. INTEGRATION OF OTHER FRAMEWORKS AND TOOLS AVAILABLE.
                   "w3af"          : "plugins.thirdparty.w3afPlugin.w3afPlugin",
                   "nessus"        : "plugins.thirdparty.nessusPlugin.nessusPlugin",
                   "nikto"         : "plugins.thirdparty.niktoPlugin.niktoPlugin",

                   #INFORMATION GATHERING PLUGINS.
                   "infoGathering" : "plugins.infogathering.infoGatheringPlugin.infoGatheringPlugin",
                   "shodan"        : "plugins.infogathering.shodanPlugin.shodanPlugin",

                   #ENUMERATION PLUGINS.
                   "crawler" : "plugins.enumeration.deepWebCrawlerPlugin.deepWebCrawlerPlugin",
                   "stemming" : "plugins.enumeration.deepWebStemmingPlugin.deepWebStemmingPlugin",
                   "dirBruter" : "plugins.enumeration.deepWebDirBruterPlugin.deepWebDirBruterPlugin",


                   #ATTACK PLUGINS.
                   "heartBleed"    : "plugins.attack.heartBleedPlugin.heartBleedPlugin",
                   "hiddenService" : "plugins.attack.maliciousHiddenServicePlugin.maliciousHiddenServicePlugin",

                   #BRUTERFORCE PLUGINS.
                   "bruter"    : "plugins.bruteforce.bruterPlugin.bruterPlugin"
                   }