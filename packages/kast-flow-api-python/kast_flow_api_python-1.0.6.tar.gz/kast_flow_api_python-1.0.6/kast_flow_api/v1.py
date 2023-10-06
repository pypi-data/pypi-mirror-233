import time
from dataclasses import MISSING, asdict, dataclass, field, fields
from enum import StrEnum
from functools import wraps
from typing import Any, Callable, Iterable, Protocol, Self, Tuple, Type, TypeVar, cast

from dacite import Config, from_dict


class KastSchemaFileName:
    @staticmethod
    def batch(schemaRegistry_path: str, topics: str) -> str:
        return f"{schemaRegistry_path}/{topics}.avsc"

    @staticmethod
    def stream(schemaRegistry_path: str, topics: str) -> str:
        return f"{schemaRegistry_path}_{topics}.avsc"


class KastFormat(StrEnum):
    AVRO = "avro"
    JSON = "json"
    CSV = "csv"
    PARQUET = "parquet"

    @staticmethod
    def unmarshal(format: str) -> "KastFormat":
        try:
            return KastFormat(format)
        except ValueError as e:
            raise KastFunctionInvalidArgumentsError(
                message=[
                    ["KastFormat", f"shoud be one of {list(map(str, KastFormat))}"],
                ],
                errors=e,
            )


T = TypeVar("T")


def kast_unmarshal(clazz: T) -> T:
    """decorator to unmarshal class as KastNode"""
    # Type ignore is necessary due to typechecker not supporting alias of dataclass
    # see: https://github.com/python/mypy/issues/9875
    #
    return dataclass(clazz, frozen=True, slots=True, kw_only=True, eq=True)  # type: ignore


class KastDataFrame(Protocol):
    @property
    def parents_id(self: Self) -> list[str]:
        ...

    @property
    def id(self: Self) -> str:
        ...

    @property
    def schema(self: Self) -> Any:
        ...

    @property
    def avro_schema(self: Self) -> str:
        ...

    @property
    def engine(self: Self) -> Any:
        ...

    @classmethod
    def read(
        cls: Type[Self], id: str, format: str, path: str, schema: str, **kwargs: Any
    ) -> "KastDataFrame":
        ...

    @classmethod
    def from_dataframe(
        cls: Type[Self], df: Any, id: str, parents: list[str] = []
    ) -> "KastDataFrame":
        ...

    @classmethod
    def create_dataframe(
        cls: Type[Self], df: Any, id: str, schema: str
    ) -> "KastDataFrame":
        ...

    def write(self: Self, format: str, topics: str, mode: str, **kwargs: Any) -> None:
        ...

    @classmethod
    def empty_dataframe(cls: Type[Self], id: str) -> "KastDataFrame":
        ...

    def create_or_replace_tempview(self: Self, name: str = "") -> "KastDataFrame":
        ...

    def map(self: Self, fn: Any, schema: str | dict[str, Any]) -> "KastDataFrame":
        ...

    def show(
        self: Self,
        lines: int = 20,
        truncate: bool = False,
        vertical: bool = False,
    ) -> None:
        ...

    def show_schema(self: Self, engine_schema: bool = False) -> None:
        ...

    def sql(self: Self, query: str) -> "KastDataFrame":
        ...

    def table_sql(self: Self, query: str) -> None:
        ...

    def checkpoint(self: Self) -> "KastDataFrame":
        ...


@dataclass(frozen=True, slots=True, kw_only=True, eq=True)
class SideOutValue:
    out: str
    schema: str


KastNodeList = Tuple["KastNode", ...]
KastOuts = Tuple[str, ...]
SideOutKey = str
SideOut = dict[SideOutKey, SideOutValue]


def make_side_out() -> SideOut:
    return cast(SideOut, dict[SideOutKey, SideOutValue])


def make_outs() -> KastOuts:
    return field(default_factory=lambda: cast(KastOuts, tuple()))


KAST_MISSING = MISSING


def kast_field(
    *,
    default=KAST_MISSING,
    default_factory=KAST_MISSING,
    init=True,
    repr=True,
    hash=None,
    compare=True,
    metadata=None,
    kw_only=KAST_MISSING,
):
    """Kast-flow version of dataclass's `field()` (just using real `field()` for now
    but making this interface will allow to change implementation without the
    need to change imports in udf and custom nodes )"""
    return field(
        default=default,
        default_factory=default_factory,
        init=init,
        repr=repr,
        hash=hash,
        compare=compare,
        metadata=metadata,
        kw_only=kw_only,
    )


@dataclass(frozen=True, slots=True, kw_only=True, eq=True)
class KastTable:
    sql: str
    type: str = "table"


class KastTool(Protocol):
    def new_kast_dataframe(
        self: Self,
        df: Any,
        schema: str = "",
    ) -> KastDataFrame:
        ...

    def empty_kast_dataframe(self: Self) -> KastDataFrame:
        ...


@dataclass(frozen=True, slots=True, kw_only=True, eq=True)
class KastFunction(Protocol):
    id: str
    registerSchema: bool = False
    checkpoint: bool = False
    outs: KastOuts = field(default_factory=make_outs)

    def compute(
        self: Self,
        tool: KastTool,
        tables: list[KastDataFrame],
    ) -> KastDataFrame:
        ...


