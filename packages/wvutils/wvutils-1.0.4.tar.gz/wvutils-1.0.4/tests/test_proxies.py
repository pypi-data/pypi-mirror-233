import pytest

from wvutils.proxies import (
    ProxyManager,
    https_to_http,
    prepare_http_proxy_for_requests,
)


@pytest.mark.parametrize(
    "address, expected",
    [
        ("https://localhost:8080", "http://localhost:8080"),
        ("http://localhost:8080", "http://localhost:8080"),
    ],
)
def test_https_to_http(address, expected):
    assert https_to_http(address) == expected


@pytest.mark.parametrize("address", ["localhost:8080", "ftp://localhost:8080", ""])
def test_https_to_http_invalid_address(address):
    with pytest.raises(ValueError, match=r"Invalid proxy address: .+"):
        https_to_http(address)


@pytest.mark.parametrize(
    "address, expected",
    [
        (
            "https://localhost:8080",
            {
                "https_proxy": "https://localhost:8080",
                "http_proxy": "http://localhost:8080",
                "HTTPS_PROXY": "https://localhost:8080",
                "HTTP_PROXY": "http://localhost:8080",
            },
        ),
        (
            "http://localhost:8080",
            {
                "https_proxy": "http://localhost:8080",
                "http_proxy": "http://localhost:8080",
                "HTTPS_PROXY": "http://localhost:8080",
                "HTTP_PROXY": "http://localhost:8080",
            },
        ),
    ],
)
def test_prepare_http_proxy_for_requests(address, expected):
    assert prepare_http_proxy_for_requests(address) == expected


@pytest.mark.parametrize("address", ["localhost:8080", "ftp://localhost:8080", ""])
def test_prepare_http_proxy_for_requests_raises_ValueError_for_invalid_address(address):
    with pytest.raises(ValueError, match=r"Invalid proxy address: .+"):
        prepare_http_proxy_for_requests(address)


def test_proxy_manager():
    proxies = ["https://proxy1.com", "https://proxy2.com", "https://proxy3.com"]
    proxy_manager = ProxyManager(proxies, reuse=True)
    # First cycle
    assert proxy_manager.proxy == proxies[0]
    assert proxy_manager.can_cycle
    # Second cycle
    proxy_manager.cycle()
    assert proxy_manager.proxy == proxies[1]
    assert proxy_manager.can_cycle
    # Third cycle
    proxy_manager.cycle()
    assert proxy_manager.proxy == proxies[2]
    assert proxy_manager.can_cycle
    # Cycle back to the first proxy
    proxy_manager.cycle()
    assert proxy_manager.proxy == proxies[0]
    assert proxy_manager.can_cycle


def test_proxy_manager_no_reuse():
    proxies = ["https://proxy1.com", "https://proxy2.com", "https://proxy3.com"]
    proxy_manager = ProxyManager(proxies, reuse=False)
    # First cycle
    assert proxy_manager.proxy == proxies[0]
    assert proxy_manager.can_cycle
    # Second cycle
    proxy_manager.cycle()
    assert proxy_manager.proxy == proxies[1]
    assert proxy_manager.can_cycle
    # Third cycle
    proxy_manager.cycle()
    assert proxy_manager.proxy == proxies[2]
    assert not proxy_manager.can_cycle
    # Fourth cycle (no proxies left)
    proxy_manager.cycle()
    assert proxy_manager.proxy is None
    assert not proxy_manager.can_cycle


def test_proxy_manager_no_proxies():
    proxy_manager = ProxyManager([], reuse=True)
    # No proxies
    assert proxy_manager.proxy is None
    assert not proxy_manager.can_cycle
    # Still no proxies
    with pytest.warns(UserWarning, match=r"Attempted to cycle a locked proxy manager"):
        proxy_manager.cycle()
    assert proxy_manager.proxy is None
    assert not proxy_manager.can_cycle


def test_proxy_manager_no_proxies_no_reuse():
    proxy_manager = ProxyManager([], reuse=False)
    # No proxies
    assert proxy_manager.proxy is None
    assert not proxy_manager.can_cycle
    # Still no proxies
    with pytest.warns(UserWarning, match=r"Attempted to cycle a locked proxy manager"):
        proxy_manager.cycle()
    assert proxy_manager.proxy is None
    assert not proxy_manager.can_cycle
