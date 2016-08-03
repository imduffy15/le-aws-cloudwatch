import logging
import json
import gzip
import socket
from StringIO import StringIO

logger = logging.getLogger()
logger.setLevel(logging.INFO)
HOST = 'localhost'
PORT = 9563


def lambda_handler(event, context):
    # Create socket connection to logstash
    sock = create_socket()

    # get CloudWatch logs
    cw_data = str(event['awslogs']['data'])

    # decode and uncompress CloudWatch logs
    cw_logs = gzip.GzipFile(fileobj=StringIO(
        cw_data.decode('base64', 'strict'))).read()

    # convert the log data from JSON into a dictionary
    log_events = json.loads(cw_logs)

    # loop through the events and send to logstash
    for log_event in log_events['logEvents']:

        # look for extracted fields, if not present, send plain message
        try:
            send_to_logstash(json.dumps(
                log_event['extractedFields']), sock)
        except KeyError:
            send_to_logstash(log_event['message'], sock)

    # close socket
    sock.close()


def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
        return s
    except socket.error, exc:
        print "Caught exception socket.error : %s" % exc


def send_to_logstash(line, logstash_socket):
    logstash_socket.sendall('%s\n' % (line))
