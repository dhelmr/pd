#!/bin/env python3

import argparse
import pandas
import sys
from io import StringIO
    

parser = argparse.ArgumentParser()
parser.add_argument("--query", "-q", help="Pandas query")
parser.add_argument("--input", "-i", help="Input file")
parser.add_argument("--output", "-o", default=None, help="Output file, if not set the output is printed to stdout")
parser.add_argument("--pretty", "-p", action="store_true")
parser.add_argument("--transpose", "-t", action="store_true")
parser.add_argument("--sort", "-s", nargs="+", help="Sort by column(s)")
parser.add_argument("--descending", help="Sort descending", action="store_true")
parser.add_argument("--drop", help="Drop column(s)", nargs="+")
parser.add_argument("--with-index", action="store_true", help="Specify for outputing the index column")
parser.add_argument("--latex", action="store_true", help="Output latex table")
parser.add_argument("--float-format", type=str, default="%.4f", help="Specify the float format in the output, e.g. '%%.4f'")
parser.add_argument("--move", nargs="+", help="Moves column X right before after column Y; format: 'X::Y'", default=None)
parser.add_argument("--rename", nargs="+", help="Renames columns, format: 'old name::new name'")
parser.add_argument("--sep", default=",", help="Column seperator")
parser.add_argument("--latex-max-bold", nargs="+", help="Marks the maximum value of each column in the latex output bold.", type=str, default=None)
parsed = parser.parse_args()

if parsed.input is None:
    text = ""
    for line in sys.stdin:
        text += line
    input_res = StringIO(text)

else:
    input_res = parsed.input

df = pandas.read_csv(input_res, index_col=False, sep=parsed.sep)

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
    


if parsed.transpose:
    df = df.T

if parsed.output is None:
    if parsed.pretty:
        print(df.to_string())
        exit(0)
    else:
        out_res = sys.stdout
 
else:
    out_res = parsed.output

out_method = df.to_csv


if parsed.latex:
    formatters_fns = {}
    if parsed.latex_max_bold is not None:
        frmt_cell = lambda x: parsed.float_format % x if isinstance(x, float) else str(x)
        def make_max_formatter(max_value):
            return lambda x: "\ŧextbf{%s}" % frmt_cell(x) if x == max_value else frmt_cell(x)
        for col in parsed.latex_max_bold:
            if col not in df.columns:
                raise ValueError("Column %s not found" % col)
            max_col_value = df[col].max()
            formatters_fns[col] = make_max_formatter(max_col_value)
        formatters = [formatters_fns[col] if col in formatters_fns else None for col in df.columns]
    else:
        formatters = None
    out_method=lambda *args, **kwargs: df.to_latex(*args, formatters=formatters, escape=False, **kwargs)
out_method(out_res, index= parsed.with_index, float_format=parsed.float_format)
