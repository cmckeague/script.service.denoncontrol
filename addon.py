import os
import xbmc
import xbmcaddon


__addon__      = xbmcaddon.Addon()
__author__     = __addon__.getAddonInfo('author')
__scriptid__   = __addon__.getAddonInfo('id')
__scriptname__ = __addon__.getAddonInfo('name')
__version__    = __addon__.getAddonInfo('version')
__language__   = __addon__.getLocalizedString
__ipaddress__  = __addon__.getSetting('ipaddress')
__port__       = int(__addon__.getSetting('port'))

__cwd__        = xbmc.translatePath( __addon__.getAddonInfo('path') ).decode("utf-8")
__resource__   = xbmc.translatePath( os.path.join( __cwd__, 'resources',  \
                                                  'lib' ) ).decode("utf-8")

sys.path.append (__resource__)

from twisted.protocols.basic import LineReceiver
from twisted.internet.serialport import BaseSerialPort
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory


mute_on = '{"id":1,"jsonrpc":"2.0", "method":"Player.PlayPause", ' \
          '"params":{"playerid":1}}'
mute_off = '{"id":1, "jsonrpc":"2.0", "method":"Player.PlayPause", ' \
           '"params":{"playerid":1}}'
xbmcCommands = {'MUON': mute_on, 'MUOFF': mute_off}

class denonAVR(LineReceiver):    
    delimiter = '\r'
    def lineReceived(self, line):
        if line in xbmcCommands.keys():
            xbmc.executeJSONRPC(xbmcCommands[line])
        else:
            print line


class denonAVR_factory(ClientFactory):
    protocol = denonAVR
    def clientConnectionFailed(self, connector, reason):
        print 'connection failed:', reason.getErrorMessage()
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print 'connection lost:', reason.getErrorMessage()
        reactor.stop()
        
denon_factory = denonAVR_factory()
reactor.connectTCP(__ipaddress__, __port__, denon_factory)
reactor.run(installSignalHandlers=0)
