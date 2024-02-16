# Autonomous-Aircraft-Drop

## Startup Instructions

Create your own fork of this repository to do work on. 

To add your work to this repository, create a PR from your fork's branch into the same branch on this repository.

### Branch Instructions

Use `git branch` to see what branch you are on:
```sh
jacksonthetford Autonomous-Aircraft-Drop $ git branch
  image-recognition-main
* main
  trajectory-main
```

Then use `git checkout <your-project-name>` to switch to the branch for your work:

``` sh
jacksonthetford Autonomous-Aircraft-Drop $ git checkout image-recognition-main
Switched to branch 'image-recognition-main'
Your branch is up to date with 'origin/image-recognition-main'.
jacksonthetford Autonomous-Aircraft-Drop $ git branch
* image-recognition-main
  main
  trajectory-main
```

If you don't have a branch locally that matches a remote branch do the following:

`git checkout -b <name-of-branch> origin/<name-of-branch>`

Do your development on your branch (either a dev or feature branch) and then create a pull request to either `trajectory-main` or `image-recognition-main`


### Docker Instructions

To run this as a docker container, for dev or testing, run the following:

```
$ docker run -d --rm --name app --entrypoint=sleep jthet/autonomous-aircraft-drop infinity
...
$ docker exec -it app bash
```

## Workflows instructions

Please do the following so the workflows pass.

### Running `pylint`:

`pylint` is used to analyze Python code for errors and enforce a coding standard. Follow these steps to lint your code:

1. **Install `pylint`** (if not already installed):

```
pip install pylint
```

2. **Run `pylint` on Your Python Files**:
Navigate to your project directory and run:

```
pylint path/to/your_script.py
```
or 

```
pylint $(git ls-files '*.py')
```
to lint all files

**Note**: you can get around the linting by putting something similar to `# pylint: disable=wrong-import-position` in the line above the line causing the renting error. 


### Running `pytest`:

`pytest` is our testing framework of choice for writing and running tests. It's essential to ensure that your code passes all tests to maintain functionality and stability.

1. **Install `pytest`** (if not already installed):

```
pip install pytest
```

2. **Run Tests with `pytest`**:
In the root directory of the project, execute:

```
pytest
```
This command will automatically find and run all tests within the `tests/` directory, if you have written tests.

**Note**: When you put your test in the `tests/` directory, you need to give pytest the path of the library/file you are importing. To do this, put the following at the top of the test file:

```
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
```









