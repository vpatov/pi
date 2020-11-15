#!/usr/bin/python
# coding: utf-8
from flask import Flask
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


history_logs = []

boot_time = subprocess.getoutput("""
    uptime | \
    perl -ne '/.*up +(?:(\d+) days?,? +)?(\d+):(\d+),.*/; $total=((($1*24+$2)*60+$3)*60);
    $now=time(); $now-=$total; $now=localtime($now); print $now,"\n";'
    """)
print("pi booted at: " + str(boot_time))
server_start_time = str(datetime.datetime.now())

class RF_Outlet():
    global history_logs

    def __init__(self, name, remote_button, on, off):
        self.name = name
        self.remote_button = remote_button
        self.on = on
        self.off = off

    def send_rf_signal(self, code, protocol=1, pulselength=186, gpio=17):
        timestamp = str(datetime.datetime.now())
        logstr = '{} [{}: {:25} protocol: {}, pulselength: {}, code: {}'.format(
            timestamp, self.remote_button, self.name, protocol, pulselength, code)
        logging.info(logstr)
        history_logs.append((timestamp, self.remote_button, self.name, code))
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
            {rf_outlets}
            <div style="border: 2px solid indianred; font-size: 30px">
                <p>Pi last booted: {boot_time} </p>
                <p>Light control server started: {server_start_time} </p>

            </div>
            <table>
                <tr>
                    <td>Time</td>
                    <td>Remote Button</td>
                    <td>Designation</td>
                    <td>Code</td>
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
</tr>
"""

rf_entry_template = """
<div>
<span>
    {name}:
    <a href="/{id}/on">On</a>
    <a href="/{id}/off">Off</a>
</span>
</div>
"""


def get_history_logs():
    global history_logs
    return '\n'.join([history_log_template.format(*hlog) for hlog in history_logs[::-1]])


def get_rf_outlets():
    return '\n'.join([rf_entry_template.format(name=rf.name, id=rf.remote_button) for rf in rf_outlets.values()])


def render_template():
    global boot_time
    global server_start_time
    return index_html.format(history_log=get_history_logs(), rf_outlets=get_rf_outlets(), boot_time=boot_time, server_start_time=server_start_time)


def send_rf_outlet(lid, on=True):
    try:
        rf_outlet = rf_outlets[int(lid)]
        if on:
            rf_outlet.turn_on()
        else:
            rf_outlet.turn_off()
        return render_template()
    except Exception as e:
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
    app.run(host='0.0.0.0', port=9999)
