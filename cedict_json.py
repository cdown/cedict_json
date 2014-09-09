#!/usr/bin/env python

from __future__ import print_function
import re


def parse(cedict_file_object):
    '''
    Yields characters from a CEDICT file object, and their metadata.

    :param cedict_file_object: a cedict-like file object
    :returns: a generator of characters and their metadata
    '''

    line_format = re.compile(
        r'^(?P<trad>[^ ]+) (?P<simp>[^ ]+) '
        '\[(?P<pinyin>[^\]]+)] /(?P<english>.+)/$'
    )

    for line in cedict_file_object:
        if line.startswith('#'):
            continue

        line = line.rstrip()
        matches = line_format.match(line)

        if matches is not None:
            yield matches.groupdict()


if __name__ == '__main__':
    import codecs
    import json
    import os
    import sys

    try:
        _, filename = sys.argv
    except ValueError:
        print(
            'Usage: %s <cedict-file>' % os.path.basename(sys.argv[0]),
            file=sys.stderr,
        )
        sys.exit(1)

    with codecs.open(filename, encoding='utf8') as f:
        print(json.dumps({'chars': list(parse(f))}))
