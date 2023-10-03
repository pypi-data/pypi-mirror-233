# mdeng

Markdown Engine for Python

Please visit: https://pypi.org/project/mdeng for PyPI Package

Please visit: https://github.com/youhengzhou/mdeng for Github repo

# Download Package

`py -m pip install mdeng -U`

## In Your Python Files

```
import mdeng

mdg = MdDB()

mdg.create({}, 'sample.md')

mdg.read('sample.md')
```

For a sample of how it works, check the `test.py` in the test folder.

This markdown engine is able to to take a dictionary such as:

![image](https://github.com/youhengzhou/mdeng/assets/60205850/dd40c1ff-3ab4-4a0c-b013-f7a131606996)

and turn it into a markdown file:

![image](https://github.com/youhengzhou/mdeng/assets/60205850/c8798503-6941-40d9-8072-a0a80ee80528)

it also supports reading a markdown file and returning a dictionary

![image](https://github.com/youhengzhou/mdeng/assets/60205850/a03b5f97-792f-4075-81ec-32bdcb688742)
