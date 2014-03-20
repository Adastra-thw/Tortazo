from core.tortazo.data.ShodanHost import  ShodanHost
from core.tortazo.Reporting import Reporting
import shodan

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

if __name__ == "__main__":
    #loadAndExecute("simplePlugin:simplePrinter", [])
    #shodanTest()
    moreTest()