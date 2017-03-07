import os
import re
import collections


def exotic(dir='.', pattern=r'[^\t\n\x20-\x7f]', ext='.txt'):
    for dirpath, dirnames, filenames in os.walk(dir):
        for f in filenames:
            if not f.endswith(ext):
                continue
            path = os.path.join(dirpath, f)
            with open(path) as fp:
                try:
                    s = fp.read()
                except UnicodeDecodeError as exn:
                    print(path, exn)
                    raise
                else:
                    yield path, re.finditer(pattern, s)


def histogram():
    result = collections.defaultdict(collections.Counter)
    for path, matches in exotic():
        for mo in matches:
            result[mo.group()][path] += 1
    return result


def main():
    from pprint import pprint
    h = histogram()
    pprint(dict(h))
    pprint({k: sum(v.values()) for k, v in h.items()})


if __name__ == '__main__':
    main()
