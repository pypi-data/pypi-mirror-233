# Arikedb Python Library


[![pipeline status](https://gitlab.com/arikedb1/languages-library-support/arikedb-python-library/badges/main/pipeline.svg)](https://gitlab.com/arikedb1/languages-library-support/arikedb-python-library/-/commits/main)
[![coverage report](https://gitlab.com/arikedb1/languages-library-support/arikedb-python-library/badges/main/coverage.svg)](https://gitlab.com/arikedb1/languages-library-support/arikedb-python-library/-/commits/main)
[![Latest Release](https://gitlab.com/arikedb1/languages-library-support/arikedb-python-library/-/badges/release.svg)](https://gitlab.com/arikedb1/languages-library-support/arikedb-python-library/-/releases)

The python client library for arikedb. This is a documentation only for the arikedb python library, to learn more about
basis of Arikedb Database visit the [official site](http://arikedb.com)

## Guide Lines

 - [Creating the instance](#creating-the-instance)
 - [Sending any command](#sending-any-command)
 - [Listing Databases](#listing-databases)
 - [Listing Roles](#listing-roles)
 - [Listing Users](#listing-users)
 - [Creating a database](#creating-a-database)
 - [Selecting a database](#selecting-a-database)
 - [Listing variables](#listing-variables)
 - [Writing data to variables](#writing-data-to-variables)
 - [Setting event for historical data](#setting-event-for-historical-data)
 - [Reading data](#reading-data)
 - [Subscribing to variables](#subscribing-to-variables)
 - [Removing variables](#removing-variables)
 - [Removing a database](#removing-a-database)
 - [Creating a role](#creating-a-role)
 - [Removing a role](#removing-a-role)
 - [Creating a user](#creating-a-user)
 - [Removing a user](#removing-a-user)
 - [Authenticating](#authenticating)
 - [Configuring the server](#configuring-the-server)

### Creating the instance
7
Using Arikedb Python Library is very easy. Let's assume we have an Arikedb server running in localhost on its default port 6923.
Go to [Arikedb](http://arikedb.com) for references

The first step is create an instance of the ArikedbClient class

```python
from arikedb import ArikedbClient

client = ArikedbClient()

```

If we are connecting to a server running on a different host and/or port just provide them in the class constructor, and the same
if you need to connect using a ssl certificate

```python
from arikedb import ArikedbClient

client = ArikedbClient("192.168.1.2", 8000, "/path/to/cert/file")
```

### Sending any command

The most generic method of ArikedbClient class is send_command. It just sends a command
like you could do it from the Arikedb CLI, and returns a dictionary with the server response.

```python
from arikedb import ArikedbClient

client = ArikedbClient()
client.connect()

resp = client.send_command("SHOW databases")
print(resp)

client.disconnect()
```
output:
```text
{'uid': '23478f3640bd410a89002e330c9e56da', 'status': 0, 'databases': ['db3', 'db2']}
```

The send command allows you to directly send arikedb commands, but most of the time will be better to use specific methods
for every command. Those methods are defined below

### Listing Databases

The list databases method give us all current databases in the server

```python
from arikedb import ArikedbClient

client = ArikedbClient()
client.connect()

databases = client.list_databases()
print(databases)

client.disconnect()
```
output:
```text
['db1', 'db2']
```

### Listing Roles

The list roles method give us all current roles in the server

```python
from arikedb import ArikedbClient

client = ArikedbClient()
client.connect()

roles = client.list_roles()
print(roles)

client.disconnect()
```
output:
```text
[{'name': 'admin', 'allowed_cmd': ['GET', 'PGET', 'SUBSCRIBE', 'PSUBSCRIBE', 'SHOW', 'VARIABLES', 'SET', 'RM', 'SET_EVENT', 'ADD_DATABASE', 'DEL_DATABASE', 'ADD_ROLE', 'DEL_ROLE', 'ADD_USER', 'DEL_USER', 'LOAD_LICENSE', 'CONFIG']}, {'name': 'writer', 'allowed_cmd': ['GET', 'PGET', 'SUBSCRIBE', 'PSUBSCRIBE', 'SHOW', 'VARIABLES', 'SET', 'RM', 'SET_EVENT', 'ADD_DATABASE', 'DEL_DATABASE']}, {'name': 'reader', 'allowed_cmd': ['GET', 'PGET', 'SUBSCRIBE', 'PSUBSCRIBE', 'SHOW', 'VARIABLES']}]
```

### Listing Users

The list roles method give us all current roles in the server

```python
from arikedb import ArikedbClient

client = ArikedbClient()
client.connect()

users = client.list_users()
print(users)

client.disconnect()
```
output:
```text
[{'username': 'john_doe', 'role': 'admin'}, {'username': 'jane_doe', 'role': 'writer'}]
```

### Creating a database

The add_database method create a database in the server

```python
from arikedb import ArikedbClient

client = ArikedbClient()
client.connect()

client.add_database("new_database")
print(client.list_databases())
...
client.disconnect()
```
output:
```text
['db1', 'db2', 'new_database']
```

### Selecting a database

Before write or read any data, we should select a database from the client instance

```python
from arikedb import ArikedbClient

client = ArikedbClient()
client.connect()

client.use("new_database")
...
client.disconnect()
```

### Listing variables

Once we selected a database, we can list the existing variables based on patterns. Next example is used
to get the full list of database variables

```python
from arikedb import ArikedbClient

client = ArikedbClient()
client.connect()

client.use("new_database")
variables = client.list_variables(["*"])
...
client.disconnect()
```
output:
```text
[{'var_name': 'var1', 'var_type': 'FLOAT'}, {'var_name': 'var2', 'var_type': 'UNSET'}]
```

### Writing data to variables

To write new values to current database variables, or to create new ones, use the set method

```python
from arikedb import ArikedbClient

client = ArikedbClient()
client.connect()

client.use("new_database")

var_values = {
    "varX": 23.1,
    "varY": "A string variable",
    "varZ": 4
}
meta = {
    "city": "New York"
}

client.set(var_values, meta)

...
client.disconnect()
```

### Setting event for historical data

To start saving historical data for one or more tags, we should define an event to trigger the data saving

```python
from arikedb import ArikedbClient
from arikedb_tools.events import TagEvent

client = ArikedbClient()
client.connect()

client.use("new_database")

client.set_event(["var*"], TagEvent.ON_CHANGE)
client.set_event(["other*"], TagEvent.ON_CROSS_LOW_THRESHOLD, threshold=2.1)

...
client.disconnect()
```

### Reading data

To read real time and historical data we can use get and pget methods, the first receive the list of tag names while the second
takes a list of pattern to match variable names

```python
from arikedb import ArikedbClient

client = ArikedbClient()
client.connect()

client.use("new_database")

data = client.get(["var1", "var2"], epoch="m")
print(data)

pdata = client.pget(["var*"], epoch="m")
print(pdata)

...
client.disconnect()
```
output:
```text
[['varX', 1696425352176, 23.1, {'city': 'New York'}], ['varY', 1696425352176, 'A string variable', {'city': 'New York'}]]
[['varX', 1696425352176, 23.1, {'city': 'New York'}], ['varZ', 1696425352176, 4, {'city': 'New York'}], ['varY', 1696425352176, 'A string variable', {'city': 'New York'}]]

```

The output is a list of variables. Each variable in the list is a list of four elements
```
[ Variable name, Timestamp, Current value, Metadata ]
```

To get historical data use the method arguments `from` and `to`

```python
import time
from arikedb import ArikedbClient

client = ArikedbClient()
client.connect()

client.use("new_database")

data = client.get(["varX", "varY"], epoch="m", from_=time.time() - 1000, to=time.time())
print(data)
data = client.get(["varX", "varY"], epoch="s", to=time.time())
print(data)
pdata = client.pget(["var*"], from_=time.time() - 1000)
print(pdata)

...
client.disconnect()
```
output:
```text
[[['varX', 1696425869.716597, 23.1, {'city': 'New York'}], ['varX', 1696425869.742981, 24.1, {'city': 'New York'}], ['varX', 1696425869.7632911, 25.1, {'city': 'New York'}], ['varX', 1696425869.7848454, 26.1, {'city': 'New York'}], ['varX', 1696425869.8179193, 27.1, {'city': 'New York'}]], [['varY', 1696425869.716597, 'A string 0', {'city': 'New York'}], ['varY', 1696425869.742981, 'A string 1', {'city': 'New York'}], ['varY', 1696425869.7632911, 'A string 2', {'city': 'New York'}], ['varY', 1696425869.7848454, 'A string 3', {'city': 'New York'}], ['varY', 1696425869.8179193, 'A string 4', {'city': 'New York'}]]]
[[['varX', 1696425869.716597, 23.1, {'city': 'New York'}], ['varX', 1696425869.742981, 24.1, {'city': 'New York'}], ['varX', 1696425869.7632911, 25.1, {'city': 'New York'}], ['varX', 1696425869.7848454, 26.1, {'city': 'New York'}], ['varX', 1696425869.8179193, 27.1, {'city': 'New York'}]], [['varY', 1696425869.716597, 'A string 0', {'city': 'New York'}], ['varY', 1696425869.742981, 'A string 1', {'city': 'New York'}], ['varY', 1696425869.7632911, 'A string 2', {'city': 'New York'}], ['varY', 1696425869.7848454, 'A string 3', {'city': 'New York'}], ['varY', 1696425869.8179193, 'A string 4', {'city': 'New York'}]]]
[[['varX', 1696425869.716597, 23.1, {'city': 'New York'}], ['varX', 1696425869.742981, 24.1, {'city': 'New York'}], ['varX', 1696425869.7632911, 25.1, {'city': 'New York'}], ['varX', 1696425869.7848454, 26.1, {'city': 'New York'}], ['varX', 1696425869.8179193, 27.1, {'city': 'New York'}]], [['varZ', 1696425869.716597, 4, {'city': 'New York'}], ['varZ', 1696425869.742981, 3, {'city': 'New York'}], ['varZ', 1696425869.7632911, 2, {'city': 'New York'}], ['varZ', 1696425869.7848454, 1, {'city': 'New York'}], ['varZ', 1696425869.8179193, 0, {'city': 'New York'}]], [['varY', 1696425869.716597, 'A string 0', {'city': 'New York'}], ['varY', 1696425869.742981, 'A string 1', {'city': 'New York'}], ['varY', 1696425869.7632911, 'A string 2', {'city': 'New York'}], ['varY', 1696425869.7848454, 'A string 3', {'city': 'New York'}], ['varY', 1696425869.8179193, 'A string 4', {'city': 'New York'}]]]

```

Now the output is a list of historical values

### Subscribing to variables

To subscribe to variables to get the latest values based on an event, let's use subscribe and psubscribe methods

```python
import time
from arikedb import ArikedbClient
from arikedb_tools.events import TagEvent

client = ArikedbClient()
client.connect()

client.use("new_database")

def callback(name: str, timestamp: float, value, meta: dict):
    print("=====================")
    print(f"Tag Name: {name}")
    print(f"Timestamp: {timestamp}")
    print(f"Tag Value: {value}")
    print(f"Tag meta: {meta}")
    print("=====================")

client.subscribe(["varY"], callback, event=TagEvent.ON_CHANGE)
client.psubscribe(["var[XZ]"], callback, epoch="ms", event=TagEvent.ON_RISING_EDGE)

for i in range(5):
    var_values = {
        "varX": 23.1 + float(i),
        "varY": f"A string {i}",
        "varZ": 4 - i
    }
    meta = {
        "city": "New York"
    }
    client.set(var_values, meta)
    time.sleep(1)

...
client.disconnect()
```
output
```text
=====================
Tag Name: varY
Timestamp: 1696426808696048128
Tag Value: A string 1
Tag meta: {'city': 'New York'}
=====================
=====================
Tag Name: varX
Timestamp: 1696426809723
Tag Value: 25.1
Tag meta: {'city': 'New York'}
=====================
=====================
Tag Name: varY
Timestamp: 1696426810744874240
Tag Value: A string 3
Tag meta: {'city': 'New York'}
=====================
=====================
Tag Name: varX
Timestamp: 1696426811773
Tag Value: 27.1
Tag meta: {'city': 'New York'}
=====================
```

### Removing variables

To permanently delete variables (including all its historical data) us rm method

```python
from arikedb import ArikedbClient

client = ArikedbClient()
client.connect()

client.use("new_database")
variables = client.rm(["var*"])
...
client.disconnect()
```

### Removing a database

To permanently delete a database with all its content

```python
from arikedb import ArikedbClient

client = ArikedbClient()
client.connect()

client.del_database("new_database")
...
client.disconnect()
```

### Creating a role

To create a role specify the role name and the list of allowed commands

```python
from arikedb import ArikedbClient
from arikedb_tools.command import Command

client = ArikedbClient()
client.connect()

client.add_role("new_role", [Command.GET, Command.PGET])
...
client.disconnect()
```

### Removing a role

To delete a role

```python
from arikedb import ArikedbClient

client = ArikedbClient()
client.connect()

client.del_role("writer")
...
client.disconnect()
```

### Creating a user

To create a user set the role, username and password

```python
from arikedb import ArikedbClient

client = ArikedbClient()
client.connect()

client.add_user("admin", "john_doe", "StrongPassword")
...
client.disconnect()
```

### Removing a user

To delete a user

```python
from arikedb import ArikedbClient

client = ArikedbClient()
client.connect()

client.del_user("john_doe")
...
client.disconnect()
```

### Authenticating

Using auth method to authenticate with user credentials

```python
from arikedb import ArikedbClient

client = ArikedbClient()
client.connect()

client.auth("john_doe", "MyStrongPassword")
...
client.disconnect()
```

### Configuring the server

Using get_config and set_config methods to get and modify server configurations. Take into account that some configuration changes
need a server restart. The reset_config will reset all configurations to its default values. And the show_config prints the configuration
in a pretty table

```python
from arikedb import ArikedbClient

client = ArikedbClient()
client.connect()

client.set_config(use_http_api=True)
    
conf = client.get_config()
print(conf)
...
client.disconnect()
```
output
```text
{'headers': ['Key', 'Value', 'Source', 'Env Var', 'Default', 'Description'], 'tab': [['use_auth', False, 'Default', 'ARIKEDB_USE_AUTH', False, 'Define if authentication is needed or not to manipulate arike databases. Changing this key needs a server restart'], ['use_ssl', False, 'Default', 'ARIKEDB_USE_SSL', False, 'Define if communication with the server will need ssl to connect. If True, also the keys `cert_file` and `key_file` should be configured, Changing this key needs a server restart'], ['use_http_api', True, 'Configured', 'ARIKEDB_USE_HTTP_API', False, 'Define if communication with the server throw http API will be enabled. See `http_host` and `http_port`'], ['host', 'localhost', 'Default', 'ARIKEDB_HOST', 'localhost', 'Bind address where the server will run. Use `localhost` (default) to run only in a local scope, or use `0.0.0.0` or a specific ip for remote access. Changing this key needs a server restart'], ['port', 6923, 'Default', 'ARIKEDB_PORT', '6923', 'Bind port where the server will run. Changing this key needs a server restart'], ['http_host', 'localhost', 'Default', 'ARIKEDB_HTTP_HOST', 'localhost', 'Bind address where the server API will run. Changing this key needs a server restart. See `use_http_api`'], ['http_port', 6924, 'Default', 'ARIKEDB_PORT', '6924', 'Bind port where the server API will run. Changing this key needs a server restart. See `use_http_api`'], ['cert_file', 'None', 'Default', 'ARIKEDB_CERT', None, 'Signed certificate file path or content to be used if server is configured with sslChanging this key needs a server restart'], ['key_file', 'None', 'Default', 'ARIKEDB_KEY', None, 'Private certificate key file path or content to be used if server is configured with sslChanging this key needs a server restart'], ['log_level', 'INFO', 'Default', 'LOG_LEVEL', 'INFO', 'Logging level for main server logs. Options are: DEBUG, INFO, WARN, ERROR, CRITICAL. Changing this key needs a server restart']], 'cell_len': [None, None, None, None, None, 70]}
╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                    Arikedb Config                                                                     │
├───────────────┬────────────┬─────────────┬───────────────────────┬────────────┬───────────────────────────────────────────────────────────────────────┤
│      Key      │    Value   │    Source   │        Env Var        │   Default  │                              Description                              │
├───────────────┼────────────┼─────────────┼───────────────────────┼────────────┼───────────────────────────────────────────────────────────────────────┤
│ use_auth      │ False      │ Default     │ ARIKEDB_USE_AUTH      │ False      │ Define if authentication is needed or not to manipulate arike databa  │
│               │            │             │                       │            │ ses. Changing this key needs a server restart                         │
├───────────────┼────────────┼─────────────┼───────────────────────┼────────────┼───────────────────────────────────────────────────────────────────────┤
│ use_ssl       │ False      │ Default     │ ARIKEDB_USE_SSL       │ False      │ Define if communication with the server will need ssl to connect. If  │
│               │            │             │                       │            │  True, also the keys `cert_file` and `key_file` should be configured  │
│               │            │             │                       │            │ , Changing this key needs a server restart                            │
├───────────────┼────────────┼─────────────┼───────────────────────┼────────────┼───────────────────────────────────────────────────────────────────────┤
│ use_http_api  │ True       │ Configured  │ ARIKEDB_USE_HTTP_API  │ False      │ Define if communication with the server throw http API will be enabl  │
│               │            │             │                       │            │ ed. See `http_host` and `http_port`                                   │
├───────────────┼────────────┼─────────────┼───────────────────────┼────────────┼───────────────────────────────────────────────────────────────────────┤
│ host          │ localhost  │ Default     │ ARIKEDB_HOST          │ localhost  │ Bind address where the server will run. Use `localhost` (default) to  │
│               │            │             │                       │            │  run only in a local scope, or use `0.0.0.0` or a specific ip for re  │
│               │            │             │                       │            │ mote access. Changing this key needs a server restart                 │
├───────────────┼────────────┼─────────────┼───────────────────────┼────────────┼───────────────────────────────────────────────────────────────────────┤
│ port          │ 6923       │ Default     │ ARIKEDB_PORT          │ 6923       │ Bind port where the server will run. Changing this key needs a serve  │
│               │            │             │                       │            │ r restart                                                             │
├───────────────┼────────────┼─────────────┼───────────────────────┼────────────┼───────────────────────────────────────────────────────────────────────┤
│ http_host     │ localhost  │ Default     │ ARIKEDB_HTTP_HOST     │ localhost  │ Bind address where the server API will run. Changing this key needs   │
│               │            │             │                       │            │ a server restart. See `use_http_api`                                  │
├───────────────┼────────────┼─────────────┼───────────────────────┼────────────┼───────────────────────────────────────────────────────────────────────┤
│ http_port     │ 6924       │ Default     │ ARIKEDB_PORT          │ 6924       │ Bind port where the server API will run. Changing this key needs a s  │
│               │            │             │                       │            │ erver restart. See `use_http_api`                                     │
├───────────────┼────────────┼─────────────┼───────────────────────┼────────────┼───────────────────────────────────────────────────────────────────────┤
│ cert_file     │ None       │ Default     │ ARIKEDB_CERT          │ None       │ Signed certificate file path or content to be used if server is conf  │
│               │            │             │                       │            │ igured with sslChanging this key needs a server restart               │
├───────────────┼────────────┼─────────────┼───────────────────────┼────────────┼───────────────────────────────────────────────────────────────────────┤
│ key_file      │ None       │ Default     │ ARIKEDB_KEY           │ None       │ Private certificate key file path or content to be used if server is  │
│               │            │             │                       │            │  configured with sslChanging this key needs a server restart          │
├───────────────┼────────────┼─────────────┼───────────────────────┼────────────┼───────────────────────────────────────────────────────────────────────┤
│ log_level     │ INFO       │ Default     │ LOG_LEVEL             │ INFO       │ Logging level for main server logs. Options are: DEBUG, INFO, WARN,   │
│               │            │             │                       │            │ ERROR, CRITICAL. Changing this key needs a server restart             │
╰───────────────┴────────────┴─────────────┴───────────────────────┴────────────┴───────────────────────────────────────────────────────────────────────╯

```
