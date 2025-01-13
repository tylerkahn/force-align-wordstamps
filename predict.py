# Prediction interface for Cog ⚙️
# https://cog.run/python

from cog import BasePredictor, Path, Input
import stable_whisper
import json

# define a test string constant
# TEST_STRING = "On that road we heard the song of morning stars; we drank in fragrances aerial and sweet as a May mist; we were rich in gossamer fancies and iris hopes; our hearts sought and found the boon of dreams; the years waited beyond and they were very fair; life was a rose-lipped comrade with purple flowers dripping from her fingers."

def extract_flat_array(json_data, show_probabilities=False):
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
                            "probability": word_info.get("probability", 0) if show_probabilities else None,
                        }
                        # Append the dictionary to the result list
                        result.append(word_dict)
        
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return []  # Return an empty list in case of any failure

class Predictor(BasePredictor):
    def setup(self):
        """Load the model into memory"""
        self.model = stable_whisper.load_model('base')

    def predict(
        self,
        audio_file: Path = Input(description="Input audio file"),
        transcript: str = Input(description="Transcript text"),
        language: str = Input(description="Language", default="en"),
        show_probabilities: bool = Input(description="Show probabilities", default=False)
    ) -> dict:
        """Run prediction on the audio file and return the JSON data"""
        if transcript is None:
            # Perform transcription
            result = self.model.transcribe(str(audio_file))
        else:
            # Perform alignment
            aligned_result = self.model.align(str(audio_file), transcript, language=language)
            aligned_words = self.model.align_words(str(audio_file), aligned_result, language)
            result = self.model.refine(str(audio_file), aligned_words)

        # Extract flat array from JSON output
        flat_array = extract_flat_array(result.to_dict(), show_probabilities)

        # Return the result as a dictionary
        return {"output": flat_array}
