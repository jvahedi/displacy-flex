# DisplaCy Flex

DisplacyFlex extends the functionality of spaCy's displacy module, providing users with enhanced flexibility to visualize and manage named entity recognition (NER) results across various text-based projects. With DisplacyFlex, customize and scale your text processing workflows with ease and precision.

## Features

- **Customizable Visualization**: Tailor the display of entity annotations with unique styles and color palettes.
- **Efficient Annotation Processing**: Accurately merge and process text spans with consistent tags.
- **Dynamic Rendering Options**: Visualize text annotations directly in Jupyter notebooks or export as HTML for wider use.
- **Robust Entity Extraction**: Extract and categorize key entities and data from textual inputs reliably.

## Installation

Clone the repository from GitHub:

```bash
git clone https://github.com/yourusername/DisplacyFlex.git
cd DisplacyFlex
```

## Usage

### Configuration for Visualization

Set up your visualization preferences to manage text annotations:

```python
from displacyflex import config_setup

labels = ['PERSON', 'ORG', 'LOCATION']
frequents = [5, 3, 4]
config_setup(labels, frequents)
```

### Visualize Text Annotations

Utilize DisplacyFlex to visualize and manage text annotations seamlessly:

```python
from displacyflex import display

text = "Alice works at Acme Corp in San Francisco."
highlight = [{'Alice': 'PERSON', 'Acme Corp': 'ORG', 'San Francisco': 'LOCATION'}]
display(text, highlight)
```

### Extract Entities Strategically

With DisplacyFlex, sort and retrieve entity data efficiently:

```python
from displacyflex import collect

corpus = ["123 Baker Street coordinates"]
predictions = [[{'123 Baker Street': 'Address', 'Coordinates': 'GPS'}]]
addys, ents, gps, errors = collect(corpus, predictions)
```

## License

DisplacyFlex is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, contact Vahedi John at [Vahedi.john@columbia.edu](mailto:Vahedi.john@columbia.edu).
