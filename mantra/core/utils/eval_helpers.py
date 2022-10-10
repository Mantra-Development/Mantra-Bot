import ast
import asyncio
import contextlib
import inspect
import io
import time
import traceback
import typing as t

import hikari
import lightbulb


def _yields_results(*args: io.StringIO) -> t.Iterator[str]:
    for name, stream in zip(("stdout", "stderr"), args):
        yield f"-dev/{name}:"
        while lines := stream.readlines(25):
            yield from (line[:-1] for line in lines)


def build_eval_globals(ctx: lightbulb.Context) -> dict[str, t.Any]:
    return {
        "asyncio": asyncio,
        "app": ctx.app,
        "bot": ctx.bot,
        "ctx": ctx,
        "hikari": hikari,
        "lightbulb": lightbulb,
    }


async def eval_python_code(
    ctx: lightbulb.Context, code: str
) -> tuple[io.StringIO, io.StringIO, int, bool]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        with contextlib.redirect_stderr(stderr):
            start_time = time.perf_counter()
            try:
                await eval_python_code_no_capture(ctx, code)
                failed = False
            except Exception:
                traceback.print_exc()
                failed = True
            finally:
                exec_time = round((time.perf_counter() - start_time) * 1000)

    stdout.seek(0)
    stderr.seek(0)
    return stdout, stderr, exec_time, failed


async def eval_python_code_no_capture(ctx: lightbulb.Context, code: str) -> None:
    globals_ = build_eval_globals(ctx)
    compiled_code = compile(code, "", "exec", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
    if compiled_code.co_flags & inspect.CO_COROUTINE:
        await eval(compiled_code, globals_)

    else:
        eval(compiled_code, globals_)
