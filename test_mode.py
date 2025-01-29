import stable_whisper
import json

def extract_flat_array(json_data):
    try:
        # Load JSON data if it's a string, or use it directly if it's already a dict
        data = json.loads(json_data) if isinstance(json_data, str) else json_data

        # Initialize the result list
        result = []

        # Check if 'segments' key is in the dictionary and iterate through each segment
        if 'segments' in data:
            for segment in data['segments']:
                # Check if 'words' key is in the segment dictionary
                if 'words' in segment:
                    for word_info in segment['words']:
                        # Create a dictionary with the desired keys
                        # trim the space around the word
                        word = word_info.get("word", "").strip()
                        word_dict = {
                            "word": word,
                            "start": word_info.get("start", 0),
                            "end": word_info.get("end", 0),
                            # "probability": word_info.get("probability", 0),
                        }
                        # Append the dictionary to the result list
                        result.append(word_dict)
        
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return []  # Return an empty list in case of any failure

# Usage example (assuming 'input_json' contains the JSON data as a string or dictionary)
input_json = '{"text": " On that road ..."}'  # Placeholder for actual JSON data
flat_array = extract_flat_array(input_json)
print(flat_array)

model = stable_whisper.load_model('base')
text = 'On that road we heard the song of morning stars; we drank in fragrances aerial and sweet as a May mist; we were rich in gossamer fancies and iris hopes; our hearts sought and found the boon of dreams; the years waited beyond and they were very fair; life was a rose-lipped comrade with purple flowers dripping from her fingers.'

aligned_result = model.align('audio.mp3', text, language='en')
aligned_words = model.align_words('audio.mp3', aligned_result, 'English')

result = model.refine('audio.mp3', aligned_words)

result.to_srt_vtt('audio.srt', word_level=True)
result.to_srt_vtt('audio.vtt') #VTT
result.to_ass('audio.ass') #ASS
result.to_tsv('audio.tsv') #TSV
result.save_as_json('audio.json')

# open json file
with open('audio.json', 'r') as f:
    data = json.load(f)

flat_array = extract_flat_array(data)

# save flat array to file
with open('audio_flat_array.json', 'w') as f:
    json.dump(flat_array, f)


# Log the result to a file
# with open('result.log', 'w') as f:
#     f.write('Transcription:\n')
#     f.write(result.transcription + '\n\n')
#     f.write('Alignment:\n')
#     for segment in result.segments:
#         f.write(f'{segment.text} ({segment.start:.2f} - {segment.end:.2f})\n')
