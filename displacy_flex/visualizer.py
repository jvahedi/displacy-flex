from spacy import displacy
import regex as re
import numpy as np


class DisplaCyFlex:
    """Class for flexible visualization of NLP entities using SpaCy's DisplaCy.

    Attributes:
        labels (list): List of entity labels.
        frequencies (list): Frequencies corresponding to labels.
        default_label (str): Default label used for merging or unknown tags.
        alpha (str): Transparency value for colors.
        colors (dict): Dictionary mapping labels to colors.
        options (dict): Configuration options for DisplaCy.
    """

    DEFAULT_COLORS = [
        "#f8e71c", "#e4e7d2", "#7aecec", "#bfeeb7", "#feca74",
        "#ff9561", "#aa9cfc", "#c887fb", "#9cc9cc", "#ffeb80",
        "#ff8197", "#f0d0ff", "#bfe1d9"
    ]

    def __init__(self, labels, frequencies=None, default_label='Misc', alpha='95'):
        """Initializes DisplaCyFlex with labels and optional color settings.

        Args:
            labels (list): Entity labels.
            frequencies (list, optional): Label frequencies for ordering colors.
            default_label (str, optional): Default label for merged tags.
            alpha (str, optional): Transparency for colors (00-ff).
        """
        self.default_label = default_label
        self.alpha = alpha
        self.labels = self._prepare_labels(labels, frequencies)
        self.colors = self._generate_colors()
        self.options = {
            "ents": self.labels,
            "colors": self.colors,
            "template": self._default_template()
        }

    def _prepare_labels(self, labels, frequencies):
        """Orders labels based on frequency.

        Args:
            labels (list): Entity labels.
            frequencies (list): Frequencies of labels.

        Returns:
            list: Ordered labels with default label prepended.
        """
        if frequencies is not None:
            order = np.argsort(-np.array(frequencies))
            labels = np.array(labels)[order].tolist()
        return [self.default_label] + labels

    def _generate_colors(self):
        """Generates color mapping for labels.

        Returns:
            dict: Label to color mapping.
        """
        colors = {}
        for i, lbl in enumerate(self.labels):
            color = self.DEFAULT_COLORS[i % len(self.DEFAULT_COLORS)] + self.alpha
            colors[lbl] = color
        return colors

    def _default_template(self):
        """Provides default HTML template for visualization.

        Returns:
            str: HTML template string.
        """
        return """  
        <mark class="entity" style="background: {bg}; padding: 0.2em 0.35em; margin: 0 0.25em; 
        line-height: 1; border-radius: 0.4em;">
            {text}
            <span style="font-size: 0.8em; font-weight: bold; font-family: arial; line-height: 1; 
            border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem;">{label}</span>
        </mark>
        """

    def indices(self, words, text):
        """Finds start and end indices of words in text.

        Args:
            words (list): Words to find.
            text (str): Original text.

        Returns:
            list: List of tuples (start, end) indices.
        """
        spans, base = [], 0
        for word in words:
            word_escaped = re.escape(word)
            matches = [m.span() for m in re.finditer(word_escaped, text) if m.start() >= base]
            span = matches[0] if matches else (-1, -1)
            spans.append(span)
            base = span[1] if span != (-1, -1) else base
        return spans

    def process_highlight(self, highlight, keep=['O'], split=True):
        """Processes annotations into separate tags and words lists.

        Args:
            highlight (list): Annotations (list of dictionaries).
            keep (list): Tags to always keep separate.
            split (bool): Whether to split or merge tags.

        Returns:
            tuple: Tags and words lists.
        """
        tags, words = [], []
        for annotation in highlight:
            for word, tag in annotation.items():
                tag_final = tag if split or tag in keep else self.default_label
                tags.append(tag_final)
                words.append(word)
        return tags, words

    def merge(self, tags, words, indices):
        """Merges consecutive words with identical tags.

        Args:
            tags (list): List of tags.
            words (list): List of words.
            indices (list): Word indices.

        Returns:
            tuple: Merged tags, words, and indices.
        """
        merged_tags, merged_words, merged_indices = [], [], []
        buffer_word, buffer_tag, buffer_span = words[0], tags[0], indices[0]

        for tag, word, span in zip(tags[1:], words[1:], indices[1:]):
            if tag == buffer_tag:
                buffer_word += f" {word}"
                buffer_span = (buffer_span[0], span[1])
            else:
                merged_tags.append(buffer_tag)
                merged_words.append(buffer_word)
                merged_indices.append(buffer_span)
                buffer_word, buffer_tag, buffer_span = word, tag, span
        merged_tags.append(buffer_tag)
        merged_words.append(buffer_word)
        merged_indices.append(buffer_span)

        return merged_tags, merged_words, merged_indices

    def structure_data(self, text, tags, indices, title=''):
        """Formats data for DisplaCy visualization.

        Args:
            text (str): Original text.
            tags (list): Tags list.
            indices (list): Word indices.
            title (str): Visualization title.

        Returns:
            dict: Formatted data for DisplaCy.
        """
        ents = [
            {"start": start, "end": end, "label": tag}
            for tag, (start, end) in zip(tags, indices) if tag != 'O' and start >= 0
        ]
        return {"text": text, "ents": ents, "title": title}

    def render(self, structured_data, save_html=None):
        """Renders visualization with DisplaCy.

        Args:
            structured_data (dict): Prepared data for DisplaCy.
            save_html (str, optional): File path to save HTML output.
        """
        html = displacy.render(
            structured_data, manual=True, style="ent",
            jupyter=save_html is None, options=self.options
        )
        if save_html:
            with open(save_html, 'w+', encoding='utf-8') as file:
                file.write(html)

    def visualize(self, text, highlight, split=True, keep=['O'], title='', save_html=None):
        """Full pipeline for visualizing annotated text.

        Args:
            text (str): Original text.
            highlight (list): Annotations.
            split (bool): Split or merge consecutive tags.
            keep (list): Tags to always keep separate.
            title (str): Visualization title.
            save_html (str, optional): File path for HTML output.
        """
        tags, words = self.process_highlight(highlight, keep=keep, split=split)
        indices = self.indices(words, text)
        if not split:
            tags, words, indices = self.merge(tags, words, indices)
        structured = self.structure_data(text, tags, indices, title)
        self.render(structured, save_html=save_html)
