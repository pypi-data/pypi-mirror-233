def read_fields_datum(spark=None, path=None, table_name=None, storage_zone=None):
    from pyspark.sql import functions as func
    import sys
    if str(storage_zone).upper() in ('RAW', 'RAWDATA'):
        storage_zone = 'RAWDATA'
    elif str(storage_zone).upper() in ('MASTER', 'MASTERDATA'):
        storage_zone = 'MASTERDATA'
    else:
        raise Exception(f'required var storage_zone in : "raw,rawdata,master, masterdata"')
    is_windows = sys.platform.startswith('win')
    if is_windows:
        path = path.replace("\\", "/")

    df = spark.read.csv(path, sep=';', header=True)
    df = df.select(*[func.col(c).alias(c.upper().replace(' ', '_').strip()) for c in df.columns]) \
        .dropDuplicates(["FIELD_ID"])
    df = df.select("FIELD_ID", "PHYSICAL_NAME_OBJECT", "PHYSICAL_NAME_FIELD", "SOURCE_FIELD",
                   "DATA_TYPE", "KEY", "FORMAT", "LOGICAL_FORMAT", "SECURITY_CLASS", "SECURITY_LABEL",
                   "MANDATORY", "FIELD_POSITION_IN_THE_OBJECT", "STORAGE_TYPE", "STORAGE_ZONE",
                   "NAME_DATA_SYSTEM", "PARTITION_COLUMN_IND")
    df = df.withColumn('FIELD_POSITION_IN_THE_OBJECT',
                       func.format_string("%03d", func.col('FIELD_POSITION_IN_THE_OBJECT').cast('int')))
    df = df[df["STORAGE_ZONE"].isin([storage_zone])]
    df = df[df["PHYSICAL_NAME_OBJECT"] == f"{table_name}"]

    df = df.orderBy(func.col("FIELD_POSITION_IN_THE_OBJECT").asc())
    return df


def generated_dataframe_schema(path=None):
    import json
    from pyspark.sql import types
    from spark_dataframe_tools import spark_reformat_dtype_data

    with open(path) as f:
        artifactory_json = json.load(f)

    struct_list = list()
    struct_string_list = list()
    for row in artifactory_json["fields"]:
        naming = str(row['name']).lower().strip()
        logical_format = row['logicalFormat']
        _reformat = spark_reformat_dtype_data(naming, logical_format, convert_string=False)
        _type = _reformat.get("_type")
        _type_string = _reformat.get("_type_string")
        struct_list.append(_type)
        struct_string_list.append(_type_string)
    spark_schema = types.StructType(struct_list)
    spark_schema_string = types.StructType(struct_string_list)
    return spark_schema, spark_schema_string


def generated_dummy_table_artifactory(spark=None,
                                      table_name=None,
                                      env="work",
                                      phase="master",
                                      code_country="pe",
                                      is_uuaa_tag=False,
                                      is_sandbox=False,
                                      token_artifactory=None,
                                      partition_colum=None,
                                      sample_parquet=10,
                                      columns_integer_default={},
                                      columns_date_default={},
                                      columns_string_default={},
                                      columns_decimal_default={},
                                      ):
    global struct_list, struct_list_string
    import os
    import sys
    import pandas as pd
    import numpy as np
    import shutil
    import json
    from pyspark.sql import functions as func
    from pyspark.sql import types
    from spark_dataframe_tools import get_color_b
    from spark_dataframe_tools import extract_only_parenthesis
    from spark_dataframe_tools import faker_generated_data
    from spark_dataframe_tools import spark_reformat_dtype_data
    from spark_dataframe_tools import requests_environ_artifactory
    from spark_dataframe_tools import request_path_schema_artifactory

    is_windows = sys.platform.startswith('win')
    spark.conf.set("spark.sql.debug.maxToStringFields", 5000)
    requests_environ_artifactory()

    artifactory_json = request_path_schema_artifactory(
        table_name=table_name, env=env, phase=phase, code_country=code_country,
        is_uuaa_tag=is_uuaa_tag, is_sandbox=is_sandbox, token_artifactory=token_artifactory)

    table_name = artifactory_json.get("name")
    _partition_colum = artifactory_json.get("partitions")
    if _partition_colum in ("", None, np.nan, np.NaN, " "):
        _partition_colum = partition_colum

    output = list()
    for _ in range(sample_parquet):
        columns_dict = dict()
        struct_list = list()
        struct_list_string = list()
        for row in artifactory_json["fields"]:
            naming = str(row['name']).lower().strip()
            logical_format = row['logicalFormat']
            parentheses = extract_only_parenthesis(format=logical_format)
            _reformat = spark_reformat_dtype_data(naming, logical_format, convert_string=False)
            _type = _reformat.get("_type")
            _type_string = _reformat.get("_type_string")
            _format_text = _reformat.get("_format_text")
            _fake = faker_generated_data(naming=naming,
                                         format=_format_text,
                                         parentheses=parentheses,
                                         columns_integer_default=columns_integer_default,
                                         columns_date_default=columns_date_default,
                                         columns_string_default=columns_string_default,
                                         columns_decimal_default=columns_decimal_default)
            columns_dict[naming] = _fake
            struct_list.append(_type)
            struct_list_string.append(_type_string)
        output.append(columns_dict)
    spark_schema = types.StructType(struct_list)
    spark_schema_string = types.StructType(struct_list_string)
    df2 = pd.DataFrame(output)
    df3 = spark.createDataFrame(df2, schema=spark_schema_string)
    for i in spark_schema.jsonValue()["fields"]:
        column_name = str(i["name"])
        column_type = str(i["type"])
        if column_type.startswith("decimal"):
            df3 = df3.withColumn(f"{column_name}", func.col(f"{column_name}").cast(f"{column_type}"))
        elif column_type.startswith("integer"):
            df3 = df3.withColumn(f"{column_name}", func.col(f"{column_name}").cast(f"{column_type}"))
        elif column_type.startswith("date"):
            df3 = df3.withColumn(f"{column_name}", func.col(f"{column_name}").cast("date"))
        elif column_type.startswith("timestamp"):
            df3 = df3.withColumn(f"{column_name}", func.col(f"{column_name}").cast("timestamp"))
        elif column_type.startswith("string"):
            df3 = df3.withColumn(f"{column_name}", func.col(f"{column_name}").cast("string"))
    directory_dummy = "DIRECTORY_DUMMY"
    if os.path.exists(os.path.join(directory_dummy)):
        shutil.rmtree(directory_dummy)
    path_directory = os.path.join(directory_dummy, table_name)
    if is_windows:
        path_directory = path_directory.replace("\\", "/")
    if not os.path.exists(path_directory):
        os.makedirs(path_directory)
    df3.coalesce(1).write.partitionBy(_partition_colum).mode("overwrite").parquet(path_directory)

    shutil.make_archive("DIRECTORY_DUMMY", "zip", "DIRECTORY_DUMMY")
    shutil.move("DIRECTORY_DUMMY.zip", f"{path_directory}.zip")

    print(get_color_b(f'GENERATED DUMMY TABLE: {table_name}'))


