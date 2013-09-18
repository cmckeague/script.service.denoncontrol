import xbmc

from twisted.protocols.basic import LineReceiver
from twisted.internet.serialport import BaseSerialPort
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory


denon_host = '___.___.___.___'
denon_port = 23

mute_on = '{"id":1,"jsonrpc":"2.0", "method":"Player.PlayPause", "params":{"PlayerID":"0"}}'
mute_off = '{"id":1, "jsonrpc":"2.0", "method":"Player.PlayPause", "params":{"PlayerID":"0"}}'
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
reactor.connectTCP(denon_host, denon_port, denon_factory)
reactor.run(installSignalHandlers=0)
