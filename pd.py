#!/bin/env python3

import argparse
import pandas
import numpy as np
import sys
from io import StringIO
from enum import Enum

from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) 

class OutputFormats(Enum):
    CSV = "csv"
    LATEX = "latex"
    JSON = "json"
    HTML = "html"
    PARQUET = "pq"

class InputFormats(Enum):
    CSV = "csv"
    JSON = "json"
    PARQUET = "pq"

ALLOWED_JSON_ORIENTS = ["split", "records", "index", "columns", "values", "table"]

parser = argparse.ArgumentParser()
parser.add_argument("--query", "-q", help="Pandas query")
parser.add_argument("--input", "-i", help="Input file")
parser.add_argument("--output", "-o", default=None, help="Output file, if not set the output is printed to stdout")
parser.add_argument("--pretty", "-p", action="store_true")
parser.add_argument("--pretty-short", "-pp", action="store_true")
parser.add_argument("--transpose", "-t", action="store_true")
parser.add_argument("--sort", "-s", nargs="+", help="Sort by column(s)")
parser.add_argument("--descending", help="Sort descending", action="store_true")
parser.add_argument("--drop", help="Drop column(s)", nargs="+")
parser.add_argument("--with-index", action="store_true", help="Specify for outputing the index column")
parser.add_argument("--to", help="Specify the output format. Choose from: %s" % [v.value for v in OutputFormats], type= lambda x: OutputFormats(x), default=OutputFormats.CSV)
parser.add_argument("--from", dest="from_format", help="Specify the input format. Choose from: %s" % [v.value for v in InputFormats], type=lambda x: InputFormats(x), default=InputFormats.CSV)
parser.add_argument("--float-format", type=str, default="%.4f", help="Specify the float format in the output, e.g. '%%.4f'")
parser.add_argument("--move", nargs="+", help="Moves column X right before after column Y; format: 'X::Y'", default=None)
parser.add_argument("--rename", nargs="+", help="Renames columns, format: 'old name::new name'")
parser.add_argument("--sep", default=",", help="Column seperator")
parser.add_argument("--latex-max-bold", nargs="+", help="Marks the maximum value of each column in the latex output bold.", type=str, default=None)

parser.add_argument("--replace-nan", help="Replace all NaN values with another value", type=float)
parser.add_argument("--json-out-orient", help="Specifies the json input orient. Choose one of %s. See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.to_json.html?highlight=to_json#pandas.Series.to_json" % ALLOWED_JSON_ORIENTS, default="records", choices=ALLOWED_JSON_ORIENTS)
parser.add_argument("--json-in-orient", help="Specifies the json output orient. Choose one of %s. See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.to_json.html?highlight=to_json#pandas.Series.to_json" % ALLOWED_JSON_ORIENTS, default="records", choices=ALLOWED_JSON_ORIENTS)
parser.add_argument("--only", nargs="+")
parser.add_argument("--columns", action="store_true", help="Prints the columns")
parser.add_argument("-n", "--nrows", action="store_true", help="Prints the number of rows")
parser.add_argument("--group-by", help="Groups by the specified column.", type=str)
parser.add_argument("--group-by-max", help="Determines the maximum column value of a group by.", type=str)
parser.add_argument("--unique", help="Prints unique values of the specified column.", type=str)
parser.add_argument("--gui", help="open pandas-gui", action="store_true")
parser.add_argument("--corr", action="store_true" )
parsed = parser.parse_args()

if parsed.group_by_max is None and parsed.group_by is not None:
    raise ValueError("--group-by and --group-by-max must be specified together.")

if parsed.input is None:
    text = ""
    for line in sys.stdin:
        text += line
    input_res = StringIO(text)

else:
    input_res = parsed.input

if parsed.from_format == InputFormats.CSV:
    df = pandas.read_csv(input_res, index_col=False, sep=parsed.sep)
elif parsed.from_format == InputFormats.JSON:
    df = pandas.read_json(input_res, orient=parsed.json_in_orient)
elif parsed.from_format == InputFormats.PARQUET:
    df = pandas.read_parquet(input_res)

if parsed.replace_nan is not None:
   df = df.replace(np.nan, parsed.replace_nan)

if parsed.query is not None:
    df = df.query(parsed.query)

