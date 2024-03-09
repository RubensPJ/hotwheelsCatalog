import sys
import pytest

sys.path.append('cogs')
from async_processing import *

# Define a fixture to create sample data for testing
@pytest.fixture
def sample_data():

    call_table_links_list = [['https://hotwheels.fandom.com/wiki/Lamborghini_Countach'], ['https://hotwheels.fandom.com/wiki/Lamborghini_Countach']]
    car_names_list = [['Countach'], ['Countach']]
    return call_table_links_list, car_names_list

# Write a test function for process_links_async
def test_process_links_async(sample_data):

    call_table_links_list, car_names_list = sample_data

    # Call function with sample data
    results = process_links_async(call_table_links_list, car_names_list)

    # Add your assertions based on the expected result
    assert isinstance(results, list)
    assert len(results) == len(call_table_links_list)

    assert all(isinstance(result, tuple) and len(result) == 2 for result in results)