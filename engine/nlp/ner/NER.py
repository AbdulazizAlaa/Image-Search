from pycorenlp import StanfordCoreNLP

def solve(text, url='http://localhost', port='9000'):
    text = preprocess(text)
    nlp = StanfordCoreNLP(url + ":" + port)
    output = ""
    while type(output) is not dict:
        output = nlp.annotate(text, properties={"annotators": "ner", "outputFormat": "json"})
    persons = []
    for sentence in output["sentences"]:
        for token in sentence["tokens"]:
            if (token["ner"] == "PERSON"):
                persons.append(token["originalText"])
    return persons

def preprocess(text):
    text = text.lower().split(" ")
    # And rule
    text = findAndTitle(text, "and")
    text = findAndTitle(text, "with")
    return " ".join(text)

def findAndTitle(array, keyword):
    for idx, item in enumerate(array):
        if item == keyword:
            array[idx + 1] = array[idx + 1].title()
    return array

