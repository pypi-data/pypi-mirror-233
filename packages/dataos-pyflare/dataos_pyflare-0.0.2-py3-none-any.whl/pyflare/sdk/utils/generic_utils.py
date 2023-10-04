import base64
import json
import os
import re

import pkg_resources

from pyflare.sdk.config import constants
from pyflare.sdk import logger
from functools import wraps

# import builtins
#
#
# def my_print(*args, **kwargs):
#     # Do something with the arguments
#     # Replace sensitive strings with a placeholder value
#     redacted_text = re.sub('(?i)secret|password|key|abfss|dfs|apikey', '*****', " ".join(str(arg) for arg in args))
#     # Print the redacted text
#     builtins.print(redacted_text)
from pyflare.sdk.config.constants import DEPOT_SECRETS_KV_REGEX, DATAOS_DEFAULT_SECRET_DIRECTORY


def decorate_logger(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        log = logger.get(fn.__name__)
        log.debug('About to run %s' % fn.__name__)

        out = fn(*args, **kwargs)

        log.debug('Done running %s' % fn.__name__)
        return out

    return wrapper


def append_properties(dict1 , dict2):
    for key, value in dict2.items():
        dict1[key] = value
    return dict1


def safe_assignment(val1, val2):
    if val2:
        return val2
    return val1


def get_jars_path():
    flare_sdk_jar_path = pkg_resources.resource_filename('pyflare.jars', 'flare_2.12-3.3.1-0.0.14.1-javadoc.jar')
    heimdall_jar_path = pkg_resources.resource_filename('pyflare.jars', 'heimdall-0.1.9.jar')
    commons_jar_path = pkg_resources.resource_filename('pyflare.jars', 'commons-0.1.9.jar')
    spark_jar_path = pkg_resources.resource_filename('pyflare.jars', 'spark-authz-0.1.9.jar')
    josn4s_jar_path = pkg_resources.resource_filename('pyflare.jars', 'json4s-jackson_2.12-3.6.12.jar')
    josn4s_jar_path = pkg_resources.resource_filename('pyflare.jars', 'json4s-jackson_2.12-4.0.6.jar')
    flare_jar_path = pkg_resources.resource_filename('pyflare.jars', 'flare_4.jar')
    return f"{commons_jar_path},{heimdall_jar_path}, {flare_sdk_jar_path}, {josn4s_jar_path}, {spark_jar_path}"


def get_abfss_spark_conf(rw_config):
    dataset_absolute_path = rw_config.dataset_absolute_path()
    dataset_auth_token = get_secret_token(rw_config.depot_details)
    account = rw_config.depot_details.get("connection", {}).get("account", "")
    endpoint_suffix = dataset_absolute_path.split(account)[1].split("/")[0].strip(". ")
    dataset_auth_key = "{}.{}.{}".format(constants.AZURE_ACCOUNT_KEY_PREFIX, account, endpoint_suffix)
    return dataset_auth_key, dataset_auth_token


# def get_gateway_client(base_url: str, api_key: str) -> GatewayClient:
#     builder = GatewayClientBuilder()
#     builder.base_url = normalize_base_url(base_url)
#     builder.apikey = api_key
#     return builder.build()


def get_secret_token(depot_details):
    return depot_details.get("secrets", {}).get(constants.AZURE_ACCOUNT_KEY, "")


def get_dataset_path(depot_config):
    return "{}.{}.{}".format(depot_config.depot_name(), depot_config.collection(),
                             depot_config.dataset_name())


def decode_base64_string(encoded_string, type):
    decoded_string = base64.b64decode(encoded_string).decode('utf-8')
    if type.casefold() == "json":
        key_value_pairs = json.loads(decoded_string)
    else:
        key_value_pairs = re.findall(DEPOT_SECRETS_KV_REGEX, decoded_string)
    return dict(key_value_pairs)


def get_secret_file_path():
    return DATAOS_DEFAULT_SECRET_DIRECTORY if os.getenv("DATAOS_SECRET_DIR") is None else \
        os.getenv("DATAOS_SECRET_DIR").rstrip('/')


def write_secret_to_file(file_path, secrets_dict):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        log.info("File exists and is not empty")
    else:
        log.info("File does not exists or is empty")
        try:
            with open(file_path, "w") as file:
                json.dump(secrets_dict, file)
            log.info(f"Secret written successfully to: {file_path}")
        except Exception as e:
            log.info(f"Error writing secret to the file: {str(e)}")
