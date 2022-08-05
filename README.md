# pd: Command-line Interface to [Pandas](https://pandas.pydata.org/) for dealing with tabular data

This is a little python tool to quickly handle tabular data in the command line, like: 

```sh
cat example.csv | pd -q "x > 30" --sort z > output.csv
```

It supports [pandas queries](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html), some basic column manipulation (renaming/reordering/...), different input and output formats (csv, json, latex, html) and sorting.

This tool should not be considered stable or complete in any kind yet and will likely be inefficient when dealing with very large csv files. It is rather meant for dealing with small and medium-sized tabular data on the command line or in scripts (e.g. quickly converting a csv to a latex table or sorting and filtering values).

## Installation

Requires python >= 3.6 and pip. Clone the git repo and install the requirements with `pip install --user -r requirements.txt`. 

Run `pd` with `./pd.py`. Below it is assumed that `pd` is an executable which links to the script.

TODO: proper installation setup with pip

## Examples

#### Read a table from json, sort records by a column and store as json 

```sh
pd --from json -i example.json --sort z --to json > sorted_by_z.json
```

#### convert a csv to a latex table and highlight the maximum number of some columns ('x' and 'z' here):

```sh
pd --from csv -i example.csv --to latex --latex-max-bold x z -o examples.tex
```

#### list columns of a csv

```
pd -i example.csv --columns
```

#### rename column:

```
pd -i example.csv --rename y::new_column_name > output.csv
```

#### Filter columns and print as a nice table 

```
pd -i example.csv --only x y --pretty
```

## Help

All CLI arguments:

```
usage: pd [-h] [--query QUERY] [--input INPUT] [--output OUTPUT] [--pretty]
          [--pretty-short] [--transpose] [--sort SORT [SORT ...]]
          [--descending] [--drop DROP [DROP ...]] [--with-index] [--to TO]
          [--from FROM_FORMAT] [--float-format FLOAT_FORMAT]
          [--move MOVE [MOVE ...]] [--rename RENAME [RENAME ...]] [--sep SEP]
          [--latex-max-bold LATEX_MAX_BOLD [LATEX_MAX_BOLD ...]]
          [--replace-nan REPLACE_NAN]
          [--json-out-orient {split,records,index,columns,values,table}]
          [--json-in-orient {split,records,index,columns,values,table}]
          [--only ONLY [ONLY ...]] [--columns] [-n] [--group-by GROUP_BY]
          [--group-by-max GROUP_BY_MAX] [--unique UNIQUE]

options:
  -h, --help            show this help message and exit
  --query QUERY, -q QUERY
                        Pandas query
  --input INPUT, -i INPUT
                        Input file
  --output OUTPUT, -o OUTPUT
                        Output file, if not set the output is printed to
                        stdout
  --pretty, -p
  --pretty-short, -pp
  --transpose, -t
  --sort SORT [SORT ...], -s SORT [SORT ...]
                        Sort by column(s)
  --descending          Sort descending
  --drop DROP [DROP ...]
                        Drop column(s)
  --with-index          Specify for outputing the index column
  --to TO               Specify the output format. Choose from: ['csv',
                        'latex', 'json', 'html']
  --from FROM_FORMAT    Specify the input format. Choose from: ['csv', 'json']
  --float-format FLOAT_FORMAT
                        Specify the float format in the output, e.g. '%.4f'
  --move MOVE [MOVE ...]
                        Moves column X right before after column Y; format:
                        'X::Y'
  --rename RENAME [RENAME ...]
                        Renames columns, format: 'old name::new name'
  --sep SEP             Column seperator
  --latex-max-bold LATEX_MAX_BOLD [LATEX_MAX_BOLD ...]
                        Marks the maximum value of each column in the latex
                        output bold.
  --replace-nan REPLACE_NAN
                        Replace all NaN values with another value
  --json-out-orient {split,records,index,columns,values,table}
                        Specifies the json input orient. Choose one of
                        ['split', 'records', 'index', 'columns', 'values',
                        'table']. See https://pandas.pydata.org/pandas-docs/st
                        able/reference/api/pandas.Series.to_json.html?highligh
                        t=to_json#pandas.Series.to_json
  --json-in-orient {split,records,index,columns,values,table}
                        Specifies the json output orient. Choose one of
                        ['split', 'records', 'index', 'columns', 'values',
                        'table']. See https://pandas.pydata.org/pandas-docs/st
                        able/reference/api/pandas.Series.to_json.html?highligh
                        t=to_json#pandas.Series.to_json
  --only ONLY [ONLY ...]
  --columns             Prints the columns
  -n, --nrows           Prints the number of rows
  --group-by GROUP_BY   Groups by the specified column.
  --group-by-max GROUP_BY_MAX
                        Determines the maximum column value of a group by.
  --unique UNIQUE       Prints unique values of the specified column.

```

## License

[Licensed under GPLv3](LICENSE.txt).
