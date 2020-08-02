#!/bin/sh

rm -rf work
mkdir work
mkdir work/input work/generated-xxd work/generated-str \
	work/compiled-xxd work/compiled-str work/times-xxd work/times-str

sizes="128 256 512 1024 2048"

for size in $sizes; do
	dd bs=1024 count=$size if=/dev/urandom of=work/input/random-${size}k
	cat /dev/urandom | tr -dc '[:alnum:]' | dd bs=1024 count=$size of=work/input/text-${size}k
done

echo
echo "=== Generating C ==="
for typ in text random; do
	hyperfine --warmup 2 -L size "$(echo "$sizes" | sed 's/ /,/g')" \
		--export-csv work/generate-times-xxd-$typ.csv \
		"xxd -i work/input/$typ-{size}k work/generated-xxd/$typ-{size}k.c"
	hyperfine --warmup 2 -L size "$(echo "$sizes" | sed 's/ /,/g')" \
		--export-csv work/generate-times-str-$typ.csv \
		"../strliteral work/input/$typ-{size}k work/generated-str/$typ-{size}k.c"
done

echo
echo "=== Compiling C ==="
for typ in text random; do
	hyperfine --warmup 2 -L size "$(echo "$sizes" | sed 's/ /,/g')" \
		--export-csv work/compile-times-xxd-$typ.csv \
		"/usr/bin/time -o work/times-xxd/$typ-{size}k.txt g++ -c work/generated-xxd/$typ-{size}k.c -o work/compiled-xxd/$typ-{size}k.o"
	hyperfine --warmup 2 -L size "$(echo "$sizes" | sed 's/ /,/g')" \
		--export-csv work/compile-times-str-$typ.csv \
		"/usr/bin/time -o work/times-str/$typ-{size}k.txt g++ -c work/generated-str/$typ-{size}k.c -o work/compiled-str/$typ-{size}k.o"
done
