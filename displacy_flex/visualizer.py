from spacy import displacy
import regex as re
import numpy as np

class DisplaCyFlex:
    DEFAULT_COLORS = [
        "#f8e71c", "#e4e7d2", "#7aecec", "#bfeeb7", "#feca74",
        "#ff9561", "#aa9cfc", "#c887fb", "#9cc9cc", "#ffeb80",
        "#ff8197", "#f0d0ff", "#bfe1d9"
    ]

    def __init__(self, labels, frequencies=None, default_label='Misc', alpha='95'):
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
        if frequencies is not None:
            order = np.argsort(-np.array(frequencies))
            labels = np.array(labels)[order].tolist()
        return [self.default_label] + labels

    def _generate_colors(self):
        colors = {}
        for i, lbl in enumerate(self.labels):
            color = self.DEFAULT_COLORS[i % len(self.DEFAULT_COLORS)] + self.alpha
            colors[lbl] = color
        return colors

    def _default_template(self):
        return '''  
        <mark class="entity" style="background: {bg}; padding: 0.2em 0.35em; margin: 0 0.25em; 
        line-height: 1; border-radius: 0.4em;">
            {text}
            <span style="font-size: 0.8em; font-weight: bold; font-family: arial; line-height: 1; 
            border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem;">{label}</span>
        </mark>
        '''