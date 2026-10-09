from datetime import datetime, timezone
from decimal import Decimal

from app.market.models import TokenMarket
from app.market.scanner import TokenScanner


token = TokenMarket(
    address="TEST",
    symbol="TEST",
    name="Test Token",
    liquidity_usd=Decimal("50000"),
    volume_5m_usd=Decimal("20000"),
    buys_5m=20,
    updated_at=datetime.now(timezone.utc),
)

scanner = TokenScanner()

result = scanner.filter_candidates([token])

print("SCANNER TEST")
print("Candidates:", len(result))

if len(result) == 1:
    print("SCANNER OK")
else:
    print("SCANNER FAILED")