import sys
import pandas as pd

sys.path.append('cogs')
from html_handler import *

def test_get_pages_list():
    result = get_pages_list("https://hotwheels.fandom.com/wiki/Lamborghini")
    assert isinstance(result,list)
    assert "/wiki/Lamborghini_Countach" in result[0]

# Define a fixture to create sample DataFrames for testing
# @pytest.fixture
# def sample_dataframes():
#     ext_table_keys = pd.DataFrame({'key': ['Lamborghini Countach']})
#     call_table_links = pd.DataFrame({'link': ['https://hotwheels.fandom.com/wiki/Lamborghini_Countach']})
#     return ext_table_keys, call_table_links

# def test_table_list(sample_dataframes):
#     ext_table_keys, call_table_links = sample_dataframes

#     # Call the function with sample DataFrames
#     result = table_list(ext_table_keys, call_table_links)

#     assert isinstance(result, dict)
#     assert len(result) == len(ext_table_keys)

#     # For example:
#     assert 'Lamborghini' in result