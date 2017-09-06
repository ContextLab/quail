import os
import base64
import json
import csv
import pickle
import time
import warnings

# optional imports for speech decoding
try:
    from google.cloud import speech
    from pydub import AudioSegment
except:
    pass


def decode_speech(path, keypath=None, save=False, speech_context=None,
                  sample_rate=44100, max_alternatives=1, language_code='en-US',
                  return_raw=False):
    """
    Decode speech for a file or folder and return results

    This function wraps the Google Speech API and ffmpeg to decode speech for
    free recall experiments.  Note: in order for this to work, you must have a
    Google Speech account, a google speech credentials file referenced in your
    _bash_profile, and ffmpeg installed on your computer.  See our readthedocs
    for more information on how to set this up:
    http://cdl-quail.readthedocs.io/en/latest/.

    Parameters
    ----------
    path : str
        Path to a wav file, or a folder of wav files.

    keypath : str
        Google Cloud Speech API key filepath. This is a JSON file containing
        credentials that was generated when creating a service account key.
        If None, assumes you have a local key that is set with an environmental
        variable. See the speech decoding tutorial for details.

    save : boolean
        False by default, but if set to true, will save a pickle with the results
        object from google speech, and a text file with the decoded words.

    speech_context : list of str
        This allows you to give some context to the speech decoding algorithm.
        For example, this could be the words studied on a given list, or all
        words in an experiment.

    sample_rate : float
        The sample rate of your audio files (default is 44100).

    max_alternatives : int
        You can specify the speech decoding to return multiple guesses to the
        decoding.  This will be saved in the results object (default is 1).

    language_code : str
        Decoding language code.  Default is en-US. See  here for more details:
        https://cloud.google.com/speech/docs/languages

    return_raw : boolean
        Intead of returning the parsed results objects (i.e. the words), you can
        return the raw reponse object.  This has more details about the decoding,
        such as confidence.

    Returns
    ----------
    words : list of str, or list of lists of str
        The results of the speech decoding. This will be a list if only one file
        is input, or a list of lists if more than one file is decoded.

    raw : google speech object, or list of objects
        You can optionally return the google speech object instead of the parsed
        results by using the return_raw flag.

    """

    # SUBFUNCTIONS
    def decode_file(file_path, client, speech_context, sample_rate, max_alternatives):

        def recognize(chunk, file_path):
            """
            Subfunction that loops over audio segments to recognize speech
            """
            # export as flac
            chunk.export(file_path + ".flac", format = "flac", bitrate="44.1k")

            # open flac file
            with open(file_path + ".flac", 'rb') as sc:
                speech_content = sc.read()

            # initialize speech sample
            sample = client.sample(content=speech_content,
                                encoding=speech.Encoding.FLAC,
                                sample_rate_hertz=sample_rate)

            # run speech decoding
            try:
                result = sample.recognize(**opts)
            except:
                result = None

            return result

        # set up speech decoding options dict
        opts = {}
        opts['language_code'] = language_code
        opts['max_alternatives'] = max_alternatives

        # load in speech context, note: max 500 words for speech context
        if speech_context:
                opts['speech_contexts']=speech_context

        # read in wav
        audio = AudioSegment.from_wav(file_path)

        # segment into 1 minute chunks
        if len(audio)>60000:
            segments = range(0,len(audio),60000)
            if segments[-1]<len(audio):
                segments.append(len(audio)-1)
            print('Audio clip is longer than 1 minute.  Splitting into %d one minute segments...' % (len(segments)-1))
            audio_chunks = []
            for i in range(len(segments)-1):
                audio_chunks.append(audio[segments[i]:segments[i+1]])
        else:
            audio_chunks = [audio]

        # loop over audio segments
        results = []
        for idx, chunk in enumerate(audio_chunks):
            results.append(recognize(chunk, file_path+str(idx)))

        # return list of results
        return results

    def parse_response(results):
        """Parses response from google speech"""
        words = []
        for idx, result in enumerate(results):
            if result is None:
                warnings.warn('No speech was decoded for segment %d' % (idx+1))
                words.append(None)
            else:
                try:
                    for segment in result:
                        for chunk in segment.transcript.split(' '):
                            if chunk != '':
                                words.append(str(chunk).upper())
                except:
                    warnings.warn('Error parsing response for segment %d' % (idx+1))

        return words

    # MAIN #####################################################################

    # initialize speech client
    if keypath:
        client = speech.Client.from_service_account_json(keypath)
    else:
        client = speech.Client()

    # make a list of files
    files = []
    if path.endswith(".wav"):
        files = [path]
    else:
        listdirectory = os.listdir(path)
        for filename in listdirectory:
            if filename.endswith(".wav"):
                files.append(path + filename)

    # initialize list of words
    words = []
    raw = []

    # loop over files
    for i, f in enumerate(files):

        # print progress
        print('Decoding file ' + str(i+1) + ' of ' + str(len(files)))

        try:

            # start timer
            start = time.time()

            # decode file
            results = decode_file(f, client, speech_context, sample_rate, max_alternatives)

            parsed_results = parse_response(results)

            # save the processed file
            words.append(parsed_results)

            # save the processed file
            raw.append(results)

            if save:
                # save the raw response in a pickle
                pickle.dump(results, open(f + ".p", "wb" ) )

                # save a text file with just the words
                with open(f + ".txt", 'w') as myfile:
                    wr = csv.writer(myfile,delimiter="\n")
                    wr.writerow(parsed_results)

            # print when finished
            print('Finished file ' + str(i+1) + ' of ' + str(len(files)) + ' in ' +
                  str(round(time.time()-start,2)) + ' seconds.')

        # handle when something goes wrong
        except ValueError as e:

            words.append("Error")
            print(e)
            print('Decoding of file ' + str(i) + 'failed.  Moving on to next file.')

    if return_raw:
        if len(words)>1:
            return raw
        else:
            return raw[0]
    else:
        if len(words)>1:
            return words
        else:
            return words[0]
