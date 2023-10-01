# -*- coding: utf-8 -*-

"""
Token 是一个需要被 evaluate 之后才能获得的值. 本模块实现如何定义一个 Token, 以及如何
evaluate 最终的值, 以及定义了一些常用的 Token.
"""

import typing as T
import dataclasses
import jmespath

from .types import T_TOKEN, T_DATA
from .constants import TokenTypeEnum, TYPE


@dataclasses.dataclass(frozen=True)
class BaseToken:
    """
    所有 Token 的基类.

    所有的 Token 必须有一些属性定义了这个 Token 是如何被 evaluate 的规则. 例如
    :class:`JmespathToken`` 就有一个 ``path`` 属性, 定义了如何从 data 中提取最终的
    value. 这些属性的定义取决于你的 Token 的 evaluation 的规则.

    所有的 Token 类必须有一个 ``def evaluate(data: T_DATA):`` 方法. 这个方法的作用是根据
     ``data`` 和 evaluation 的规则提取储最终的 value. 这个 data 通常是一个 dict 对象,
     但也可以是 list, str, int, float, bool 等任何可以用 jmespath 处理的对象.
    """

    def to_dict(self) -> T.Dict[str, T.Any]:
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, dct: T.Dict[str, T.Any]):
        return cls(**dct)

    def evaluate(
        self,
        data: T_DATA,
    ) -> T.Any:  # pragma: no cover
        raise NotImplementedError


@dataclasses.dataclass(frozen=True)
class RawToken(BaseToken):
    """
    这种类型的 token 会将 value 中的值原封不动的返回.

    :param value: 所要返回的值. 可以是任何对象.

    .. versionadded:: 0.1.1
    """

    value: T.Any = dataclasses.field()

    def evaluate(self, data: T_DATA) -> T.Any:  # pragma: no cover
        return self.value


@dataclasses.dataclass(frozen=True)
class JmespathToken(BaseToken):
    """
    这种类型的 token 会从一个叫 ``data`` 的字典对象中通过 jmespath 语法获取最终的值.

    :param path: jmespath 的语法.

    .. versionadded:: 0.1.1
    """

    path: str = dataclasses.field()

    def evaluate(self, data: T_DATA) -> T.Any:  # pragma: no cover
        return jmespath.search(self.path[1:], data)


@dataclasses.dataclass(frozen=True)
class SubToken(BaseToken):
    """
    这种类型的 token 是一个字符串模板, 而模板中的变量都是从一个叫 ``data`` 的字典对象中通过
    jmespath 语法获取的.

    举例, 我们的 template 是 ``Hello {FIRSTNAME} {LASTNAME}!``,
    而我们的 data 如下::

        {"first_name": "John", "last_name": "Doe"}

    这个 FIRSTNAME, LASTNAME 需要从 data 中提取出来 (虽然看似不需要做任何处理, 但这里只是举例,
    用来说明这个 "提取" 的过程). 其中 params 参数如下::

        {
            "FIRSTNAME": "$first_name",
            "LASTNAME": "$last_name",
        }

    这个 params 的意思是从 data 中提取 ``$first_name`` 给 ``FIRSTNAME``, 提取 ``$last_name``
    给 ``LASTNAME``. 这里的 ``$first_name`` 是 jmespath 语法. 之后的 params 就可以作为
    字符串模板的参数, 通过 ``template.format(**params)`` 来最终生成字符串. 例如最终提取后的
    params 就是::

        {
            "FIRSTNAME": "John",
            "LASTNAME": "Doe",
        }

    然后最终的 ``Hello {FIRSTNAME} {LASTNAME}!`` 渲染后的结果就是 ``Hello John Doe!``.

    总结下来, ``SubToken`` 的使用方法是::

        >>> token = SubToken(
        ...     template="Hello {FIRSTNAME} {LASTNAME}!",
        ...     params={
        ...         "FIRSTNAME": "$first_name",
        ...         "LASTNAME": "$last_name",
        ...     },
        ... )
        >>> token.evaluate(
        ...     data={"first_name": "John", "last_name": "Doe"},
        ... )
        'Hello John Doe!'

    :param template: 字符串模板.
    :param params: 字符串模板所需的数据, 是一个 key value 键值对, 其中值既可以是 literal,
        也可以是一个 token. 也就是说这个 params 中的 value 的内容也是可以作为 token 被
        evaluate 的. 换言之, 支持嵌套.

    .. versionadded:: 0.1.1
    """

    template: T_TOKEN = dataclasses.field()
    params: T.Union[T_TOKEN, T.Dict[str, T_TOKEN]] = dataclasses.field(
        default_factory=dict
    )

    def evaluate(self, data: T_DATA) -> str:
        """
        todo: add docstring
        """
        return evaluate_token(self.template, data).format(
            **evaluate_token(self.params, data)
        )


