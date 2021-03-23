# Pandas for the command-line

Use pandas for querying csv files or tabular data in the command-line, like: 

```cat example.csv | pd -q "x > 30" --sort z```. 

It supports [pandas queries](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html), some basic column manipulation (renaming/reordering/...), different input and output formats and sorting.

## Installation

Clone the git repo and install the requirements with `pip install --user -r requirements.txt`.

## Examples

* Read a table from json, sort records by a column and store as json 

`pd --from json -i example.json --sort z --to json > sorted_by_z.json`

* convert a csv to a latex table and highlight the maximum number of some columns ('x' and 'z' here):

`pd --from csv -i example.csv --to latex --latex-max-bold x z -o examples.tex`

* list columns of a csv

`pd -i example.csv --columns`

* rename column:

`pd -i example.csv --rename y::new_column_name > output.csv`

## Help

All CLI arguments:

```
usage: pd [-h] [--query QUERY] [--input INPUT] [--output OUTPUT] [--pretty]
          [--pretty-short] [--transpose] [--sort SORT [SORT ...]]
          [--descending] [--drop DROP [DROP ...]] [--with-index] [--to TO]
          [--from FROM_FORMAT] [--float-format FLOAT_FORMAT]
          [--move MOVE [MOVE ...]] [--rename RENAME [RENAME ...]] [--sep SEP]
          [--latex-max-bold LATEX_MAX_BOLD [LATEX_MAX_BOLD ...]] [--columns]
          [--replace-nan REPLACE_NAN]
          [--json-out-orient {split,records,index,columns,values,table}]
          [--json-in-orient {split,records,index,columns,values,table}]

optional arguments:
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
  --columns
  --replace-nan REPLACE_NAN
                        Replace all NaN values with another value
  --json-out-orient {split,records,index,columns,values,table}
                        Specifies the json format. Choose one of ['split',
                        'records', 'index', 'columns', 'values', 'table']. See
                        https://pandas.pydata.org/pandas-docs/stable/reference
                        /api/pandas.Series.to_json.html?highlight=to_json#pand
                        as.Series.to_json
  --json-in-orient {split,records,index,columns,values,table}
                        Specifies the json orient. Choose one of ['split',
                        'records', 'index', 'columns', 'values', 'table']. See
                        https://pandas.pydata.org/pandas-docs/stable/reference
                        /api/pandas.Series.to_json.html?highlight=to_json#pand
                        as.Series.to_json

```

## License

[Licensed under GPLv3](LICENSE.txt).