import asyncio
import inspect


def pytest_pyfunc_call(pyfuncitem):
    test_function = pyfuncitem.obj

    if not inspect.iscoroutinefunction(test_function):
        return None

    kwargs = {
        name: pyfuncitem.funcargs[name]
        for name in pyfuncitem._fixtureinfo.argnames
    }

    asyncio.run(test_function(**kwargs))

    return True
