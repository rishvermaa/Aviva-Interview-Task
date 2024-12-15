#Importing relevant libraries
import pandas as pd
import json
import re
import uuid
from collections import Counter
from datetime import datetime


def count_common_words(json_file: str):
    #Loading the file with exception handling
    try:
        with open(json_file, 'r') as file:
            petitions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading file: {e}")
        return

    #Defined a function to extract words that are 5+ letters
    def find_words(text):
        return re.findall(r'\b\w{5,}\b', text)

    #Counting all words across all petitions
    all_words = []  #List to hold all words from all petitions
    for petition in petitions:
        abstract = petition.get('abstract', {}).get('_value', '')
        label = petition.get('label', {}).get('_value', '')
        combined = (f"{abstract} | {label}".lower())
        #Extracting words and adding them to the list
        all_words.extend(find_words(combined))

    #Finding the 20 most common words
    repitive_words = [word for word, _ in Counter(all_words).most_common(20)]

    #Counting words for each petition and assigning unique ID
    data = []
    for petition in petitions:
        uid = str(uuid.uuid4())[:8]
        abstract = petition.get('abstract', {}).get('_value', '')
        label = petition.get('label', {}).get('_value', '')
        combined_text = (f"{abstract} | {label}".lower())
        # Count occurrences of each common word in the petition text
        word_count = {word: len(re.findall(r'\b' + re.escape(word) + r'\b', combined_text)) for word in repitive_words}
        word_count['petition_uid'] = uid
        data.append(word_count)

    #Stopping empty files to be generated
    if not data or not repitive_words:
        print('No files generated as there is no data to process.')
        return

    else:        
        timestamp = datetime.now().strftime('%Y%m%d_%H_%M_%S')
        output_file = f"Output_Data_{timestamp}.csv"    
        df = pd.DataFrame(data, columns=['petition_uid'] + repitive_words)
        df.to_csv(output_file, index=False)
        print(f"Export data created successfully: {output_file}")
