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

   virtualenv .venv
   pip install -r requirements.txt
   ./watson_tts.py

Credentials
===========

In order to connect to the Watson streaming server you need username
and password. You can find these on your bluemix console for the
service you have added. The username looks like a UUID, the password
looks like a hash.

Copy speech.cfg.example to speech.cfg to ensure that's valid.


watson_tts.py
=============

The basic command just takes the argument on the command line and
converts it to speech, which is then routed directly to your audio.

You can do this with a quoted sentence like so.

::

   ./watson_tts.py "Mary had a little lamb, her fleece was white as snow."

You can also put any `SPR markup`_ that you desire if you are trying
to get sounds for words that aren't understood.

::

   ./watson_tts.py '<phoneme alphabet="ibm" ph=".0tx.1me.0Fo">tomato</phoneme>'

Because the files are cached in a local audio/ directory, only the
first use of a phrase will hit the network.

.. _SPR markup: https://www.ibm.com/watson/developercloud/doc/text-to-speech/SPRs.shtml
