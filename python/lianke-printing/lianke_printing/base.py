import requests


class LiankePrintingException(Exception):
    def __init__(self, code: [int, None], msg: str, client=None, request=None, response=None):
        """
        :param code: Error code
        :param msg: Error message
        """
        self.code = code
        self.msg = msg
        self.client = client
        self.request = request
        self.response = response

    def __str__(self):
        s = f"Error code: {self.code}, message: {self.msg}"
        return s

    def __repr__(self):
        _repr = f"{self.__class__.__name__}({self.code}, {self.msg})"
        return _repr


class LiankePrintingBase:
    API_BASE_URL = "https://cloud.wisiyilink.com/api"

    def __init__(self, api_key: str, device_id: str, device_key: str):
        self._http = requests.Session()
        self.api_key = api_key
        self.device_id = device_id
        self.device_key = device_key

    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith(("http://", "https://")):
            api_base_url = kwargs.pop("api_base_url", self.API_BASE_URL)
            url = f"{api_base_url}{url_or_endpoint}"
        else:
            url = url_or_endpoint

        if "headers" not in kwargs:
            kwargs["headers"] = {"API_KEY": self.api_key}
        else:
            kwargs["headers"]["API_KEY"] = self.api_key

        res = self._http.request(method=method, url=url, **kwargs)
        try:
            res.raise_for_status()
        except requests.RequestException as reqe:
            raise LiankePrintingException(
                code=None,
                msg="",
                client=self,
                request=reqe.request,
                response=reqe.response,
            )

        return self._handle_result(res, method, url, **kwargs)

    def _handle_result(self, res, method=None, url=None, **kwargs):
        result = res.json()
        if "code" in result and result["code"] != 200:
            code = result["code"]
            msg = result.get("msg")
            raise LiankePrintingException(code, msg, client=self, request=res.request, response=res)
        return result

    def get(self, url, **kwargs):
        return self._request(method="get", url_or_endpoint=url, **kwargs)

    def post(self, url, **kwargs):
        return self._request(method="post", url_or_endpoint=url, **kwargs)

    def delete(self, url, **kwargs):
        return self._request(method="delete", url_or_endpoint=url, **kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._http.close()
