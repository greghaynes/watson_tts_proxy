==================
 Watson TTS Proxy
==================

This project is attempting to create an HTTP proxy service for Watson
that makes it possible to use Watson TTS in a network poor
environment. All Text chunks are encoded and create content
addressable local files so that future attempts to encode the same
text just shortcut and use the same files.

Installation
============

Currently this is just a simple set of scripts that run under a python
virtualenv. To get this working do the following:

::

   cd watson_tts_proxy
   virtualenv .venv
   pip install -U .

Credentials
===========

In order to connect to the Watson streaming server you need username
and password. You can find these on your bluemix console for the
service you have added. The username looks like a UUID, the password
looks like a hash.

Copy speech.cfg.example to speech.cfg to ensure that's valid.


watson-tts
==========

The basic command just takes the argument on the command line and
converts it to speech, which is then routed directly to your audio.

You can do this with a quoted sentence like so.

::

   watson-tts "Mary had a little lamb, her fleece was white as snow."

You can also put any `SPR markup`_ that you desire if you are trying
to get sounds for words that aren't understood.

::

   watson-tts '<phoneme alphabet="ibm" ph=".0tx.1me.0Fo">tomato</phoneme>'

Because the files are cached in a local audio/ directory, only the
first use of a phrase will hit the network.


watson-tts-proxy
================

There are times when you want to interact with the Watson TTS service,
but may have intermittent network. In order to handle this scenario we
have built a transparent caching proxy for Watson TTS service.

This service is started by running:

::

   watson-tts-proxy

By default this starts a service listening on
http://localhost:8888. You can specify a different port with the `-p`
option.

Once a particular phrase is fetched from Watson it's cached locally so
that future calls with the same phrase don't require the network.

watson-tts-proxy-client
=======================

The watson_tts_proxy_client.py is just a version of watson_tts.py
program which works against the proxy server.

.. _SPR markup: https://www.ibm.com/watson/developercloud/doc/text-to-speech/SPRs.shtml
