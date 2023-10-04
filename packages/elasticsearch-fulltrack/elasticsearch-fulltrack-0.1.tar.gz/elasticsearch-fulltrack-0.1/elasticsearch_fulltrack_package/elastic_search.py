"""DSL Search."""
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple
from dateutil.tz import UTC
from django.utils import dateparse
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q, Search, connections
import pytz

logger = logging.getLogger(__name__)
date_types = ["shipment_date", "date_shipped", "delivery_date", "latest_event_time", "latest_harmonized_update_time"]

class ElasticSearchFulltrack(object):
    
    def __init__(self,es_host=None,es_user=None,es_password=None,parcel_status=None,es_port=None):
        self.es_password = es_password
        self.es_user = es_user
        self.es_host = es_host
        self.es_port = es_port 
        self.parcel_statuses = parcel_status 

    def _es_config(self) -> None:
        port = self.es_port
        schema = "https"
        host = self.es_host
        user = self.es_user
        password = self.es_password
        url = f"{schema}://{host}:{port}"
        client = Elasticsearch(
            url, basic_auth=(user, password), ca_certs="ca.crt", verify_certs=False, max_retries=5, retry_on_timeout=True
        )
        connections.add_connection("default", client)


    def _range_filter(
        self,
        filter_type: str,
        filter_data: Dict[Any, Any],
        open_api_request: bool = True,
    ) -> Q:
        """Add date filter."""
        start_date = filter_data["start_date"]
        end_date = filter_data["end_date"]
        not_shipment = None

        if start_date is None and end_date is None:
            end_date = datetime.now(UTC)
            start_date = end_date - timedelta(days=30 * 6)
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            filter_type = "shipment_date"
            not_shipment = Q("bool", should=[~Q("exists", field="shipment_date")])
        else:
            if open_api_request:
                start_date = dateparse.parse_datetime(start_date)
                end_date = dateparse.parse_datetime(end_date)
                # Convert the datetime to UTC timezone
                utc_timezone = pytz.timezone('UTC')
                start_date = start_date.astimezone(utc_timezone)
                end_date = end_date.astimezone(utc_timezone)
            else:
                start_date = dateparse.parse_datetime(start_date).date()
                end_date = dateparse.parse_datetime(end_date).date()
                if end_date:
                    end_date = end_date + timedelta(days=1)

        date_filter = Q("range", **{filter_type: {"gte": start_date, "lte": end_date}})
        return date_filter | not_shipment if not_shipment else date_filter

    def _terms_filter(self,filter_name: str, filter_data: Dict[str, str]) -> Q:
        """Carrier Filter."""
        filter_type = {filter_name: filter_data}
        return Q("terms", **filter_type)


    def sort_data(self,s: Search, sort_key: str, is_forward: bool) -> Search:
        """Add sort."""
        original_sort = "asc"
        if sort_key.startswith("-"):
            sort_key = sort_key[1:]
            original_sort = "desc"

        if original_sort == "asc":
            order = "asc" if is_forward else "desc"
        else:
            order = "desc" if is_forward else "asc"

        if sort_key not in date_types:
            sort_key = f"{sort_key}"
        sort_query = {sort_key: order, "ft_id": order}
        return s.sort(sort_query)


    def paginate(self,s: Search, prev_sort: list[str], page_size: int) -> Search:
        """Add pagination."""
        extra_param: dict[str, Any] = {"size": page_size}
        if prev_sort:
            extra_param.update({"search_after": prev_sort})
        return s.extra(**extra_param)


    def _search_es(self, search_request: Dict[Any, Any], open_api_request=False) -> Q:
        # Mapping of field name aliases
        rename_mappings = {
            "carrier": "carrier_name",
            "origin": "origin",
            "destination": "destination",
            "product_code": "product_code",
            "customer": "customer_id",
            "recipient_name": "recipient_name",
            "shipment_date": "shipment_date",
            "date_shipped": "date_shipped",
            "status": "current_status",
            "subsidiary_id": "subsidiary_id",
            "delivery_date": "delivery_date",
        }

        # Rename the keys in search_request based on the mappings
        updated_search_request = {rename_mappings.get(key, key): value for key, value in search_request.items()}

        all_filter = []
        filter_types = {
            "range": date_types,
            "terms": [
                "current_status",
                "subsidiary_id",
                "carrier_name",
                "origin",
                "destination",
                "product_code",
                "customer_id",
                "recipient_name",
            ],
        }

        # Check if "range" filters are present in the search_request
        found_range_filters = any(item in updated_search_request for item in filter_types["range"])
        if (not found_range_filters) and not open_api_request:
            # If no "range" filters are found and open_api is True, set shipment_date to None
            updated_search_request["shipment_date"] = {"start_date": None, "end_date": None}

        if "ids" in updated_search_request:
            # Handle "ids" filter
            id_fields = ["tracking_id",] if open_api_request else ["tracking_id","business_id","order_id"]
            id_filter = Q(
                "bool",
                should=[self._terms_filter(field, updated_search_request["ids"]) for field in id_fields],
            )
            all_filter.append(id_filter)

        for filter_type, filter_value in updated_search_request.items():
            search_filter = None
            if filter_type in filter_types["range"]:
                search_filter = self._range_filter(filter_type, filter_value,open_api_request=open_api_request)
            if filter_type in filter_types["terms"]:
                search_filter = self._terms_filter(filter_type, filter_value)
            if search_filter:
                all_filter.append(search_filter)

        return Q("bool", must=all_filter)


    def _add_calculated_fields(self,data):
        """"""
        from apps.parcels.views import GridView

        data = GridView.get_stepper_status(data)
        return GridView.get_harmonized_desc(data)


    def _inject_sort_result(self,hit, final_data):
        """Sort result."""

        sort = hit["sort"]
        sort_params = []
        for param in sort:
            sort_params.append(str(param))
        final_data["sort"] = sort_params


    def _inject_script_fields(self,source_data, field_data):
        """Inject script fields."""
        extra_fields = ["parcel_status", "subsidiary_name", "parcel_progress_as_int"]
        for key in field_data:
            if key in extra_fields:
                source_data[key] = field_data[key][0]

    def _get_count(self,s: Search) -> int:
        return int(s.count())


    def _get_data(self,s, open_api_request=False,reverse=False):
        response = s.execute()
        hits = response["hits"]["hits"]
        data = []
        sort_value = None
        for hit in hits:
            source_data = hit["_source"].to_dict()
            self._inject_sort_result(hit, source_data)
            sort_value = source_data.get("sort")
            
            if not open_api_request:
                field_data = hit["fields"].to_dict()
                self._inject_script_fields(source_data, field_data)

            if open_api_request:
                item = {
                    "tracking_id": source_data.get("tracking_id"),
                    "current_status": self.parcel_statuses[int(source_data.get("current_status"))],
                    "latest_event_time": source_data.get("latest_event_time"),
                    "order_id": source_data.get("order_id"),
                    "business_id": source_data.get("business_id"),
                    "destination": source_data.get("destination"),
                    "origin": source_data.get("origin"),
                    "ft_id": source_data.get("ft_id"),
                    "return_ref": source_data.get("return_ref")
                }
            else:
                item = source_data
            data.append(item)
        return data,sort_value
    
    def get_ft_ids(self,data: List[dict]) -> List[str]:
        """
        Extract ft_ids from a list of dictionaries.

        Args:
            data (List[dict]): A list of dictionaries containing data.

        Returns:
            List[str]: A list of ft_ids extracted from the data.
        """
        return [item["ft_id"] for item in data]
    
    def open_api_filters(self,customer_id):
        customer_id_filter = Q("term", customer_id=customer_id)
        return customer_id_filter

    def search(self,search_request: Dict[Any, Any], open_api_request=False, paginate_=True, bulk=False,date_range=False) -> List[str]:
        """Search in Elasticsearch index."""
        self._es_config()
        sort_field = search_request['sort']
        s = Search(using="default",index="parcel_grid").params(request_timeout=30)
        
        merged_query = self._search_es(search_request=search_request,open_api_request=open_api_request)
        s = s.query(merged_query)
        s = self.sort_data(s, sort_field, search_request.get("forward",None))        
        s = self.paginate(s, search_request.get("search_after", None), search_request.get("secret_pagu_sizu", 50))
        if not open_api_request:
            s = s.script_fields(
            subsidiary_name={
                "script": {"source": "def subsidiary = doc['subsidiary'].value; return subsidiary.replace('_', ' ');"}
            },
            parcel_status={
                "script": {
                    "source": "if (doc['exception_status'].size() != 0 && doc['exception_status'].value < 0) "
                    "{ 'Exception Parcel' } "
                    "else if (doc['return_ref'].value.contains('T') ||"
                    " doc['return_ref'].value.contains('true')) "
                    "{ 'Return Parcel' }"
                    " else { 'Outbound Parcel' }"
                }
            },
            parcel_progress_as_int={
                "script": {
                    "source": "if(doc['parcel_progress'].size() != 0)"
                    "{return (int)(doc['parcel_progress'].value)} return null"
                }
            },
            ).source("*")
        count = self._get_count(s)
        data,sort_value = self._get_data(s,open_api_request=open_api_request)
        if not search_request["forward"]:
            data.reverse()
        if open_api_request:
            return data ,True if len(data) > int(search_request.get("secret_pagu_sizu", 50)) else False,sort_value
        return data ,True if len(data) > int(search_request.get("secret_pagu_sizu", 50)) else False,count
