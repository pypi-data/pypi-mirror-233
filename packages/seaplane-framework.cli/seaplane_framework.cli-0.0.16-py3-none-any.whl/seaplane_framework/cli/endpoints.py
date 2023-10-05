import io

import click

import seaplane_framework.api
from seaplane_framework.api.apis.tags import endpoint_api
from seaplane_framework.cli import util


ENDPOINT_STREAM = "_SEAPLANE_ENDPOINT"
ENDPOINT_SUBJECT_IN = ENDPOINT_STREAM + ".in.%s.%s"
ENDPOINT_SUBJECT_OUT = ENDPOINT_STREAM + ".out.%s.%s"


@click.group(name="endpoints")
def endpoints():
    """Seaplane Endpoints"""


@endpoints.command(name="request")
@click.argument("endpoint")
@click.option(
    "--data", "-d", help="Request body, @ to load a file, @- for stdin", required=True
)
def request(endpoint, data):
    """send data to the request endpoint"""
    configuration = util.api_config()
    if not configuration:
        return
    body = util.read_or_return_string(data)
    with seaplane_framework.api.ApiClient(configuration) as api_client:
        api_instance = endpoint_api.EndpointApi(api_client)
        path_params = {"endpoint": endpoint}
        try:
            resp = api_instance.submit_to_endpoint(
                path_params=path_params,  # type: ignore
                body=bytes(body, encoding="utf-8"),  # type: ignore
            )
            print(resp.body)
        except seaplane_framework.api.ApiException as e:
            click.echo(
                click.style(
                    "Exception when calling EndpointApi->submit_to_endpoint: %s\n"
                    % e.reason,
                    fg="red",
                )
            )
            click.echo(e.body)


@endpoints.command(name="response")
@click.argument("endpoint")
@click.argument("message_id")
def response(endpoint, message_id):
    """get data from the response endpoint"""
    configuration = util.api_config()
    if not configuration:
        return
    with seaplane_framework.api.ApiClient(configuration) as api_client:
        api_instance = endpoint_api.EndpointApi(api_client)
        path_params = {
            "endpoint": endpoint,
            "message_id": message_id,
        }
        try:
            resp = api_instance.get_from_endpoint(
                path_params=path_params,  # type: ignore
                stream=True,
                accept_content_types=("application/octet-stream",),
                skip_deserialization=True,
            )
            print(resp.response.read())
        except seaplane_framework.api.ApiException as e:
            click.echo(
                click.style(
                    "Exception when calling EndpointApi->get_from_endpoint: %s\n"
                    % e.reason,
                    fg="red",
                )
            )
            click.echo(e.body)
