import re
import sys


ENCODINGS = {
    0: 'latin1 windows-1252'.split(),
    10: 'mac-roman latin2'.split(),
}
'Encodings to try along with their associated penalties'


HEURISTIC = {
    0: 'æøåÆØÅ',
    0.1: 'éàä™',
    # All others have a penalty of 1
}
'Penalties of the non-ascii characters that we expect to see'


def _compile_heuristic(heuristic):
    '''
    Turn HEURISTIC into a dictionary mapping characters to scores.
    '''
    return {ch: score for score, chs in heuristic.items() for ch in chs}


def _get_score(content, encoding, symbol_score):
    '''
    Sum the penalties of non-ascii characters in binary data for a particular
    encoding. Returns +infinity if decoding fails.
    '''
    try:
        s = content.decode(encoding)
    except UnicodeDecodeError:
        return float('inf')
    # Match all non-ASCII characters.
    pattern = r'[^\t\n\x20-\x7f]'
    return sum(symbol_score.get(mo.group(), 1)
               for mo in re.finditer(pattern, s))


def guess_encoding(content, encodings=ENCODINGS, heuristic=HEURISTIC,
                   verbose=True):
    try:
        content.decode('utf8')
    except UnicodeDecodeError:
        pass
    else:
        return 'utf8'
    scores = {}
    symbol_score = _compile_heuristic(heuristic)
    for enc_score, encodings in encodings.items():
        for encoding in encodings:
            scores[encoding] = (
                enc_score + _get_score(content, encoding, symbol_score))
    if verbose:
        ranking = sorted(scores.keys(), key=lambda k: scores[k])
        print('Guessing encoding %s from the following:' % ranking[0],
              file=sys.stderr)
        for i, enc in enumerate(ranking):
            print('%s. %s (score=%.1f)' % (i+1, enc, scores[enc]),
                  file=sys.stderr)
    return min(scores.keys(), key=lambda k: scores[k])


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='+')
    args = parser.parse_args()

    for filename in args.filename:
        with open(filename, 'rb') as fp:
            print('%s\t%s' % (filename, guess_encoding(fp.read())))


if __name__ == '__main__':
    main()
