KBYTES = 10

.PHONY: all
all: run-test

test-data-$(KBYTES)k:
	dd if=/dev/urandom of=$@ bs=1024 count=$(KBYTES) || rm -f $@

../strliteral: ../strliteral.c
	$(MAKE) -C .. strliteral

test-data.c: test-data-$(KBYTES)k ../strliteral
	../strliteral --always-escape --ident data $< $@ || rm -f $@

test: test.c test-data.c
	$(CC) -finput-charset=UTF8 -fexec-charset=LATIN1 -o $@ $^

.PHONY: run-test
run-test: test
	./test test-data-$(KBYTES)k

.PHONY: clean
clean:
	rm -f test test-data-*k test-data.c
