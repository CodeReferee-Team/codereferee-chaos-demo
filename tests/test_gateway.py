import io
import os
from unittest.mock import patch

from app.main import proxy_item


def test_gateway_returns_the_upstream_item():
    with patch.dict(os.environ, UPSTREAM_URL="http://api:8000"):
        with patch("app.main.urlopen", return_value=io.BytesIO(b'{"item_id": 7}')) as request:
            assert proxy_item(7) == {"item_id": 7}
    request.assert_called_once_with("http://api:8000/items/7", timeout=2)
