from simpleworkspace.__lazyimporter__ import __LazyImporter__
if(__LazyImporter__.TYPE_CHECKING):
    from . import console as _console
    from . import module as _module
    from . import regex as _regex
    from . import stopwatch as _stopwatch
    from . import strings as _strings
    from . import bytes as _bytes
    from . import linq as _linq
    from . import progressbar as _progressbar

console: '_console' = __LazyImporter__(__package__, '.console')
module: '_module' = __LazyImporter__(__package__, '.module')
regex: '_regex' = __LazyImporter__(__package__, '.regex')
stopwatch: '_stopwatch' = __LazyImporter__(__package__, '.stopwatch')
strings: '_strings' = __LazyImporter__(__package__, '.strings')
bytes: '_bytes' = __LazyImporter__(__package__, '.bytes')
linq: '_linq' = __LazyImporter__(__package__, '.linq')
progressbar: '_progressbar' = __LazyImporter__(__package__, '.progressbar')