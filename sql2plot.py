#!/usr/bin/env python3

import sys
import logging

from pathlib import Path
from configparser import ConfigParser, ExtendedInterpolation

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sqlalchemy import create_engine


class PConf:
    def __init__(self, config_filename):

        self.configfile = Path(config_filename)
        config = ConfigParser(interpolation=ExtendedInterpolation())
        initini = self.configfile.parent.joinpath("init.ini")
        if initini.exists():
            config.read(str(initini))
        config.read(self.configfile)
        self.dsn = config["plot"]["dsn"]
        self.x = config["plot"]["x label"]
        self.y = config["plot"]["y label"]
        self.title = config["plot"]["title"]
        self.out_types = config["plot"].get("output types", "png").split(",")
        self.plot_type = config["plot"].get("plot type", "line")
        self.sql = []
        for section in config.sections():
            if section.startswith("sql-"):
                dataset = {"query": config[section]["query"]}
                dataset["marker"] = config[section].get("marker", "o")
                self.sql.append(dataset)

    def output_filenames(self):
        for filetype in self.out_types:
            yield self.configfile.with_suffix("." + filetype)


def dist_plot(sql, df):
    plot = sns.distplot(df, rug=True)
    return plot

def cat_plot(sql, df):
    plot = sns.catplot(data=df, x="x", y="y", hue="name", kind="bar", palette="muted")
    return plot


def line_plot(sql, df):
    markers = [sql["marker"] for n in df.name]
    df2 = pd.pivot_table(df, columns="name", index="x", values="y")
    plot = sns.lineplot(data=df2, dashes=False, markers=markers)
    return plot


def lineregion_plot(sql, df):
    plot = sns.lineplot(data=df, dashes=False, hue="name", x='x', y='y')

    return plot


def mk_plot(config_filename):
    conf = PConf(config_filename)
    engine = create_engine(conf.dsn)
    sns.set_style("whitegrid")
    plot = None

    for sql in conf.sql:
        df = pd.read_sql_query(sql["query"], engine)
        if conf.plot_type == "line":
            plot = line_plot(sql, df)
        elif conf.plot_type == "lineregion":
            plot = lineregion_plot(sql, df)
        elif conf.plot_type == "cat":
            plot = cat_plot(sql, df)
        elif conf.plot_type in ["histogram", "distribution", "distplot"]:
            plot = dist_plot(sql, df)
        else:
            logging.warning("No plot type defined, making a line plot")
            plot = line_plot(sql, df)
    if plot is None:
        logging.error("Nothing to plot.")
        raise ValueError("nothing to plot")

    plot.set(title=conf.title, xlabel=conf.x, ylabel=conf.y)
    for outfile in conf.output_filenames():
        if hasattr(plot, "figure"):
            plot.figure.savefig(outfile)
        else:
            plot.savefig(outfile)
        print("Saved plot to {}".format(outfile))

    plt.clf()  # Clear the current plot


if __name__ == "__main__":

    args = sys.argv[1:]
    if args:
        for name in args:
            if not name.endswith("init.ini"):
                mk_plot(name)
    else:
        name = None
        print("Please supply one or more ini files")
