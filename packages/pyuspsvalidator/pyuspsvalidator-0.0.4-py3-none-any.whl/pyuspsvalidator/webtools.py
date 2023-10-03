import requests
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring, dump


class WebToolsRequest:
    def __init__(self, user_id):
        self.user_id = user_id
        self.api_url = 'https://secure.shippingapis.com/ShippingAPI.dll'
        self.test_api_url = 'https://secure.shippingapis.com/ShippingAPITest.dll'
        self.address_fields = ('Address1', 'Address2',
                               'City', 'State', 'Zip5', 'Zip4')
        self.tags = {
            'verify': 'AddressValidateRequest',
            'zipcode': 'ZipCodeLookupRequest',
            'citystate': 'CityStateLookupRequest'
        }
        self.test_data = [
            {
                'address2': '910 West Ave',
                'city': 'Miami Beach',
                'state': 'FL'
            },
            {
                'address2': '601 E. 39th Street',
                'city': 'Miami',
                'state': 'FL',
                'zip5': '33137'
            }
        ]

    def build_request_xml(self, data, root_tag):
        root = Element(root_tag, USERID=self.user_id)
        for i, address in enumerate(data):
            address_element = SubElement(root, 'Address', ID=str(i))
            for field in self.address_fields:
                SubElement(address_element, field).text = address.get(field.lower())
        return tostring(root)

    def request(self, api_name, xml, test=False):
        url = self.test_api_url if test else self.api_url
        response = requests.get(url, params={'API': api_name, 'XML': xml})
        return Response(response)

    def verify(self, data):
        xml = self.build_request_xml(data, self.tags['verify'])
        return self.request('Verify', xml)

    def zipcode_lookup(self, data):
        xml = self.build_request_xml(data, self.tags['zipcode'])
        return self.request('ZipCodeLookup', xml)

    def citystate_lookup(self, data):
        xml = self.build_request_xml(data, self.tags['citystate'])
        return self.request('CityStateLookup', xml)

    def _test_request(self, method):
        api_name = method.capitalize()
        xml = self.build_request_xml(self.test_data, self.tags[method])
        response = self.request(api_name, xml)
        print(response)

    def verify_test(self):
        self._test_request('verify')

    def zipcode_lookup_test(self):
        self._test_request('zipcode')

    def citystate_lookup_test(self):
        self._test_request('citystate')

    def make_all_test_requests(self):
        self.verify_test()
        self.zipcode_lookup_test()
        self.citystate_lookup_test()


class Response:
    def __init__(self, response):
        self.address_fields = (
            'Address1',
            'Address2',
            'City',
            'State',
            'Zip5',
            'Zip4')
        self.response = response
        self.et = self._response_to_et(self.response)
        self._check_et_errors(self.et)
        self.data = self._build_address_dict(self.et)
        self.index = len(self.data)

    def _response_to_et(self, response):
        return fromstring(response.content)

    def _check_et_errors(self, et):
        if et.tag == 'Error':
            print(self.response.status_code)
            print(self.response.content)
            dump(et)
            raise ValueError("Error encountered in the response XML.")

    def _build_address_dict(self, et):
        addresses = {}
        for address_element in et.findall('Address'):
            address = {
                key.lower(): address_element.findtext(key)
                for key in self.address_fields
            }
            address['id'] = address_element.get('ID')
            addresses[address['id']] = WebToolsAddress(address)
        return addresses

    def __getitem__(self, key):
        key = str(key)
        if key in self.data:
            return self.data[key]
        raise IndexError("Key not found: {}".format(key))


class WebToolsAddress:
    def __init__(self, address):
        self._address = address

    def __str__(self):
        fields = ('address1', 'address2')
        address_parts = [
            self._address[field] for field in fields if self._address[field]]
        address_parts.append(self.last_line)
        return "\n".join(address_parts)

    @property
    def address1(self):
        return self._address['address1']

    @property
    def address2(self):
        return self._address['address2']

    @property
    def city(self):
        return self._address['city']

    @property
    def state(self):
        return self._address['state']

    @property
    def zip4(self):
        return self._address['zip4']

    @property
    def zip5(self):
        return self._address['zip5']

    @property
    def address_lines(self):
        return "\n".join([self.address1, self.address2]).strip()

    @property
    def zipcode(self):
        return '{}-{}'.format(self.zip5, self.zip4)

    @property
    def citystate(self):
        return '{}, {}'.format(self.city, self.state)

    @property
    def last_line(self):
        return '{} {}'.format(self.citystate, self.zipcode)
