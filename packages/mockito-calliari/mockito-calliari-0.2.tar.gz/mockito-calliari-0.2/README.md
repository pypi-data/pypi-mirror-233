# Motivation
When employing mocks to substitute actual databases in unit tests, a common challenge arises wherein the tests may not accurately reflect the data in the database, thereby overlooking specific and unique scenarios.

To address this issue, Mockito strives to standardize the data being mocked.

# Structure
Imagine that are 2 SQL tables, with the following structures:

table1
> Column |Type
>--------|------------
> id| integer
> name| text
> menus| text

table2
> Column |Type
>--------|------------
> id| integer
> name| text
> description| text

Based on them, it is necessary to create a dictionary, where the keys are the names of the tables, and the values are a list of dictionaries, where these dictionary keys would be the table columns and the values are examples of data to be returned by Mockito.

In the example below, the dictionary will contain `table1` and `table2`, where the `table1` will have 2 data examples and the `table2` only will have 1.

_**data_file.py**_

    DEFAULT_BASES = {
        "table1": [
            {"id": 1, "name": "Guest", "menus": "menu_1"},
            {"id": 2, "name": "Some One", "menus": "menu_2"},
        ],
        "table2": [
            {"id": 1, "name": "OtherName", "Description": "Super important data"},
        ]
    }

# Method one()
## Basic utilization:
The function below returns the `id` and `name` from `table1`:

_**file.py**_

    def return_table_data(id):
        table_data = Table1.query.filter(
            Table1.id == id
        ).with_entities(
            Table1.id,
            Table1.name
        ).first()
        
        return table_data

The function test, using the method `one()` from `Mockito` will be something like this:

    from mockito.mockito import Mockito

    from data_file import DEFAULT_BASES
    from file import return_table_data
    
    
    @mock_patch('file.Table1')
    class TestReturnData():
    def test_retorn_data(self, mock_table1):
        mock_table1.query.filter.return_value.with_entities.return_value.first.return_value = (
            Mockito(
                data_dict={"table1": ["id", "name"]},
                data_bases=DEFAULT_BASES,
            ).one()
        )
        
        response = return_table_data(id = 1)
        print(response)
        print(response.id)
        print(response.name)
        print(response.to_dict())

Outputs:

    <MoMock>
    1
    Guest
    {"id": 1, "name": "Guest"}

The object return from the `Mockito` is called `MoMock`, which is a `Mock` with a method called `to_dict()`

## Column with alias:
To assign the alias `potato` to the `name` column within the function, provide the list `["name", "potato"]` to Mockito. Note that the `id` column will also be included in the result, but it won't be given an alias:

    from mockito.mockito import Mockito

    from data_file import DEFAULT_BASES
    from file import return_table_data
    
    
    @mock_patch('file.Table1')
    class TestReturnData():
    def test_retorn_data(self, mock_table1):
        mock_table1.query.filter.return_value.with_entities.return_value.first.return_value = (
            Mockito(
                data_dict={"table1": ["id", ["name", "potato"]]},
                data_bases=DEFAULT_BASES,
            ).one()
        )
        
        response = return_table_data(id = 1)
        print(response)
        print(response.id)
        print(response.potato)
        print(response.to_dict())

Outputs:

    <MoMock>
    1
    Guest
    {"id": 1, "potato": "Guest"}

## Non-existent column:
If a column is passed to `Mockito` that does not exist in `DEFAULT_BASES` for the table in question, it will have the value `invalid column` in its place, in the example below the `foo` column was chosen and it is not present in the `DEFAULT_BASES` dictionary for the `table1` table:

    from mockito.mockito import Mockito

    from data_file import DEFAULT_BASES
    from file import return_table_data
    
    
    @mock_patch('file.Table1')
    class TestReturnData():
    def test_retorn_data(self, mock_table1):
        mock_table1.query.filter.return_value.with_entities.return_value.first.return_value = (
            Mockito(
                data_dict={"table1": ["id", "foo"]},
                data_bases=DEFAULT_BASES,
            ).one()
        )
        
        response = return_table_data(id = 1)
        print(response)
        print(response.id)
        print(response.foo)
        print(response.to_dict())

Outputs:

    <MoMock>
    1
    invalid column
    {"id": 1, "foo": "invalid column"}

## Joins
To retrieve data from multiple tables, you can achieve this by providing the table name along with its respective columns to `Mockito`. In the example below, it will return the `id` and `name` columns from `table1`, as well as the `description` column from the `table2`:
_**file2.py**_

    def return_table_data(id):
        table_data = Table1.query.filter(
            Table1.id == id
        ).join(
            Table2, "some valid condition here"
        ).with_entities(
            Table1.id,
            Table1.name
        ).first()
        
        return table_data

