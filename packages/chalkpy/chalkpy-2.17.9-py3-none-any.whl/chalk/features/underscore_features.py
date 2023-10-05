import warnings
from typing import Any, Dict, Tuple, Union

from chalk.features.feature_field import Feature
from chalk.features.feature_wrapper import FeatureWrapper
from chalk.features.filter import Filter
from chalk.features.underscore import (
    Underscore,
    UnderscoreAttr,
    UnderscoreBinaryOp,
    UnderscoreCall,
    UnderscoreItem,
    UnderscoreRoot,
    UnderscoreUnaryOp,
)
from chalk.utils.collections import ensure_tuple


def parse_underscore_df_item(exp: Underscore, columns: Dict[Tuple[str, ...], Union[Feature, str]]) -> Any:
    """
    Parse a (potentially underscore) expression passed through as a filter/projection for
    a dataframe, matching underscores based on the available set of columns.
    """
    return _parse_underscore_df_item(
        exp=exp,
        # Transform columns to be immutable
        columns=tuple(item for item in columns.items()),
    )


def _parse_underscore_df_item(exp: Any, columns: Tuple[Tuple[Tuple[str, ...], Union[Feature, str]], ...]) -> Any:
    # Features of the dataframe are to be written as a dictionary of the fqn split up mapped to
    # the original features. The dictionary is represented immutably here.
    if not isinstance(exp, Underscore):
        # Recursive call hit non-underscore, deal with later
        return exp

    elif len(columns) == 0:
        # No more columns implies a mismatching underscore
        return ValueError(f"No matches in DataFrame {exp}")

    elif isinstance(exp, UnderscoreRoot):
        # Could be any of the remaining possible columns: if there are multiple
        # columns, the behavior may be ambiguous
        if len(columns) > 1:
            warnings.warn(
                UserWarning(
                    f"Ambiguous underscore in DataFrame call '{exp}'. Any of the columns {columns} could be chosen."
                )
            )
        return columns[0][1]

    elif isinstance(exp, UnderscoreAttr):
        attr = exp._chalk__attr
        # Remove the context for the attribute from each matching column
        new_columns = tuple((fqn_tuple[:-1], feature) for (fqn_tuple, feature) in columns if fqn_tuple[-1] == attr)
        if len(new_columns) == 0:
            raise AttributeError(
                f"Unmatched attribute '{attr}' in expression '{exp}'. This DataFrame contains the columns "
                f"{[c[1].root_fqn for c in columns]}"
            )
        return _parse_underscore_df_item(exp=exp._chalk__parent, columns=new_columns)

    elif isinstance(exp, UnderscoreItem):
        parent = _parse_underscore_df_item(exp=exp._chalk__parent, columns=columns)
        if isinstance(parent, Feature):
            parent_wrapper = FeatureWrapper(parent)
            parsed_annotation = parent_wrapper._chalk_feature.typ.parsed_annotation

            from chalk.features.dataframe import DataFrameMeta

            if isinstance(parsed_annotation, DataFrameMeta):
                column_list = parsed_annotation.columns
                feature_dict = {ensure_tuple(column.root_fqn.split(".")): column for column in column_list}
                return parent_wrapper[parse_underscore_df_item(exp._chalk__key, feature_dict)]
            raise TypeError(f"'{exp._chalk__parent}' in '{exp}' resolved to '{parent}', which is not a DataFrame")

        # How does one even key on a non-feature
        raise TypeError(f"Resolved underscore {parent} is of type {type(parent)} and not Feature")

    elif isinstance(exp, UnderscoreCall):
        raise NotImplementedError(
            f"Calls on underscores in DataFrames is currently unsupported. Found expression {exp}"
        )

    elif isinstance(exp, UnderscoreBinaryOp):
        return Filter(
            lhs=_parse_underscore_df_item(exp=exp._chalk__left, columns=columns),
            operation=exp._chalk__op,
            rhs=_parse_underscore_df_item(exp=exp._chalk__right, columns=columns),
        )

    elif isinstance(exp, UnderscoreUnaryOp):
        return Filter(
            lhs=_parse_underscore_df_item(exp=exp._chalk__operand, columns=columns),
            operation=exp._chalk__op,
            rhs=None,
        )

    raise NotImplementedError(f"Unrecognized underscore expression {exp}")
