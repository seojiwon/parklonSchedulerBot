import xmpp
from datetime import time, datetime

defaultAccount = "your-account used for Parklonia App"
heatPadAccount = "your-device-id@iunplug.co.kr" # See the back of your Parklonia device 
                                                # This is not a boiler, but a small device called Parklonia.
                                                # http://www.parklonia.com/
class HeatPadBot:
    def __init__(self):
        self.login()
        self.heatpadIdx = 1 # If you have multiple heat-pads, change this index to refer to the pad you want to control.
        
    def login(self):       
        import getpass
        account = raw_input("Gtalk account(default:%s):"%defaultAccount)
        if not account:
            account = defaultAccount
        jid=xmpp.protocol.JID(account)
        conn=xmpp.Client(jid.getDomain(), debug=[])
        conn.connect()
        passwd = getpass.getpass("%s passwd:"%account)
        conn.auth(jid.getNode(),passwd)
        conn.sendInitPresence()
        self.conn = conn

    def scheduleOnOff(self, on=None, off=None):
        if on: self.schedule(on, self.turnOn)
        if off: self.schedule(off, self.turnOff)

    def schedule(self, time, func):
        h = time.hour
        m = time.minute
        print "Scheduling ",func.im_func.func_name,"at",time
        while self.conn.Process(10):
            now = datetime.now()
            if now.hour == h and now.minute == m:
                func()
                break
            
    def turnOn(self):
        print "turning on"
        self.conn.send(xmpp.protocol.Message(heatPadAccount, 
                '''R9HAUTO_JSON{"type":"request","payload":{"indexes":[{"idx":%d,"heaters":[{"power":true,"htidx":1}]}],"command":"setstate","devtype":"thermomat"},"msgid":"4F95D3PE1A","version":1}'''%self.heatpadIdx, 
                typ='chat'))

    def turnOff(self):
        # This doesn't seem to work. Need to understand the protocol.
        print "turning off"
        self.conn.send(xmpp.protocol.Message(heatPadAccount, 
                '''R9HAUTO_JSON{"type":"request","payload":{"indexes":[{"idx":%d,"heaters":[{"power":false,"htidx":1}]}],"command":"setstate","devtype":"thermomat"},"msgid":"F2ESTPFTG3","version":1}}'''%self.heatpadIdx,
                typ='chat'))

bot = HeatPadBot()
bot.scheduleOnOff(on=time(3, 10))
