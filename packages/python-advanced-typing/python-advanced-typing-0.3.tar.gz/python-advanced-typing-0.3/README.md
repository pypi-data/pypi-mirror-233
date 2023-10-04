
# Python Advanced Typing

## Overview

### Description

`python-advanced-typing` is a simple Python package to help developers validate the types of variables in their codebase. With support for checking individual variables or multiple variables at once, it offers a concise way to ensure that the data you're working with meets your expectations.
### Features
- **Single Variable Check**: Compare a variable's type against a specific type or multiple acceptable types.
- **Bulk Verification**: Validate the types of multiple variables simultaneously using a list.
## Setup Instructions
**Install the Package using**:

```
pip install python-advanced-typing
```

## Usage
### Check Individual Variable
```python
from python_advanced_typing import check_type

x = "Hello"
check_type(x, "x", str)
```
### Bulk Check Multiple Variables
```python
from python_advanced_typing import check_type

x = "Hello"
y = 123
z = [1, 2, 3]

check_type(
    (x, "x", str),
    (y, "y", int),
    (z, "z", list)
)
```

## Contributing
As this is an open-source project hosted on GitHub, your contributions and improvements are welcome! Follow these general steps for contributing:

1. **Fork the Repository**: 
Start by forking the main repository to your personal GitHub account.

2. **Clone the Forked Repository**: 
Clone your forked repository to your local machine.

    ```
    git clone https://github.com/YidiSprei/PythonAdvancedTyping.git
    ```

3. **Create a New Branch**: 
Before making any changes, create a new branch:

    ```
    git checkout -b feature-name
    ```

4. **Make Your Changes**: 
Implement your features, enhancements, or bug fixes.

5. **Commit & Push**:

    ```
    git add .
    git commit -m "Descriptive commit message about changes"
    git push origin feature-name
    ```
   
6. **Create a Pull Request (PR)**: 
Go to your forked repository on GitHub and click the "New Pull Request" button. Make sure the base fork is the original repository, and the head fork is your repository and branch. Fill out the PR template with the necessary details.

Remember to always be respectful and kind in all interactions with the community. It's all about learning, growing, and helping each other succeed!

## Acknowledgments
Crafted with 💙 by Yidi Sprei. Kudos to all contributors and the expansive Python community for encouragement and motivation.

