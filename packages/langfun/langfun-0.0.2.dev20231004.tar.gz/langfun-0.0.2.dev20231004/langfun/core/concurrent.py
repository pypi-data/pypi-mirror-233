# Copyright 2023 The Langfun Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utility library for handling concurrency in langfun."""

import concurrent.futures
import dataclasses
import random
import time
from typing import Any, Callable, Iterable, Iterator, Sequence, Tuple, Type, Union

from langfun.core import component
import pyglove as pg
from tqdm import auto as tqdm


def with_context_access(func: Callable[..., Any]) -> Callable[..., Any]:
  """Derives a user function with the access to the current context."""
  with component.context() as current_context:
    pass

  def _func(*args, **kwargs) -> Any:
    with component.context(**current_context):
      return func(*args, **kwargs)

  return _func


class RetryError(RuntimeError):
  """Retry error."""

  def __init__(
      self,
      func: Callable[..., Any],
      errors: list[Exception],
      wait_intervals: list[int],
  ):
    assert len(errors) == len(wait_intervals) + 1

    super().__init__()
    self.func = func
    self.errors = errors
    self.wait_intervals = wait_intervals

  @property
  def attempts(self) -> int:
    """Returns the number of attempts made."""
    return len(self.errors)

  def __repr__(self) -> str:
    return (
        'RetryError('
        + pg.object_utils.kvlist_str(
            [
                ('func', self.func, None),
                ('errors', self.errors, None),
                ('wait_intervals', self.wait_intervals, None),
            ],
            compact=True,
        )
        + ')'
    )

  def __str__(self) -> str:
    wait_interval_str = ', '.join([str(x) for x in self.wait_intervals])
    return (
        f'Calling {self.func!r} failed after {self.attempts} attempts '
        f'(wait time: {wait_interval_str} seconds). '
        f'Last error: {self.errors[-1]}'
    )

  def __eq__(self, other: 'RetryError') -> bool:
    if not isinstance(other, RetryError):
      return False
    return (self.func is other.func
            and self.errors == other.errors
            and self.wait_intervals == other.wait_intervals)

  def __ne__(self, other: 'RetryError') -> bool:
    return not self.__eq__(other)

  def __hash__(self) -> int:
    return hash((
        RetryError, self.func, tuple(self.errors), tuple(self.wait_intervals)))


def with_retry(
    func: Callable[[Any], Any],
    retry_on_errors: Union[
        Union[Type[Exception], Tuple[Exception, str]],
        Sequence[Union[Type[Exception], Tuple[Exception, str]]],
    ],
    max_attempts: int,
    retry_interval: int | tuple[int, int] = (5, 60),
    exponential_backoff: bool = True,
    seed: int | None = None,
) -> Callable[..., Any]:
  """Derives a user function with retry on error.

  Args:
    func: A user function.
    retry_on_errors: A sequence of exception types or tuples of exception type
      and error messages (described in regular expression) as the desired
      exception types to retry.
    max_attempts: Max number of attempts if an error to retry is encountered.
    retry_interval: The (base) retry interval in seconds. If a tuple, the retry
      interval will be randomly chosen between the first and the second element
      of the tuple.
    exponential_backoff: If True, exponential wait time will be applied on top
      of the base retry interval.
    seed: Random seed to generate retry interval. If None, the seed will be
      determined based on current time.

  Returns:
    A function with the same signature of the input function, with the retry
    capability.
  """
  rand = random if seed is None else random.Random(seed)

  def _func(*args, **kwargs) -> Any:
    def base_interval() -> int:
      if isinstance(retry_interval, tuple):
        return rand.randint(retry_interval[0], retry_interval[1])
      else:
        assert isinstance(retry_interval, int)
        return retry_interval

    def next_wait_interval(attempt: int) -> float:
      if not exponential_backoff:
        attempt = 1
      return base_interval() * (2 ** (attempt - 1))

    wait_interval = None
    wait_intervals = []
    errors = []
    while True:
      with pg.catch_errors(retry_on_errors) as error_context:
        return func(*args, **kwargs)

      # Branch when errors are met for retry.
      errors.append(error_context.error)
      if len(errors) < max_attempts:
        wait_interval = next_wait_interval(len(errors))
        wait_intervals.append(wait_interval)

        pg.logging.warning(
            f'Calling {func!r} encountered {error_context.error!r} '
            f'(attempts={len(errors)}), retrying in {wait_interval} seconds...'
        )

        time.sleep(wait_interval)
      else:
        raise RetryError(func, errors, wait_intervals)

  return _func


