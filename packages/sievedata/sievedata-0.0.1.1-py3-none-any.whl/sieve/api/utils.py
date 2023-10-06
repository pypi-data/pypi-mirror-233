"""
Utility functions for the Sieve API
"""

import requests
from .auth import api_key

def post(
    url,
    data,
    headers={
        'Content-Type': 'application/json',
        'X-API-KEY': api_key()
    }
):
    """
    POST data to a URL
    """

    return requests.post(url, json=data, headers=headers)

def get(
    url,
    headers={
        'Content-Type': 'application/json',
        'X-API-KEY': api_key()
    }
):
    """
    GET data from a URL
    """
    return requests.get(url, headers=headers)

def delete(
    url,
    headers={
        'Content-Type': 'application/json',
        'X-API-KEY': api_key()
    }
):
    """
    DELETE data from a URL
    """
    return requests.delete(url, headers=headers)