@dataclasses.dataclass(frozen=True)
class JoinToken(BaseToken):
    """
    这种类型的 Token 可以用一个分隔符将一个数组中的字符串连接起来. 这里的 separator 可以是
    literal, 也可以是一个 token. 而 array 本身既可以是一个 literal, 也可以是一个 token,
    而如果 array 是一个 list 的话, 里面的元素既可以是 literal, 也可以是 token.

    注: 如果 array 中的元素不是字符串, 会被自动用 str() 函数转换成字符串.

    :param sep: str 或是 token
    :param array: list of str 或是 list of token 或者是一个 evaluate 的结果是 array 的 token.

    .. versionadded:: 0.1.1
    """

    sep: T_TOKEN = dataclasses.field()
    array: T.Union[T_TOKEN, T.List[T_TOKEN]] = dataclasses.field(default_factory=list)

    def evaluate(self, data: T_DATA) -> str:
        """
        todo: add docstring
        """
        return evaluate_token(self.sep, data).join(
            [str(i) for i in evaluate_token(self.array, data)]
        )


@dataclasses.dataclass(frozen=True)
class SplitToken(BaseToken):
    """
    这种类型的 Token 可以用一个分隔符将一个字符串分割为字符串列表. 这里的分隔符和字符串可以是
    literal, 也可以是一个 token.

    :param sep: str 或是 token
    :param text: str 或是是一个 evaluate 的结果是 str 的 token.

    .. versionadded:: 0.2.1
    """

    sep: T_TOKEN = dataclasses.field()
    text: T_TOKEN = dataclasses.field()

    def evaluate(self, data: T_DATA) -> str:
        """
        todo: add docstring
        """
        return evaluate_token(self.text, data).split(
            evaluate_token(self.sep, data)
        )


@dataclasses.dataclass(frozen=True)
class MapToken(BaseToken):
    """
    这种类型的 Token

    一个分隔符将一个数组中的字符串连接起来. 这里的 separator 可以是
    literal, 也可以是一个 token. 而 array 本身既可以是一个 literal, 也可以是一个 token,
    而如果 array 是一个 list 的话, 里面的元素既可以是 literal, 也可以是 token.

    注: 如果 array 中的元素不是字符串, 会被自动用 str() 函数转换成字符串.

    :param key: str 或是 token.
    :param mapper: key value 键值对, 其中 value 可以是 token, 又或者是一个 evaluate
        的结果是 key value 键值对的 token.
    :param default: 如果 key 不在 mapper 中的默认值.

    .. versionadded:: 0.1.1
    """

    key: T_TOKEN = dataclasses.field()
    mapper: T.Union[T_TOKEN, T.Dict[str, T_TOKEN]] = dataclasses.field()
    default: T_TOKEN = dataclasses.field(default=None)

    def evaluate(self, data: T_DATA) -> str:
        """
        todo: add docstring
        """
        # mapper = self._evaluate_mapper(data)
        return evaluate_token(self.mapper, data).get(
            evaluate_token(self.key, data),
            evaluate_token(self.default, data),
        )


