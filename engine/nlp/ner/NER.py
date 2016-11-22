from pycorenlp import StanfordCoreNLP

def solve(text, url='http://localhost', port='9000'):
    """This is where the magic happens."""
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
    """Some feature engineering."""
    text = text.lower().replace(",", " , ").split(" ")
    # First word is capital
    text[0] = text[0].title()
    # And rule
    text = findAndTitle(text, "and")
    # With rule
    text = findAndTitle(text, "with")
    # Comma rule
    text = findAndTitle(text, ",")
    return " ".join(text).replace(" , ", ", ")

def findAndTitle(array, keyword):
    """Turn every word after keyword into capital."""
    for idx, item in enumerate(array):
        if item == keyword:
            array[idx + 1] = array[idx + 1].title()
    return array

