# jomiel-messages

[![pypi-pyversions](https://img.shields.io/pypi/pyversions/jomiel-messages?color=%230a66dc)][pypi]
[![pypi-v](https://img.shields.io/pypi/v/jomiel-messages?color=%230a66dc)][pypi]
[![pypi-wheel](https://img.shields.io/pypi/wheel/jomiel-messages?color=%230a66dc)][pypi]
[![pypi-status](https://img.shields.io/pypi/status/jomiel-messages?color=%230a66dc)][pypi]
[![code-style](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi]: https://pypi.org/project/jomiel-messages
[black]: https://pypi.org/project/black

The Python bindings for the [jomiel] protobuf messages.

[jomiel]: https://github.com/guendto/jomiel

## About

The bindings have been generated from the protobuf declaration files of
[jomiel-proto]

[jomiel-proto]: https://github.com/guendto/jomiel-proto/

## Installation

```shell
pip install jomiel-messages
```

Install from the repository, e.g. for development:

```shell
git clone https://github.com/guendto/jomiel-messages.git
cd jomiel-messages
./bin/gen
pip install -e .
```

## Usage

Serialize an inquiry message:

```python
from jomiel_messages.protobuf.v1alpha1.message_pb2 import Inquiry

inquiry = Inquiry()
inquiry.media.input_uri = 'https://foo.bar/baz'
serialized_string = Inquiry.SerializeToString(inquiry)
# ...
```

De-serialize a response message:

```python
from jomiel_messages.protobuf.v1alpha1.message_pb2 import Response
from jomiel_messages.protobuf.v1alpha1.status_pb2 import STATUS_CODE_OK

response = Response()
response.ParseFromString(serialized_string)

if response.status.code != STATUS_CODE_OK:
  print(f"message={response.status.message})
  print(f"status-code={response.status.code}")
  print(f"error-code={response.status.error}")
  print(f"http-code={response.status.http.code}")
  # ...
else:
  # ...
```

## License

`jomiel-messages` is licensed under the [Apache License version
2.0][aplv2].

[aplv2]: https://www.tldrlegal.com/l/apache2

## Acknowledgements

### Subprojects (as git subtrees)

- [src/jomiel_messages/proto/](src/jomiel_messages/proto/) of
  [jomiel-proto]
