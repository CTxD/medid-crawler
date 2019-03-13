# Running

#### Virtual environment
Consider using a virtual environment (and possibly a virtual environment manager such as *virtualenvwrapper*) for requirements for this project.

Using virtualenvwrapper:
```bash
workon <environment name>
``` 

#### Installing dependencies
```bash
pip install -r requirements/<dev|prod>
``` 

#### Running
```bash
python ./source/main.py
``` 


## Some notes on linting
Prospector is used for linting, using all default tools as well as the addition of mypy and vulture. mypy checks for type inconsistencies, and vulture checks for unused variables, functions, and methods.
See [Prospector supported tools](https://prospector.readthedocs.io//en/master/supported_tools.html) for a list of all supported tools and what they check.

### Ignoring certain errors across all files
Some errors are irrelevant or annoying (such as pep8's "blank line at EOF" (W391)) and does not provide any additional quality to the code base. These types of errors can be disabled in the Prospector profile file, _.prospector.yaml_. Only do this for errors, which should be ignored across *all* files!

### Ignoring single lines
Sometimes you may write code which violates pep8 (See: [A foolish conistency is the Hobgoblin of little minds](https://www.python.org/dev/peps/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds)), which triggers the corresponding error message by Prospector. If you are certain the code you have written is not invalid despite triggering linter errors, you should add ```  # noqa``` (Note the 2 whitespaces before '#' and single whitespace after!) at the end of the line. This informs Prospector to ignore the line when analysing the file.