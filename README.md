# DisplaCyFlex

DisplaCyFlex is an enhanced visualization tool built on top of spaCy's DisplaCy module. It offers flexible and customizable visualization options for named entity recognition (NER), making it simple and intuitive to manage and visualize annotated text data across NLP projects.

## Features

- **Customizable Entity Visualization:** Easily configure entity labels, color schemes, and styles.
- **Efficient Annotation Management:** Precisely merge adjacent entities and handle text spans.
- **Dynamic Output Formats:** Render visualizations directly within Jupyter notebooks or export as interactive HTML.
- **Easy Integration:** Designed for seamless integration into existing NLP pipelines and workflows.

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/displacyflex.git
cd displacyflex
pip install -r requirements.txt
```

## Usage

### Quick Start

Import and initialize the visualizer:

```python
from displacy_flex import DisplaCyFlex

labels = ['PERSON', 'ORG', 'LOCATION']
frequencies = [120, 80, 50]
visualizer = DisplaCyFlex(labels, frequencies)
```

### Visualizing Text

Render annotated text easily:

```python
text = "Alice works at Acme Corp in San Francisco."
highlight = [
    {"Alice": "PERSON"},
    {"works": "O"},
    {"at": "O"},
    {"Acme": "ORG"},
    {"Corp": "ORG"},
    {"in": "O"},
    {"San": "LOCATION"},
    {"Francisco": "LOCATION"}
]

visualizer.visualize(text, highlight, split=False, title='Example Visualization', save_html='example.html')
```

### Advanced Configuration

Customize visualization with your own labels and frequencies:

```python
custom_labels = ['DATE', 'EVENT', 'GPE']
custom_freqs = [30, 20, 10]
custom_visualizer = DisplaCyFlex(custom_labels, custom_freqs, default_label='ENTITY')
```

## Testing

Run tests with:

```bash
python -m unittest discover tests
```

## License

DisplaCyFlex is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, contact Vahedi John at [vahedi.john@columbia.edu](mailto:vahedi.john@columbia.edu).
