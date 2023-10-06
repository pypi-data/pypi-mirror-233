"""
A simple tool for converting JSON to an HTML table.

This is based off of the `json2html` project, see:
https://github.com/latture/json2table/blob/master/json2table/json2table.py
"""

import html
import json
from typing import Optional, Union

Json = Union[dict[str, "Json"], list["Json"], int, float, str, None, bool]


def convert(
    json_input: Json, attributes_json_output: Optional[list[str]] = None, table_attributes=None
) -> str:
    """
    Convert JSON to HTML table format.

    Parameters
    ----------
    json_input : dict
        JSON object to convert into HTML.
    attributes_json_output : list[str]
        List of attributes to include in the JSON output.
    table_attributes : dict, optional
        Dictionary of ``(key, value)`` pairs describing attributes to add to the table.
        Each attribute is added according to the template ``key="value". For example,
        the table ``{ "border" : 1 }`` modifies the generated table tags to include
        ``border="1"`` as an attribute. The generated opening tag would look like
        ``<table border="1">``. Default is ``None``.

    Returns
    -------
    str
        String of converted HTML.

    An example usage is shown below:

    >>> json_object = {"key" : "value"}
    >>> table_attributes = {"border" : 1}
    >>> html = convert(json_object, build_direction=build_direction, table_attributes=table_attributes)
    >>> print(html)
    "<table border="1"><tr><th>key</th><td>value</td></tr></table>"

    """
    json_converter = JsonConverter(
        attributes_json_output=attributes_json_output, table_attributes=table_attributes
    )
    return json_converter.convert(json_input)


