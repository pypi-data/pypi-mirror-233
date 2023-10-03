"""
Methods for creating the python API for Appian Process Mining.
"""

import warnings
from typing import Optional

from .process_mining_api import ProcessMiningAPI


def create_api(
    scheme: str,
    host: str,
    token: Optional[str] = None,
    instance: int = 1,
    port: int = None,
    application_root: str = None,
    **kwargs,
):
    """Create a configured Lana API.

    The returned api stores the url for a Appian Process Mining
    api as well as your authentication. After creation you can us it to
    manage the Appian process mining resources. Among other things you can
    upload data from python pandas data frames directly or connect logs
    and shiny dashboard resources referencing them by their names.

        api = create_api('https', 'cloud-backend.lanalabs.com', '<a token>')
        upload_response = api.upload_event_log_df(
                                'new-event-log', df_event_log,
                                time_format='YYYY-mm-dd,
                                df_case=df_case_attributes)
        shiny_dashboard = api.create_shiny_dashboard('new-shiny-dashboard')
        connection_response = api.connect_shiny_dashboard(
                                    upload_response.json()['id'],
                                    shiny_dashboard['id'])

    It also provides basic methods to make HTTP verb requests
    directly to the lana endpoints. For example

        response_list = api.get('/api/v2/dashboards')

    Will return a response with a list of dashboard metadata.

    Args:
        scheme:
            A string denoting the scheme of the connection to Lana, usually
            http or https.
        host:
            A string denoting the host of the Lana API.
        token:
            A string representing the user token used for user authentication.
        port:
            (optional) An integer or string denoting the port for the lana
            api. If not set, default ports for the scheme are be used.
        application_root:
            (optional) A string denoting the application root. Only required
            if your lana api is placed outside the URL root, e.g. "/lana-api"
            instead of "/". Has to start with a slash.
        **kwargs:
            Keyword arguments to pass to requests for the initial
            request retrieving user information.
    """

    return ProcessMiningAPI(
        scheme, host, instance, token, port, application_root, **kwargs
    )
