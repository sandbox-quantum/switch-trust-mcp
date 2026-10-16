"""Per-credential client cache and rate limiting for a multi-tenant deployment.

Today this package is a single-user stdio server: one process, one OS
environment, one ``SwitchTrustClient`` for its whole lifetime (see
``server.py``'s module-level ``_client`` singleton). A hosted deployment that
accepts a different Switch Trust API key per connection instead needs two
things a single-user process never did:

- a client cache keyed by *credential*, not by the raw secret itself, so a
  heap dump, debugger watch, or accidental log of a dict's keys does not
  trivially enumerate live API keys;
- a per-credential rate limit, so one caller cannot turn the backend-request
  budget a single tool call already enforces (``server.py``'s
  ``find_issues_for_file`` bounds one call to 300 backend requests) into
  unbounded backend load by making that call in a tight loop.

Not wired into ``server.py`` yet: this is the credential-isolation building
block for that work, developed and tested on its own first.
"""

from __future__ import annotations

import hashlib
import threading
import time
from collections import OrderedDict
from collections.abc import Callable
from typing import Generic, TypeVar

ClientT = TypeVar("ClientT")


def hash_api_key(api_key: str) -> str:
    """One-way pseudonym for an API key, safe to use as a cache or log key.

    Switch Trust API keys are high-entropy random secrets, not low-entropy
    human-chosen passwords, so a plain SHA-256 digest is not reversible by a
    dictionary or rainbow-table attack the way an unsalted password hash would
    be. This only protects the *cache's keys* from casual enumeration — the
    cached client value still holds the live key internally, because it needs
    it to authenticate requests. That value's own ``__repr__`` is scrubbed
    separately (see ``client.py``'s ``_ScrubbedAuthenticatedClient``); this
    function does not change that, it only keeps the raw secret out of the
    cache's key space.
    """
    if not api_key:
        raise ValueError("api_key must be non-empty")
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()


class ClientCache(Generic[ClientT]):
    """Bounded cache of per-credential clients, keyed by ``hash_api_key``.

    A hosted server sees a bounded, slowly changing set of real tenants but an
    unbounded set of *attempted* keys (typos, revoked keys, abuse probes).
    Keying by hash and evicting the least-recently-used entry past
    ``max_entries`` keeps memory bounded without needing to know the tenant
    count in advance.

    ``factory`` is called with the *raw* ``api_key`` (not the hash) on a cache
    miss, since the client needs the real key to authenticate; only the cache's
    own key space is pseudonymized.
    """

    def __init__(
        self, factory: Callable[[str], ClientT], max_entries: int = 1000
    ) -> None:
        if max_entries < 1:
            raise ValueError("max_entries must be at least 1")
        self._factory = factory
        self._max_entries = max_entries
        self._entries: OrderedDict[str, ClientT] = OrderedDict()
        self._lock = threading.Lock()

    def get(self, api_key: str) -> ClientT:
        key = hash_api_key(api_key)
        with self._lock:
            client = self._entries.get(key)
            if client is not None:
                self._entries.move_to_end(key)
                return client
            client = self._factory(api_key)
            self._entries[key] = client
            if len(self._entries) > self._max_entries:
                self._entries.popitem(last=False)
            return client

    def __len__(self) -> int:
        with self._lock:
            return len(self._entries)


class RateLimitExceeded(Exception):
    """Raised when a credential has exhausted its request budget."""

    def __init__(self, retry_after_seconds: float) -> None:
        self.retry_after_seconds = retry_after_seconds
        super().__init__(
            "Rate limit exceeded for this API key. Retry after "
            f"{retry_after_seconds:.1f}s."
        )


class RateLimiter:
    """Per-credential token bucket, keyed by ``hash_api_key``.

    One bucket per credential, refilled continuously at ``rate`` tokens/sec up
    to ``burst`` tokens. Call ``acquire(api_key, cost)`` before doing
    backend-request work; it raises ``RateLimitExceeded`` instead of blocking,
    so a tool handler can surface a clear, immediate error rather than stall a
    request waiting for tokens to refill.

    ``cost`` lets one call spend more than one token. A single
    ``find_issues_for_file`` call can fan out to hundreds of backend requests
    (bounded per-call by ``server.py``'s own request budget); charging it
    proportionally to the backend requests it actually made stops a caller
    from running that in a tight loop and turning a per-call cap into
    unbounded requests-per-second against the backend.

    One lock guards every bucket. Each acquisition only does a handful of
    arithmetic operations under the lock, so this does not become a
    throughput bottleneck at the request rates a single backend instance can
    take in the first place; it trades a little contention for not having to
    reason about per-key lock lifecycles.
    """

    def __init__(self, rate: float, burst: float) -> None:
        if rate <= 0 or burst <= 0:
            raise ValueError("rate and burst must be positive")
        self._rate = rate
        self._burst = burst
        # hash(api_key) -> (tokens available, last refill timestamp)
        self._buckets: dict[str, tuple[float, float]] = {}
        self._lock = threading.Lock()

    def acquire(self, api_key: str, cost: float = 1.0) -> None:
        if cost <= 0:
            raise ValueError("cost must be positive")
        key = hash_api_key(api_key)
        now = time.monotonic()
        with self._lock:
            tokens, last_refill = self._buckets.get(key, (self._burst, now))
            tokens = min(self._burst, tokens + (now - last_refill) * self._rate)
            if tokens < cost:
                self._buckets[key] = (tokens, now)
                raise RateLimitExceeded(
                    retry_after_seconds=(cost - tokens) / self._rate
                )
            self._buckets[key] = (tokens - cost, now)

    def __len__(self) -> int:
        with self._lock:
            return len(self._buckets)
