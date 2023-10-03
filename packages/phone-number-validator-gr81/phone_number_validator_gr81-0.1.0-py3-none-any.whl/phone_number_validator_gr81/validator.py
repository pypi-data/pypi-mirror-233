import requests


# PhoneNumberValidator class initializes with an API key and returns a class instance.
# This object provides a URL as a service endpoint to verify the validity of a provided phone number.
#
# There are two methods in the class:
#   - _make_api_call(): Private method. It constructs the request and communicates with the API.
#   - validate(): Public method. It checks if the phone number is not empty, makes an API call, 
#                 checks for successful response and then validates the content of response.
#
# Note: Method validate() will raise ValueError if the phone number is empty.
#       It also raises any HTTP errors if response from API is not OK (200).

class PhoneNumberValidator:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.api_url = "https://api.numlookupapi.com/v1/validate/"

    def _make_api_call(self, phone_number: str, country_code: str = None):
        params = {"apikey": self.api_key}
        if country_code:
            params["country_code"] = country_code
        response = requests.get(self.api_url + phone_number, params=params)
        return response

    def validate(self, phone_number: str, country_code: str = None) -> bool:
        if not phone_number:
            raise ValueError("Phone Number cannot be empty!")
        response = self._make_api_call(phone_number, country_code)

        if response.ok:
            return response.json()["valid"]
        else:
            response.raise_for_status()
