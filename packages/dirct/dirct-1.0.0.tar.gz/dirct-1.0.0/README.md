# dirct
A dict that reflects the contents of a directory.

## Installation

You can install this package with pip.
```sh
$ pip install dirct
```

## Links

[![Documentation](https://img.shields.io/badge/Documentation-C61C3E?style=for-the-badge&logo=Read+the+Docs&logoColor=%23FFFFFF)](https://abrahammurciano.github.io/python-dirct)

[![Source Code - GitHub](https://img.shields.io/badge/Source_Code-GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=%23FFFFFF)](https://github.com/abrahammurciano/python-dirct.git)

[![PyPI - dirct](https://img.shields.io/badge/PyPI-dirct-006DAD?style=for-the-badge&logo=PyPI&logoColor=%23FFD242)](https://pypi.org/project/dirct/)

## Usage

### Example directory

Consider the following directory `path/to/directory/` that contains data about a video game.
```
path/to/directory/
├── __self__.toml
├── publisher.toml
├── version
└── levels/
	├── castle.lvl.json
	├── dungeon.lvl.json
	└── forest.lvl.json
```

### Parsing files

The directory may contain any number of files and subdirectories. Files ending in `.toml`, `.json`, `.yaml`, and `.yml` are parsed correctly according to their respective formats, and all other files are read as text if it can be decoded or as bytes otherwise. You can associate custom parsers with file extensions by passing them to the `parsers` argument of the `Dirct` constructor.

```python
Dirct("path/to/directory", parsers={"csv": lambda s: tuple(csv.DictReader(io.StringIO(s)))})
```

### Mapping files to/from keys

Converting between file names and dictionary keys is handled by a `KeyMapper` object, which can be passed to the `key_mapper` argument of the `Dirct` constructor.

#### Basename key mapper (default)

The basename key mapper ignores leading dots and all trailing extensions. If `hidden=False` is passed to the constructor, then leading dots are not ignored.

In case of a name collision when mapping a key to a path, an `AmbiguityError` is raised unless `strict=False` was passed to the constructor, in which case a warning is logged and one of the paths is chosen. (For a given directory's contents, the same path will be chosen consistently.)

```python
>>> d = Dirct("path/to/directory") # Default key mapper
>>> tuple(d.keys())
('publisher', 'version', 'levels')
>>> d["publisher"] # Gets the contents of publisher.toml
{'name': 'Probabilitor the Annoying', 'founded': 2015}
>>> d["publisher.toml"] # Also works
{'name': 'Probabilitor the Annoying', 'founded': 2015}
>>> d[".publisher.foo.json"] # Also works because the leading dot and file extensions are ignored
{'name': 'Probabilitor the Annoying', 'founded': 2015}
```

#### Exact key mapper

The exact key mapper only recognizes keys that exactly match the file/directory names.

```python
>>> from dirct import ExactKeyMapper
>>> d = Dirct("path/to/directory", key_mapper=ExactKeyMapper())
>>> tuple(d.keys())
('publisher.toml', 'version', 'levels')
>>> d["publisher.toml"] # Gets the contents of publisher.toml
{'name': 'Probabilitor the Annoying', 'founded': 2015}
>>> d["publisher"]
KeyError: 'publisher'
>>> d[".publisher.toml"]
KeyError: '.publisher.toml'
>>> d["publisher.json"]
KeyError: 'publisher.json'
```

### `__self__`

A directory may contain a single special file called `__self__.*` with any known extension. The contents of this file are parsed to a dictionary (an `InvalidSelfError` is raised if it can't be parsed as a dictionary) which is then merged with the rest of the directory's contents (explicit files/subdirectories take precedence over `__self__.*`). This allows you to keep some of the keys in a single file and the rest in separate files or subdirectories.

For example, `__self__.toml` may contain the following:

```toml
name = "Dungeons, Dungeons, and More Dungeons"
release_date = 2021-01-01
```

```python
>>> d = Dirct("path/to/directory")
>>> d["name"]
'Dungeons, Dungeons, and More Dungeons'
```
