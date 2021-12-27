import os
import json

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class HTTPClientException(Exception):
    def __init__(self, message, status_code=None):
        self.status_code = status_code
        super().__init__(message)

    @classmethod
    def create_from_response(cls, response):
        parsed_response = response.json()
        try:
            message = "Server returned {}, code {}: {}".format(
                response.status_code,
                parsed_response["code"],
                parsed_response["message"],
            )
        except Exception:
            message = "Server returned {}".format(response.status_code)

        return cls(message, response.status_code)


class BaseHTTPClient:
    def __init__(self, host, port):
        if not host.startswith("http://"):
            self.host = "http://" + host
        self.port = port
        self.base_url = "{}:{}".format(self.host, self.port)

        self.sess = requests.Session()
        retry_strategy = Retry(
            total=5, backoff_factor=0.1, status_forcelist=[502, 503, 504]
        )
        self.sess.mount("http://", HTTPAdapter(max_retries=retry_strategy))

    def do_request(
        self,
        method,
        url,
        operation_name,
        headers=None,
        data=None,
        params=None,
        json=None,
        client_exception_class=None,
        timeout=None,
    ):
        client_exception_class = client_exception_class or HTTPClientException
        if not issubclass(client_exception_class, HTTPClientException):
            raise TypeError()

        headers = headers or {}

        try:
            resp = self.sess.request(
                method,
                url,
                headers=headers,
                data=data,
                params=params,
                json=json,
                timeout=timeout,
            )
            if int(resp.status_code) // 100 != 2:
                raise client_exception_class.create_from_response(resp)
            elif resp.status_code == 204:
                return resp.text
            return resp.json()
        except client_exception_class as e:
            raise e
        except Exception as e:
            raise client_exception_class(
                "Error in {}: {}".format(operation_name, str(e))
            ) from e


class StylePredictorClient(BaseHTTPClient):
    def get_base_url(self):
        return self.base_url + "/api/v1"

    def predict(self, text, model_name):
        # "http://localhost:8080/v1/Predictions/predict"

        url = self.get_base_url() + "/Predictions/predict"
        data = {"text": text, "model_name": model_name}
        response = self.do_request(
            method="POST",
            url=url,
            operation_name="predict",
            data=data,
        )
        return response