def concurrent_execute(
    func: Callable[[Any], Any],
    parallel_inputs: list[Any],
    max_workers: int = 32,
    retry_on_errors: Union[
        Type[Exception],
        Tuple[Type[Exception], ...],
        None,
    ] = None,
    max_attempts: int = 5,
    retry_interval: int | tuple[int, int] = (5, 60),
    exponential_backoff: bool = True,
) -> list[Any]:
  """Executes a function concurrently under current component context.

  Args:
    func: A user function.
    parallel_inputs: The inputs for `func` which will be processed in parallel.
    max_workers: The max number of workers.
    retry_on_errors: A sequence of exception types or tuples of exception type
      and error messages (described in regular expression) as the desired
      exception types to retry.
    max_attempts: Max number of attempts if an error to retry is encountered.
    retry_interval: The (base) retry interval in seconds. If a tuple, the retry
      interval will be randomly chosen between the first and the second element
      of the tuple.
    exponential_backoff: If True, exponential wait time will be applied on top
      of the base retry interval.

  Returns:
    A list of ouputs. Each is the return value of `func` based on the input
      value. Order is preserved.
  """
  if retry_on_errors is not None:
    func = with_retry(
        func,
        retry_on_errors,
        max_attempts=max_attempts,
        retry_interval=retry_interval,
        exponential_backoff=exponential_backoff,
    )

  with concurrent.futures.ThreadPoolExecutor(
      max_workers=max_workers
  ) as executor:
    return list(executor.map(with_context_access(func), parallel_inputs))


@dataclasses.dataclass
class Job:
  """Thread pool job."""

  func: Callable[[Any], Any]
  arg: Any
  result: Any = pg.MISSING_VALUE
  error: Exception | None = None
  start_time: float | None = None
  end_time: float | None = None

  def __call__(self) -> Any:
    self.start_time = time.time()
    try:
      self.result = self.func(self.arg)
      return self.result
    except Exception as e:  # pylint: disable=broad-exception-caught
      self.error = e
      return e
    finally:
      self.end_time = time.time()

  def mark_canceled(self, error: Exception) -> None:
    """Marks the job as canceled."""
    self.error = error
    self.end_time = time.time()

  @property
  def elapse(self) -> float:
    """Returns the running time in seconds since the job get started."""
    if self.start_time is None:
      return 0.0
    if self.end_time is None:
      return time.time() - self.start_time
    return self.end_time - self.start_time


