"""Base Request and Response Objects"""
import re
from typing import Dict, Optional
from urllib.parse import parse_qs, urlparse

from .data import GallonModel, Json, field, loads

JSON_CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    "Content-Type": "application/json",
}

PATHPARAM_REGEX = re.compile(r"{(\w+)}")



class Request(GallonModel):
    """
    Request Object
    Interface that defines the shape of incoming http requests
    """

    url: str = field(...)
    method: str = field(...)
    body: Optional[str] = field(default=None)
    path_params: Optional[Dict[str, str]] = field(default=None)
    headers: Dict[str, str] = field(default_factory=lambda:JSON_CORS_HEADERS)
    
    def json(self, exclude_none: bool = True): # type: ignore
        """
        Convert and return the body as a JSON object if Content-Type is application/json.

        Returns:
            None: if body is empty or Content-Type is not application/json.
            Json: the body as a JSON object.
        """
        if self.body is None:
            raise ValueError("Request body is empty")
        if self.headers.get("Content-Type") != "application/json":
            raise ValueError("Request Content-Type is not application/json")
        body = loads(self.body)
        if exclude_none:
            if isinstance(body, dict):
                for key, value in body.items():
                    if value is None:
                        body.pop(key)
                return body
            else:
                return [v for v in body if v is not None ] # type: ignore
        return body

    @property
    def content_type(self):
        """
        Get the value of the Content-Type header.

        Returns:
            str: the value of the Content-Type header.
        """
        return self.headers.get("content-type", "application/json")

    @property
    def content_length(self):
        """
        Get the value of the Content-Length header.
        If Content-Length is not set, it calculates the length of the body and sets the header accordingly.

        Returns:
            str: the value of the Content-Length header.
        """
        if self.headers.get("Content-Length") is None:
           raise ValueError("Request Content-Length is not set")
        assert self.headers.get("Content-Length") == str(len(self.body or ""))
        return self.headers.get("Content-Length", "0")

    @property
    def query(self):
        """
        Parse and return the query parameters from the URL.

        Returns:
            dict: the query parameters.
        """
        return {k: v[0] for k, v in parse_qs(urlparse(self.url).query).items()}


class Response(GallonModel):
    """
    Response Object
    Interface that defines the shape of outgoing http responses
    """

    status: int = field(default=200)
    body: Optional[str] = field(default=None)
    headers: dict[str,str] = field(...)
   
    def json(self, exclude_none: bool = True)->Json: # type: ignore
        """
        Convert and return the body as a JSON object.

        Returns:
            None: if body is empty.
            Json: the body as a JSON object.
        """
        if self.body is None:
            return {}
        if exclude_none:
            body = loads(self.body)
            if isinstance(body, dict):
                for key, value in body.items():
                    if value is None:
                        body.pop(key)
                return body
            else:
                return [v for v in body if v is not None ]  # type: ignore
        return loads(self.body)

    @property
    def content_type(self)->str:
        """
        Get the value of the Content-Type header.

        Returns:
            str: the value of the Content-Type header.
        """
        return self.headers.get("Content-Type", "application/json") 

    @property
    def content_length(self)->str:  
        """
        Get the value of the Content-Length header.
        If Content-Length is not set, it calculates the length of the body and sets the header accordingly.

        Returns:
            str: the value of the Content-Length header.
        """
        if self.headers.get("Content-Length") is None:
            self.headers["Content-Length"] = str(len(self.body or ""))
        assert self.headers.get("Content-Length") == str(len(self.body or ""))  
        return self.headers.get("Content-Length", "0")
