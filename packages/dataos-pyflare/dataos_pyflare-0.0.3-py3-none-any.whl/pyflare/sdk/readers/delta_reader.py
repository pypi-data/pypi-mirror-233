import ast
import base64

from pyflare.sdk.config import constants
from pyflare.sdk.config.read_config import ReadConfig
from pyflare.sdk.readers.file_reader import FileInputReader
from pyflare.sdk.utils import logger

log = logger.get(__name__)


class DeltaInputReader(FileInputReader):
    DELTA_CONF = '''[
            ("spark.sql.catalog.{catalog_name}","org.apache.spark.sql.delta.catalog.DeltaCatalog"),
            ("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        ]'''

    def __init__(self, read_config: ReadConfig):
        super().__init__(read_config)

    def read(self):
        spark_options = self.read_config.spark_options
        io_format = self.read_config.io_format
        dataset_path = self.read_config.dataset_absolute_path()
        if spark_options:
            df = self.spark.read.options(**spark_options).format(io_format).load(dataset_path)
        else:
            df = self.spark.read.format(io_format).load(dataset_path)
        return df

    def read_stream(self):
        pass

    def get_conf(self):
        log.debug("calling : ", f"_{self.read_config.depot_type()}_{self.read_config.io_format}")
        return getattr(self, f"_{self.read_config.depot_type()}_{self.read_config.io_format}")()

    def _abfss_delta(self):
        dataset_absolute_path = self.read_config.dataset_absolute_path()
        delta_conf = ast.literal_eval(self.DELTA_CONF.format(catalog_name=self.read_config.depot_name()))
        dataset_auth_token = self._get_secret_token()
        account = self.read_config.depot_details.get("connection", {}).get("account", "")
        endpoint_suffix = dataset_absolute_path.split(account)[1].split("/")[0].strip(". ")
        dataset_auth_key = "{}.{}.{}".format(constants.AZURE_ACCOUNT_KEY_PREFIX, account, endpoint_suffix)
        delta_conf.append((dataset_auth_key, dataset_auth_token))
        return delta_conf

    def _get_secret_token(self):
        encoded_secret = self.read_config.depot_details.get("secrets", {}).get("data", {})[0].get("base64Value", "")
        decoded_secrets_list = base64.b64decode(encoded_secret).decode('UTF8').split("\n")
        secret_token = ""
        for decoded_secret in decoded_secrets_list:
            if constants.STORAGE_ACCOUNT_KEY in decoded_secret:
                secret_token = decoded_secret.split(f"{constants.STORAGE_ACCOUNT_KEY}=")[1]
        return secret_token

    def _get_dataset_path(self):
        return "{}.{}.{}".format(self.read_config.depot_name(), self.read_config.collection(),
                                 self.read_config.dataset_name())
