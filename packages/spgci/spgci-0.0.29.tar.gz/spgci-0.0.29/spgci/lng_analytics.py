from __future__ import annotations
from typing import Union, Optional, List
from requests import Response
from spgci.api_client import get_data, Paginator
from spgci.utilities import list_to_filter
from pandas import Series, DataFrame, to_datetime  # type: ignore
from datetime import date


class LNGGlobalAnalytics:
    """
    Lng Tenders Data - Bids, Offers, Trades

    Includes
    --------

    ``get_tenders()`` to see fetch Tenders based on tenderStatus,cargo_type,contract_type,contract_option.\n

    """

    _endpoint = "lng/v1/"

    @staticmethod
    def _paginate(resp: Response) -> Paginator:
        j = resp.json()
        total_pages = j["metadata"]["totalPages"]

        if total_pages <= 1:
            return Paginator(False, "page", 1)

        return Paginator(True, "page", total_pages)

    @staticmethod
    def _convert_to_df(resp: Response) -> DataFrame:
        j = resp.json()
        df = DataFrame(j["results"])

        if len(df) > 0:
            df["openingDate"] = to_datetime(df["openingDate"])
            df["closingDate"] = to_datetime(df["closingDate"])
            df["validityDate"] = to_datetime(df["validityDate"])
            df["liftingDeliveryPeriodFrom"] = to_datetime(
                df["liftingDeliveryPeriodFrom"]
            )
            df["liftingDeliveryPeriodTo"] = to_datetime(df["liftingDeliveryPeriodTo"])

        return df

    def get_tenders(
        self,
        *,
        tender_status: Optional[Union[list[str], "Series[str]", str]] = None,
        cargo_type: Optional[Union[list[str], "Series[str]", str]] = None,
        contract_type: Optional[Union[list[str], "Series[str]", str]] = None,
        contract_option: Optional[Union[list[str], "Series[str]", str]] = None,
        country_name: Optional[Union[list[str], "Series[str]", str]] = None,
        issued_by: Optional[Union[list[str], "Series[str]", str]] = None,
        lifting_delivery_period_from: Optional[date] = None,
        lifting_delivery_period_from_lt: Optional[date] = None,
        lifting_delivery_period_from_lte: Optional[date] = None,
        lifting_delivery_period_from_gt: Optional[date] = None,
        lifting_delivery_period_from_gte: Optional[date] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        raw: bool = False,
        paginate: bool = False,
    ) -> Union[DataFrame, Response]:
        """
        Fetch the data based on the filter expression.

        Parameters
        ----------
        tender_status : Optional[Union[list[str], Series[str], str]], optional
            filter by tender_status, by default None
        cargo_type : Optional[Union[list[str], Series[str], str]], optional
            filter by cargo_type, by default None
        contract_type : Optional[Union[list[str], Series[str], str]], optional
            filter by contract_type, by default None
        contract_option : Optional[Union[list[str], Series[str], str]], optional
            filter by contract_option, by default None
        country_name : Optional[Union[list[str], Series[str], str]], optional
            filter by country_name, by default None
        raw : bool, optional
            return a ``requests.Response`` instead of a ``DataFrame``, by default False
        filter_exp: string
            pass-thru ``filter`` query param to use a handcrafted filter expression, by default None

        Returns
        -------
        Union[pd.DataFrame, Response]
            DataFrame
                DataFrame of the ``response.json()``
            Response
                Raw ``requests.Response`` object

        Examples
        --------
        **Simple**
        >>> ci.LngTenders().get_tenders()
        """
        endpoint_path = "tenders"
        filter_params: List[str] = []
        filter_params.append(list_to_filter("tenderStatus", tender_status))
        filter_params.append(list_to_filter("cargoType", cargo_type))
        filter_params.append(list_to_filter("contractType", contract_type))
        filter_params.append(list_to_filter("contractOption", contract_option))
        filter_params.append(list_to_filter("countryName", country_name))
        filter_params.append(list_to_filter("issuedBy", issued_by))

        if lifting_delivery_period_from is not None:
            filter_params.append(
                f'liftingDeliveryPeriodFrom = "{lifting_delivery_period_from}"'
            )
        if lifting_delivery_period_from_gt is not None:
            filter_params.append(
                f'liftingDeliveryPeriodFrom > "{lifting_delivery_period_from_gt}"'
            )
        if lifting_delivery_period_from_gte is not None:
            filter_params.append(
                f'liftingDeliveryPeriodFrom >= "{lifting_delivery_period_from_gte}"'
            )
        if lifting_delivery_period_from_lt is not None:
            filter_params.append(
                f'liftingDeliveryPeriodFrom < "{lifting_delivery_period_from_lt}"'
            )
        if lifting_delivery_period_from_lte is not None:
            filter_params.append(
                f'liftingDeliveryPeriodFrom <= "{lifting_delivery_period_from_lte}"'
            )

        filter_params = [fp for fp in filter_params if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_params)
        elif len(filter_params) > 0:
            filter_exp = " AND ".join(filter_params) + " AND (" + filter_exp + ")"

        params = {"page": page, "pageSize": page_size, "filter": filter_exp}

        response = get_data(
            path=f"{self._endpoint}{endpoint_path}",
            params=params,
            df_fn=self._convert_to_df,
            paginate_fn=self._paginate,
            raw=raw,
            paginate=paginate,
        )
        return response
