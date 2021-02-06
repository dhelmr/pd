Pandas for the command-line

```
usage: pd.py [-h] [--query QUERY] [--input INPUT] [--output OUTPUT] [--pretty]
             [--transpose] [--sort SORT [SORT ...]] [--descending]
             [--drop DROP [DROP ...]] [--with-index] [--latex]
             [--float-format FLOAT_FORMAT] [--move MOVE [MOVE ...]]
             [--rename RENAME [RENAME ...]]

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
  --with-index
  --latex
  --float-format FLOAT_FORMAT
  --move MOVE [MOVE ...]
                        Moves column X right before after column Y; format:
                        'X::Y'
  --rename RENAME [RENAME ...]
                        Renames columns, format: 'old name::new name'

```
