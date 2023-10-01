"""
provides an interface for fortune-style .dat files.

Contains:
    - FortuneFile
    - FortuneFileError
"""
from pathlib import Path
from logging import warn, debug
from random import randint
import struct
import re
from pprint import pp


DEFAULT_FORTUNE_PATH = '/usr/share/games/fortunes'
MAX_TRIES = 1000


class FortuneFileError(BaseException):
    pass


class FortuneFile:
    """Interface for fortune-style .dat files"""

    def __init__(self, filename=None):
        debug(f'FortuneFile({filename})')
        self.path = None
        self.offsets = []
        (self.version, self.length,
         self.longest, self.shortest) = (0, 0, 0, 0)
        if filename is not None:
            try:
                self.load_file(filename)
            except Exception as e:
                raise e
                warn(f'didnt load: {filename}')

    def __str__(self):
        return f'FortuneFile({self.path}): {self.length} entries'

    @classmethod
    def load_path(cls, path):
        debug(f'load_path({path})')
        files = []
        path = Path(path)
        if not path.exists():
            pass
        elif path.is_dir():
            files = [FortuneFile(p) for p in path.rglob('*.dat')]
        else:
            files = [FortuneFile(path)]
        return files

    @property
    def data_path(self):
        return self.path.parent / self.path.stem

    def load_file(self, fn):
        debug(f'load_file({fn})')
        self.path = fn if isinstance(fn, Path) else Path(fn)
        if not self.path.exists() and isinstance(fn, str) and fn.isalnum():
            self.path = Path(f'{DEFAULT_FORTUNE_PATH}/{fn}.dat')
        if self.path.exists() and self.data_path.exists():
            try:
                with self.path.open('rb') as dat:
                    header = struct.unpack('>IIIIIcxxx', dat.read(24))
                    (self.version, self.length,
                     self.longest, self.shortest) = header[0:4]
                    self.offsets = [
                        struct.unpack('>I', dat.read(4))[0]
                        for i in range(self.length + 1)
                        ]
            except Exception as e:     # noqa: E722
                warn(f'error reading fortune file "{fn}"!  {e}')
                raise FortuneFileError(e)
        else:
            warn(f'fortune file "{fn}" not found!')
            raise FortuneFileError

    def get_random(self, opts):
        fortune = None
        for i in range(1, MAX_TRIES):
            try:
                num = randint(1, self.length)
                fortunes_all = self.data_path.read_bytes()
                debug(f'fortunes length: {len(fortunes_all)}')
                debug(f'number of offsets: {self.length} ({len(self.offsets)})')
                debug(f'random number: {num}')
                debug(
                    f'offsets: {self.offsets[num - 1]} - {self.offsets[num] - 2}')
                debug(f'starts with {fortunes_all[self.offsets[num - 1]]}')
                fortune_bytes = fortunes_all[self.offsets[num - 1]:
                                             self.offsets[num] - 2]
                fortune = fortune_bytes.decode()
                debug(f'fortune: {fortune}')
                flags = re.I if opts.ignore_case else re.NOFLAG
                if opts.match:
                    debug(f'match: {opts.match}')
                if ((opts.match and not re.search(opts.match, fortune, flags))
                        or (opts.short and len(fortune) > opts.short_max)
                        or (opts.long and len(fortune) < opts.short_max)):
                    continue
                return fortune
            except UnicodeDecodeError:
                warn('unicode decode error')
        else:
            return 'No fortune today!'
