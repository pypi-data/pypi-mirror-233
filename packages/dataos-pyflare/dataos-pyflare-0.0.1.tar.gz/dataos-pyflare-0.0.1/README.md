# Pyflare

### What it does:
Pyflare is written ground up to provide native support in Python versions 3.x.
This sdk makes it easy to integrate your Python application, library, or script with the data ecosystem.

SDK abstracts out the challenges/complexity around data flow. User can just focus on data transformations and 
business logic.


### Steps to install

* pip install pyflare-0.0.12-py3-none-any.whl

That's it. Enjoy!!

### How to use:

Define mandatory fields 

#### sparkConf [optional] : 
    Define spark conf as per your need.
#### token: 
    Provide Dataos API token.
#### DATAOS_FQDN: 
    Provide dataos fully qualified domain name.
#### with_depot(): 
    Provide dataos address to be usd in current session with correct acl.
#### load(): 
    method to load data from source.
#### save(): 
    method to write data to sink.


### Samples:

```python
from pyflare.sdk import load, save, session_builder

# Define your spark conf params here
sparkConf = [("spark.app.name", "Dataos Sdk Spark App"), ("spark.master", "local[*]"), ("spark.executor.memory", "4g"),
             ("spark.jars.packages", "com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.25.1,"
                                     "com.google.cloud.bigdataoss:gcs-connector:hadoop3-2.2.17,"
                                    "net.snowflake:spark-snowflake_2.12:2.11.0-spark_3.3")
             ]

# Provide dataos token here
token = "bWF5YW5rLjkxYzZiNDQ3LWM3ZWYtNGZhYS04YmEwLWMzNjk3MzQ1MTQyNw=="

# provide dataos fully qualified domain name
DATAOS_FQDN = "sunny-prawn.dataos.app"

# initialize pyflare session
spark = session_builder.SparkSessionBuilder() \
    .with_spark_conf(sparkConf) \
    .with_user_apikey(token) \
    .with_dataos_fqdn(DATAOS_FQDN) \
    .with_depot("dataos://icebase:retail/city", "r") \
    .with_depot("dataos://sanitysnowflake:public/customer", "w") \
    .build_session()

# load() method will read dataset city from the source and return a governed dataframe
df_city = load(name="dataos://icebase:retail/city", format="iceberg")

# perform, required transformation as per business logic
df_city = df_city.drop("__metadata")

# save() will write transformed dataset to the sink
save(name="dataos://sanitysnowflake:public/customer", mode="overwrite", dataframe=df_city, format="snowflake")
```