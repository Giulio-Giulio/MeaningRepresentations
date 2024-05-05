# Term Project for Meaning Representations

## Formalia
- **Team**: Giulio Cusenza, Giulio Posfortunati
- **Module**: Language & Cognition
- **Option**: 6 ECTS (graded)

## Guide

The tool was developed with Python 3.12.0. We suggest using this version and running the following command to set up the runtime environment:

```
pip install -r requirements.txt
```

Once set up, refer to [this repository](https://github.com/bjascob/amrlib-models?tab=readme-ov-file) to download the parser model data (we suggest the `parse_xfm_bart_base` model), and store the .json and .bin files in `resources/model_stog/`. Once the model is downloaded, run `App.py`. You should see the folliwing prompt:

```
Ask a question about a famous person, event, place, or anything:
> 
```

Enter your query and wait. Parsing sentences from long Wikipedia article will take very long. You can limit the number of sentences that are parsed by changing the `n_sentences` parameter in `App.py`. You can also change the number of displayed answers by adjusting `n_answers`.
