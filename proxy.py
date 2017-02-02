#!/usr/bin/env python

# Copyright 2016 IBM All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import BaseHTTPServer

import requests

import os.path
import urllib2


class WatsonTTSServer(BaseHTTPServer.BaseHTTPRequestHandler):
    """A request handler to create a magic local Watson TTS server"""

    def do_POST(self):
        """ Translate a local HTTP request to Watson TTS """
        real_url = ("https://stream.watsonplatform.net/text-to-speech/api" +
                    self.path)
        # pull out the body to send
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)

        # make the real request
        resp = requests.post(real_url, headers=self.headers, data=post_body)

        # TODO(sdague): intermediate debugging, keep a copy around.
        with open("proxytmp.wav", 'wb') as f:
            f.write(resp.content)

        # Process request back to client
        self.send_response(resp.status_code)
        for header in resp.headers:
            # Requests has now decoded the response so some
            # characteristics of this may no longer be relevant. Don't
            # send them.
            if header not in ("connection", "content-length",
                              "keep-alive"):
                self.send_header(header, resp.headers[header])

        self.end_headers()
        # The client expects chunked encoding, which is just a way to
        # stream data as it shows up with per line content length. We
        # already have *all* the data, so we can send a single line
        # which has it all with the right length.
        tosend = '%X\r\n%s\r\n' % (len(resp.content), resp.content)
        self.wfile.write(tosend)
        # Then we need to send the null to signal to the client that
        # we're done and it should close out shop.
        self.wfile.write('0\r\n\r\n')


def parse_opts():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-p', '--port',
                        help='port to bind to [default: 8888]',
                        type=int,
                        default=8888)
    return parser.parse_args()


def main():
    opts = parse_opts()
    server_address = ('', opts.port)
    httpd = BaseHTTPServer.HTTPServer(server_address, WatsonTTSServer)

    print "Test Server is running at http://localhost:%s" % opts.port
    print "Ctrl-C to exit"
    print

    while True:
        httpd.handle_request()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "\n"
        print "Thanks for testing! Please come again."