_**Test_file.py**_

    from mockito.mockito import Mockito

    from data_file import DEFAULT_BASES
    from file2 import return_table_data
    
    
    @mock_patch('file2.Table1')
    class TestReturnData():
    def test_retorn_data(self, mock_table1):
        mock_table1.query.filter.return_value.join.return_value.with_entities.return_value.first.return_value = (
            Mockito(
                data_dict={
                    "table1": ["id", "name"],
                    "table2": ["description"],
                },
                data_bases=DEFAULT_BASES,
            ).one()
        )
        
        response = return_table_data(id = 1)
        print(response)
        print(response.id)
        print(response.name)
        print(response.description)
        print(response.to_dict())

Outputs:

    <MoMock>
    1
    Guest
    Super important data
    {"id": 1, "name": "Guest": "description": "Super important data"}

# Method all_combinations()
## Basic utilization:
This method is similar to `one()` but will return a list of all combinations in the `DEFAULT_TABLES` variable.

    from mockito.mockito import Mockito

    from data_file import DEFAULT_BASES
    from file import return_table_data
    
    
    @mock_patch('file.Table1')
    class TestReturnData():
    def test_retorn_data(self, mock_table1):
        mock_table1.query.filter.return_value.with_entities.return_value.first.return_value = (
            Mockito(
                data_dict={"table1": ["id", "name"]},
                data_bases=DEFAULT_BASES,
            ).all_combinations()
        )
        
        response = return_table_data(id = 1)
        print(response)
        print(response[0].id)
        print(response[0].name)
        print(response[0].to_dict())
        print(response[1].id)
        print(response[1].name)
        print(response[1].to_dict())

Outputs:

    [<MoMock>, <MoMock>]
    1
    Guest
    {"id": 1, "name": "Guest"}
    2
    Some One
    {"id": 2, "name": "Some One"}

## Return list of dictionaries:
The `all_combinations` method has the `return_dicts` parameter (which by default is equal to `False`) and if changed to `True`, it will return a list of dictionaries instead of `MoMock` objects.

    from mockito.mockito import Mockito

    from data_file import DEFAULT_BASES
    from file import return_table_data
    
    
    @mock_patch('file.Table1')
    class TestReturnData():
    def test_retorn_data(self, mock_table1):
        mock_table1.query.filter.return_value.with_entities.return_value.first.return_value = (
            Mockito(
                data_dict={"table1": ["id", "name"]},
                data_bases=DEFAULT_BASES,
            ).all_combinations(return_dicts=True)
        )
        
        response = return_table_data(id = 1)
        print(response)


Outputs:

    [{"id": 1, "name": "Guest"}, {"id": 2, "name": "Some One"}]

## Joins
Just like in the case of the `one()` method, you can pass the table name and its columns to `Mockito`, the difference is that `Mockito` will combine all possible values. In the example below, table1 has 2 possible values, and table2 has only 1, thus `all_combinations` returns 2 results, being a combination of the first value from `table1` with the only value from `table2`, and the second value from the `table1` with a single value from the `table2`.

    from mockito.mockito import Mockito

    from data_file import DEFAULT_BASES
    from file2 import return_table_data
    
    
    @mock_patch('file2.Table1')
    class TestReturnData():
    def test_retorn_data(self, mock_table1):
        mock_table1.query.filter.return_value.join.return_value.with_entities.return_value.first.return_value = (
            Mockito(
                data_dict={
                    "table1": ["id", "name"],
                    "table2": ["description"],
                },
                data_bases=DEFAULT_BASES,
            ).all_combinations()
        )
        
        response = return_table_data(id = 1)
        print(response)
        print(response[0].id)
        print(response[0].name)
        print(response[0].description)
        print(response[0].to_dict())
        print(response[1].id)
        print(response[1].name)
        print(response[1].description)
        print(response[1].to_dict())

Outputs:

    [<MoMock>, <MoMock>]
    1
    Guest
    Super important data
    {"id": 1, "name": "Guest", "description": "Super important data"}
    2
    Some One
    Super important data
    {"id": 2, "name": "Some One", "description": "Super important data"}

The table below is a representation of how `MoMock` elements would be constructed:

> Values |First value from table2
>--------|------------
> First value from table1 | First MoMock
> Second value from table1 | Second MoMock

If `table2` also had 2 values, the `all_combinations` method would return a list with 4 combinations, with the structure:

> Values |First value from table2 | Second value from table2
>--------|------------|------------
> First value from table1 | First MoMock | Third MoMock
> Second value from table1 | Second MoMock | Fourth MoMock