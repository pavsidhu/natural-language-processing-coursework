# Natural Language Processing Asssignment

## Installation

`pip install -r requirements.txt`

### Downloads

Place these downloads in the root folder.

- Training emails should go in `training/`
- Untagged emails should go in `untagged/`
- Data sets
  - `GoogleNews-vectors-negative300.bin`
- Stanford NER Tagger
  - `stanford-ner.jar`
  - `english.all.3class.distsim.crf.ser.gz`

## Usage

```
python main.py [train, test, ontology]
```

- `Train` uses the training set, removes the tags, retags, calculates the F1 scores and outputs the emails to `output` folder.

- `Test` uses the test set, tags them and outputs the emails to the `output` folder.

- `Ontology` classifies the test emails and outputs the emails with their ontology classifications.
