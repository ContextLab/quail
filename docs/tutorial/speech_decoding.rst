
Automated Speech Decoding
-------------------------

In a typical free recall experiment, after the experiment completes the
experimenter (or a team of experience-hungry undergraduates) will
manually transcribe the verbal responses from a subject by listening to
audio files, and coding each word. This process can take hours, and is
typically not exciting, to say the least. To help with this problem, we
created a ``decode_speech`` function, which wraps the Google Speech API
and a software package called ``ffmpeg`` to automatically transcribe the
responses. Furthermore, it allows the experimenter to transcribe in
(almost) realtime, which makes adaptive free recall experiments a
possibility. To use this feature (assuming that you are using a mac or
linux machine), you must first set up ffmpeg and Google Speech API:

Setting up ``ffmpeg``
---------------------

``ffmpeg`` is native application that processes audio and video files.
We will use it to convert .wav files to the .flac format, which will
allow us to send the files to Google Speech. To set up:

On a mac:
~~~~~~~~~

-  Make sure you have brew installed. If you don't, paste this into your
   terminal window:

``/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"``

-  Install ffmpeg

``brew install ffmpeg``

Setting up the Google Speech API
--------------------------------

Under the hood, ``quail`` uses the Google Speech API to transcribe audio
responses. Follow the instructions below to set it up. Note: the API is
not free, but its quite reasonable. Up to 60 minutes/month is free, and
after that it costs $0.006 per 15 seconds. For a typical study (16
study/test blocks) allowing for a minute of recall after each, the price
comes out to ~$0.38 per subject. To set it up, follow these steps:

1. Sign up for a Google Cloud account.

   -  https://cloud.google.com/ (you will need to enter a credit card
      number)

2. Create a project.

-  Click "Select a project", and create a new one. You can have a single
   project for all recall studies, or a separate project for each study.
   Then, navigate to your new project.

4. Enable to Speech API.

-  Click the "Dashboard" icon.
-  Click "Enable API"
-  Click "Speech API" which will be listed under "Google Cloud Machine
   Learning".
-  Click "Enable".

5. Set up a service account.

-  Click "Credentials".
-  Click "Create credentials" and select "Service account key".
-  Click "Service account" and select "new service account".
-  Name the account ("owner") and then select the role "Project->Owner".
-  Click "Create".

If you followed these steps, a JSON formatted API keyfile will be
downloaded to your local computer. This file is your ticket to speech
decoding, so keep it safe. Everything should now be setup! Below is a
basic example of how to use it:

::

    #import
    import quail

    # decode speech
    recall_data = quail.decode_speech('../data/sample.wav', keypath='path/to/keyfile.JSON')

    # print results
    print(recall_data)

Super-user tip:
~~~~~~~~~~~~~~~

The credentials can also be set up as an environmental variable. To do
this, edit your .bash\_profile, adding the line:

::

    export GOOGLE_APPLICATION_CREDENTIALS='/path/to/keyfile.JSON'

You'll need to launch a fresh terminal instance and then the
``decode_speech`` function should work without the explicit keypath:

::

    # decode speech
    recall_data = quail.decode_speech('../data/sample.wav')
