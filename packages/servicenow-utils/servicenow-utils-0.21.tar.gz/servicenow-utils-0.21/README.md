# ServiceNow Incident Retrieval Module

This module provides utilities to retrieve incidents from ServiceNow within a specified date range.

## Features

- Fetch incidents from ServiceNow based on a date range.
- Breaks down the retrieval into intervals for efficient fetching.
- Converts incident data into a Pandas DataFrame for easy data manipulation.

## Installation

```bash
pip install servicenow-utils
```

## Usage

First, ensure you have the necessary dependencies:

```bash
pip install pandas requests
```

Then, use the module as follows:

```python
from servicenow_utils import get_incidents

# Define your ServiceNow connection details
url = "YOUR_SERVICE_NOW_URL"
endpoint = "YOUR_ENDPOINT"
user_name = "YOUR_USERNAME"
password = "YOUR_PASSWORD"

df = get_incidents(
    current_day='2023-04-01', 
    end_day='2023-04-30',
    url=url,
    endpoint=endpoint,
    user_name=user_name,
    password=password
)
```

## Functions

### `day_plus_one(day: str) -> str`

Increments the given day by one.

### `day_string_to_dt(day: str) -> datetime`

Converts a string representation of a day into a datetime object.

### `get_incidents(current_day, end_day, url, endpoint, user_name, password, start_hour=0, hour_interval=8, count_limit=2000) -> pd.DataFrame`

Fetches incidents from ServiceNow within the given date range and returns them as a Pandas DataFrame.

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
