======================================
 Installation Instructions on Windows
======================================

Tested on Windows 7 & 10

Install Python
==============

Go to http://python.org and click on Downloads -> Install Python 3.6.

Run the installer, and check the box for "Include Python in Path"

Download the Code
=================

Download the code from https://github.com/ibm-dev/watson_tts_proxy
under Clone or Download.

Expand it wherever is convenient.

Configure Server
================

You have to configure a `speech.cfg` as per the main readme. It needs
to be in the directory you extracted above.

Running the Server
==================

Open a CMD Prompt.

cd to the directory where the watson_tts_proxy code is.

Run::

  pip install -r requirements.txt

  python watson_tts_proxy.py

Testing the Server
==================

In another CMD prompt

Run::

  python watson_tts_proxy_client.py "Hello There"

You should see the request being processed by the proxy server, and
hear "Hello There" spoken through your speakers.