def concurrent_map(
    func: Callable[[Any], Any],
    parallel_inputs: Iterable[Any],
    *,
    executor: concurrent.futures.ThreadPoolExecutor | None = None,
    max_workers: int = 32,
    ordered: bool = False,
    show_progress: bool = False,
    timeout: int | None = None,
    silence_on_errors: Union[
        Type[Exception], Tuple[Type[Exception], ...], None
    ] = Exception,
    retry_on_errors: Union[
        Type[Exception],
        Tuple[Type[Exception], ...],
        None,
    ] = None,
    max_attempts: int = 5,
    retry_interval: int | tuple[int, int] = (5, 60),
    exponential_backoff: bool = True,
) -> Iterator[tuple[Any, Any, Exception | None]]:
  """Maps inputs to outptus via func concurrently under current context.

  Args:
    func: A user function.
    parallel_inputs: The inputs for `func` which will be processed in parallel.
    executor: Thread pool exeutor to pool work items. If None, a new thread pool
      executor will be created for current execution.
    max_workers: The max number of workers.
    ordered: If True, the returned iterator will emit (input, output, error) in
      the order of the elements in `parallel_inputs`. Otherwise, elements that
      are finished earlier will be delivered first.
    show_progress: If True, show progress on console.
    timeout: The timeout in seconds for processing each input. It is the total
      processing time for each input, even multiple retries take place. If None,
      there is no timeout.
    silence_on_errors: If None, any errors raised during processing any inputs
      will be raised. Otherwise, the matched errors will not raise, instead,
      they will be returned as the third_element of the tuple.
    retry_on_errors: A sequence of exception types or tuples of exception type
      and error messages (described in regular expression) as the desired
      exception types to retry. These errors are usually transient error.
    max_attempts: Max number of attempts if an error to retry is encountered.
    retry_interval: The (base) retry interval in seconds. If a tuple, the retry
      interval will be randomly chosen between the first and the second element
      of the tuple.
    exponential_backoff: If True, exponential wait time will be applied on top
      of the base retry interval.

  Yields:
    An iterator of (input, output, error).

  Raises:
    Exception: Erros that are not in `silence_on_errors` or `retry_on_errors`,
      or retry on such errors has reached max attempts.
  """

  if retry_on_errors:
    func = with_retry(
        func,
        retry_on_errors,
        max_attempts=max_attempts,
        retry_interval=retry_interval,
        exponential_backoff=exponential_backoff,
    )

  executor = executor or concurrent.futures.ThreadPoolExecutor(
      max_workers=max_workers)

  with executor:
    future_to_job = {}
    pending_futures = []
    total = 0
    for inputs in parallel_inputs:
      job = Job(func, inputs)
      future = executor.submit(
          with_context_access(job),
      )
      pending_futures.append(future)
      future_to_job[future] = job
      total += 1

    progress = tqdm.tqdm(total=total) if show_progress else None
    def update_progress(
        success: int,
        failure: int,
        last_error: Exception | None = None) -> None:
      if progress is not None:
        completed = success + failure
        description = 'Success: %.2f%% (%d/%d), Failure: %.2f%% (%d/%d)' % (
            success * 100.0 / completed, success, completed,
            failure * 100.0 / completed, failure, completed
        )
        progress.set_description(description)

        if last_error is not None:
          error_text = repr(last_error)
          if len(error_text) >= 64:
            error_text = error_text[:64] + '...'
          postfix = {'LastError': error_text}
          progress.set_postfix(postfix)
        progress.update(1)

    success, failure, last_error = 0, 0, None
    if ordered:
      for future in pending_futures:
        job = future_to_job[future]
        wait_time = (timeout - job.elapse) if timeout else None
        try:
          _ = future.result(timeout=wait_time)
          if job.error is not None:
            last_error = job.error
            failure += 1
            if not (
                silence_on_errors and isinstance(job.error, silence_on_errors)):
              raise job.error
          else:
            success += 1
        except concurrent.futures.TimeoutError:
          future.cancel()
          last_error = TimeoutError(
              f'Execution time ({job.elapse}) exceeds {timeout} seconds.')
          job.mark_canceled(last_error)
          failure += 1
        update_progress(success, failure, last_error)
        yield job.arg, job.result, job.error
    else:
      while pending_futures:
        completed_batch = set()
        try:
          for future in concurrent.futures.as_completed(
              pending_futures, timeout=timeout):
            job = future_to_job[future]
            del future_to_job[future]
            if job.error is not None:
              last_error = job.error
              failure += 1
              if not (
                  silence_on_errors and isinstance(job.error, silence_on_errors)
              ):
                raise job.error   # pylint: disable=g-doc-exception
            else:
              success += 1
            update_progress(success, failure, last_error)
            yield job.arg, job.result, job.error
            completed_batch.add(future)
        except concurrent.futures.TimeoutError:
          pass

        remaining_futures = []

        # When timeout is None, all future shall be completed through the loop
        # above.
        if timeout is not None:
          for future in pending_futures:
            if future in completed_batch:
              continue
            job = future_to_job[future]
            if job.elapse > timeout:
              if not future.done():
                future.cancel()
                job.mark_canceled(
                    TimeoutError(f'Execution time ({job.elapse}) '
                                 f'exceeds {timeout} seconds.'))

              if job.error is not None:
                last_error = job.error
                failure += 1
              else:
                success += 1

              update_progress(success, failure, last_error)
              yield job.arg, job.result, job.error
            else:
              remaining_futures.append(future)

        pending_futures = remaining_futures

    if progress is not None:
      progress.close()
