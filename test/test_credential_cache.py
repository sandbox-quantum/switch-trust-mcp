"""Unit tests for the per-credential client cache and rate limiter.

Hermetic: no network, no real Switch Trust client — the cache is exercised
with a trivial factory and the rate limiter with a fake clock, so timing is
deterministic.
"""

import pytest

from switch_trust_mcp.credential_cache import (
    ClientCache,
    RateLimiter,
    RateLimitExceeded,
    hash_api_key,
)

# --------------------------------------------------------------------------
# hash_api_key
# --------------------------------------------------------------------------


class TestHashApiKey:
    def test_deterministic(self):
        assert hash_api_key("sk_abc123") == hash_api_key("sk_abc123")

    def test_different_keys_different_hashes(self):
        assert hash_api_key("sk_abc123") != hash_api_key("sk_abc124")

    def test_does_not_contain_raw_key(self):
        assert "sk_abc123" not in hash_api_key("sk_abc123")

    def test_rejects_empty_key(self):
        with pytest.raises(ValueError):
            hash_api_key("")


# --------------------------------------------------------------------------
# ClientCache
# --------------------------------------------------------------------------


class TestClientCache:
    def test_factory_called_once_per_key(self):
        calls = []

        def factory(api_key):
            calls.append(api_key)
            return object()

        cache = ClientCache(factory)
        cache.get("sk_a")
        cache.get("sk_a")
        cache.get("sk_a")
        assert calls == ["sk_a"]

    def test_different_keys_get_different_clients(self):
        cache = ClientCache(lambda api_key: object())
        client_a = cache.get("sk_a")
        client_b = cache.get("sk_b")
        assert client_a is not client_b
        assert len(cache) == 2

    def test_cache_keys_are_hashed_not_raw(self):
        cache = ClientCache(lambda api_key: object())
        cache.get("sk_super_secret")
        assert "sk_super_secret" not in cache._entries
        assert hash_api_key("sk_super_secret") in cache._entries

    def test_evicts_least_recently_used_past_max_entries(self):
        cache = ClientCache(lambda api_key: api_key, max_entries=2)
        cache.get("sk_a")
        cache.get("sk_b")
        cache.get("sk_c")  # evicts sk_a, the least recently used
        assert len(cache) == 2
        calls = []

        def factory(api_key):
            calls.append(api_key)
            return api_key

        cache = ClientCache(factory, max_entries=2)
        cache.get("sk_a")
        cache.get("sk_b")
        cache.get("sk_a")  # touches sk_a, so sk_b becomes least recently used
        cache.get("sk_c")  # evicts sk_b, not sk_a
        assert calls == ["sk_a", "sk_b", "sk_c"]
        cache.get("sk_a")  # still cached: no second factory call
        assert calls == ["sk_a", "sk_b", "sk_c"]

    def test_rejects_non_positive_max_entries(self):
        with pytest.raises(ValueError):
            ClientCache(lambda api_key: object(), max_entries=0)


# --------------------------------------------------------------------------
# RateLimiter
# --------------------------------------------------------------------------


class TestRateLimiter:
    def test_allows_up_to_burst_immediately(self):
        limiter = RateLimiter(rate=1, burst=3)
        limiter.acquire("sk_a")
        limiter.acquire("sk_a")
        limiter.acquire("sk_a")  # exactly burst, should not raise

    def test_raises_once_burst_exhausted(self):
        limiter = RateLimiter(rate=1, burst=2)
        limiter.acquire("sk_a")
        limiter.acquire("sk_a")
        with pytest.raises(RateLimitExceeded):
            limiter.acquire("sk_a")

    def test_keys_are_independent(self):
        limiter = RateLimiter(rate=1, burst=1)
        limiter.acquire("sk_a")
        limiter.acquire("sk_b")  # independent bucket, should not raise

    def test_refills_over_time(self, monkeypatch):
        now = [1000.0]
        monkeypatch.setattr(
            "switch_trust_mcp.credential_cache.time.monotonic", lambda: now[0]
        )
        limiter = RateLimiter(rate=1, burst=1)
        limiter.acquire("sk_a")
        with pytest.raises(RateLimitExceeded):
            limiter.acquire("sk_a")
        now[0] += 1.0  # one token's worth of time passes
        limiter.acquire("sk_a")  # should not raise: bucket refilled

    def test_cost_can_exceed_one(self, monkeypatch):
        now = [1000.0]
        monkeypatch.setattr(
            "switch_trust_mcp.credential_cache.time.monotonic", lambda: now[0]
        )
        limiter = RateLimiter(rate=1, burst=10)
        limiter.acquire("sk_a", cost=8)
        with pytest.raises(RateLimitExceeded):
            limiter.acquire("sk_a", cost=5)  # only 2 tokens left
        limiter.acquire("sk_a", cost=2)  # exactly what remains

    def test_retry_after_reflects_deficit(self, monkeypatch):
        now = [1000.0]
        monkeypatch.setattr(
            "switch_trust_mcp.credential_cache.time.monotonic", lambda: now[0]
        )
        limiter = RateLimiter(rate=2, burst=1)
        limiter.acquire("sk_a")
        with pytest.raises(RateLimitExceeded) as exc_info:
            limiter.acquire("sk_a")
        # Deficit is ~1 token at rate=2/sec, so retry_after is ~0.5s.
        assert exc_info.value.retry_after_seconds == pytest.approx(0.5)

    def test_rejects_non_positive_rate_or_burst(self):
        with pytest.raises(ValueError):
            RateLimiter(rate=0, burst=1)
        with pytest.raises(ValueError):
            RateLimiter(rate=1, burst=0)

    def test_rejects_non_positive_cost(self):
        limiter = RateLimiter(rate=1, burst=1)
        with pytest.raises(ValueError):
            limiter.acquire("sk_a", cost=0)
