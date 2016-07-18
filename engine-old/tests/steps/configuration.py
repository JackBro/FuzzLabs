from behave import *
import os
import sys
import inspect

ROOT_DIR = os.path.dirname(
                os.path.abspath(
                    inspect.getfile(inspect.currentframe()
                )))

sys.path.append(ROOT_DIR + "/../../classes")
from ConfigurationHandler import ConfigurationHandler

@given('we have a configuration file')
def step_impl(context):
    assert os.path.isfile(ROOT_DIR + "/../../etc/engine.config")
    context.config_file = ROOT_DIR + "/../../etc/engine.config"

@when('we read the configuration')
def step_impl(context):
    context.config_data = ConfigurationHandler(context.config_file).get()

@then('we get a dictionary')
def step_impl(context):
    assert type(context.config_data) is dict

