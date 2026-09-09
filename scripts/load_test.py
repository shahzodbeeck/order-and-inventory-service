import os
import uuid
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8080")
STOCK_QUANTITY = 10
PARALLEL_REQUESTS = 50


def register_and_login() -> str:
    email = f"loadtest-{uuid.uuid4()}@example.com"
    password = "load-test-pass-123"

    resp = requests.post(
        f"{BASE_URL}/auth/register/",
        json={"email": email, "password": password},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["access"]


def create_product(token: str) -> str:
    resp = requests.post(
        f"{BASE_URL}/products",
        json={"name": "Load Test Product", "price": "9.99", "stock_quantity": STOCK_QUANTITY},
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["id"]


def place_order(token: str, product_id: str) -> int:
    resp = requests.post(
        f"{BASE_URL}/orders",
        json={"items": [{"product_id": product_id, "quantity": 1}]},
        headers={
            "Authorization": f"Bearer {token}",
            "Idempotency-Key": str(uuid.uuid4()),
        },
        timeout=10,
    )
    return resp.status_code


def main():
    token = register_and_login()
    product_id = create_product(token)

    print(f"Product {product_id} created with stock_quantity={STOCK_QUANTITY}")
    print(f"Firing {PARALLEL_REQUESTS} parallel POST /orders requests...")

    results = []
    with ThreadPoolExecutor(max_workers=PARALLEL_REQUESTS) as executor:
        futures = [
            executor.submit(place_order, token, product_id)
            for _ in range(PARALLEL_REQUESTS)
        ]
        for future in as_completed(futures):
            results.append(future.result())

    counts = Counter(results)
    print("Status code counts:", dict(counts))

    success = counts.get(201, 0)
    conflict = counts.get(409, 0) + counts.get(422, 0)

    print(f"Successful (201): {success}")
    print(f"Rejected (409/422): {conflict}")

    if success == STOCK_QUANTITY:
        print(f"PASS: exactly {STOCK_QUANTITY} orders succeeded")
    else:
        print(f"FAIL: expected {STOCK_QUANTITY} successes, got {success}")


if __name__ == "__main__":
    main()
