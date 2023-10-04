from __future__ import annotations

import logging
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Optional

import pandas as pd
from atoti_core import (
    HTML_MIME_TYPE as _HTML_MIME_TYPE,
    TEXT_MIME_TYPE as _TEXT_MIME_TYPE,
    Context,
)
from typing_extensions import override

from ._widget_conversion_details import (
    CONVERT_QUERY_RESULT_TO_WIDGET_MIME_TYPE as _CONVERT_QUERY_RESULT_TO_WIDGET_MIME_TYPE,
    WidgetConversionDetails,
)

if TYPE_CHECKING:
    # This requires pandas' optional dependency jinja2.
    from pandas.io.formats.style import Styler  # pylint: disable=nested-import


class QueryResult(pd.DataFrame):
    """pandas DataFrame corresponding to the result of a query ran in ``"pretty"`` *mode*.

    It is indexed by the queried levels (date levels become :class:`pandas.DatetimeIndex`).

    .. note::
        Unless mutated in place, the ``__repr__()``, ``_repr_html_()``, ``_repr_latex_()``, and ``_repr_mimebundle_()`` methods will use:

        * The caption of levels and members instead of their name.
        * The formatted value of measures instead of their value.
    """

    # See https://pandas.pydata.org/pandas-docs/stable/development/extending.html#define-original-properties
    _internal_names = [  # noqa: RUF012
        *pd.DataFrame._internal_names,  # type: ignore[attr-defined] # pyright: ignore[reportGeneralTypeIssues]
        "_atoti_context",
        "_atoti_formatted_values",
        "_atoti_get_styler",
        "_atoti_has_been_mutated",
        "_atoti_initial_dataframe",
        "_atoti_widget_conversion_details",
    ]
    _internal_names_set = set(_internal_names)  # noqa: RUF012

    def __init__(
        self,
        # pandas does not expose the types of these arguments.
        data: Any = None,
        index: Any = None,
        *,
        context: Optional[Context] = None,
        formatted_values: pd.DataFrame,
        get_styler: Callable[[], Styler],
    ):
        # `pandas-stub` declares a `__new__` but `pandas` actually have an `__init__`.
        super().__init__(data, index)  # type: ignore[call-arg] # pyright: ignore[reportGeneralTypeIssues]

        self._atoti_context = context
        self._atoti_formatted_values = formatted_values
        self._atoti_get_styler = get_styler
        self._atoti_has_been_mutated = False
        self._atoti_initial_dataframe: pd.DataFrame = self.copy(deep=True)
        self._atoti_widget_conversion_details: Optional[WidgetConversionDetails] = None

    # The conversion to an Atoti widget and the styling are based on the fact that this dataframe represents the original result of the MDX query.
    # If the dataframe was mutated, these features should be disabled to prevent them from being incorrect.
    def _has_been_mutated(self) -> bool:
        if not self._atoti_has_been_mutated and not self.equals(
            self._atoti_initial_dataframe
        ):
            self._atoti_has_been_mutated = True

            logging.getLogger("atoti.query").warning(
                "The query result has been mutated: captions, formatted values, and styling will not be shown."
            )

        return self._atoti_has_been_mutated

    @property
    @override
    def style(self) -> Styler:
        """Return a styler following the style included in the CellSet from which the DataFrame was converted (if it has not been mutated)."""
        return super().style if self._has_been_mutated() else self._atoti_get_styler()

    def _get_dataframe_to_repr(self, *, has_been_mutated: bool) -> pd.DataFrame:
        return (
            self._atoti_initial_dataframe
            if has_been_mutated
            else self._atoti_formatted_values
        )

    def _atoti_repr(self, *, has_been_mutated: bool) -> str:
        return repr(self._get_dataframe_to_repr(has_been_mutated=has_been_mutated))

    @override
    def __repr__(self) -> str:
        return self._atoti_repr(has_been_mutated=self._has_been_mutated())

    def _atoti_repr_html(self, *, has_been_mutated: bool) -> str:
        dataframe_to_repr = self._get_dataframe_to_repr(
            has_been_mutated=has_been_mutated
        )
        # `pandas-stubs` lacks the `_repr_html_` method.
        html: str = dataframe_to_repr._repr_html_()  # type: ignore[operator] # pyright: ignore[reportGeneralTypeIssues]
        return html

    def _repr_html_(self) -> str:
        return self._atoti_repr_html(has_been_mutated=self._has_been_mutated())

    def _atoti_repr_latex(self, *, has_been_mutated: bool) -> str:
        dataframe_to_repr = self._get_dataframe_to_repr(
            has_been_mutated=has_been_mutated
        )
        # `pandas-stubs` lacks the `_repr_latex_` method.
        latex: str = dataframe_to_repr._repr_latex_()  # type: ignore[operator] # pyright: ignore[reportGeneralTypeIssues]
        return latex

    def _repr_latex_(self) -> str:
        return self._atoti_repr_latex(has_been_mutated=self._has_been_mutated())

    def _repr_mimebundle_(
        self,
        include: object,  # noqa: ARG002
        exclude: object,  # noqa: ARG002
    ) -> dict[str, object]:
        has_been_mutated = self._has_been_mutated()

        mimebundle: dict[str, object] = {
            _HTML_MIME_TYPE: self._atoti_repr_html(has_been_mutated=has_been_mutated),
            _TEXT_MIME_TYPE: self._atoti_repr(has_been_mutated=has_been_mutated),
        }

        if self._atoti_widget_conversion_details and not self._has_been_mutated():
            mimebundle[_CONVERT_QUERY_RESULT_TO_WIDGET_MIME_TYPE] = {
                "mdx": self._atoti_widget_conversion_details.mdx,
                "sessionId": self._atoti_widget_conversion_details.session_id,
                "widgetCreationCode": self._atoti_widget_conversion_details.widget_creation_code,
            }

        return mimebundle
