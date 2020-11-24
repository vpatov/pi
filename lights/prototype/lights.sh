#!/bin/bash

#2020-11-13 21:25:11 - [INFO] receive: 1406220 [pulselength 186, protocol 1]
#2020-11-13 21:25:12 - [INFO] receive: 1406211 [pulselength 185, protocol 1]
#2020-11-13 21:25:12 - [INFO] receive: 1406220 [pulselength 186, protocol 1]
#2020-11-13 21:25:12 - [INFO] receive: 1406220 [pulselength 186, protocol 1]
#2020-11-13 21:25:13 - [INFO] receive: 2097152 [pulselength 2213, protocol 4]
#2020-11-13 21:25:13 - [INFO] receive: 1406211 [pulselength 186, protocol 1]
#2020-11-13 21:25:13 - [INFO] receive: 2810115 [pulselength 83, protocol 3]
#2020-11-13 21:25:13 - [INFO] receive: 1406220 [pulselength 186, protocol 1]
#2020-11-13 21:25:14 - [INFO] receive: 1406220 [pulselength 186, protocol 1]
#2020-11-13 21:25:17 - [INFO] receive: 768 [pulselength 218, protocol 1]
#2020-11-13 21:25:17 - [INFO] receive: 12288 [pulselength 247, protocol 1]
#2020-11-13 21:25:17 - [INFO] receive: 64 [pulselength 1270, protocol 4]
#2020-11-13 21:25:18 - [INFO] receive: 1406211 [pulselength 185, protocol 1]
#2020-11-13 21:25:19 - [INFO] receive: 1406211 [pulselength 186, protocol 1]
#2020-11-13 21:25:19 - [INFO] receive: 1406211 [pulselength 187, protocol 1]
#2020-11-13 21:25:20 - [INFO] receive: 1406220 [pulselength 185, protocol 1]

#parser = argparse.ArgumentParser(description='Sends a decimal code via a 433/315MHz GPIO device')
#parser.add_argument('code', metavar='CODE', type=int,
#                    help="Decimal code to send")
#parser.add_argument('-g', dest='gpio', type=int, default=17,
#                    help="GPIO pin (Default: 17)")
#parser.add_argument('-p', dest='pulselength', type=int, default=None,
#                    help="Pulselength (Default: 350)")
#parser.add_argument('-t', dest='protocol', type=int, default=None,
#                    help="Protocol (Default: 1)")
#args = parser.parse_args()

if [ $1 == "off" ]; then
	python3 send.py -p 186 -t 1 1406220
fi
if [ $1 == "on" ]; then
	python3 send.py -p 186 -t 1 1406211
fi
