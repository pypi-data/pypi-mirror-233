# PyUSPSValidator
📮 PyUSPSValidator: Simplifying USPS WebTools, one address at a time! 🐍✉️ Verify and validate with ease, thanks to this Python-powered wrapper. Say goodbye to address woes! 🚀📍

## Features

- Verification of addresses
- Zip code lookup
- City and state lookup
- Built-in testing with predefined test data

## Installation


Install the package using pip:

```bash
pip install pyuspsvalidator
```

### Dependencies:

Make sure to install the required module:
```
pip install requests
```

## Usage

### Initialization

To use the WebToolsRequest class, initialize it with your user ID.

```python
from webtools import WebToolsRequest

api = WebToolsRequest("YOUR_USER_ID")
```

### Verify an Address

This method allows you to validate the given address.

```python
data = [{
    'address2':'910 West Ave',
    'city':'Miami Beach',
    'state':'FL'
}]

response = api.verify(data)
address = response['0']

print(str(address))
```

### Zip Code Lookup

This method retrieves a zip code for a given address.

```python
data = [{
    'address2':'910 West Ave',
    'city':'Miami Beach',
    'state':'FL'
}]

response = api.zipcode_lookup(data)
address = response['0']

print(address.zipcode)
```

### City and State Lookup

Get city and state information based on the provided zip code.

```python
data = [{
    'zip5':'33139'
}]

response = api.citystate_lookup(data)
address = response['0']

print(address.citystate)
```

### Testing

You can use the provided test methods to validate the setup.

```python
api.make_all_test_requests()
```

## Response Handling

Every method returns a `Response` object, which can be indexed using integer keys to retrieve address information. Each address is represented as a `WebToolsAddress` object which can be easily printed or accessed using properties.

## Contribution

If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcome.

## Issues

If you discover any issues, bugs, or have feedback, please file an issue on the GitHub page or send a pull request.

## License

This project is licensed under the MIT License.

## Disclaimer

This is an unofficial Python wrapper. Always refer to the official WebTools API documentation for accurate information.