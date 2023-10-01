#!/usr/bin/env python3
"""
DOCSTRING for first public console interface.

USAGE:
    vaticinator [options]
"""
import sys
import re
from functools import cached_property
from argparse import ArgumentParser, Namespace
from random import randint
from logging import warn, debug, getLogger, WARN, INFO, DEBUG
from pathlib import Path
from vaticinator.libs.fortune_file import FortuneFile, DEFAULT_FORTUNE_PATH
from pprint import pp


class Vaticinator:
    VALID_FLAGS = ('all', 'show_file', 'equal', 'list_files', 'long', 'off',
                   'short', 'ignore_case', 'wait', 'u', 'verbose', 'debug')
    VALID_ARGS = {'match': str, 'short_max': int}

    def __init__(self, cmd=None, params=[], *args, **kwargs):
        self.args = cmd
        self._files = {}
        self.set_default_options()
        if params or args or kwargs:
            self.process_options(params, *args, **kwargs)

    def main(self, main_args=None):
        debug('main')
        args = main_args or self.args or sys.argv[1:]
        self.process_args(args)
        return self.run()

    def get_options(self):
        return self._options

    def set_options(self, val):
        if val is None:
            return
        if not isinstance(val, Namespace):
            raise TypeError('Vaticinator.options must be of type '
                            + f'argparse.Namespace ({val} is of '
                            + f'type {type(val)})')
        self._options = val
        if self._options.verbose:
            getLogger().setLevel(INFO)
        if self._options.debug:
            getLogger().setLevel(DEBUG)

    options = property(get_options, set_options)

    def set_default_options(self):
        kwargs = {'match': None, 'short_max': 160}
        for flag in self.VALID_FLAGS:
            kwargs.setdefault(flag, False)
        self._options = Namespace(**kwargs)
        return self._options

    def process_log_level(self):
        if self._options.verbose:
            getLogger().setLevel(INFO)
        if self._options.debug:
            getLogger().setLevel(DEBUG)

    def process_args(self, args=None):
        debug('process_args')
        parser = ArgumentParser()
        parser.add_argument('-a', '--all', action='store_true',
                            help='Choose from all lists of maxims, both offensive and not.')
        parser.add_argument('-c', '--show-file', action='store_true',
                            help='Show the cookie file from which the fortune came.')
        parser.add_argument('-e', '--equal', action='store_true',
                            help='Consider all fortune files to be of equal size.')
        parser.add_argument('-f', '--list-files', action='store_true',
                            help='Print out the list of files which would be searched; don’t print a fortune.')
        parser.add_argument('-l', '--long', action='store_true',
                            help='Long dictums only.')
        parser.add_argument('-m', '--match', type=str,
                            help='Print out all fortunes which match the basic regular expression pattern.')
        parser.add_argument('-n', '--short-max', default=160, type=int,
                            help='Set the longest fortune length considered short.')
        parser.add_argument('-o', '--off', action='store_true',
                            help='Choose only from potentially offensive aphorisms.')
        parser.add_argument('-s', '--short', action='store_true',
                            help='Short apothegms only.')
        parser.add_argument('-i', '--ignore-case', action='store_true',
                            help='Ignore case for -m patterns.')
        parser.add_argument('-w', '--wait', action='store_true',
                            help='Wait before termination for an amount of time calculated from the number of characters in the message.')
        parser.add_argument('-u', action='store_true',
                            help='Don’t translate UTF-8 fortunes to the locale when searching or translating.')
        parser.add_argument('-v', '--verbose', action='store_true')
        parser.add_argument('-d', '--debug', action='store_true')
        parser.add_argument('params', metavar='arg', nargs='*',
                            help='[#%%] file/directory/all')
        self.options = parser.parse_args(args)
        self.process_log_level()
        return self.options

    def process_options(self, *args, **kwargs):
        debug('process_options')

        for arg in args:
            if arg in self.VALID_FLAGS and arg not in kwargs:
                kwargs[arg] = True
        for k, v in kwargs:
            if k not in (self.VALID_FLAGS + self.VALID_ARGS.keys()):
                warn(f'option "{k}" not recognized!')
                del kwargs[k]
            if (k in self.VALID_FLAGS and type(v) is not bool) or \
                    (k in self.VALID_ARGS and type(v) is not self.VALID_ARGS[k]):
                warn(f'"{k}" is not valid for option {k}')

        for k, v in kwargs:
            setattr(self.options, k, v)

        self.process_log_level()
        return self.options

    def process_files(self, params):
        debug('process_files')
        self._files = {}
        next_weight = None
        while len(params):
            next_sym = params.pop(0)
            if m := re.fullmatch(r'([0-9]+)%?', next_sym):
                next_weight = m.group(0)
            else:
                for next_file in FortuneFile.load_path(next_sym):
                    self._files[next_file] = next_weight

    def run(self, cmd=[], params=[], *args, **kwargs):
        debug('run')
        if cmd:
            self.process_args(cmd)
        if params or args or kwargs:
            self.process_options(params, *args, **kwargs)
        self.process_files(self.options.params)
        if self.options.show_file:
            pass
        elif self.options.list_files:
            pass
        # elif self.options.version:
        #     pass
        else:
            fortune = self.fortune
            print(fortune)
            return 0

    @property
    def files(self):
        f = self._files or self.default_files
        r = []
        for k, v in f.items():
            if not (v and k.length):
                debug(f'removing file {k}')
                r.append(k)
        for k in r:
            del f[k]
        return f

    @cached_property
    def default_files(self):
        def_files = {}
        def_path = DEFAULT_FORTUNE_PATH if self.options.all \
            else f'{DEFAULT_FORTUNE_PATH}/fortunes.dat'
        for next_file in FortuneFile.load_path(def_path):
            def_files[next_file] = 1
            debug(f'{next_file.path} has {next_file.length} entries')
        return def_files

    @property
    def fortune(self):
        if not self.options:
            self.process_options()
        total = sum(self.files.values())
        num = randint(0, total - 1)
        debug(f'fortune() file #{num}/{total}')
        selected = None
        for ff, weight in self.files.items():
            debug(f'{ff}: {num} - {weight}')
            num -= weight
            if num < 0:
                debug(f'{ff.path} is selected')
                selected = ff
                if selected.length > 0:
                    break
                warn(f'{ff} has no entries!')

        return selected.get_random(self.options)


def main(*args, **kwargs):
    return Vaticinator(*args, **kwargs).main()


if __name__ == '__main__':
    exit(main())
