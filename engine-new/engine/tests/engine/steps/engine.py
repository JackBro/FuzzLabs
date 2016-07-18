from behave import *
import json
import httplib

ENGINE_PROT = "http"
ENGINE_HOST = "localhost"
ENGINE_PORT = 26000

@given('the engine is accessible')
def step_impl(context):
    conn = httplib.HTTPConnection(ENGINE_HOST, ENGINE_PORT, True, 3)
    res = None
    try:
        conn.request("HEAD","/")
        res = conn.getresponse()
    except Exception, ex:
        res = None

    assert (res != None)

@when('we attempt to set up the API key')
def step_impl(context):
    conn = httplib.HTTPConnection(ENGINE_HOST, ENGINE_PORT, True, 3)
    conn.request("GET","/setup/apikey")
    res = conn.getresponse()
    assert (res != None)
    context.status = res.status
    context.data   = res.read()

@when('we attempt to initialize ACL')
def step_impl(context):
    conn = httplib.HTTPConnection(ENGINE_HOST, ENGINE_PORT, True, 3)
    conn.request("GET","/setup/acl")
    res = conn.getresponse()
    assert (res != None)
    context.status = res.status
    context.data   = res.read()

@when('we attempt a ping request')
def step_impl(context):
    conn = httplib.HTTPConnection(ENGINE_HOST, ENGINE_PORT, True, 3)
    apikey = None
    with open("./config/config.json", "r") as f:
        apikey = json.loads(f.read()).get('security').get('apikey')
    conn.request("GET","/ping?apikey=" + apikey)
    res = conn.getresponse()
    assert (res != None)
    context.status = res.status
    context.data   = json.loads(res.read())

@then('the API key is returned')
def step_impl(context):
    assert (context.status == 200)
    data = json.loads(context.data)
    assert (data.get('apikey') != None)
    assert (len(data.get('apikey')) != 0)

@then('we get forbidden message')
def step_impl(context):
    assert (context.status == 403)
    data = json.loads(context.data)
    assert (data.get('apikey') == None)

@then('we get no error')
def step_impl(context):
    assert (context.status == 200)

@then('we get pong response')
def step_impl(context):
    assert (context.status == 200)
    assert (context.data.get('message') == "pong")

