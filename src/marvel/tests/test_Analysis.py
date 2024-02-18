import pytest
from marvel.Analysis import Analysis

def test_analysis_init():
    # Unit Test for the __init__ method
    analysis = Analysis('configs/secrets.yml')  
    print(analysis.config)
    assert analysis.config['public_key'] == '611fe14dca29441682d09a1c3e7ea305'  # replace with your actual test

def test_load_data():
    # Unit Test for the load_data method
    analysis = Analysis('configs/secrets.yml')  
    data = analysis.load_data()
    assert data is not None  

def test_compute_analysis():
    # Unit Test for the compute_analysis method
    analysis = Analysis('configs/secrets.yml')  
    processed_data = analysis.compute_analysis()
    print(processed_data)
    assert processed_data is not None  