class JsonConverter:
    """
    Class that manages the conversion of a JSON object to a string of HTML.

    Methods
    -------
    convert(json_input)
        Converts JSON to HTML.
    """

    _attributes_json_output: list[str]
    """
    List of attributes to get a JSON rendering in the output.
    """

    _table_opening_tag: str
    """
    Opening tag for the table. (like '<table>')
    """

    def __init__(
        self,
        attributes_json_output: Optional[list[str]] = None,
        table_attributes: Optional[dict[str, str]] = None,
    ):
        """
        Initialize the converter.
        """
        self._attributes_json_output = attributes_json_output or []
        if table_attributes is not None and not isinstance(table_attributes, dict):
            raise TypeError("Table attributes must be either a `dict` or `None`.")

        self._table_opening_tag = f"<table{JsonConverter._dict_to_html_attributes(table_attributes)}>"

    def convert(self, json_input: Json) -> str:
        """
        Convert JSON to HTML Table format.

        Parameters
        ----------
        json_input : dict
            JSON object to convert into HTML.

        Returns
        -------
        str
            String of converted HTML.
        """

        if len(json_input) == 1:
            key = list(json_input.keys())[0]
            if key in self._attributes_json_output:
                return f"<b>{html.escape(key)}</b>: {html.escape(json.dumps(json_input[key]))}"
            elif not isinstance(json_input[key], list) and not isinstance(json_input[key], dict):
                return f"<b>{html.escape(key)}</b>: {html.escape(json_input[key])}"

        html_output = self._table_opening_tag
        for key, value in iter(json_input.items()):
            html_output += f"<tr><th>{self._markup(key):s}</th>"
            if key in self._attributes_json_output:
                html_output += f"<td>{html.escape(json.dumps(value))}</td>"
            else:
                if isinstance(value, list):
                    html_output += self._maybe_club(value)
                else:
                    html_output += self._markup_table_cell(value)
            html_output += "</tr>"
        html_output += "</table>"
        return html_output

    def _markup_table_cell(self, value: Json) -> str:
        """
        Wrap the generated HTML in table cell `<td></td>` tags.

        Parameters
        ----------
        value : object
            Object to place in the table cell.

        Returns
        -------
        str
            String of HTML wrapped in table cell tags.
        """
        return f"<td>{self._markup(value):s}</td>"

    def _markup_header_row(self, headers: list[str]) -> str:
        """
        Create a row of table header items.

        Parameters
        ----------
        headers : list
            List of column headers. Each will be wrapped in `<th></th>` tags.

        Returns
        -------
        str
            Table row of headers.
        """
        return "<tr><th>" + "</th><th>".join([html.escape(h) for h in headers]) + "</th></tr>"

    @staticmethod
    def _dict_to_html_attributes(d: Json) -> str:
        r"""
        Convert a dictionary to a string of ``key=\"value\"`` pairs.

        If ``None`` is provided as the dictionary an empty string is returned,
        i.e. no html attributes are generated.

        Parameters
        ----------
        d : dict
            Dictionary to convert to html attributes.

        Returns
        -------
        str
            String of HTML attributes in the form ``key_i=\"value_i\" ... key_N=\"value_N\"``,
            where ``N`` is the total number of ``(key, value)`` pairs.
        """
        if d is None:
            return ""

        return "".join(f' {html.escape(key)}="{html.escape(value)}"' for key, value in iter(d.items()))

    @staticmethod
    def _list_of_dicts_to_column_headers(list_of_dicts: list[dict[str:Json]]) -> Optional[list[str]]:
        """
        Detect if all entries in an list of ``dict``'s have identical keys.

        Returns the keys if all keys are the same and ``None`` otherwise.

        Parameters
        ----------
        list_of_dicts : list
            List of dictionaries to test for identical keys.

        Returns
        -------
        list or None
            List of column headers if all dictionary possessed the same keys. Returns ``None`` otherwise.
        """

        if len(list_of_dicts) < 2 or not all(isinstance(item, dict) for item in list_of_dicts):
            return None

        column_headers = list_of_dicts[0].keys()
        for d in list_of_dicts[1:]:
            if len(d.keys()) != len(column_headers) or not all(header in d for header in column_headers):
                return None
        return column_headers

    def _markup(self, entry: Json) -> str:
        """
        Recursively generates HTML for the current entry.

        Parameters
        ----------
        entry : object
            Object to convert to HTML. Maybe be a single entity or contain multiple and/or nested objects.

        Returns
        -------
        str
            String of HTML formatted json.
        """
        if entry is None:
            return ""
        if isinstance(entry, list):
            list_markup = "<ul>"
            for item in entry:
                list_markup += f"<li>{self._markup(item):s}</li>"
            list_markup += "</ul>"
            return list_markup
        if isinstance(entry, dict):
            return self.convert(entry)

        # default to stringifying entry
        return html.escape(f"{entry}")

    def _maybe_club(self, list_of_dicts: list[dict[str:Json]]) -> str:
        """
        Create optimized table if all keys in a list of dicts are identical.

        If all keys in a list of dicts are identical, values from each ``dict``
        are clubbed, i.e. inserted under a common column heading. If the keys
        are not identical ``None`` is returned, and the list should be converted
        to HTML per the normal ``convert`` function.

        Parameters
        ----------
        list_of_dicts : list
            List to attempt to club.

        Returns
        -------
        str or None
            String of HTML if list was successfully clubbed. Returns ``None`` otherwise.

        Example
        -------
        Given the following json object::

            {
                "sampleData": [
                    {"a":1, "b":2, "c":3},
                    {"a":5, "b":6, "c":7}]
            }


        Calling ``_maybe_club`` would result in the following HTML table:
        _____________________________
        |               |   |   |   |
        |               | a | c | b |
        |   sampleData  |---|---|---|
        |               | 1 | 3 | 2 |
        |               | 5 | 7 | 6 |
        -----------------------------

        Adapted from a contribution from @muellermichel to ``json2html``.
        """
        column_headers = JsonConverter._list_of_dicts_to_column_headers(list_of_dicts)
        if column_headers is None:
            # common headers not found, return normal markup
            html_output = self._markup(list_of_dicts)
        else:
            html_output = self._table_opening_tag
            html_output += self._markup_header_row(column_headers)
            for list_entry in list_of_dicts:
                html_output += "<tr><td>"
                html_output += "</td><td>".join(
                    self._markup(list_entry[column_header]) for column_header in column_headers
                )
                html_output += "</td></tr>"
            html_output += "</table>"

        return f"<td>{html_output}</td>"
