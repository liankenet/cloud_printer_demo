import requests


class LiankePrintingBase:
    API_BASE_URL = "https://cloud.liankenet.com"

    def __init__(self, api_key):
        self._http = requests.Session()
        self.api_key = api_key

    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith(("http://", "https://")):
            api_base_url = kwargs.pop("api_base_url", self.API_BASE_URL)
            url = f"{api_base_url}{url_or_endpoint}"
        else:
            url = url_or_endpoint

        if "headers" not in kwargs:
            kwargs["headers"] = {"API_KEY": self.api_key}

        res = self._http.request(method=method, url=url, **kwargs)
        try:
            res.raise_for_status()
        except requests.RequestException as reqe:
            raise WeChatClientException(
                errcode=None,
                errmsg=None,
                client=self,
                request=reqe.request,
                response=reqe.response,
            )

        return self._handle_result(res, method, url, **kwargs)

    def _handle_result(self, res, method=None, url=None, **kwargs):
        result = json.loads(res.content.decode("utf-8", "ignore"), strict=False)
        if "errcode" in result:
            result["errcode"] = int(result["errcode"])

        if "errcode" in result and result["errcode"] != 0:
            errcode = result["errcode"]
            errmsg = result.get("errmsg", errcode)
            if self.auto_retry and errcode in (
                WeChatErrorCode.INVALID_CREDENTIAL.value,
                WeChatErrorCode.INVALID_ACCESS_TOKEN.value,
                WeChatErrorCode.EXPIRED_ACCESS_TOKEN.value,
            ):
                logger.info("Component access token expired, fetch a new one and retry request")
                self.fetch_access_token()
                kwargs["params"]["component_access_token"] = self.session.get(
                    f"{self.component_appid}_component_access_token"
                )
                return self._request(method=method, url_or_endpoint=url, **kwargs)
            elif errcode == WeChatErrorCode.OUT_OF_API_FREQ_LIMIT.value:
                # api freq out of limit
                raise APILimitedException(errcode, errmsg, client=self, request=res.request, response=res)
            else:
                raise WeChatClientException(errcode, errmsg, client=self, request=res.request, response=res)
        return
