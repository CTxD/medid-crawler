- For each module, make a single test file, named *test_\<name of module>.py*

- Inside the file, import unittest and the module to be tested as such:
    ```python
    import unittest
    import ..<module name>
    ``` 

- Define a class (inheriting from unittest.TestCase) containing test cases for each functionality to be tested:
    ```python
    class Test<module name>(unittest.TestCase):
        def test_<name of functionality to be tested>_<description of what is being tested>(self):
            # tests
    ``` 

Following the naming convention means tests are short and concise and only test a specific functionality. This means multiple test-methods must be written to test a single functionality. The naming convention allows for quick identification of what exactly is tested and if a test fails it allows for easy identification of *which* test has failed. See https://docs.python-guide.org/writing/tests/ for guidelines and good practices w.r.t. unittesting. 

Example of the naming convention for a few tests for a 'add' function:
```python
...
    def test_add_1_and_2(self):
        self.assertEqual(add(1, 2) 3)

    def test_add_neg1_and_2(self):
        self.assertEqual(add(-1, 2) 1)
``` 


See https://docs.python.org/3/library/unittest.html for references.