if parsed.sort is not None:
    df = df.sort_values(by=parsed.sort, ascending=(not parsed.descending))

if parsed.drop is not None:
    df = df.drop(columns=parsed.drop)

if parsed.rename is not None:
    if type(parsed.rename) is not list:
        parsed.rename = [parsed.rename]

    renames = {}
    for operation in parsed.rename:
        old, new = operation.split("::")
        renames[old] = new
    df = df.rename(columns=renames)

if parsed.move is not None:
    columns = list(df.columns)
    if type(parsed.move) is not list:
        parsed.move = [parsed.move]
    for operation in parsed.move:
        X,Y = operation.split("::")
        columns.insert(columns.index(Y), columns.pop(columns.index(X)))
    df = df.reindex(columns = columns)

if parsed.group_by is not None:
    gb = df.groupby(parsed.group_by)
    max_values = gb[parsed.group_by_max].agg('max').reset_index()
    df = pandas.merge(df, max_values, how='left', on=parsed.group_by, suffixes=("","_y"))
    df = df[df[parsed.group_by_max] == df[parsed.group_by_max+"_y"]]
    df.drop(columns=[parsed.group_by_max+"_y"], inplace=True)


if parsed.transpose:
    df = df.T

if parsed.columns:
    for col in df.columns:
        print(col)
    exit(0)

if parsed.unique:
    unique_values = df[parsed.unique].unique()
    for val in unique_values:
        print(val)
    exit(0)

if parsed.nrows:
    print(len(df))
    exit(0)

if parsed.only is not None:
    df = df[parsed.only]

if parsed.corr:
    df = df.corr()

if parsed.gui:
    from pandasgui import show
    show(df)
    exit(0)

if parsed.output is None:
    if parsed.pretty:
        print(df.to_string())
        exit(0)
    elif parsed.pretty_short:
        print(df)
        exit(0)
    else:
        out_res = sys.stdout
 
else:
    out_res = parsed.output

def escape_latex(text: str) -> str:
    return text.replace("_", "\\_")

def wrap_latex_output(df, out_res, *args, replaces: dict, **kwargs):
    text = df.to_latex(*args, **kwargs)
    if replaces is not None:
        for key, value in replaces.items():
            text = text.replace(key, value)
    if type(out_res) is str:
        with open(out_res, "w") as f:
            f.write(text)
    else:
        out_res.write(text)

if parsed.to == OutputFormats.LATEX:
    formatters_fns = {}
    if parsed.latex_max_bold is not None:
        replace_str_start = "QQA"
        replace_str_end = "QQB"
        frmt_cell = lambda x: parsed.float_format % x if isinstance(x, float) else str(x)
        def make_max_formatter(max_value):
            return lambda x: "%s%s%s" % (replace_str_start,frmt_cell(x), replace_str_end) if x == max_value else frmt_cell(x)
        for col in parsed.latex_max_bold:
            if col not in df.columns:
                raise ValueError("Column %s not found" % col)
            max_col_value = df[col].max()
            formatters_fns[col] = make_max_formatter(max_col_value)
        formatters = [formatters_fns[col] if col in formatters_fns else frmt_cell for col in df.columns]
        replaces = {
            replace_str_start: "\\textbf{",
            replace_str_end: "}"
        }
    else:
        formatters = None
        replaces = None
    out_method= lambda *args, **kwargs: wrap_latex_output(df, *args, formatters=formatters, replaces=replaces, float_format=parsed.float_format, index= parsed.with_index, **kwargs)
elif parsed.to == OutputFormats.JSON:
    out_method = lambda *args, **kwargs: df.to_json(*args, orient=parsed.json_out_orient)
elif parsed.to == OutputFormats.HTML:
     out_method = lambda *args, **kwargs: df.to_html(*args, float_format=parsed.float_format, index= parsed.with_index, **kwargs)
elif parsed.to == OutputFormats.CSV:
    out_method = lambda *args, **kwargs: df.to_csv(*args, float_format=parsed.float_format, index= parsed.with_index, **kwargs)
elif parsed.to == OutputFormats.PARQUET:
    out_method = lambda *args, **kwargs: df.to_parquet(*args, compression="gzip", float_format=parsed.float_format, index= parsed.with_index, **kwargs)
else:
    raise RuntimeError("Unexpected output format: %s" % parsed.to)
out_method(out_res)
