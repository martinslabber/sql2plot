# sql2plot

Going from SQL to a plot in 2 easy steps

1. Write an *.ini* file with your connection string (DSN) and SQL statement in.
2. Run sql2plot.py with the name of your *.ini* file as the argument.

The sql2plot utility itself does very little; it stands on the shoulders of giants and glues some impressive features together to help a lazy man.

Python3 [ConfigParser][1] (in ExtendedInterpolation mode) allows for flexible configuration with inheritance and simple templating.
[Pandas][2] do queries and data wrangling; Pandas uses [SqlAlchemy][3].
[Seaborn][4] creates the plots; Seaborn uses [Matplotlib][5].

## Dependencies

Python3 with the following modules are necessary:
pandas
sqlalchemy
matplotlib
seaborn

## Usage

If all the listed dependencies are met on your system, you can call sql2plot.py with one or more *.ini* files as arguments.

> python3 sql2plot.py myplots/redvsblue.ini myplots/greenvsorange.ini

If you pass in an *.ini* file named 'init.ini', it will be ignored.

## Configuration

in the *.ini* file a *[plot]* section is required.
The *[plot]* section can have the following keys.
- dsn - Database connection string
- plot type - The type of plot. This can be "line" or "cat"
- title - Title of the plot
- x label - Label of the X axis
- y label - Label of the Y axis
- output types - A comma-separated list of file formats, e.g. "png,pdf"

All sections with a name that starts with *sql-* needs a query key.
The value of the query key should be an SQL statement that returns columns name,x, and y. Multi-line queries are supported, indent from the second line.
The *sql-* sections can also have a marker key; the value of the marker key should be a Matplotlib marker [character][6].

[1]:https://docs.python.org/3/library/configparser.html#module-configparser "ConfigParser"
[2]:https://pandas.pydata.org/ "Pandas"
[3]:https://www.sqlalchemy.org/ "SqlAlchemy"
[4]:https://seaborn.pydata.org/ "seaborn"
[5]:https://matplotlib.org "Matplotlib"
[6]:https://matplotlib.org/api/markers_api.html?highlight=marker#module-matplotlib.markers "Matplotlib Markers"
