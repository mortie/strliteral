#!/usr/bin/env python3

import re
import csv
import glob
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
from adjustText import adjust_text

compilePlots = [
    [ "XXD, random data",             "work/compile-times-xxd-random.csv" ],
    [ "XXD, text data",               "work/compile-times-xxd-text.csv" ],
    [ "String literals, random data", "work/compile-times-str-random.csv" ],
    [ "String literals, text data",   "work/compile-times-str-text.csv" ],
]

generatePlots = [
    [ "XXD, random data",             "work/generate-times-xxd-random.csv" ],
    [ "XXD, text data",               "work/generate-times-xxd-text.csv" ],
    [ "String literals, random data", "work/generate-times-str-random.csv" ],
    [ "String literals, text data",   "work/generate-times-str-text.csv" ],
]

compileMemPlots = [
    [ "XXD, random data",             "work/times-xxd/random-*.txt" ],
    [ "XXD, text data",               "work/times-xxd/text-*.txt" ],
    [ "String literals, random data", "work/times-str/random-*.txt" ],
    [ "String literals, random data", "work/times-str/text-*.txt" ],
]

def drawTimes(plots, title, ylabel, xlabel, fname):
    print(fname)
    texts = []
    for plot in plots:
        path = plot[1]
        label = plot[0]
        keys = []
        values = []
        with open(path) as f:
            reader = csv.DictReader(f)
            for d in reader:
                keys.append(float(d["parameter"]))
                values.append(float(d["median"]) * 1000) # seconds -> milliseconds

        texts.append(plt.text(keys[-1], values[-1], f"{values[-1]:.0f}ms", va="center"))
        plt.plot(keys, values, "o-", label=label)

    adjust_text(texts)
    plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val:.0f}kB"))
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val:.0f}ms"))
    plt.xticks(keys, rotation=40)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.savefig(fname, bbox_inches="tight")
    plt.clf()

def drawMem(plots, title, ylabel, xlabel, fname):
    print(fname)
    texts = []
    rssrx = re.compile(r".* (.*?)maxresident.*")
    sizerx = re.compile(r".*-(.*?)k\.txt")
    for plot in plots:
        pathglob = plot[1]
        label = plot[0]
        keys = []
        values = []
        for path in glob.iglob(pathglob):
            with open(path) as f:
                kb = rssrx.match(f.readline()).group(1)
                size = sizerx.match(path).group(1)
                keys.append(float(size))
                values.append(float(kb) / 1024)

        keys, values = zip(*sorted(zip(keys, values), key=lambda kv: kv[0]))
        texts.append(plt.text(keys[-1], values[-1], f"{values[-1]:.0f}MB", va="center"))
        plt.plot(keys, values, "o-", label=label)

    adjust_text(texts)
    plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val:.0f}kB"))
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val:.0f}MB"))
    plt.xticks(keys, rotation=40)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.savefig(fname, bbox_inches="tight")
    plt.clf()

drawTimes(compilePlots, "Compile Times",
        "Compile Time (ms)", "Embedded File Size (kB)", "compile-times.svg")
drawTimes(generatePlots, "Code Gen Times",
        "Generate Time (ms)", "Embedded File Size (kB)", "generate-times.svg")
drawMem(compileMemPlots, "Compiler Memory Usage",
        "Compiler Memory Usage (MB)", "Embedded File size (kB)", "compile-mem.svg")
