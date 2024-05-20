#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Downloads all the articles from the Tulu language WikiPedia and preprocesses 
them to get a monolingual dataset of sentences in Tulu language. The latest
articles from the Tulu language wikipedia are downloaded from 
"https://dumps.wikimedia.org/tcywiki/latest/tcywiki-latest-pages-articles-multistream.xml.bz2"

Usage:
    python tcy_wikipedia_downloader.py
    
"""

import urllib.request
import bz2
import subprocess
import os

import sys
from pathlib import Path

from blingfire import text_to_sentences

import unicodedata

print(os.getcwd())

# URL of the Wikimedia dump file (Tulu Wikipedia)
url_tcywiki = 'https://dumps.wikimedia.org/tcywiki/latest/tcywiki-latest-pages-articles-multistream.xml.bz2'

# Download the file
with urllib.request.urlopen(url_tcywiki) as response:
    compressed_file = response.read()

# Decompress the data
decompressed_file = bz2.decompress(compressed_file)

# Save the decompressed file
decompressed_file_path = 'tcywiki-latest-pages-articles-multistream.xml'
with open(decompressed_file_path, 'wb') as file:
    file.write(decompressed_file)

print("Processing the Wikimedia dump file...")

# Shell script downloaded from https://gist.github.com/sgraaf/7c061824b1c57c292faa0a123d95a714#file-extract_and_clean_wiki_dump-sh
shell_script_path = 'extract_and_clean_wiki_dump.sh'

# Make the shell script executable
subprocess.run(['chmod', '+x', shell_script_path])

# Run the shell script on the decompressed file
subprocess.run([f'./{shell_script_path}', decompressed_file_path])

# Delete the temporary decompressed file
os.remove(decompressed_file_path)

print(f"Extraction and cleaning completed. The output is in {decompressed_file_path.replace('.xml', '.txt')}")


# preprocess_wiki_dump: https://gist.github.com/sgraaf/926c52fba668f779f5ecac81d21e98a0#file-preprocess_wiki_dump-py

wiki_dump_file_in = decompressed_file_path.replace('.xml', '.txt')
wiki_dump_file_out = decompressed_file_path.replace('.xml', '_preprocessed.txt')

print(f'Pre-processing {wiki_dump_file_in} to {wiki_dump_file_out}...')
"""
with open(wiki_dump_file_out, 'w', encoding='utf-8') as out_f:
    with open(wiki_dump_file_in, 'r', encoding='utf-8') as in_f:
        for line in in_f:
            sentences = text_to_sentences(line)

            # check if at least half of the characters in each line are Kannada characters (to ensure quality)
            len_sentence = len(sentences)
            num_kannada = 0
            for characters in sentences:
                try:
                    # Attempt to get the Unicode name for the character
                    name_unicode = unicodedata.name(characters)
                    # Count if it is a Kannada character
                    if 'KANNADA' in name_unicode:
                        num_kannada = num_kannada + 1
                        
                except ValueError:
                    # If ValueError is raised, the character has no Unicode name
                    pass
            if num_kannada >= len_sentence/2:
                out_f.write(sentences + '\n')
                 
print(f'Successfully pre-processed {wiki_dump_file_in} to {wiki_dump_file_out}...')
"""
# Read the document
with open(wiki_dump_file_in, 'r', encoding='utf-8') as in_f:
    lines = in_f.readlines()

sentences = []
for line in lines:
    sentence = text_to_sentences(line)
    sentences.extend(sentence.split('\n'))

print(f"Number of lines after blingfire: {len(sentences)}")

# Use a set to store unique lines
unique_sentences = set()

processed_sentences = []

for sentence in sentences:
        # Strip leading and trailing whitespace
        sentence = sentence.strip()
        # Remove redundant spaces within the line
        sentence = ' '.join(sentence.split())
        
        # Check if the line contains more than one word
        if len(sentence.split()) > 1:
            # Check if the line is unique
            if sentence not in unique_sentences:
                # check if at least half of the characters in each line are Kannada characters (to ensure quality)
                len_sentence = len(sentence)
                num_kannada = 0
                
                for character in sentence:
                    try:
                        # Attempt to get the Unicode name for the character
                        name_unicode = unicodedata.name(character)
                        # Count if it is a Kannada character
                        if 'KANNADA' in name_unicode:
                            num_kannada = num_kannada + 1
                            
                    except ValueError:
                        # If ValueError is raised, the character has no Unicode name
                        pass
                
                if num_kannada >= len_sentence/2:
                    unique_sentences.add(sentence)
                    processed_sentences.append(sentence)
                    
print(f"Number of lines in the end: {len(processed_sentences)}")
# Write the preprocessd lines to a file
with open(wiki_dump_file_out, 'w', encoding='utf-8') as out_f:
    for line in processed_sentences:
            out_f.write(line + '\n')
            
print(f'Successfully pre-processed {wiki_dump_file_in} to {wiki_dump_file_out}...')

