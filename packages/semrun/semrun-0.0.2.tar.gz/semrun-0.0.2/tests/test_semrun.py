import pytest
from semrun.semrun import SemRun

def test_function():
    return "This is a test function"

def test_semrun_initialization():
    function_topic_dict = {test_function: 'test_topic'}
    semrun = SemRun(function_topic_dict)
    assert test_function in semrun.functions, "Initialization failed: functions not set correctly"
    assert 'test_topic' in semrun.topics, "Initialization failed: topics not set correctly"