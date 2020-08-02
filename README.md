# strliteral

`strliteral` is a tool to embed data into C or C++ programs. It does this by
generating string literals which contain the data you want to embed, which
is orders of magnitude faster to compile than the character arrays generated
by `xxd -i`.

For more info on performance and such, read this article:
https://mort.coffee/home/fast-cpp-embeds/

`strliteral` has no dependencies outside of the stdlib, and should support any
conforming C89 compiler or newer.

## Usage

The basic syntax for `strliteral` is:

	strliteral [options] [infile] [outfile]

if no outfile is provided, the default is stdout. If no infie is provided,
the default is stdin.

The options are:

* `-h`, `--help`: Show a help dialog
* `--no-const`: Output mutable variables instead of consts
* `--always-escape`: Always escape every byte with an octal escape, instead
  of only escaping "weird" characters. Useful in edge cases related to weird
  source and execution charsets.
* `-l`, `--line-length <length>`: Set the number of characters in a string literal.
  Default: 100
* `-i`, `--ident <ident>`: Set the identifier. Default: generate an identifier
  based on the infile name.

## Incorporatng into a build system

Unless and until `strliteral` becomes a common package in distros, I would recommend
bundling a copy of `strliteral.c` with your project, especially if it's open source.
Here's an example GNU Makefile which can generate object files in
`build/static/` from files in `static/`:

``` Makefile
build/static/%.o: build/static/%.c
	@mkdir -p $(@D)
	$(CC) -o $@ -c $<

build/static/%.c: static/% build/static/strliteral
	@mkdir -p $(@D)
	./build/static/strliteral $< $@

build/static/strliteral: strliteral.c
	@mkdir -p $(@D)
	$(CC) -O3 -o $@ $<
```
