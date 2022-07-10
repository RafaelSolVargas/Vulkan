from typing import Dict


class URLAnalyzer:
    def __init__(self, url: str) -> None:
        self.__url = url
        self.__queryParamsQuant = self.__url.count('&') + self.__url.count('?')
        self.__queryParams: Dict[str, str] = self.__getAllQueryParams()

    @property
    def queryParams(self) -> dict:
        return self.__queryParams

    @property
    def queryParamsQuant(self) -> int:
        return self.__queryParamsQuant

    def getCleanedUrl(self) -> str:
        firstE = self.__url.index('&')
        return self.__url[:firstE]

    def __getAllQueryParams(self) -> dict:
        if self.__queryParamsQuant <= 1:
            return {}

        params = {}
        arguments = self.__url.split('&')
        arguments.pop(0)

        for queryParam in arguments:
            queryName, queryValue = queryParam.split('=')
            params[queryName] = queryValue

        return params
