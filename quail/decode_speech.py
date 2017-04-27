import os
import base64
import json
import csv
import pickle
from google.cloud import speech
from pydub import AudioSegment


def decode_speech(path, save=False, speech_context=None,
                  sample_rate=44100, max_alternatives=1, language_code='en-US'):
    """
    Decode speech for a file or folder and return results
    """

    # SUBFUNCTIONS
    def decode_file(file_path, client, speech_context, sample_rate, max_alternatives):

        # set up speech decoding options dict
        opts = {}
        opts['language_code'] = language_code
        opts['max_alternatives'] = max_alternatives

        def parse_response(results):
            """Parses response from google speech"""
            words = []
            for result in results:
                for chunk in result.transcript.split(' '):
                    if chunk != '':
                        words.append(str(chunk).upper())
            return words

        # load in speech context, note: max 500 words for speech context
        if speech_context:
                opts['speech_context']=speech_context

        # read in wav
        audio = AudioSegment.from_wav(file_path)

        # export as flac
        audio.export(file_path + ".flac", format = "flac", bitrate="44.1k")

        # open flac file
        with open(file_path + ".flac", 'rb') as sc:
            speech_content = sc.read()

        # initialize speech sample
        sample = client.sample(content=speech_content,
                            encoding=speech.Encoding.FLAC,
                            sample_rate=sample_rate)

        # run speech decoding
        return sample.sync_recognize(**opts)


    # MAIN #####################################################################

    # initialize speech client
    client = speech.Client()

    # make a list of files
    files = []
    if path[-1] is '/':
        listdirectory = os.listdir(path)
        for filename in listdirectory:
            if filename.endswith(".wav"):
                files.append(path + filename)
    else:
        files = [path]

    # initialize list of words
    words = []

    # loop over files
    for f in files:

        # decode file
        results = decode_file(f, client, speech_context, sample_rate, max_alternatives)

        # save the processed file
        words.append(parse_response(results))

        if save:
            # save the raw response in a pickle
            pickle.dump(results, open(f + ".p", "wb" ) )

            # save a text file with just the words
            with open(f + ".txt", 'wb') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                wr.writerow(words)

    return words
