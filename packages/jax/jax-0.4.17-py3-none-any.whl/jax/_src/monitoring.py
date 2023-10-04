# Copyright 2022 The JAX Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utilities for instrumenting code.

Code points can be marked as a named event. Every time an event is reached
during program execution, the registered listeners will be invoked.

A typical listener callback is to send an event to a metrics collector for
aggregation/exporting.
"""
from typing import Callable, Protocol, Union


class EventListenerWithMetadata(Protocol):

  def __call__(self, event: str, **kwargs: Union[str, int]) -> None:
    ...


_event_listeners_with_metadata: list[EventListenerWithMetadata] = []
_event_listeners: list[Callable[[str], None]] = []
_event_duration_secs_listeners: list[Callable[[str, float], None]] = []


def record_event(event: str, **kwargs: Union[str, int]) -> None:
  """Record an event."""
  if not kwargs:
    for callback in _event_listeners:
      callback(event)
  else:
    for callback in _event_listeners_with_metadata:
      callback(event, **kwargs)


def record_event_duration_secs(event: str, duration: float) -> None:
  """Record an event duration in seconds (float)."""
  for callback in _event_duration_secs_listeners:
    callback(event, duration)

def register_event_listener(callback: Callable[[str], None]) -> None:
  """Register a callback to be invoked during record_event()."""
  _event_listeners.append(callback)


# TODO(b/301446522): Merge this function with register_event_listener.
def register_event_listener_with_kwargs(
    callback: EventListenerWithMetadata,
) -> None:
  """Register a callback to be invoked during record_event()."""
  _event_listeners_with_metadata.append(callback)


def register_event_duration_secs_listener(
    callback : Callable[[str, float], None]) -> None:
  """Register a callback to be invoked during record_event_duration_secs()."""
  _event_duration_secs_listeners.append(callback)

def get_event_duration_listeners() -> list[Callable[[str, float], None]]:
  """Get event duration listeners."""
  return list(_event_duration_secs_listeners)

def get_event_listeners() -> list[Callable[[str], None]]:
  """Get event listeners."""
  return list(_event_listeners)

def _clear_event_listeners():
  """Clear event listeners."""
  global _event_listeners, _event_duration_secs_listeners
  _event_listeners = []
  _event_duration_secs_listeners = []

def _unregister_event_duration_listener_by_callback(
    callback: Callable[[str, float], None]) -> None:
  """Unregister an event duration listener by callback.

  This function is supposed to be called for testing only.
  """
  assert callback in _event_duration_secs_listeners
  _event_duration_secs_listeners.remove(callback)

def _unregister_event_duration_listener_by_index(index: int) -> None:
  """Unregister an event duration listener by index.

  This function is supposed to be called for testing only.
  """
  size = len(_event_duration_secs_listeners)
  assert -size <= index < size
  del _event_duration_secs_listeners[index]

def _unregister_event_listener_by_callback(
    callback: Callable[[str], None]) -> None:
  """Unregister an event listener by callback.

  This function is supposed to be called for testing only.
  """
  assert callback in _event_listeners
  _event_listeners.remove(callback)
