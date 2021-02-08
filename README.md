Pandas for the command-line

Use pandas for querying csv files or tabular data in the command-line, like: 

```cat example.csv | pd -q "x > 30" --sort z```. 

It supports [pandas queries](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html) and some basic column manipulation (renaming/reordering/...) and sorting.

All CLI arguments:

```
usage: pd [-h] [--query QUERY] [--input INPUT] [--output OUTPUT] [--pretty]
          [--transpose] [--sort SORT [SORT ...]] [--descending]
          [--drop DROP [DROP ...]] [--with-index] [--latex]
          [--float-format FLOAT_FORMAT] [--move MOVE [MOVE ...]]
          [--rename RENAME [RENAME ...]] [--sep SEP]

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
  --transpose, -t
  --sort SORT [SORT ...], -s SORT [SORT ...]
                        Sort by column(s)
  --descending          Sort descending
  --drop DROP [DROP ...]
                        Drop column(s)
  --with-index          Specify for outputing the index column
  --latex               Output latex table
  --float-format FLOAT_FORMAT
                        Specify the float format in the output, e.g. '%.4f'
  --move MOVE [MOVE ...]
                        Moves column X right before after column Y; format:
                        'X::Y'
  --rename RENAME [RENAME ...]
                        Renames columns, format: 'old name::new name'
  --sep SEP             Column seperator

```
