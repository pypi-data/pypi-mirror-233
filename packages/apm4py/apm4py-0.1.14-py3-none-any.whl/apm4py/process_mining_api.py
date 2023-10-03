"""
All functional parts of the API are combined in the class ProcessMiningAPI.

"""

from apm4py.aggregation import AggregationAPI
from apm4py.logs import LogsAPI
from apm4py.resources import ResourceAPI


class ProcessMiningAPI(LogsAPI, AggregationAPI, ResourceAPI):
    """The Python API for Appian Process Mining.

    It allows programmatic management of all lana resources.

    All required information to make authenticated requests to the api are
    passed during construction and stored. Named request methods are
    provided as wrappers around requests library methods, that add required
    header fields. Additional headers to the requests library methods can be
    passed as keyword arguments.

    Attributes:
        url (str):
            The base url of the api (scheme, host and port).
        user (User):
            A User dataclass encapsulating the user of the api information.
        headers (dict):
            The authorization header used for every request by default.
    """

    pass
