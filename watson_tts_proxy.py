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
try:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
except ImportError:
    from http.server import HTTPServer, BaseHTTPRequestHandler
import hashlib
from os.path import join, dirname, exists

import requests


class WatsonTTSServer(BaseHTTPRequestHandler):
    """A request handler to create a magic local Watson TTS server"""

    def fake_headers(self):
        # TODO(sdague): really do the right content type

        return {
            "content-type": "audio/wav",
            "content-disposition": 'inline; filename="result.wav"',
            "transfer-encoding": "chunked",
        }

    def do_POST(self):
        """ Translate a local HTTP request to Watson TTS """
        real_url = ("https://stream.watsonplatform.net/text-to-speech/api" +
                    self.path)
        # pull out the body to send
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # make a content addressable local storage path based on
        # string args (which is voice & audio type) and body, which is
        # the text to be sent. This should be a good unique seed.
        hash_seed = self.path.encode('utf-8') + post_body
        fname = hashlib.sha256(hash_seed).hexdigest() + ".wav"
        fullfile = join(dirname(__file__), "audio", fname)
        if not exists(fullfile):
            # make the real request
            resp = requests.post(real_url, headers=self.headers,
                                 data=post_body)

            # TODO(sdague): intermediate debugging, keep a copy around.
            with open(fullfile, 'wb') as f:
                f.write(resp.content)
                print("Wrote cached content to %s" % fullfile)

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
            content = resp.content
            self.wfile.write(('%X\r\n' % len(content)).encode('utf-8'))
            self.wfile.write(content)
            self.wfile.write(b'\r\n')

        else:
            print("Reading from cached content")
            self.send_response(200)
            for k, v in self.fake_headers().items():
                self.send_header(k, v)
            self.end_headers()
            with open(fullfile, 'rb') as f:
                content = f.read()
                self.wfile.write(('%X\r\n' % len(content)).encode('utf-8'))
                self.wfile.write(content)
                self.wfile.write(b'\r\n')

        # Then we need to send the null to signal to the client that
        # we're done and it should close out shop.
        self.wfile.write(b'0\r\n\r\n')


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
    httpd = HTTPServer(server_address, WatsonTTSServer)

    print("Test Server is running at http://localhost:%s" % opts.port)
    print("Ctrl-C to exit")
    print

    while True:
        httpd.handle_request()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        print("Thanks for testing! Please come again.")
