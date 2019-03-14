- For each module, make a single test file, named *test_\<name of module>.py*

- Inside the file, import unittest and the module to be tested as such:
    ```python
    import unittest
    import ..<module name>
    ``` 

- Define a class (inheriting from unittest.TestCase) containing test cases for each functionality to be tested:
    ```python
    class Test<module name>(unittest.TestCase):
        def test_<name of functionality to be tested>(self):
            # tests
    ``` 

See https://docs.python.org/3/library/unittest.html for references.