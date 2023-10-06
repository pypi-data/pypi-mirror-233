from pprint import pprint as _pprint
import typing as _typing
import urllib.parse as _parse
from typing import Optional as _Optional, List as _List
import urllib.parse as _urllib_parse

import requests as _requests

from .connection import FetchModule as __FetchModule
from .snapshot import SnapshotModule as _SnapshotModule
from . import schemas as _schemas
from .schemas import DataType, ParamDatetime, _ParamDataType

_PATH_PARSE = "parse"


class DPHelper(__FetchModule):  # also includes Config
    def __init__(
        self,
        *,
        is_verbose=False,
        proxy_provider=None,
        proxy_params={},
        request_drop_on_failure_count=4,
        request_initial_sleep_after_failure_in_s=3,
        request_sleep_increase_power=2,
        backend_url="https://data-platform-backend-4ddpl.ondigitalocean.app",
    ) -> None:
        self._init_config_values()
        self.IS_VERBOSE = bool(is_verbose)
        self.REQUEST_DROP_ON_FAILURE_COUNT = int(request_drop_on_failure_count)
        self.REQUEST_INITIAL_SLEEP_AFTER_FAILURE_IN_S = int(
            request_initial_sleep_after_failure_in_s
        )
        self.REQUEST_SLEEP_INCREASE_POWER = int(request_sleep_increase_power)
        self.set_backend_url(str(backend_url))
        self.snapshot = _SnapshotModule(config=self, fetcher=self)
        self.PROXY_PROVIDER = proxy_provider
        self.PROXY_PARAMS = proxy_params

    def __get_utils_url(self, path: str) -> str:
        "joins root url with specified path"
        # appending "/" to root so path gets joined, not overwriten
        # >>> "http://q.w/r" == _parse.urljoin("http://q.w/e", "r")
        # >>> "http://q.w/e/r" == _parse.urljoin("http://q.w/e" + "///////", "r")
        url = _parse.urljoin(self.BACKEND_URL + "/", self.BACKEND_UTILS_PATH)
        return _parse.urljoin(url + "/", path)

    def parse_rows(
        self,
        schema: _List[str],
        data: _List[_List[str]],
        verbose: _Optional[bool] = None,
    ) -> _List[dict]:
        """parses from (look below) to list of dict (look even more below)
        >>> schema = [header1, header2, ...]
        >>> data = [
            [cell1_value, cell2_value, ...],  # 1st row
            [Cell1_value, Cell2_value, ...],  # 2nd row
            ...
        ]

        returns list of dict:
        >>> return_value = [
            {header1: cell1_value, header2: cell2_value}, # 1st row
            {header2: Cell1_value, header2: Cell2_value}, # 2nd row
            ...
        ]

        :param schema: list of headers (eg price, area, floor, id, balcony, status, ...)
        :param data: two-dimensional list of data; It will be parsed as `data[row][column]`. Value has to be json-serializable (string, int, float, not instance of class, ...)
        :param verbose: shall error text be printed?"""
        # local verbose > config verbose
        verbose = self.IS_VERBOSE if verbose is None else verbose

        _data = {
            "schema": schema,
            "data": data,
        }

        response = self._request_or_repeat(
            _requests.post,
            url=self.__get_utils_url(_PATH_PARSE),
            json=_data,
            params={"cell_cnt": len(schema) * len(data)},
        )

        try:
            json_data: dict = response.json()
            is_success = json_data["is_success"]
            if not is_success and verbose:
                _pprint(json_data.get("error"))
            return json_data.get("results", [])
        except Exception:
            raise RuntimeError(
                "Could not understand remote server response for rows-parsing. "
                f"Try updating {self.PACKAGE_NAME} and try again"
            )

    def transform_map(
        self,
        schema_map: dict,
        data: _List[dict],
        parse=True,
        verbose: _Optional[bool] = None,
        *,
        exclude_extra_fields=False,
        parse_also_extra_fields=False,
    ) -> _List[dict]:
        """Renames keys of data, parses on demand.
        >>> schema_map = {"kaina": "price", "plotas": "area"}
        >>> data = [{"kaina": 1, "plotas": 2}]
        >>> return_data = [{"price": 1, "area": 2}] # if parse is False

        :param schema_map: dict where key is old-key, value is new-key (the one which is wanted)
        :param data: list of dicts, whose keys will be renamed, values parsed (if parse=True)
        :param parse: rename schema and parse values? Elsewise, only schema will be renamed
        :param verbose: verbose parse_rows errors?
        :param exlude_extra_fields: should fields, that are not inside schema_map, be excluded from result?
        :param parse_also_extra_fields: should extra fields be parsed? else they will sustain original formatting.
        :return: list of dicts with renamed keys
        """

        keys_old = schema_map.keys()
        keys_extra = set(data[0].keys()) - set(keys_old)
        keys_combined = keys_extra.union(set(keys_old))

        if not exclude_extra_fields:
            # if extra fields not to be excluded, make sure the data is not malformed:
            # each row has exactly same keys

            for i, row in enumerate(data):
                row_keys = set(row.keys())
                if row_keys != keys_combined:
                    extra = row_keys - keys_combined
                    extra_str = f"data[{i}] has extra keys: {extra}; " if extra else ""
                    missing = keys_combined - row_keys
                    missing_str = (
                        f"data[{i}] is missing these keys: {missing}; "
                        if missing
                        else ""
                    )
                    raise RuntimeError(
                        "Keys mismatch in transformation: " f"{extra_str}{missing_str}"
                    )

        if parse:
            is_extra_excluded = exclude_extra_fields or not parse_also_extra_fields
            _keys = keys_old if is_extra_excluded else keys_combined
            unpack_dict = lambda row: [row.get(key) for key in _keys]
            schema = [schema_map[key] if key in keys_old else key for key in _keys]
            parsed_data = self.parse_rows(
                # values of schema_map - to what we want to rename
                schema=schema,
                # for parsing, data has to be without labels, unpacked into array
                data=[unpack_dict(row) for row in data],
                verbose=verbose,
            )

            # parsed data loses unparsed fields. Append them
            if not exclude_extra_fields and not parse_also_extra_fields:
                for new_row, old_row in zip(parsed_data, data):
                    new_row.update({key: old_row.get(key) for key in keys_extra})

            return parsed_data

        # else we will do renaming locally
        return [
            {
                schema_map.get(key) if key in keys_old else key: row.get(key)
                for key in keys_combined
            }
            for row in data
        ]

    @staticmethod
    def update_table(
        data: _List[dict],
        f_check: _typing.Callable[[dict], bool],
        f_update: _typing.Callable[[dict], dict],
    ) -> _List[dict]:
        """updates matching table rows using provided `f_update`. Returns altered table.

        :param data: list of dictionaries - list of rows.
        :param f_check: function that will return `True` if the row has to be altered.
        This function will be checked upon each row.
        :param f_update: function whose returned value will be applied to checked rows.
        :return: Altered version of original table
        """
        results: list[dict] = []
        for row in data:
            result = {}
            result.update(row)
            if f_check(row):
                payload = f_update(row)
                result.update(payload)

            results.append(result)

        return results

    def geocode(self, location: str, is_reverse: bool) -> dict:
        """
        also see `.get_coords(...)`, `.get_address(...)`
        :param location: address or lat,lng
        :param is_reverse: reverse geocode coordinates to address? (Expect coordinates in location?)
        :return:
        {'address': 'smth', 'lat': 55.55, 'lng': 55.55, ...}"""
        response = self._request_or_repeat(
            _requests.post,
            self.__get_utils_url("geocode/"),
            params={"is_reverse": is_reverse},
            json={"location": str(location)},
        )
        self._response_ok_or_raise(response)
        return response.json()

    @staticmethod
    def __coords_to_location(lat: float, lng: float) -> str:
        return f"{lat},{lng}"

    def get_coords(self, address: str) -> dict:
        """>>> .get_coords("Didlaukio g. 59, Vilnius")
        {'lat': 54.7316978, 'lng': 25.2619945}

        """
        location = self.geocode(address, is_reverse=False)
        return {"lat": location.get("lat"), "lng": location.get("lng")}

    def get_address(self, lat: float, lng: float) -> _Optional[str]:
        """>>> .get_address(54.7316978, 25.2619945)
        'Didlaukio g. 59, 08302 Vilnius, Lithuania'
         >>> # would return None if no address found by coordinates
        """
        location = self.geocode(self.__coords_to_location(lat, lng), is_reverse=True)
        return location.get("address")

    def get_address_components(
        self,
        address: _Optional[str] = None,
        lat: _Optional[float] = None,
        lng: _Optional[float] = None,
        raw=True,
    ):
        if not raw:
            raise NotImplemented(
                f"Not raw address components are not supported in current {self.PACKAGE_NAME} version."
            )
        is_reverse = False if address else True
        location_str = address if address else self.__coords_to_location(lat, lng)
        location = self.geocode(location_str, is_reverse=is_reverse)
        return location.get("raw_address_components")

    def parse_value(
        self,
        value: _typing.Any,
        _type: DataType,
        params: _typing.Dict[_ParamDataType, _typing.Any] = None,
        verbose: _Optional[bool] = None,
    ) -> _typing.Any:
        """parses a single value using datatype and appending its parameters:
        if datatype is DataType.DATETIME and params is {ParamsDatetime.LOCALE: "lt"},
        then datatype will be transformed into `datetime?locale=lt` .
        returns parsed value
        """
        if isinstance(params, dict):
            _new_dict = {}
            for _key, _value in params.items():
                # normalize, to avoid "ParamDatetime.LOCALE" as key
                _key = _key.value if isinstance(_key, _ParamDataType) else str(_key)
                _new_dict[_key] = _value
            params = _new_dict

        # todo: find lib that would handle array values correctly (not as str(array))
        _params = _urllib_parse.urlencode(params) if params else None
        _type = _type.value if isinstance(_type, DataType) else str(_type)
        _type = f"{_type}?{_params}" if _params else _type

        results = self.parse_rows(schema=[_type], data=[[value]], verbose=verbose)
        if results is None:
            return None
        elif len(results) == 0:
            return None
        else:
            row = results[0]
            if len(row) != 1:
                return None
            # return first value because only one value was to be parsed
            return next(iter(row.values()))
