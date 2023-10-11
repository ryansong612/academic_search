import os
import datetime
import tiktoken
import string

def TokenCheck(msg):
    content = msg.get("content", "")
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-16k-0613")
    tokens = encoding.encode(content)
    token_count = len(tokens)
    return token_count

def SplitParagraph(paragraphs):
    # Creating a list to store the split segments
    split_segments = []
    segment_id = 1

    block_count = 450
    for paragraph in paragraphs:
        # Splitting the paragraph into sentences
        sentences = paragraph['content'].split('. ')

        # Initializing variables
        current_segment = ""

        for sentence in sentences:
            # Checking if adding the current sentence exceeds the maximum length
            if TokenCheck({"content": current_segment + sentence}) >= block_count:
                # Appending the current segment to the list
                split_segments.append({
                    "id": segment_id,
                    "content": current_segment.strip(),
                    "source": paragraph.get('source'),
                    "time": paragraph.get('time')
                })
                segment_id += 1 # Incrementing the segment ID
                current_segment = "" # Resetting the current segment

            current_segment += sentence + '. '   # Adding the current sentence to the current segment

        # Appending the remaining segment (if any)
        if current_segment:
            split_segments.append({
                "id": segment_id,
                "content": current_segment.strip(),
                "source": paragraph.get('source'),
                "time": paragraph.get('time')
            })

        segment_id += 1 # Incrementing the segment ID for the next paragraph

        for item in split_segments:
            content = item['content']
            punctuation_count = content.count(',') + content.count('.')
            if punctuation_count > 40:
                split_segments.remove(item)

    return split_segments

def GetFolderFileList(folder_path):
    file_names = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_names.append(file_name)
    return file_names

def DateString():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")
    return formatted_datetime

def separate_words_and_punctuations(input_string):
    words = []
    punctuations = []
    word_buffer = []
    for char in input_string:
        if char in string.whitespace:
            if word_buffer:
                words.append(''.join(word_buffer))
                word_buffer = []
        elif char in string.punctuation:
            if word_buffer:
                words.append(''.join(word_buffer))
                word_buffer = []
            punctuations.append(char)
        else:
            word_buffer.append(char)
    
    if word_buffer:
        words.append(''.join(word_buffer))
    return words, punctuations

def punctuationPercentage(msg):
    words, punctuations = separate_words_and_punctuations(msg)
    try:
        percentage = len(punctuations) / len(punctuations + words)
    except:
        return 0
    return percentage
        