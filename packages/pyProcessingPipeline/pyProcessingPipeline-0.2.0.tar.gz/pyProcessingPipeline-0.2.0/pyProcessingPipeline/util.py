"""Helper functions used in the processing package.

Functions
---------
batch_generator
    Used for splitting a list into smaller batches.
"""

from collections.abc import Generator, Sequence
from typing import TypeVar

T = TypeVar("T")


def batch_generator(
    list_to_batch: Sequence[T], batch_size: int
) -> Generator[list[T], None, None]:
    """Batch list into multiple batches of batch_size or less.

    This returns multiple batches with batch_size length.
    The last match might be smaller than batch_size if
    the length of the input list is not cleanly divisible by
    batch_size.

    >>> main_list = [1, 2, 3, 4, 5, 6, 7, 8]
    >>> sub_lists = [sublist for sublist in batch_generator(main_list, 3)]
    >>> sub_lists
    [[1, 2, 3], [4, 5, 6], [7, 8]]

    or used in a for-loop

    >>> for sublist in batch_generator(main_list, 4):
    ...     print(sublist)
    [1, 2, 3, 4]
    [5, 6, 7, 8]

    Parameters
    ----------
    list_to_batch : list[T]
        List which from which smaller batches should be created.
    batch_size : int
        The maximum size of each sub-batch.

    Yields
    ------
    Generator[list[T], None, None]
        Generator which yields each sub-batch.
    """
    # Uses ceiling integer division
    amount_of_batches = -(len(list_to_batch) // -batch_size)

    for i in range(amount_of_batches):
        left_index = i * batch_size
        right_index = left_index + batch_size
        yield list(list_to_batch[left_index:right_index])
