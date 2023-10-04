"""The objective of this module is to provide a class that will help mocking
database data, considering that it will always return the same values from
the same tables, and these values
must be related with the real data.
"""
from itertools import product
from typing import Any, Dict, List, Union

from mock import Mock


class MoMock(Mock):
    def to_dict(self):
        return {key: getattr(self, key) for key in self._args}


class Mockito:
    def __init__(
        self,
        data_dict: Dict[str, List[Union[str, List[str]]]],
        data_bases: Dict[str, List[Dict[str, Any]]],
    ):
        """
        Args:
            Example:
            data_dict = {
                database1: [field11, [field12, alias_field12], field13],
                database2: [field21, field22, [field23, alias_field23]]
            }
        Returns:
            None.
        """
        self.data_dict = data_dict
        self.data_bases = data_bases

    def prepare_mock(self, data_bases: Dict[str, Any]) -> MoMock:
        response = MoMock()
        args = []

        for db_name, db_columns_list in self.data_dict.items():
            for column in db_columns_list:
                if isinstance(column, list):
                    setattr(
                        response,
                        column[1],
                        data_bases.get(db_name, {}).get(
                            column[0], "invalid column"
                        ),
                    )
                    args.append(column[1])
                else:
                    setattr(
                        response,
                        column,
                        data_bases.get(db_name, {}).get(
                            column, "invalid column"
                        ),
                    )
                    args.append(column)

        setattr(response, "_args", args)

        return response

    def one(self) -> MoMock:
        """Return the first values for the chosen tables."""
        data_bases = {
            base: self.data_bases.get(base, [])[0]
            for base in self.data_dict.keys()
        }

        return self.prepare_mock(data_bases)

    def all_combinations(self, return_dicts: bool = False) -> List[MoMock]:
        """Return all the possibles combinations from the chosen tables."""
        data_bases = {
            base: self.data_bases.get(base, [])
            for base in self.data_dict.keys()
        }
        all_combinations = []
        for key, values in data_bases.items():
            structured_data = []
            for value in values:
                structured_data.append({key: value})
            all_combinations.append(structured_data)
        del data_bases
        del structured_data
        all_combinations = list(product(*all_combinations))

        response = []
        for product_tuple in all_combinations:
            values = {}
            for t1 in product_tuple:
                values.update(t1)
            response.append(
                self.prepare_mock(values).to_dict()
                if return_dicts
                else self.prepare_mock(values)
            )

        return response
