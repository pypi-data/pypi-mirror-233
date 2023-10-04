from pyflare.sdk.config.write_config import WriteConfig
from pyflare.sdk.writers.writer import Writer
from pyflare.sdk.utils import logger

log = logger.get(__name__)


class FileOutputWriter(Writer):
    
    def __init__(self, write_config: WriteConfig):
        super().__init__(write_config)
    
    def write(self, df):
        pass
    
    def write_stream(self):
        pass
    
    def get_conf(self):
        pass
    
    def write_csv(self):
        pass
    
    def write_json(self):
        pass
    
    def write_parquet(self):
        pass
