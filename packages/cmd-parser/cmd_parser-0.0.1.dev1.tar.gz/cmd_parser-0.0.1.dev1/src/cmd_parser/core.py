import re
import shlex
from abc import ABC
from typing import Iterator, Match
from copy import copy
from functools import singledispatch


class AbstractTokenHandler(ABC):

    kind = ''
    matches: Match[str]
    pattern = ''
    token = None

    def __init__(self, next_handler):
        self.next = next_handler

    def handle(self, token):
        self.token = token
        if matches := re.match(self.pattern, token):
            self.matches = matches
            return copy(self)
        else:
            return self.next.handle(token)


class NoHandler(AbstractTokenHandler):
    kind = 'default'


class CommandHandler(AbstractTokenHandler):
    pattern = r'(?:!|:)([a-z]+[0-9_]?+)'
    kind = 'command'


class ArgsHandler(AbstractTokenHandler):
    pattern = r'([a-zA-Z0-9_\s]+)'
    kind = 'args'


class KwargsHandler(AbstractTokenHandler):
    pattern = r'([a-z_]+[0-9_]+)=(?:[\"\'])?([a-zA-Z0-9_\s]+)(?:[\"\'])?'
    kind = 'kwargs'


def handler_factory():
    no_handler = NoHandler(next_handler=None)
    command_handler = CommandHandler(next_handler=no_handler)
    args_handler = ArgsHandler(next_handler=command_handler)
    kwargs_handler = KwargsHandler(next_handler=args_handler)
    return kwargs_handler


def asdict(parser: Iterator) -> dict:
    output = {'command': None, 'args': [], 'kwargs': {}}

    @singledispatch
    def dispatch(handler):
        raise ValueError(f"No handler for the token -> '{handler.token}'")

    @dispatch.register
    def _(handler: CommandHandler):
        output[handler.kind] = handler.matches.group(1)

    @dispatch.register
    def _(handler: ArgsHandler):
        output[handler.kind].append(handler.matches.group(1))

    @dispatch.register
    def _(handler: KwargsHandler):
        output[handler.kind][handler.matches.group(1)] = handler.matches.group(
            2
        )

    for handler in parser:
        dispatch(handler)

    return output


def parse(string: str) -> Iterator:
    lex = shlex.shlex(string, posix=True)
    lex.whitespace_split = True

    handler = handler_factory()

    for token in lex:
        yield handler.handle(token=token)


def main():
    import time

    t = time.process_time()
    print(
        asdict(parse('!command arg1 arg2 param1="value1 test" param2=value2'))
    )
    elapsed_time = time.process_time() - t
    print(elapsed_time)


if __name__ == '__main__':
    main()
