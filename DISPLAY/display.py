from spacy import displacy  # Importing displacy for visualization of NLP annotations
import regex as re  # Import regex for text matching and manipulation
import numpy as np  # Import numpy for numerical operations

CONFIGURED = False  # Global flag to check if configuration has been set up

def config_setup(labels, frequents, otherwise='Address'):
    """
    Configures the visualization settings for entity labels and their colors.
    
    Args:
        labels (list[str]): List of entity labels.
        frequents (list[int]): Frequency count of each label, used for sorting.
        otherwise (str, optional): Default label for unmatched entities. Defaults to 'Address'.
    """
    global options
    global CONFIGURED
    if not CONFIGURED:  # Perform configuration only if not already configured
        TPL_ENT_RTL = """  # Template for rendering entities with custom HTML styles
        <mark class="entity" style="background: {bg}; padding: 0.20em 0.35em; margin: 0 0.25em; line-height: 1; border-radius: 0.4em">
            {text}
            <span style="font-size: 0.8em; font-weight: bold; font-family: ariel; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem; margin-right: 0.2rem">{label}{kb_link}</span>
        </mark>
        """
        alpha = '95'  # Opacity value for colors
        DEFAULT_COLORS = [
            "#f8e71c", "#e4e7d2", "#7aecec", "#bfeeb7", "#feca74",
            "#ff9561", "#aa9cfc", "#c887fb", "#9cc9cc", "#ffeb80",
            "#ff8197", "#ff8197", "#f0d0ff", "#bfe1d9", "#bfe1d9",
            "#e4e7d2", "#e4e7d2", "#e4e7d2", "#e4e7d2",
        ]
        
        # Append transparency to each color
        DEFAULT_COLORS = [clr + alpha for clr in DEFAULT_COLORS]
        
        lbl, freq = labels, frequents
        # Sort labels by frequency in descending order
        order = np.argsort(-freq)
        lbl = lbl[order].tolist()
        lbl = [otherwise] + lbl  # Prepend default label
        # Create a color map dictionary for the labels
        colors = {lbl[i]: DEFAULT_COLORS[i % len(DEFAULT_COLORS)] for i in range(len(lbl))}
        options = {"ents": lbl, "colors": colors, "template": TPL_ENT_RTL}  # Configure options
        CONFIGURED = True  # Update configuration flag

def indices(words, text):
    '''
    Determines the start and end indices of words within the original text.

    Args:
        words (list[str]): Words extracted from the text.
        text (str): The complete original text.

    Returns:
        spans (list[tuple]): Start and end indices for each word in the original text.
    '''
    spans = []
    base = 0  # Start searching from the beginning of the text
    for word in words:
        word = re.escape(word)  # Escape special characters for regex
        iter = re.finditer(word, text)  # Find all occurrences of the word in text
        # Get all spans starting after the base index
        all_spans = [m.span() for m in iter if m.span()[0] >= base]
        if all_spans:
            span = all_spans[0]  # Take the first match
            spans.append(span)
            base = span[1]  # Update base to end of the current match
        else:
            spans.append((-1, -1))  # No match found
    return spans

def data(text, highlight, split=True, keep=['O', 'GPS'], otherwise='Address'):
    '''
    Aggregates the information needed for visualization using displacy.
    
    Args:
        text (str): Original text to display.
        highlight (list[dict]): Highlighted annotations with words and labels from model predictions.
        split (bool): Determines whether to merge adjacent tags. Defaults to True.
        keep (list[str]): Tags kept unchanged when merging. Defaults to ['O', 'GPS'].
        otherwise (str): Default tag for non-kept merged entities. Defaults to 'Address'.

    Returns:
        tuple: Original text, tags, words, and their index positions.
    '''
    L = len(highlight)
    if split:  # If not merging tags
        tags = [x for i in range(L) for x in highlight[i].values()]  
    else:
        tags = [x if x in keep else otherwise 
                for i in range(L) 
                for x in highlight[i].values()]  # Merge non-kept tags

    words = [x for i in range(L) for x in highlight[i].keys()]  # Extract words
    ind = indices(words, text)  # Get indices for words
    return text, tags, words, ind

def merge(tags, words, ind):
    '''
    Merges consecutive words and their tags if they are the same.

    Args:
        tags (list[str]): Current list of tags for words.
        words (list[str]): Current list of words.
        ind (list[tuple]): Indices for the words within the original text.

    Returns:   
        tuple: Updated tags, words, and their indices after merging.
    '''
    T = tags
    # Boolean array where True indicates adjacent tags are the same
    msk = np.append((np.array(T)[:-1] == np.array(T)[1:]), [False])
    i = 0
    for num in range(len(msk) - 1):
        if msk[num]:  # If current and next tags are the same
            T[i:i+2] = [T[i]]  # Merge the tags
            words[i:i+2] = [' '.join(words[i:i+2])]  # Merge the words
            ind[i:i+2] = [(ind[i][0], ind[i+1][1])]  # Adjust the span
        else:
            i += 1
    return T, words, ind

