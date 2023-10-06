# Marops Config

Marops Config is used to load config stored inside the `~/.config/greenroom` folder.

## Install

* `pip install -e ./libs/marops_config`

## Usage

### Reading config

```python
from marops_config import read

config = read()
```

### Writing config

```python
from marops_config import write, MaropsConfig

config = MaropsConfig()

write(config)

```

### Generating schemas

After changing the dataclasses, you can generate the schemas with:

```bash
python3 -m marops_config.generate_schemas
```