token_class_mapper = {
    TokenTypeEnum.raw.value: RawToken,
    TokenTypeEnum.jmespath.value: JmespathToken,
    TokenTypeEnum.sub.value: SubToken,
    TokenTypeEnum.join.value: JoinToken,
    TokenTypeEnum.split.value: SplitToken,
    TokenTypeEnum.map.value: MapToken,
}


def evaluate_token(
    token: T.Any,
    data: T_DATA,
) -> T.Any:
    """
    自动判断 token 是什么类型, 应该用什么策略来 evaluate.

    **如果 Token 是一个字符串**

    那么有两种情况:

    1. 字符串以 ``$`` 开头, 表示这是一个 jmespath 语法, 那么自动将其作为
        ``JmespathToken(path=token)`` 来 evaluate 数据.
    2. 字符串中包含 Python 中的 string template 语法, 类似 ``{key}`` 这种, 则表示这是
        一个 string template, 而 data 就作为参数传给这个 string template, 使用
        ``token.format(**data)`` 来 evaluate 数据. 值得注意的是, 如果这个 token 中
        不包含 string template 语法, ``token.format(**data)`` 也不会失败, 只不过没有
        任何效果, 只是将这个 string 原样返回而已.

    **如果 Token 是一个字典**

    情况 1, 这就是一个普通的字典, 不过字典中的 value 可能也是一个 token, 那么就遍历它的值尝试
    进行 evaluate 即可.

    情况 2, 这是一个代表着复杂 token 对象的 字典. 那么这个字典就是一个用于创建 Token 对象的数据.
    这个字典必定包含 ``type`` 和 ``kwargs`` 字段. 这里我们会检查 ``type`` 字段的值, 如果不是
    任何一个 :class:`~jmespath_token.constants.TokenTypeEnum` 中的一个, 则会按照情况 1 处理.

    - ``type`` 字段代表这个 token 的类型, 它的值必须是
    :class:`~jmespath_token.constants.TokenTypeEnum` 中所定义的. 每一个 Type
        都对应着此模块下定义的一个 Token 类. 例如 :class:`SubToken``, :class:`JoinToken``
    - ``kwargs`` 字典代表了创建 Token 类所用到的参数. 例如 :class:`SubToken`` 的参数是
        ``{"template": "my_string_template", "params": {"key": "value"}}``.

    例如下面这个就是一个 :class:`SubToken` 的例子::

        {
            "type": "Token::Sub",
            "kwargs": {
                "template": "arn:aws:s3:::{bucket}",
                "params": {
                    "bucket": "$Name"
                }
            }
        }

    **如果 Token 是一个 collection 容器**

    例如它是一个列表, 那么就遍历它的每一个元素, 尝试进行 evaluate 即可.

    **如果 Token 既不是字符串也不是字典也不是 collection**

    那么就视其为 literal, 直接返回.
    这里注意的是如果想要返回的值是一个字典或是列表, 但你希望它是一个 literal, 并不希望杯 evaluate,
     那么, 你需要用 ``RawToken`` 的语法显式的指定它是一个 Raw, 例如
     ``{"type": "raw", "kwargs": {"value": my_dictionary_here}}``.

     .. versionadded:: 0.1.1
    """
    if isinstance(token, str):
        if token.startswith("$"):
            return JmespathToken(path=token).evaluate(data)
        else:  # literal
            return token
    elif isinstance(token, list):
        return [evaluate_token(item, data) for item in token]
    elif isinstance(token, dict):
        if TokenTypeEnum.is_valid_value(token.get(TYPE, "UNKNOWN")):
            token_type = token[TYPE]
            token_class = token_class_mapper[token_type]
            return token_class(**token["kwargs"]).evaluate(data)
        else:
            return {key: evaluate_token(value, data) for key, value in token.items()}
    else:  # literal
        return token
