#!/usr/bin/python
# coding: utf-8
from flask import Flask, request
import subprocess
import logging
import datetime

# RF Config and methods

class TestBackupRFDevice:
    def __init__(self, *kwargs):
        pass

    def enable_tx(self, *kwargs):
        pass

    def tx_code(self, *kwargs):
        pass

    def cleanup(self, *kwargs):
        pass


try:
    from rpi_rf import RFDevice
except:
    RFDevice = TestBackupRFDevice
    logging.error("Using fake RFDevice. All light controls will be no-ops")

def now():
    ts = datetime.datetime.now()
    return ts.strftime('%A %Y-%h-%d'), ts.strftime('%H:%M:%S.') +  ts.strftime('%f')[:4]

history_logs = []

local_ip_prefix='192.168'
ip_map =  {
    '192.168.1.13': 'Vasia (vasinator)',
    '192.168.1.4': 'Olya Samsung TV??? lol',
    '192.168.1.6': 'Olya\'s aiFone',
    '192.168.1.2': 'Pi99',
    '127.0.0.1':   'Pi99',
    '192.168.1.9': 'Greg\'s Rectangular Black Desktop Computer (DESKTOP-MLEQ2VQ)',
    '192.168.1.10': 'vas pixel2'
}

print("ip_map:", ip_map)

boot_time = subprocess.getoutput("""
    uptime | \
    perl -ne '/.*up +(?:(\d+) days?,? +)?(\d+):(\d+),.*/; $total=((($1*24+$2)*60+$3)*60);
    $now=time(); $now-=$total; $now=localtime($now); print $now,"\n";'
    """)
print("pi booted at: " + str(boot_time))
server_start_time = datetime.datetime.now().strftime('%a %h %d %H:%M:%S %Y')
class RF_Outlet():
    global history_logs
    global ip_map

    def __init__(self, name, remote_button, on, off):
        self.name = name
        self.remote_button = remote_button
        self.on = on
        self.off = off

    def send_rf_signal(self, code, protocol=1, pulselength=186, gpio=17):
        date, timestamp = now()
        ip_addr = request.remote_addr
        probable_requestor = ip_map.get(ip_addr,'Unknown')
        from_lan = ip_addr.startswith('192.168') or ip_addr == '127.0.0.1'
        details = (date, timestamp, self.remote_button, self.name, code, from_lan)

        logstr = '{}    {} [{}: {:25}, code: {}, from_lan: {}, ip: {}, prequestor: {}'.format(*details, ip_addr, probable_requestor)
        logging.info(logstr)
        history_logs.append(details)
        rfdevice = RFDevice(gpio)
        rfdevice.enable_tx()
        rfdevice.tx_code(code, protocol, pulselength)
        rfdevice.cleanup()

    def turn_on(self):
        self.send_rf_signal(code=self.on)

    def turn_off(self):
        self.send_rf_signal(code=self.off)


rf1 = RF_Outlet("Vasia's Room", 1, on=1398067, off=1398076)
rf4 = RF_Outlet("Michael's Room", 4, on=1400067, off=1400076)
rf5 = RF_Outlet("Living Room", 5, on=1406211, off=1406220)

rf_outlets = {1: rf1, 4: rf4, 5: rf5}

# Simple flask app

app = Flask(__name__)


index_html = """
<html>
    <body>
        <div style="font-size: 36px">
            <a href="/">Pi99</a>
            <table style="font-size: 32px">
                <tr>
                    <td style="width:270px"><td>
                    <td></td>
                    <td></td>
                </tr>
                {rf_outlets}
            </table>
            <div style="border: 2px solid indianred; font-size: 30px">
                <table style="font-family: 'Courier New', Courier, monospace;">
                    <tr>
                        <td style="color: #093c1d; width:400px"> 
                            Pi99 last boot: 
                        </td>
                        <td>
                            {boot_time} 
                        </td>
                    </tr>

                    <tr>
                        <td style="color: #093c1d"> 
                            Light control server started: 
                        </td>
                        <td>
                            {server_start_time} 
                        </td>
                    </tr>
                </table>
                <p></p>
            </div>
            <br>
            <table style="font-family: 'Courier New', Courier, monospace; font-size: 18px">
                <tr>
                    <td style="width:250px">Date</td>
                    <td style="width:200px">Time</td>
                    <td style="width:200px">Remote Button</td>
                    <td style="width:200px">Target</td>
                    <td style="width:200px">Code</td>
                    <td style="width:150px">From LAN?</td>
                </tr>
                {history_log}
            </table>
        </div>
    </body>
</html>
"""

history_log_template = """
<tr>
    <td>{}</td>
    <td>{}</td>
    <td>{}</td>
    <td>{}</td>
    <td>{}</td>
    <td>{}</td>
</tr>
"""

rf_entry_template = """
<tr>
    <td>
        {name}
    </td>
    <td>
        <a href="/{id}/on">  <img alt="On"  src="/static/on_b.png"  width="60px"></img></a>
    </td>
    <td>
        <a href="/{id}/off"> <img alt="Off" src="/static/off_b.png" width="60px"></img></a>
    </td>   
<tr>
"""



def get_history_logs():
    global history_logs
    return '\n'.join([history_log_template.format(*hlog) for hlog in history_logs[::-1]])


def get_rf_outlets():
    return '\n'.join([rf_entry_template.format(name=rf.name, id=rf.remote_button) for rf in rf_outlets.values()])


def render_template():
    global boot_time
    global server_start_time
    return index_html.format(
        history_log=get_history_logs(),
        rf_outlets=get_rf_outlets(),
        boot_time=boot_time,
        server_start_time=server_start_time)


def send_rf_outlet(lid, on=True):
    try:
        rf_outlet = rf_outlets[int(lid)]
        if on:
            rf_outlet.turn_on()
        else:
            rf_outlet.turn_off()
        return render_template()
    except Exception as e:
        logging.error(e)
        return "Error! Go back\nerror: {}".format(str(e))


@app.route('/')
def entry_point():
    return render_template()


@app.route('/<lid>/on')
def turn_on(lid):
    return send_rf_outlet(lid, True)


@app.route('/<lid>/off')
def turn_off(lid):
    return send_rf_outlet(lid, False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
