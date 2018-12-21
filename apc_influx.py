# Python script to read UPS Data from an APC USV using apcaccess
import subprocess
import re
from influxdb import InfluxDBClient

# Configuration InfluxDB
INFLUX_URL = '192.168.10.81'
INFLUX_PORT = 8086
INFLUX_DB = 'usv'

INFLUX = InfluxDBClient(INFLUX_URL, INFLUX_PORT, '', '', INFLUX_DB)

# Run apcaccess and save output in out
prc = subprocess.Popen(["/sbin/apcaccess", "status"], stdout=subprocess.PIPE)
out = prc.communicate()[0].decode("utf-8")

# Select attributes
attributes=["LOADPCT", "BCHARGE", "TIMELEFT", "NOMPOWER"]


# Parse apcaccess and send selected attributes to influx
for attribute in attributes:
  attrib_value = re.search(r'{}\s*:\s([\d]+)'.format(attribute), out)
  INFLUX_PAYLOAD = [
    {
      "measurement": "APC",
      "tags": {
        "type": "APC"
      },
        "fields": {
          "{}".format(attribute): int(attrib_value.group(1))
      }
    }
  ]
  INFLUX.write_points(INFLUX_PAYLOAD)
