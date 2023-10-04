# Synapse Power Tools

Utilities for using [Synapse](https://www.synapse.org/).

## Dependencies

- [Python3.10+](https://www.python.org/)
- A [Synapse](https://www.synapse.org/) account with a username/password. Authentication through a 3rd party (.e.g.,
  Google) will not work, you must have a Synapse user/pass for
  the [API to authenticate](http://docs.synapse.org/python/#connecting-to-synapse).

## Install

```bash
pip install syntools
```

## Configuration

Your Synapse credentials can be provided on the command line (`--username`, `--password`) or via environment variables.

```bash
SYNAPSE_USERNAME=your-synapse-username
SYNAPSE_PASSWORD=your-synapse-password
```

## Usage

```text
usage: syntools [-h] [--version] {download,find-id,copy,move,list} ...

Synapse Power Tools

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit

Commands:
  {download,find-id,copy,move,list}
    download            Download folders and files from Synapse.
    find-id             Find a Synapse ID by a Synapse path (e.g., MyProject/Folder/file.txt).
    copy                Copy Synapse entities from one container to another.
    move                Move Synapse entities from one container to another.
    list                List Synapse entities in one or more containers.

```

## Development Setup

```bash
pipenv --python 3.10
pipenv shell
make pip_install
make build
make install_local
```

See [Makefile](Makefile) for all commands.

### Testing

- Create and activate a virtual environment:
- Rename [.env-template](.env-template) to [.env](.env) and set each of the variables.
- Run the tests: `make test`
