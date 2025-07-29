from displacy_flex import DisplaCyFlex

labels = ['ORG', 'LOC', 'PERSON']
frequencies = [100, 80, 50]

visualizer = DisplaCyFlex(labels, frequencies)

text = "Elon Musk founded OpenAI in California."
highlight = [{"Elon": "PERSON"}, {"Musk": "PERSON"}, {"founded": "O"},
             {"OpenAI": "ORG"}, {"in": "O"}, {"California": "LOC"}]

visualizer.visualize(text, highlight, split=False, title='Example Visualization', save_html='example.html')