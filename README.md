# Force align transcript to audio

## Introduction

WhisperX provides word-level timestamps for audio files, but often you'll need to "force align" audio **perfectly** to source-of-truth transcript text. This capability is offered by [stable-ts](https://github.com/jianfch/stable-ts).

Here we've created an opinionated isolation of stable-ts's alignment methods. We've wrapped this logic in a Cog interface and simplified its outputs so it can used as a standalone endpoint, e.g., on [replicate.com](https://replicate.com/cureau/force-align-wordstamps).

If your audio is extremely clean (e.g., AI-generated), you can use a lighter weight model like [forced-alignment-model](https://github.com/quinten-kamphuis/forced-alignment-model) based of the Meta's torchaudio's MMS model. But even a little background noise can throw off the outputs.

## Table of Contents

- [Force align transcript to audio](#force-align-transcript-to-audio)
  - [Introduction](#introduction)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
    - [Inference](#inference)
  - [Self-hosted Installation](#self-hosted-installation)
    - [Prerequisites](#prerequisites)
    - [Setup](#setup)
  - [Usage](#usage)
  - [API Reference](#api-reference)
    - [`predict.py`](#predictpy)
      - [Constants](#constants)
      - [Functions](#functions)
      - [Classes](#classes)
  - [Example](#example)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgements](#acknowledgements)
  - [Contact](#contact)
  - [Getting Help](#getting-help)

## Features

- **Transcription:** Convert audio files into text using the `stable_whisper` model.
- **Alignment:** Align provided transcripts with audio files to enhance accuracy.
- **Probability Scores:** Optionally display word-level probability scores.
- **Flexible Inputs:** Supports various input configurations, including specifying language and transcript text.

### Inference

Use the [Replicate](https://replicate.com/cureau/force-align-wordstamps) model as-is.

[![Replicate](https://replicate.com/cureau/force-align-wordstamps/badge)](https://replicate.com/cureau/force-align-wordstamps)

## Self-hosted Installation

### Prerequisites

- Python 3.12
- [Cog](https://cog.run/) installed

### Setup

**Clone the Repository**

   ```bash
   git clone https://github.com/crone-ai/force-align-wordstamps
   cd your-repo-name
   ```

**Create a Virtual Environment**

   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   ```

**Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

**Install Cog**

   Follow the [Cog installation guide](https://cog.run/docs/introduction) to install Cog and set it up if using replicate, or deploying to a containerized environment.

## Usage

The primary functionality is encapsulated in the `predict.py` file, which defines a `Predictor` class compatible with Cog. Here's how to use it:

1. **Configure `cog.yaml`**

   Ensure that your `cog.yaml` is properly configured to use the `Predictor` class from `predict.py`.

   ```yaml
   build:
     python_version: "3.12"
     pip:
       install:
         - -r requirements.txt

   predict:
     - python predict.py
   ```

2. **Run Prediction**

   Use Cog's CLI to run predictions.

   ```bash
   cog predict --audio_file path/to/audio.mp3 --transcript "Your transcript here" --language "en" --show_probabilities
   ```

## API Reference

### `predict.py`

#### Constants

- **TEST_STRING**

  A default transcript used for alignment if no transcript is provided.

  ```python
  TEST_STRING = "On that road we heard the song of morning stars; we drank in fragrances aerial and sweet as a May mist; we were rich in gossamer fancies and iris hopes; our hearts sought and found the boon of dreams; the years waited beyond and they were very fair; life was a rose-lipped comrade with purple flowers dripping from her fingers."
  ```

#### Functions

- **`extract_flat_array(json_data, show_probabilities=False)`**

  Extracts a flat array of words with their timings and optional probabilities from the JSON output.

  - **Parameters:**
    - `json_data` (str or dict): The JSON data to extract from.
    - `show_probabilities` (bool): Whether to include probability scores.

  - **Returns:** `list` of word dictionaries.

#### Classes

- **`Predictor(BasePredictor)`**

  The main predictor class for Cog.

  - **Methods:**
    - `setup(self)`: Loads the `stable_whisper` model into memory.
    - `predict(self, audio_file, transcript, language, show_probabilities)`: Performs transcription or alignment based on inputs and returns the results.

## Example

Here's a simple example of how to use the predictor:

```bash
cog predict \
--audio_file "audio.mp3" \
--transcript "Sample transcript text." \
--language "en" \
--show_probabilities
```

** Response:

```json
{
  "output": [
    {
      "word": "On",
      "start": 0,
      "end": 0.1
    },
    {
      "word": "that",
      "start": 0.1,
      "end": 0.2
    },
    {
      "word": "road",
      "start": 0.2,
      "end": 0.3
    },
    ...
  ]
}
```


## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/YourFeature`.
5. Open a pull request.

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

These key projects are behind the prediction interface:

- [**stable-ts**](https://github.com/jianfch/stable-ts): Developed by Jian, this project enhances transcription accuracy by stabilizing timestamps in OpenAI's Whisper model.

- [**faster-whisper**](https://github.com/guillaumekln/faster-whisper): A reimplementation of OpenAI's Whisper model using CTranslate2, offering up to 4 times faster transcription with reduced memory usage.

## Contact

For any questions or suggestions, please open an issue in the repository or contact [kyle@crone.ai](mailto:kyle@crone.ai).

## Getting Help

If you encounter any issues or have questions, feel free to reach out by opening an issue in the repository.