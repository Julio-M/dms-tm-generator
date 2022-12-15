# DMS- Table mapping script generator

This is a python script that reads a file that inlcudes a list of `tables`, and generates a `table-mapping.json` file to be used with Database migration tasks in `DMS`.

## Before you run

Before you run the script, make sure you have a `.txt` in the root directory, that lists all the `tables` you want to include in the `table-mapping` file.

example `table-example.txt`
```
table1
table2
table3
```

If any of the tables require an `add-prefix` rule-action, then make sure you include the keyword `add-prefix` next to the table name in your `.txt` file.

example
```
table1 add-prefix // space between table name and keyword is important
table2
table3
```

> **_NOTE:_** You will be prompted to add the value you want for the prefix when you run the script

## How to run

Now that you `.txt. file is ready, all you have to do is run the following command (in the root directory):

`make run`

example of `table_mapping.json` file

```
{
    "rules": [
        {
            "rule-type": "transformation",
            "rule-id": 133217270651029775251720185826470797345,
            "rule-name": "95a55e6aefcc4b6cb3cb9fe9167b8bc8",
            "rule-target": "table",
            "object-locator": {
                "schema-name": "public",
                "table-name": "BetaUser"
            },
            "rule-action": "add-prefix",
            "value": "example_"
        },
        {
            "rule-type": "selection",
            "rule-id": 146070652287577011669169078964960673232,
            "rule-name": "ef94fd111c664410a00b9848c1cb9b44",
            "object-locator": {
                "schema-name": "public",
                "table-name": "BetaUser"
            },
            "rule-action": "include",
            "filters": []
        }
    ]
}
```


## Requirements

`bullet==2.2.0`

## Credits

This script is based on and borrows code from this repo: `emreoztoprak/dms-table-mapping-generator`