def structure(text, tags, ind, title='<u>DDD</u>'):
    '''
    Structures the data for displacy rendering.

    Args:
        text (str): Original text to highlight.
        tags (list[str]): Tags for highlighting.
        ind (list[tuple]): Indices of words within the text.
        title (str): Optional title for visualization. Defaults to '<u>DDD</u>'.

    Returns:   
        dict: Dictionary format required by displacy to render entities.
    '''
    # Create a dictionary for the displacy visualization
    dic_ents = {
        "text": text,
        "ents": [{"start": ind[i][0], "end": ind[i][1], "label": tags[i]} for i in range(len(tags)) if tags[i] != 'O'],
        "title": title
    }
    return dic_ents

def render(text, tags, words, ind, combine=True, save=False):
    '''
    Renders annotated text using displacy.

    Args:
        text (str): Original text to highlight.
        tags (list[str]): Tags for each word.
        words (list[str]): Words from the text.
        ind (list[tuple]): Indices of words in the text.
        combine (bool): Merge adjacent tags if True. Defaults to True.
        save (bool): Save as HTML if True, else render in notebook. Defaults to False.
    '''
    if combine:  # Merge tags if needed
        tags, words, ind = merge(tags, words, ind)
    dic_ents = structure(text, tags, ind)  # Prepare data for visualization
    if not save:
        # Render directly in Jupyter notebook
        displacy.render(dic_ents, manual=True, style="ent", jupyter=True, minify=True, options=options)
    else:
        # Render to HTML file
        html = displacy.render(dic_ents, manual=True, style="ent", jupyter=False, options=options)
        with open("./text.html", 'w+', encoding="utf-8") as fp:
            fp.write(html)

def display(text, highlight, labels=[], frequents=[], split=True, keep=['O', 'GPS'], otherwise='Address', save=False):
    '''
    Master function to prepare text and annotations for displacy visualization.

    Args:
        text (str): Original text to display.
        highlight (list[dict]): Highlighted annotations from model.
        labels (list[str]): Optional list of labels.
        frequents (list[int]): Frequencies to sort labels.
        split (bool): Merge adjacent tags if False. Defaults to True.
        keep (list[str]): Tags to keep unchanged. Defaults to ['O', 'GPS'].
        otherwise (str): Default tag for non-kept merged entities. Defaults to 'Address'.
        save (bool): Save output as HTML if True. Defaults to False.
    '''
    if not labels or not frequents:  # Determine labels and frequencies if not provided
        labels, frequents = np.unique((df['labels'])[~df['labels'].isnull()], return_counts=True)
    config_setup(labels, frequents)  # Set up configuration
    text, tags, words, ind = data(text, highlight, keep=keep, split=split, otherwise=otherwise)  # Aggregate data
    render(text, tags, words, ind, save=save)  # Render visualization

# def collect(corpus, predict_):
#     '''
#     Extracts and collects discrete entities labeled by a NER model.
# 
#     Args:
#         corpus (pd.Series or list of str): List of original texts.
#         predict_ (list of list of dict): Tagged text responses from the model.
# 
#     Returns:   
#         tuple: Lists of extracted addresses, entities, GPS coordinates, and processing errors.
#     '''
#     Addys = []  # List to store extracted addresses
#     Ents = []  # List to store extracted entity names
#     Gps = []  # List to store extracted GPS coordinates
#     errors = []  # List to record errors in processing
#     for N in range(len(predict_)):
#         text, prediction = corpus[N], predict_[N]
#         try:
#             # Aggregate and merge data
#             text, tags, words, ind = data(text, prediction, split=False, keep=['O', 'GPS', 'Entity'], otherwise='Address')
#             tags, words, ind = merge(tags, words, ind)
#             fragment, signal = np.array(words), np.array(tags)
#             addys = (fragment[signal == 'Address']).tolist()
#             ents = (fragment[signal == 'Entity']).tolist()
#             gps = (fragment[signal == 'GPS']).tolist()            
#         except Exception as e:  # Catch errors in data processing
#             addys = ['FAIL']
#             ents = ['FAIL']
#             gps = ['FAIL']
#             errors.append(N)  # Append error index
#         Addys.append(addys)
#         Ents.append(ents)
#         Gps.append(gps)
    return Addys, Ents, Gps, errors
