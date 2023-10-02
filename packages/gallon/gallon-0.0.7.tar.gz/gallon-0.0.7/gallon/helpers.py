
import functools
import logging
from typing import Any

from .data import GallonModel, dumps
from .objects import Response


@functools.singledispatch
def make_response(response: Any):
    """Return the response"""
    return response

@make_response.register(Response)
def _(response: Response):
    """Return the response"""
    return response

@make_response.register(int)
def _(response: int):
    """Return the response"""
    return make_response(
        Response(
            status=response,
            headers={"Content-Type": "text/plain"},
            body="",
        )
    )

@make_response.register(bytes)
def _(response: bytes):
    """Return the response"""
    return make_response(
        Response(
            status=200,
            headers={"Content-Type": "application/octet-stream"},
            body=response,
        )
    )

@make_response.register(bytearray)
def _(response: bytearray):
    """Return the response"""
    return make_response(
        Response(
            status=200,
            headers={"Content-Type": "application/octet-stream"},
            body=response,
        )
    )

@make_response.register(bool)
def _(response: bool):
    """Return the response"""
    return make_response(
        Response(
            status=200,
            headers={"Content-Type": "text/plain"},
            body=str(response),
        )
    )

@make_response.register(float)
def _(response: float):
    """Return the response"""
    return make_response(
        Response(
            status=200,
            headers={"Content-Type": "text/plain"},
            body=str(response),
        )
    )


@make_response.register(str)
def _(response: str): 
    if response.startswith("<"):
        return make_response(
            Response(
                status=200,
                headers={"Content-Type": "text/html"},
                body=response,
            )
        )
    return make_response(
        Response(
            status=200,
            headers={"Content-Type": "text/plain"},
            body=response,
        )
    )


@make_response.register(dict)
def _(response: dict[str, Any]):
    return make_response(
        Response(
            status=200,
            headers={"Content-Type": "application/json"},
            body=dumps(response),
        )
    )


@make_response.register(GallonModel)
def _(response: GallonModel):
    return make_response(
        Response(
            status=200,
            headers={"Content-Type": "application/json"},
            body=dumps(response.dict()),
        )
    )


@make_response.register(list)
def _(response: list[GallonModel]):
    return make_response(
        Response(
            status=200,
            headers={"Content-Type": "application/json"},
            body=dumps([item.dict() for item in response]),
        )
    )

@make_response.register(tuple)
def _(response: tuple[GallonModel]):
    return make_response(
        Response(
            status=200,
            headers={"Content-Type": "application/json"},
            body=dumps([item.dict() for item in response]),
        )
    )

@make_response.register(set)
def _(response: set[GallonModel]):
    return make_response(
        Response(
            status=200,
            headers={"Content-Type": "application/json"},
            body=dumps([item.dict() for item in response]),
        )
    )

@make_response.register(type(None))
def _(response: None):
    return make_response(
        Response(
            status=200,
            headers={"Content-Type": "text/plain"},
            body="",
        )
    )



def setup_logger():
    """Setup the logger"""
    logger = logging.getLogger("Gallon Server")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(handler)
    return logger
