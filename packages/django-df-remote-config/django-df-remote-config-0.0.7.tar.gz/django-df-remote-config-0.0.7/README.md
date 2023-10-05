
# Django DF Remote Config

Module for managing frontend application confiuration


/remote_config/?part=legal&bundle_id=com.roblevine.saferide&...

{
"auth": {},
"app_config": {},
"app_launch": {}
}


## Installation:

- Install the package

```
pip install django-df-remote-config
```


- Include default `INSTALLED_APPS` from `df_remote_config.defaults` to your `settings.py`

```python
from df_remote_config.defaults import DF_REMOTE_CONFIG_INSTALLED_APPS

INSTALLED_APPS = [
    ...
    *DF_REMOTE_CONFIG_INSTALLED_APPS,
    ...
]

```


## Development

Installing dev requirements:

```
pip install -e .[test]
```

Installing pre-commit hook:

```
pre-commit install
```

Running tests:

```
pytest
```
