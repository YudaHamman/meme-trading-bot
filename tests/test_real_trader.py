from decimal import Decimal

import httpx
import pytest
from solders.keypair import Keypair

from app.config.settings import settings
from app.execution.real_trader import RealSolanaTrader


def make_trader(monkeypatch, handler):
    monkeypatch.setattr(
        settings,
        "real_trading_enabled",
        True,
    )

    trader = RealSolanaTrader(
        api_key="test-api-key",
        base_url="https://example.test/swap/v2",
        private_key=str(Keypair()),
        max_trade_usd=Decimal("5"),
    )
    trader.client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        timeout=20,
    )

    return trader


def test_usd_to_input_amount_rejects_oversized_trade(monkeypatch):
    trader = make_trader(
        monkeypatch,
        lambda request: httpx.Response(200, json={}),
    )

    with pytest.raises(ValueError):
        trader.usd_to_input_amount(
            Decimal("6"),
            Decimal("150"),
        )


async def test_create_order_sends_expected_jupiter_request(monkeypatch):
    requests = []

    def handler(request):
        requests.append(request)

        return httpx.Response(
            200,
            json={
                "requestId": "req-1",
                "transaction": "ZmFrZQ==",
                "outAmount": "100",
                "router": "metis",
                "mode": "manual",
            },
        )

    trader = make_trader(
        monkeypatch,
        handler,
    )

    order = await trader.create_order(
        output_mint="TokenMint",
        amount=12345,
    )

    assert order.request_id == "req-1"
    assert order.transaction == "ZmFrZQ=="

    request = requests[0]

    assert request.url.path == "/swap/v2/order"
    assert request.headers["x-api-key"] == "test-api-key"
    assert request.url.params["inputMint"] == trader.input_mint
    assert request.url.params["outputMint"] == "TokenMint"
    assert request.url.params["amount"] == "12345"
    assert request.url.params["taker"] == trader.wallet_address


async def test_execute_order_posts_signed_transaction(monkeypatch):
    requests = []

    def handler(request):
        requests.append(request)

        return httpx.Response(
            200,
            json={
                "status": "Success",
                "signature": "abc",
                "code": 0,
            },
        )

    trader = make_trader(
        monkeypatch,
        handler,
    )

    result = await trader.execute_order(
        signed_transaction="signed",
        request_id="req-1",
        last_valid_block_height=123,
    )

    assert result["status"] == "Success"

    request = requests[0]

    assert request.url.path == "/swap/v2/execute"
    assert request.headers["x-api-key"] == "test-api-key"
    assert request.read()
    assert b"req-1" in request.content
    assert b"signed" in request.content
    assert b"123" in request.content
