from typing import TypeVar, Callable, List, Protocol
import inspect

from arthur.common.exceptions import UnexpectedTypeError, UnexpectedValueError

M = TypeVar("M")


class PaginatedResponse(Protocol[M]):
    data: List[M]


def paginate(
    func: Callable[..., PaginatedResponse[M]],
    max_pages=100,
    page_size=50,
    page_start=1,
    verify_end=True,
    **func_kwargs,
) -> List[M]:
    # ensure the function has 'page' and 'page_size' inputs
    func_args = inspect.getfullargspec(func).args
    if not ("page" in func_args and "page_size" in func_args):
        raise UnexpectedTypeError(
            f"function {func.__name__} does not have 'page' and 'page_size' parameters, so cannot "
            f"be used in paginate()"
        )

    # fetch results in pages
    page = page_start
    results: List[M] = []
    cur_result: List[M] = []
    while page <= max_pages:
        func_kwargs.update({"page": page, "page_size": page_size})
        cur_result = func(**func_kwargs).data
        results.extend(cur_result)
        page += 1

    # ensure we didn't hit the end
    if verify_end and page >= max_pages and len(cur_result) == page_size:
        func_kwargs.update({"page": max_pages + 1})
        if len(func(**func_kwargs).data) > 0:
            raise UnexpectedValueError(
                f"Results exist past last page, set verify_end=False to ignore or increase max "
                f"pages"
            )

    return results