def generated_dummy_table_datum(spark=None,
                                path=None,
                                table_name=None,
                                storage_zone=None,
                                sample_parquet=10,
                                partition_colum=["cutoff_date"],
                                columns_integer_default={},
                                columns_date_default={},
                                columns_string_default={},
                                columns_decimal_default={},
                                ):
    global struct_list, struct_list_string
    import os
    import sys
    import pandas as pd
    import shutil
    from pyspark.sql import functions as func
    from pyspark.sql import types
    from spark_dataframe_tools import get_color_b
    from spark_dataframe_tools import extract_only_parenthesis
    from spark_dataframe_tools import faker_generated_data
    from spark_dataframe_tools import spark_reformat_dtype_data

    is_windows = sys.platform.startswith('win')
    spark.conf.set("spark.sql.debug.maxToStringFields", 5000)

    df = read_fields_datum(spark=spark, path=path, table_name=table_name, storage_zone=storage_zone)
    df = df.select("PHYSICAL_NAME_OBJECT", "PHYSICAL_NAME_FIELD", "LOGICAL_FORMAT")

    output = list()
    for _ in range(sample_parquet):
        columns_dict = dict()
        struct_list = list()
        struct_list_string = list()
        for row in df.collect():
            naming = str(row['PHYSICAL_NAME_FIELD']).lower().strip()
            logical_format = row['LOGICAL_FORMAT']
            parentheses = extract_only_parenthesis(format=logical_format)
            _reformat = spark_reformat_dtype_data(naming, logical_format, convert_string=False)
            _type = _reformat.get("_type")
            _type_string = _reformat.get("_type_string")
            _format_text = _reformat.get("_format_text")
            _fake = faker_generated_data(naming=naming,
                                         format=_format_text,
                                         parentheses=parentheses,
                                         columns_integer_default=columns_integer_default,
                                         columns_date_default=columns_date_default,
                                         columns_string_default=columns_string_default,
                                         columns_decimal_default=columns_decimal_default)
            columns_dict[naming] = _fake
            struct_list.append(_type)
            struct_list_string.append(_type_string)
        output.append(columns_dict)
    spark_schema = types.StructType(struct_list)
    spark_schema_string = types.StructType(struct_list_string)
    df2 = pd.DataFrame(output)
    df3 = spark.createDataFrame(df2, schema=spark_schema_string)
    for i in spark_schema.jsonValue()["fields"]:
        column_name = str(i["name"])
        column_type = str(i["type"])
        if column_type.startswith("decimal"):
            df3 = df3.withColumn(f"{column_name}", func.col(f"{column_name}").cast(f"{column_type}"))
        if column_type.startswith("integer"):
            df3 = df3.withColumn(f"{column_name}", func.col(f"{column_name}").cast(f"{column_type}"))
        elif column_type.startswith("date"):
            df3 = df3.withColumn(f"{column_name}", func.col(f"{column_name}").cast("date"))
        elif column_type.startswith("timestamp"):
            df3 = df3.withColumn(f"{column_name}", func.col(f"{column_name}").cast("timestamp"))

    directory_dummy = "DIRECTORY_DUMMY"
    if os.path.exists(os.path.join(directory_dummy)):
        shutil.rmtree(directory_dummy)
    path_directory = os.path.join(directory_dummy, table_name)
    if is_windows:
        path_directory = path_directory.replace("\\", "/")
    if not os.path.exists(path_directory):
        os.makedirs(path_directory)
    df3.coalesce(1).write.partitionBy(partition_colum).mode("overwrite").parquet(path_directory)

    shutil.make_archive("DIRECTORY_DUMMY", "zip", "DIRECTORY_DUMMY")
    shutil.move("DIRECTORY_DUMMY.zip", f"{path_directory}.zip")

    print(get_color_b(f'GENERATED DUMMY TABLE: {table_name}'))
