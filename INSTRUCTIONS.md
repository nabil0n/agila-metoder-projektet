## Get started
### Install Python and Poetry
Install the Python version specified in [pyproject.toml](pyproject.toml) to your system.

Install Poetry [(Instructions on their website)](https://python-poetry.org/) or run the command

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Install Requirements
Most of the requirements are installed with the following command
```bash
cd path/to/git-repo
poetry env use 3.10 # Tells Poetry which Python version to use
make install_dependencies
```

### Other Commands
Other useful commands for the project can be found in the [Makefile](Makefile).


### Tips
All your python code should go inside of the src/newsfeed folder. This makes it so that you can "build" your own python package easily.