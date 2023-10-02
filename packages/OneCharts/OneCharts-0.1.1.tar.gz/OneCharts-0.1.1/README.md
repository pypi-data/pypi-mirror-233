# Python wrapper for One Charts API
[One Charts](https://onecharts.io) - **Create and Manage charts with Ease!**

One Charts is a data visualization platform, using which, users can create various charts such as Line Charts, Pie Charts, Bar Charts, Scatter Charts etc., ([supported charts](https://onecharts.io/collection)) and customize them easily.

[One Charts API](https://onecharts.io/api) - using One charts REST API, users can create, update charts *programatically and in realtime*.

This repository contains the python wrapper to interact with the One Charts API.
# Authentication

The One Charts API uses API key to authenticate requests. You can view and manage your API key in the [user profile](https://onecharts.io/profile).

# Installation

```bash
$ git clone https://github.com/onechartsio/onecharts-py.git
$ cd onecharts-py
$ python setup.py install
```

# Basic Usage
Import and initialize the `onecharts` object as:
```python
>>> import onecharts
>>> oc = onecharts.OneCharts(API_KEY)  # Add your API Key.
```

### [Get User Charts](https://onecharts.io/api#user_charts)
`oc.get_user_charts()` method can be  used to retrieve public charts of an user. Example usage:
```python
>>> charts = oc.get_user_charts('adam', q='stock')
>>> print(charts)
{
   "charts":[
      {
         "chart_id":"k-jOPzitp-MzB6",
         "chart_title":"top 10 stocks",
         "created_time":"2022-12-17T11:04:21.307Z",
         "chart_type":"pie",
         "chart_sub_type":"basic_pie",
         "thumbnail_path":"piechart",
         "cloned_from":"piechart"
      },
      {
         "chart_id":"o-SDEvxw9-7A0g",
         "chart_title":"dowjones Stocks daily trend",
         "created_time":"2022-12-17T11:04:21.307Z",
         "chart_type":"line",
         "chart_sub_type":"basicline",
         "thumbnail_path":"linechart",
         "cloned_from":"linechart"
      },
   ],
   "success":true
}
```

### [Create a New Chart](https://onecharts.io/api#new_chart)
`oc.create_new_chart()` method can be  used to create a new chart. Example usage:
```python
>>> data = None  # Can contain some dictionary to overwrite the default data that's being cloned from.
>>> res = oc.create_new_chart('piechart', chart_title='Rainfall in 2023', visibility='private', notes='Some notes', data=data)
>>> print(res)
{
    'chart_id': 'KArrNpHzM-RLCo',
    'success': True
}
```
The above method creates a new piechart as shown below, which can be accessed using The created chart can be accessed using `https://onecharts.io/chart/KArrNpHzM-RLCo`
[![image](https://static.onecharts.io/img/onecharts-api-create-new-charts.webp)](https://onecharts.io?ref=github)

### [Get Chart Config](https://onecharts.io/api#get_chart_config)
`oc.get_chart_config()` method can be  used to get the config of a chart. Example usage:
```python
>>> res = oc.get_chart_config('KArrNpHzM-RLCo')
>>> print(res)
{
    "chart": {
        "chart_id": "KArrNpHzM-RLCo",
        "chart_title": "Rainfall in 2023",
        "created_time": "2023-09-10T06:03:20.694646Z",
        "modified_time": "2023-09-10T06:03:20.694646Z",
        "chart_type": "pie",
        "chart_sub_type": "basic_pie",
        "thumbnail_path": "piechart",
        "cloned_from": "piechart",
        "owner": "onecharts",
        "notes": "Some notes",
        "visibility": "private",
        "chart_options": {
            "emphasis": [
                {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowColor": "rgba(0, 0, 0, 0.5)",
                        "shadowOffsetX": 0,
                    }
                }
            ],
            "legend": [{"align": "auto", "bottom": "0%", "left": "45%", "right": "0%"}],
            "series": [{"radius": "70%", "seriesLayoutBy": "row", "type": "pie"}],
            "title": [
                {"left": "50%", "text": "Pie Chart", "textAlign": "center", "top": "0%"}
            ],
            "tooltip": [{"trigger": "item"}],
        },
    },
    "success": True,
}
```

### [Get Chart Data](https://onecharts.io/api#get_chart_data)
`oc.get_chart_data()` method can be  used to get the data of a chart. Example usage:
```python
>>> res = oc.get_chart_data('KArrNpHzM-RLCo')
>>> print(res)
{
    "data": {
        "labels": ["Jan", "Feb", "Mar", "Apr"],
        "dataset": [
            {"name": "Jan", "value": 12},
            {"name": "Feb", "value": 16},
            {"name": "Mar", "value": 19},
            {"name": "Apr", "value": 22},
        ],
    },
    "success": True,
}
```

### [Update Chart Data](https://onecharts.io/api#update_chart_data)
`oc.update_chart_data()` method can be  used to get the data of a chart. Example usage:
```python
>>> # The data should follow specific format.
>>> # Learn more about the format from here: https://onecharts.io/api#update_chart_data
>>> data = {
    'dataset': [
        {
            'name': "Jan",
            "value": 120
        }
    ]
}
>>> res = oc.update_chart_data('KArrNpHzM-RLCo', overwrite=False, data=data)
>>> print(res)
{
    'success': True
}
```
The above method updates an existing chart (corresponding to chart id: `KArrNpHzM-RLCo`) as shown below.
[![image](https://static.onecharts.io/img/onecharts-api-update-chart-data.webp)](https://onecharts.io?ref=github)
