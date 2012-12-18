#!/usr/bin/env python

import timeit
import urilib.parsing

uri    = 'http://anonymous:password@www.google-analytics.com:80/path/goes/here/?parameter=value?#Fragment?'
number = 100000

for parser in urilib.parsing.parsers:
    setup     = 'import urilib.parsing as parsing'
    statement = 'parsing.parsers["%s"]("%s")' % (parser, uri)
    time      = timeit.Timer(statement, setup=setup).timeit(number=number)

    avg = time / number

    print "%8.8s => [ total: %2.2f, average: %2.3g ]" % (parser, time, avg)
