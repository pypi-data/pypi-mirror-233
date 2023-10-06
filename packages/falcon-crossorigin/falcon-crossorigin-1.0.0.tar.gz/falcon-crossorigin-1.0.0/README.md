# falcon-crossorigin [![codecov](https://codecov.io/gh/alexferl/falcon-crossorigin/branch/master/graph/badge.svg)](https://codecov.io/gh/alexferl/falcon-crossorigin)

A simple [Falcon](https://github.com/falconry/falcon) module for Cross-Origin Resource Sharing (CORS).


## Install
```shell script
pip install falcon-crossorigin
```

## Usage
```python
import falcon
from falcon_crossorigin import CrossOrigin

cross_origin = CrossOrigin(
    allow_origins="https://app.example.com",
    allow_methods="GET,POST",
    allow_headers="Pragma,Expires,Cache-Control",
    allow_credentials=True,
    expose_headers="Link",
    max_age=3600,
)

api = falcon.API(middleware=[cross_origin])
```

## Credits
Port of [Echo's](https://github.com/labstack/echo) [CORS middleware](https://github.com/labstack/echo/blob/1f6cc362cc91b22e5889b2674e45cf3545d6ee21/middleware/cors.go).
