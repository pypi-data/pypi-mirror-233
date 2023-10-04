from unittest import TestCase

from parameterized import parameterized, parameterized_class

DATA_TABLES = {
    "table_1": [
        {"column_1": "value1", "column_2": "value2"},
        {"column_1": "value3", "column_2": "value4"},
    ],
    "table_2": [{"column_5": "value5", "column_6": "value6"}],
}


@parameterized_class(
    ("data", "expected_response1", "expected_response2"),
    [
        (
            {
                "table_1": [
                    "column_1",
                    ["column_1", "column_1_with_alias"],
                    "nonexistent_column",
                ],
                "table_2": ["column_5", "column_6"],
            },
            {
                "column_1": "value1",
                "column_1_with_alias": "value1",
                "nonexistent_column": "invalid column",
                "column_5": "value5",
                "column_6": "value6",
            },
            {
                "column_1": "value3",
                "column_1_with_alias": "value3",
                "nonexistent_column": "invalid column",
                "column_5": "value5",
                "column_6": "value6",
            },
        )
    ],
)
class TestMockito(TestCase):
    def test_mockito_one(self):
        from src.mockito.mockito import Mockito

        response = Mockito(data_dict=self.data, data_bases=DATA_TABLES).one()

        self.assertEqual(
            response.column_1, self.expected_response1["column_1"]
        )
        self.assertEqual(
            response.column_1_with_alias,
            self.expected_response1["column_1_with_alias"],
        )
        self.assertEqual(
            response.nonexistent_column,
            self.expected_response1["nonexistent_column"],
        )
        self.assertEqual(
            response.column_5, self.expected_response1["column_5"]
        )
        self.assertEqual(
            response.column_6, self.expected_response1["column_6"]
        )
        self.assertEqual(response.to_dict(), self.expected_response1)

    @parameterized.expand([(False,), (True,)])
    def test_mockito_all_combinations(self, return_dicts):
        from src.mockito.mockito import Mockito

        response = Mockito(
            data_dict=self.data, data_bases=DATA_TABLES
        ).all_combinations(return_dicts=return_dicts)

        if return_dicts:
            self.assertEqual(response[0], self.expected_response1)
            self.assertEqual(response[1], self.expected_response2)
        else:
            self.assertEqual(response[0].to_dict(), self.expected_response1)
            self.assertEqual(
                response[0].column_1, self.expected_response1["column_1"]
            )
            self.assertEqual(
                response[0].column_1_with_alias,
                self.expected_response1["column_1_with_alias"],
            )
            self.assertEqual(
                response[0].nonexistent_column,
                self.expected_response1["nonexistent_column"],
            )
            self.assertEqual(
                response[0].column_5, self.expected_response1["column_5"]
            )
            self.assertEqual(
                response[0].column_6, self.expected_response1["column_6"]
            )

            self.assertEqual(response[1].to_dict(), self.expected_response2)
            self.assertEqual(
                response[1].column_1, self.expected_response2["column_1"]
            )
            self.assertEqual(
                response[1].column_1_with_alias,
                self.expected_response2["column_1_with_alias"],
            )
            self.assertEqual(
                response[1].nonexistent_column,
                self.expected_response2["nonexistent_column"],
            )
            self.assertEqual(
                response[1].column_5, self.expected_response2["column_5"]
            )
            self.assertEqual(
                response[1].column_6, self.expected_response2["column_6"]
            )
