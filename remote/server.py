import signal
import sys
import time
import logging
import socket

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )
gpio = 27

class TestBackupRFDevice:
  def __init__(self, *kwargs):
    self.rx_code_timestamp = 1234
    self.rx_code = 4567

  def cleanup(self, *kwargs):
    pass

  def enable_rx(self, *kwargs):
    pass

hostname=socket.gethostname()

try:
  from rpi_rf import RFDevice
except:
  RFDevice = TestBackupRFDevice
  logging.error("Using fake RFDevice. All light controls will be no-ops")

rfdevice = None

# pylint: disable=unused-argument
def exithandler(signal, frame):
  rfdevice.cleanup()
  sys.exit(0)


def listen_for_rf_signals():
  rfdevice = RFDevice(gpio)
  prev_timestamp = None

  signal.signal(signal.SIGINT, exithandler) 
  rfdevice.enable_rx()

  logging.info("Listening for RF codes on GPIO {}".format(gpio))
  while True:
    try:
      if rfdevice.rx_code_timestamp != prev_timestamp:
        prev_timestamp = rfdevice.rx_code_timestamp
        code = rfdevice.rx_code
        logging.info("Received code: {}".format(code))
      time.sleep(1)
    except Exception as e:
      rfdevice.cleanup()
      logging.error(e.with_traceback())
      break


listen_for_rf_signals()
rfdevice.cleanup()