@dataclass(frozen=True, slots=True, kw_only=True, eq=True)
class Internal:
    modules: set[str]


def make_internal() -> Internal:
    """load python module files
    By default, load __name__
    """
    return Internal(modules={__name__})


@dataclass(frozen=True, slots=True, kw_only=True, eq=True)
class PredefinedAttributesMixin:
    id: str
    type: str
    name: str = ""
    schema: str = ""
    sideOut: SideOut = field(default_factory=make_side_out)
    out: KastOuts = make_outs()
    settings: dict[str, Any] = field(default_factory=dict)
    internal: Internal = field(default_factory=make_internal)

    def clazz_settings_name(self: Self) -> str:
        names: list[str] = self.type.split("-")
        return "".join([word.capitalize() for word in names])


class KastNode(PredefinedAttributesMixin):
    def __init__(self: Self, **kwargs: Any) -> None:
        return super().__init__(**kwargs)

    @property
    def fn(self: Self) -> KastFunction:
        target: str = self.clazz_settings_name()
        modules: set[str] = self.internal.modules
        import importlib

        for mod in modules:
            try:
                clazz = getattr(importlib.import_module(mod), target)
                compute: KastFunction = clazz(
                    **self.settings, outs=self.out, id=self.id
                )
                return from_dict(  # type: ignore
                    data_class=clazz,
                    data=asdict(compute),
                    config=Config(check_types=True),
                )
            except AttributeError:
                continue
            except Exception as e:
                raise KastFunctionInvalidArgumentsError(
                    message=[
                        ["Origin", str(e)],
                        ["Function", mod],
                        ["ID", self.id],
                    ],
                    errors=e,
                )
        raise KastNodeNotFoundError(
            message=[
                ["Origin", f"{target} is an unknown function implementation"],
                ["ID", self.id],
            ],
            errors=None,
        )

    @classmethod
    def from_dict(cls: Type[Self], modules: set[str], **kwargs: dict[str, Any]) -> Self:
        clazz_attrs = {f.name for f in fields(cls)}
        known_fields: dict[str, Any] = {
            k: v for k, v in kwargs.items() if k in clazz_attrs
        }
        known_fields["out"] = tuple(known_fields.get("out", tuple()))
        unknown_fields: dict[str, Any] = {
            **{k: v for k, v in kwargs.items() if k not in clazz_attrs},
        }
        unknown_fields["schema"] = known_fields.get("schema", "")
        return cls(
            **{
                **known_fields,
                "settings": unknown_fields,
                "internal": Internal(modules=modules),
            }
        )


Fn = TypeVar("Fn", bound=Callable[..., Any])


def timeit(wrapped_func: Fn) -> Fn:
    @wraps(wrapped_func)
    def duration(*args: list[Any], **kwargs: dict[str, Any]) -> Any:
        start_time = time.perf_counter()
        result = wrapped_func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time

        print(
            f"Function {wrapped_func.__name__}{args} {kwargs} Took {total_time:.4f} seconds to compute"
        )
        return result

    return cast(Fn, duration)


class KastManifest:
    __nodes: KastNodeList

    def __init__(self: Self, nodes: KastNodeList) -> None:
        self.__nodes = nodes

    def deser(self: Self, *add_modules: str) -> KastNodeList:
        nodes_raw: list[KastNode] = []
        for node in self.__nodes:
            node_dict: dict[str, Any] = cast(dict[str, Any], node)
            nodes_raw.append(
                KastNode.from_dict(
                    modules={__name__, *add_modules},
                    **node_dict,
                )
            )
        return cast(KastNodeList, nodes_raw)


class KastBaseError(Exception):
    """base error for errors requiring better feedback"""

    def __init__(
        self: Self,
        errors: Any = None,
        message: list[list[str]] = [],
        message_maxcolwidths: Iterable[int | None] = None,
        before: str = "",
        after: str = "",
    ) -> None:
        super().__init__(message)
        self.errors = errors
        self._message = message
        self._before = before
        self._after = after
        self._message_maxcolwidths = message_maxcolwidths

    def __str__(self: Self) -> str:
        from tabulate import tabulate

        return f"\n\n{self._before}\n{tabulate(tabular_data=self._message, tablefmt='grid', maxcolwidths=self._message_maxcolwidths)}\n{self._after}\n"


class KastNodeNotFoundError(KastBaseError):
    "When node is missing from the dag, this error is raised"


class KastUnsupportedDAGOperationError(KastBaseError):
    "when unsupported operation happens on the graph dag pub/sub, this error is raised"


class KastFunctionInvalidArgumentsError(KastBaseError):
    """when required, unknown or invalid arguments are passed as arguments to a function,
    this error is raised"""


class KastConfigDeserializationError(KastBaseError):
    "When invalid configuration file is passed, this error is raised"


class KastInvalidDataFrameBackendError(KastBaseError):
    "When invalid backend is requested, this error is raised"
