# wivi_graph_client_py

**wivi_graph_client_py** is a Python GraphQL client library designed to interact with the **wivi_graph** Apollo Server, enabling users to easily ingest and fetch data from the associated Timescale database. This library simplifies the process of interacting with your **wivi_graph** server and managing data requests, making it effortless to integrate with your TypeScript applications.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)

## Installation

You can install **wivi_graph_client_py** using pip:

```bash
pip install wivi_graph_client_py
```

## Usage

**Pre-Requisites:** 
- Running Wivi Graph Apollo Server
- Install graphql-core and requests

You can use this library by importing it into your project and using the built-in functions:

```python
from wivi_graph_client_py.client import GraphQL_Client

    client = GraphQL_Client(endpoint)
    variables = {
        "input": {
            "configurationId": "3",
            "info": [
                {
                    "time": "2022-10-09T00:00:00Z",
                    "stats": [
                        {"name": "DevInfoTest", "svalue": "100Km/h", "value": 100}
                    ],
                }
            ],
        }
    }
    response = client.create_device_info(variables)
```

The above piece of code will make connection with the server and create data of device info in the timescale database

## Features

1. Configuration Related Functions:
   a. create_configuration
   b. get_configuration

2. Device Info Related Functions:
   a. create_device_info
   b. delete_device_info
   c. get_device_info

3. DTC Related Functions:
   a. create_dtc
   b. delete_dtc
   c. get_dtc

4. ECU Related Functions:
   a. get_ecu

5. Formula Related Functions:
   a. upsert_formula
   b. upsert_formula_constant
   c. load_formula
   d. calculate_formula

6. GPS Related Functions:
   a. upsert_gps
   b. delete_gps
   c. get_gps

7. Message related Functions:
   a. create_message
   b. get_message

8. Network Stats related Functions:
   a. create_network_stats
   b. get_network_stats

9. Network related Functions:
   a. get_network

10. Signal related Functions:
    a. upsert_signal_data
    b. delete_signal_data
    c. get_signals
    d. get_signal_data

11. Version related Functions:
    a. upsert_version
    b. delete_version
    c. get_version
