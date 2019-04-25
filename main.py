import base64
import getopt
import json
import logging
import paho.mqtt.client as mqtt
import os
import subprocess, sys
import time


def on_subscribe(mqclient, mquserdata, mid, granted_qos):
    """Methode wird nach dem Verbindungsaufbau mit der Queue aufgerufen"""
    logger.info("Subscribed: "+str(mid)+" "+str(granted_qos))


def on_message(mqclient, mquserdata, msg):
    """Methode wird bei neuen Nachrichten aufgerufen"""
    logger.info("Neuen Druckauftrag empfangen.")
    msgbody = json.loads(msg.payload)
    save_file(msgbody)
    options = msgbody["options"]
    options.insert(0, "lp")
    options.append("%s/%s" % (os.getcwd(), msgbody["filename"]))
    print_file(options)
    time.sleep(15)
    os.remove(msgbody["filename"])
    logger.info("Verarbeitung abgeschlossen")


def save_file(msgbody):
    file_decoded = base64.decodebytes(bytearray(msgbody["file"], "UTF-8"))
    decode_result = open(msgbody["filename"], 'wb')
    decode_result.write(file_decoded)
    logger.info("Neue Datei: " + str(msgbody["filename"]))
    decode_result.close()


def print_file(options):
    """Print a given pdf-file. path must be absolute."""
    logger.info("Drucke mit Aufruf: " + str(options))
    returncode = subprocess.run(options)
    logger.info("Druck liefert ReturnCode: " + str(returncode.returncode))


def main(argv):
    user = ""
    password = ""
    host = ""
    port = 0
    topic = ""

    try:
        opts, args = getopt.getopt(argv, "u:c:h:p:t:")
    except getopt.GetoptError:
        print("main.py -u <user> -c <password> -h <host> -p <port> -t <topic>")
        sys.exit(2)

    if len(opts) == 0 or len(opts) > 5:
        print("main.py -u <user> -c <password> -h <host> -p <port> -t <topic>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-u":
            user = arg
        elif opt == "-c":
            password = arg
        elif opt == "-h":
            host = arg
        elif opt == "-p":
            port = int(arg)
        elif opt == "-t":
            topic = arg

    client = mqtt.Client("pyPrintHelper")
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.username_pw_set(user, password)
    client.connect(host, port=port)
    client.subscribe(topic, qos=1)

    client.loop_forever()


if __name__ == "__main__":
    # create logger with 'spam_application'
    logger = logging.getLogger('mqtt')
    logger.setLevel(logging.INFO)
    # create file handler which logs even debug messages
    # fh = logging.StreamHandler()
    fh = logging.FileHandler('pyPrintHelper.log')
    fh.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)

    main(sys.argv[1:])
