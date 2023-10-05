from typing import Any, Callable, List
from hypothesis import given, strategies as st


def random_tester(function: Callable[..., Any], num_tests: int, test_templates: List[str], *args) -> None:
    @given(*args)
    def wrapped_test(*inputs):
        arg_names = function.__code__.co_varnames[:function.__code__.co_argcount]
        test_cases = [test.format(**{name: arg for name, arg in zip(arg_names, inputs)}) for test in test_templates]
        for case in test_cases:
            try:
                assert eval(case, {}, {'foo': function})
            except AssertionError:
                print(f"Failed test: {case}")
                print(f"Input values: {inputs}")
                return
    for i in range(num_tests):
        wrapped_test()

def foo(n: str) -> int:
    if len(n) < 1000:
        return 0
    else:
        return 1
print(random_tester(foo, 100, ["z = ${1}; foo(z) == foo(z) + foo(z)"], st.integers()))
