# -*- coding: utf-8 -*-

from jmespath_token.token import (
    TokenTypeEnum,
    RawToken,
    JmespathToken,
    SubToken,
    JoinToken,
    SplitToken,
    MapToken,
    evaluate_token,
)

data = {
    "firstname": "John",
    "lastname": "Doe",
}


class Test:
    def _test_RawToken(self):
        for value in [
            None,
            1,
            "hello",
            "$firstname",
            [1, 2, 3],
            ["hello", "world"],
            ["$firstname", "$lastname"],
            {"key": "value"},
            {"firstname": "$firstname"},
        ]:
            token = RawToken(value=value)
            assert token.evaluate(None) == value
            assert token.evaluate("world") == value
            assert token.evaluate([1, 2]) == value
            assert token.evaluate({"firstname": "alice"}) == value

            assert token.to_dict() == {"value": value}
            assert RawToken.from_dict({"value": value}) == token

    def _test_JmespathToken(self):
        token = JmespathToken(path="$name")
        assert token.evaluate({"name": "John"}) == "John"
        assert token.to_dict() == {"path": "$name"}
        assert JmespathToken.from_dict({"path": "$name"}) == token

        token = JmespathToken(path="$@")
        assert token.evaluate("John") == "John"
        assert token.to_dict() == {"path": "$@"}
        assert JmespathToken.from_dict({"path": "$@"}) == token

    def _test_SubToken(self):
        # simple case
        token = SubToken(template="hello {name}", params={"name": "$name"})
        assert token.evaluate({"name": "John"}) == "hello John"
        dct = {
            "template": "hello {name}",
            "params": {"name": "$name"},
        }
        assert token.to_dict() == dct
        assert SubToken.from_dict(dct) == token

        # nested
        token = SubToken(
            template="hello {name}",
            params={
                "name": {
                    "type": TokenTypeEnum.jmespath,
                    "kwargs": {"path": "$name"},
                }
            },
        )
        assert token.evaluate({"name": "John"}) == "hello John"

    def _test_JoinToken(self):
        # simple case
        token = JoinToken(
            sep="$sep",
            array=["hello", "$lastname", "$firstname", "world"],
        )
        assert (
            token.evaluate({"sep": ", ", "firstname": "John", "lastname": "Doe"})
            == "hello, Doe, John, world"
        )
        dct = {
            "sep": "$sep",
            "array": ["hello", "$lastname", "$firstname", "world"],
        }
        assert token.to_dict() == dct
        assert JoinToken.from_dict(dct) == token

        # array is a token
        token = JoinToken(
            sep="$sep",
            array="$array",
        )
        assert token.evaluate({"sep": ", ", "array": ["Doe", "John"]}) == "Doe, John"

        # nested
        token = JoinToken(
            sep=", ",
            array=[
                "$lastname",
                {
                    "type": TokenTypeEnum.sub,
                    "kwargs": {
                        "template": "{firstname}",
                        "params": {"firstname": "$firstname"},
                    },
                },
            ],
        )
        assert token.evaluate({"firstname": "John", "lastname": "Doe"}) == "Doe, John"

    def _test_SplitToken(self):
        # seder
        token = SplitToken(
            sep=",",
            text="blue,green",
        )
        dct = {
            "sep": ",",
            "text": "blue,green",
        }
        assert token.to_dict() == dct
        assert SplitToken.from_dict(dct) == token

        # simple case
        token = SplitToken(
            sep=",",
            text="blue,green",
        )
        assert token.evaluate({}) == ["blue", "green"]

        token = SplitToken(
            sep="$sep",
            text="$text",
        )
        assert token.evaluate({"sep": ",", "text": "blue,green"}) == ["blue", "green"]

        # nested
        token = SplitToken(
            sep=", ",
            text={
                "type": TokenTypeEnum.join,
                "kwargs": {
                    "sep": ", ",
                    "array": ["$lastname", "$firstname"],
                },
            },
        )
        assert token.evaluate({"firstname": "John", "lastname": "Doe"}) == [
            "Doe",
            "John",
        ]

    def _test_MapToken(self):
        token = MapToken(
            key="$name",
            mapper={"alice": "$female", "bob": "$male"},
            default="unknown",
        )
        assert (
            token.evaluate({"name": "alice", "female": "girl", "male": "boy"}) == "girl"
        )
        dct = {
            "key": "$name",
            "mapper": {"alice": "$female", "bob": "$male"},
            "default": "unknown",
        }
        assert token.to_dict() == dct
        assert MapToken.from_dict(dct) == token

        token = MapToken(
            key="alice",
            mapper="$@",
            default="unknown",
        )
        assert token.evaluate(data={"alice": "girl"}) == "girl"

    def _test_evaluate_token_simple_case(self):
        # implicit raw token
        assert evaluate_token("hello", data) == "hello"

        # implicit raw token
        assert evaluate_token([1, 2, 3], data) == [1, 2, 3]

        # implicit raw token
        assert evaluate_token({"key": "value"}, data) == {"key": "value"}

        # implicit jmespath token
        assert evaluate_token("$firstname", data) == "John"

        # implicit list of token
        assert evaluate_token(["$firstname", "$lastname"], data) == ["John", "Doe"]

        # implicit dict, and value is token
        assert evaluate_token(
            {"firstname": "$firstname", "lastname": "$lastname"},
            data,
        ) == {"firstname": "John", "lastname": "Doe"}

        # explicit raw token
        assert (
            evaluate_token(
                {
                    "type": TokenTypeEnum.raw,
                    "kwargs": {"value": "hello"},
                },
                data,
            )
            == "hello"
        )
        assert evaluate_token(
            {
                "type": TokenTypeEnum.raw,
                "kwargs": {"value": {"type": TokenTypeEnum.raw}},
            },
            data,
        ) == {"type": TokenTypeEnum.raw}

        # explicit jmespath token
        assert (
            evaluate_token(
                {
                    "type": TokenTypeEnum.jmespath,
                    "kwargs": {"path": "$firstname"},
                },
                data,
            )
            == "John"
        )

        # sub token
        assert (
            evaluate_token(
                {
                    "type": TokenTypeEnum.sub,
                    "kwargs": {
                        "template": "Hello {FIRSTNAME} {LASTNAME}! Today is my {AGE} years birthday!",
                        "params": {
                            "FIRSTNAME": "$firstname",
                            # params can be any token
                            "LASTNAME": {
                                "type": TokenTypeEnum.jmespath,
                                "kwargs": {"path": "$lastname"},
                            },
                            "AGE": 18,
                        },
                    },
                },
                data,
            )
            == "Hello John Doe! Today is my 18 years birthday!"
        )

        # join token
        assert (
            evaluate_token(
                {
                    "type": TokenTypeEnum.join,
                    "kwargs": {
                        "sep": ", ",
                        "array": [
                            "$lastname",
                            {
                                "type": TokenTypeEnum.jmespath,
                                "kwargs": {"path": "$firstname"},
                            },
                        ],
                    },
                },
                data,
            )
            == "Doe, John"
        )

        # split token
        assert evaluate_token(
            {
                "type": TokenTypeEnum.split,
                "kwargs": {
                    "sep": ", ",
                    "text": {
                        "type": TokenTypeEnum.join,
                        "kwargs": {
                            "sep": ", ",
                            "array": ["$lastname", "$firstname"],
                        },
                    },
                },
            },
            data,
        ) == ["Doe", "John"]

        # map token
        assert (
            evaluate_token(
                {
                    "type": TokenTypeEnum.map,
                    "kwargs": {
                        "key": "$name",
                        "mapper": {"alice": "$female", "bob": "$male"},
                        "default": "unknown",
                    },
                },
                {"name": "alice", "female": "girl", "male": "boy"},
            )
            == "girl"
        )

    def _test_evaluate_deeply_nested_token(self):
        token = {
            "type": TokenTypeEnum.join,
            "kwargs": {
                "sep": ", ",
                "array": [
                    {
                        "type": TokenTypeEnum.sub,
                        "kwargs": {
                            "template": "my first name is {firstname}",
                            "params": {
                                "firstname": {
                                    "type": TokenTypeEnum.sub,
                                    "kwargs": {
                                        "template": "{firstname}",
                                        "params": {
                                            "firstname": "$firstname",
                                        },
                                    },
                                },
                            },
                        },
                    },
                    {
                        "type": TokenTypeEnum.sub,
                        "kwargs": {
                            "template": "my last name is {lastname}",
                            "params": {
                                "lastname": "$lastname",
                            },
                        },
                    },
                ],
            },
        }
        value = evaluate_token(token, data)
        assert value == "my first name is John, my last name is Doe"

    def test(self):
        self._test_RawToken()
        self._test_JmespathToken()
        self._test_SubToken()
        self._test_JoinToken()
        self._test_SplitToken()
        self._test_MapToken()
        self._test_evaluate_token_simple_case()
        self._test_evaluate_deeply_nested_token()


if __name__ == "__main__":
    from jmespath_token.tests.helper import run_cov_test

    run_cov_test(__file__, "jmespath_token.token", preview=False)
