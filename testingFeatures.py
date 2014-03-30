from core.tortazo.data.ShodanHost import  ShodanHost
#from core.tortazo.Reporting import Reporting
import shodan
import plugins
import inspect, itertools

def moreTest():
    try:
        shodanKeyString = "XGacliX7RBhkxAT0LgfenUmdtlRsRmjQ"
        shodanApi = shodan.Shodan(shodanKeyString)
        results = shodanApi.search("apache")
        for result in results['matches']:
            print 'IP: %s' % result['ip_str']
            print result['data']
            print ''
        info = shodanApi.info()
        for inf in info:
            print '%s: %s: ' %(inf, info[inf])

    except shodan.APIError, e:
        print 'Error: %s' % e


def shodanTest():
    #shodanKeyString = open("/home/adastra/Escritorio/shodanKey").readline().rstrip('\n')
    #shodanApi = shodan.Shodan(shodanKeyString)
    shodanKeyString = "XGacliX7RBhkxAT0LgfenUmdtlRsRmjQ"
    shodanApi = shodan.Shodan(shodanKeyString)

    results = shodanApi.host("193.33.37.219")

    shodanHost = ShodanHost()
    shodanHost.results = results
    shodanHost.host = "193.33.37.219"
    shodanHost.keyInfo = shodanApi.info()
    reporter = Reporting()
    reporter.generateShodanReport(shodanHost, 'D:\\shodan.html')

def loadAndExecute(listPlugins, torNodesFound):
        '''
        Load and execute external rutines (plugins)
        '''
        #simplePlugin:simplePrinter,argName1=arg1,argName2=arg2,argNameN=argN;anotherSimplePlugin:anotherSimpleExecutor,argName1=arg1,argName2=arg2,argNameN=argN
        if listPlugins is None:
            print "[-] You should specify a list of plugins with the option -P/--use-plugins"
            return
        plugins = listPlugins.split(";")
        for plugin in plugins:
            pluginModule, pluginClass = plugin.split(":")
            if pluginModule is None or pluginClass is None:
                print "[-] Format "+ listPlugins +" invalid. Check the documentation to use plugins in Tortazo"
                return
            try:
                module = __import__("plugins."+pluginModule)
                pluginArguments = pluginClass.split(',')
                pluginClassName = pluginArguments[0]
                pluginArguments.remove(pluginClassName)
                components = ("plugins."+pluginModule+"."+pluginClassName).split('.')
                print "[+] Loading plugin..."
                for comp in components[1:]:
                    module = getattr(module, comp)
                reference = module()
                reference.setNodes(torNodesFound)
                print "[+] Done!"
                print "[+] Parsing the arguments for the plugin..."
                pluginArgumentsToSet = {}
                for arg in pluginArguments:
                    argumentItem = arg.split('=')
                    argumentName = argumentItem[0]
                    argumentValue = argumentItem[1]
                    print "[+] Argument Name %s with value %s" %(argumentName, argumentValue)
                    if argumentValue is None:
                        print "[-] Error: Argument Name %s without value... " %(argumentName)
                    pluginArgumentsToSet[argumentName] = argumentValue
                reference.setPluginArguments(pluginArgumentsToSet)
                reference.runPlugin()
            except ImportError, importErr:
                print "[-] Error loading the class. Your plugin class should be located in 'plugins' package. Check if "+pluginModule+"."+pluginClass+" exists"

if __name__ == "__main__":
    #loadAndExecute("simplePlugin:simplePrinter", [])
    #shodanTest()
    #moreTest()
    #__import__("plugins.simplePlugin")
    loadAndExecute("nessusPlugin:nessusPlugin,function1=listPlugins,function2=getPolicyByName,policy_id=222",[])
    #loadAndExecute("simplePlugin:simplePrinter,arg1=val1,arg2=val2,arg3=val3",[])