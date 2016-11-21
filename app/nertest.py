import sys
sys.path.insert(0, "..")
from engine.nlp.ner import NER
print NER.solve("Hello")
