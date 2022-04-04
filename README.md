# pyzoopla

Library for accessing property information from Zoopla.

## Installation

```shell
$ pip install pyzoopla
```

## Usage

```python
from pyzoopla import Zoopla

zoopla = Zoopla()

regions = zoopla.get_for_sale_regions()

for region in regions:
    properties = zoopla.get_for_sale_properties(region)
    print(properties)
```
