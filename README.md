# MIDI2ScoreTransformer
Code for the ISMIR 2024 paper ["End-to-end Piano Performance-MIDI to Score Conversion with Transformers"](https://arxiv.org/abs/2410.00210)

## Installation
The code is written in Python 3.11 and relies on the following packages
- everything mentioned in `requirements.txt`
- `MuseScore`: https://github.com/musescore/MuseScore (depending on your platform, please adjust the path in `constants.py`)


Due to delays and difficulties merging changes with upstream versions, we currently require installing custom versions of the following packages (will be done automatically with `requirements.txt`):

- `music21`: https://github.com/TimFelixBeyer/music21 (fixes tie-stripping and contains various other tweaks)
- `score_transformer`: https://github.com/TimFelixBeyer/ScoreTransformer (for score_similarity metrics and tokenization comparisons)

In addition, you must manually clone and install this package:
- `muster`: https://github.com/TimFelixBeyer/amtevaluation.github.io (fixes various memory leak issues of the original version)

### Datasets
Please use this version of the ASAP-Dataset as it contains some fixes.

- `ASAPDataset`: [https://github.com/TimFelixBeyer/ASAPDataset](https://github.com/TimFelixBeyer/asap-dataset/tree/8cba199e15931975542010a7ea2ff94a6fc9cbee) (contains a few fixes for the ASAP dataset, make sure you select the correct commit for reproducibility and place the `asap-dataset` folder into the `data` folder).
- `ACPAS`: [https://cheriell.github.io/research/ACPAS_dataset/](https://cheriell.github.io/research/ACPAS_dataset/) (only download `metadata_R.csv` and `metadata_S.csv`, place them into a folder called `ACPAS-dataset` and put it into the `data` folder)

Afterwards, your `data` folder should look like this:
```
data
├── ACPAS-dataset
│   ├── metadata_R.csv
│   └── metadata_S.csv
└── asap-dataset
```

### Setup (Inference)
 Download pre-trained model:
   - Get [`MIDI2ScoreTF.ckpt`](https://github.com/TimFelixBeyer/MIDI2ScoreTransformer/releases) from Releases
   - Place in project root directory

## Usage
Convert MIDI files to MusicXML scores:

```bash
python inference.py path/to/input.midi [OPTIONS]
```

### Options:
| Flag           | Description                                  | Default                  |
|----------------|----------------------------------------------|--------------------------|
| `-m`, `--model` | Path to model checkpoint                    | `MIDI2ScoreTF.ckpt`      |
| `-o`, `--output`| Custom output path (.xml)                   | `<input_name>.xml`       |

### Example Commands
1. Basic conversion (uses default model and output name):
```bash
python inference.py my_piano_performance.mid
```

2. Custom output path and model:
```bash
python inference.py jazz_improvisation.mid -m custom_model.ckpt -o jazz_score.xml
```

### Setup (Training)
1. Run `dataset.py` to preprocess the datasets and populate the cache.
2. Run `chunker.py` to create the beat-aligned chunks.
3. More instructions to follow
