## The Engine
This is the root folder for our Engine.
It is split into two parts
* nlp
* cv

In each of these you can put your modules in the form of function definitions, or a class if you module needs to be instantiated.
You can even further split your folders, for example
nlp/ner/

when we import from the app the import will look like
```
	from engine.nlp.ner import *
```

This way we keep our work modular and easily accessible by the API.


### Modifying System path
Before we can import our engine we need to let python know where to find our engine.
In order to do this we need to modify the System path, this is where python looks for modules.

to do this

```
	import sys
	sys.path.insert(0, "..")
```
Where .. is the root of our repo (This is where the Engine folder exists).

To make your module seeable by python you still need to add an empty __init__.py file, this lets python understand you are a module.

I've placed a simple script at the App directory (nertest.py) to demonstrate how to load the NER module.
You can follow it to understand how to import a module and how to define a module.
