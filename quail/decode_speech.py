from __future__ import print_function
from builtins import str
from builtins import range
import os
import json
import csv
import pickle
import time
import warnings
import pandas as pd

# optional imports for speech decoding
try:
    import whisper
    HAS_WHISPER = True
except ImportError:
    HAS_WHISPER = False


def decode_speech(path, model_size='base', save=False, return_raw=False, **kwargs):
    """
    Decode speech for a file or folder and return results using OpenAI Whisper.

    Parameters
    ----------
    path : str
        Path to a wav file, or a folder of wav files.

    model_size : str
        Whisper model size: 'tiny', 'base', 'small', 'medium', 'large'.
        Default is 'base'.

    save : boolean
        False by default. If true, saves results object (pickle) and text transcript.

    return_raw : boolean
        If True, returns the full Whisper result dictionary. 
        If False (default), returns a list of (WORD, START, END) tuples.
        
    **kwargs : dict
        Additional arguments passed to whisper.transcribe (e.g. language).

    Returns
    ----------
    words : list of str, or list of lists of str
        The results of the speech decoding.
    """
    
    if not HAS_WHISPER:
        raise ImportError("openai-whisper not installed. pip install openai-whisper")

    # Load model
    print(f"Loading Whisper model: {model_size}...")
    model = whisper.load_model(model_size)
    print("Model loaded.")

    # make a list of files
    files = []
    if path.endswith(".wav") or path.endswith(".mp3") or path.endswith(".m4a") or path.endswith(".flac"):
        files = [path]
    elif os.path.isdir(path):
        listdirectory = os.listdir(path)
        for filename in listdirectory:
            if filename.lower().endswith((".wav", ".mp3", ".m4a", ".flac")):
                files.append(os.path.join(path, filename))
    else:
        raise ValueError("Path must be an audio file or directory of audio files.")

    # initialize results
    results = []
    
    # loop over files
    for i, f in enumerate(files):
        print('Decoding file ' + str(i+1) + ' of ' + str(len(files)) + f": {f}")
        start = time.time()
        
        try:
            # Decode
            # Whisper expects path or array. Path is fine.
            # word_timestamps=True needed for offsets
            result = model.transcribe(f, word_timestamps=True, **kwargs)
            
            if return_raw:
                parsed = result
            else:
                # Parse into (WORD, START, END) format matching Quail legacy
                parsed = []
                for segment in result['segments']:
                    # Ensure words are available
                    if 'words' in segment:
                         for w in segment['words']:
                             parsed.append((w['word'].strip().upper(), w['start'], w['end']))
                    else:
                        # Fallback if no word level timestamps (shouldn't happen with word_timestamps=True)
                        # Just split text? Timestamps will be approximate segment level
                        text = segment['text'].strip().upper()
                        for t_word in text.split():
                             parsed.append((t_word, segment['start'], segment['end']))

            # Save
            if save:
                # save raw pickle
                with open(f + ".p", "wb") as pfile:
                    pickle.dump(result, pfile)
                
                # save text
                if not return_raw:
                     pd.DataFrame(parsed).to_csv(f + '.txt', header=False, index=False)
                else:
                    with open(f + '.txt', 'w') as tfile:
                        tfile.write(result['text'])

            results.append(parsed)
            
            print('Finished in ' + str(round(time.time()-start,2)) + ' seconds.')

        except Exception as e:
            print(f"Error decoding {f}: {e}")
            results.append("Error")

    if len(results) == 1:
        return results[0]
    else:
        return results
