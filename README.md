# tatbeea · تطبيع

Small, dependency-free Arabic text normalization for Python.

Arabic text that means the same thing is often written differently: with or
without harakat, with أ / إ / آ or a bare ا, with ى or ي, with Arabic-Indic or
Latin digits, stretched with tatweel. That breaks search, deduplication and
matching. `tatbeea` folds these variants into one form.

```python
>>> from tatbeea import normalize
>>> normalize("أَهْلـــاً بِكَ فِي ٢٠٢٦")
'اهلا بك في 2026'
>>> {normalize(w) for w in ["إسلام", "اسلام", "إِسْلَام", "اسـلام"]}
{'اسلام'}
```

## Install

```bash
pip install git+https://github.com/hasan-0097/tatbeea
```

## What it does

| Function | Example |
| --- | --- |
| `remove_tashkeel` | `مُحَمَّد` → `محمد` |
| `remove_tatweel` | `مـــرحبا` → `مرحبا` |
| `normalize_alef` | `أ إ آ ٱ` → `ا` |
| `normalize_yeh` | `ى` → `ي` |
| `normalize_teh_marbuta` | `ة` → `ه` (off by default in `normalize`) |
| `normalize_digits` | `٢٠٢٦` / `۲۰۲۶` → `2026` |
| `to_arabic_digits` | `2026` → `٢٠٢٦` |
| `normalize` | all of the above + collapse whitespace; each step can be switched off |

```python
normalize(text, tashkeel=True, tatweel=True, alef=True, yeh=True,
          teh_marbuta=False, digits=True, collapse_spaces=True)
```

## Command line

```bash
tatbeea "مُحَمَّدٌ رَسُولُ"
cat file.txt | tatbeea --keep-digits
```

## Development

```bash
python -m unittest discover -s tests
```

No dependencies beyond the standard library. Contributions are welcome — see
[CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
