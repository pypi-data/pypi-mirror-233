#!/usr/bin/env python3


# Core Library modules
import json
import re
import sys
from typing import Optional

# Third party modules
import keyring
import requests

# Local modules
from .cli import _parse_args
from .exceptions import request_exception

URL = "http://api.ipstack.com/"


def get_api_key() -> str:
    api_key = keyring.get_password("ipstack", "api_key")
    return api_key


def set_api_key(api_key: str) -> None:
    keyring.set_password("ipstack", "api_key", api_key)


def delete_api_key() -> None:
    keyring.delete_password("ipstack", "api_key")


def validate_key(api_key: str) -> bool:
    if len(api_key) == 32 and api_key.isalnum():
        return True
    else:
        return False


def validate_ipv4(ip: str) -> bool:
    pattern = (
        r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4]"
        r"[0-9]|[01]?[0-9][0-9]?)){3}$"
    )
    return bool(re.match(pattern, ip))


def request_key() -> str:
    new_key = ""
    while True:
        try:
            new_key = input("Please enter your API key:")
            if validate_key(new_key):
                break
            else:
                print(f"'{new_key}' does not appear to be a valid API key")
        except KeyboardInterrupt:
            sys.exit(1)

    set_api_key(new_key)
    return new_key


@request_exception
def get_ip_meta(ip_address: str, api_key: str) -> Optional[str]:
    url = f"{URL}{ip_address}?access_key={api_key}"
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching data. Status code: {response.status_code}")


def get_active_key(stored: str, cli: str) -> Optional[str]:
    if stored is None and cli is None:
        return request_key()
    elif cli is not None:
        if validate_key(cli):
            set_api_key(cli)
            return cli
        elif stored:
            return stored
        else:
            return None
    elif stored:
        return stored


def main():  # type: ignore
    args, parser = _parse_args(sys.argv[1:])
    ip_addr = args.ip_address
    stored_key = get_api_key()
    cli_key = args.key

    active_key = get_active_key(stored_key, cli_key)

    if validate_ipv4(ip_addr):
        meta = get_ip_meta(ip_addr, active_key)
        if meta:
            lat = meta.get("latitude")
            long = meta.get("longitude")
            if lat and long:
                raw = {
                    "ip": ip_addr,
                    "coordinates": {"latitude": lat, "longitude": long},
                }
                print(json.dumps(raw, indent=4))
            else:
                print("An error occurred getting meta data - check your api key")
    else:
        print(f"{ip_addr} is not a valid IPv4 address")


if __name__ == "__main__":
    SystemExit(main())  # type: ignore
