import pandas as pd
import pyspark
from IPython.display import display, HTML

from spark_dataframe_tools.functions.generator import show_pd_df
from spark_dataframe_tools.functions.generator import show_size_df
from spark_dataframe_tools.functions.generator import show_spark_df
from spark_dataframe_tools.utils import BASE_DIR
from spark_dataframe_tools.utils.utils_color import get_color
from spark_dataframe_tools.utils.utils_color import get_color_b
from spark_dataframe_tools.utils.utils_color import get_color_g
from spark_dataframe_tools.utils.utils_color import get_color_r
from spark_dataframe_tools.utils.utils_faker import faker_generated_data
from spark_dataframe_tools.utils.utils_reformat_type import extract_only_parenthesis
from spark_dataframe_tools.utils.utils_reformat_type import extract_only_column_text
from spark_dataframe_tools.utils.utils_reformat_type import spark_reformat_dtype_data

from spark_dataframe_tools.utils.utils_enviroment import requests_environ_artifactory

from spark_dataframe_tools.utils.utils_session_retry import requests_retry_session
from spark_dataframe_tools.utils.utils_session_retry import request_path_schema_artifactory

pyspark.sql.dataframe.DataFrame.show2 = show_spark_df
pyspark.sql.dataframe.DataFrame.size = show_size_df
pd.DataFrame.show2 = show_pd_df

style_df = """
<style>
.output_subarea.output_text.output_stream.output_stdout > pre {
   width:max-content;
}
.p-Widget.jp-RenderedText.jp-OutputArea-output > pre {
   width:max-content;
}"""
display(HTML(style_df))

utils_color = ["BASE_DIR", "get_color", "get_color_b", "get_color_g", "get_color_r"]
utils_faker = ["faker_generated_data"]
utils_reformat_dtype = ["extract_only_parenthesis", "extract_only_column_text", "spark_reformat_dtype_data"]
utils_env = ["requests_environ_artifactory"]
utils_session = ["requests_retry_session", "request_path_schema_artifactory"]
dataframe_all = ["show_pd_df", "show_spark_df", "apply_dataframe"]

__all__ = utils_color + utils_faker + utils_reformat_dtype + \
          utils_env + utils_session + dataframe_all
