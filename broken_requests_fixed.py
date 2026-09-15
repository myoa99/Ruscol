import requests


def fetch_json_safely(url: str, timeout_sec: int = 5) -> dict:
    try:
        response = requests.get(url, timeout=timeout_sec)
    except requests.exceptions.Timeout:
        print(f"[ERROR] Request timed out after {timeout_sec} seconds: {url}")
        return {}
    except requests.exceptions.RequestException as error:
        print(f"[ERROR] Network error: {error}")
        return {}

    if not response.ok:
        print(
            f"[ERROR] HTTP request failed: "
            f"status_code={response.status_code}, url={response.url}"
        )
        return {}

    try:
        data = response.json()
    except ValueError:
        print(f"[ERROR] Response is not valid JSON: {response.url}")
        return {}

    print(f"[OK] JSON response received: {response.url}")
    return data


def main() -> None:
    print("\n=== Test 1: slow response ===")
    fetch_json_safely(
        "https://httpbin.org/delay/10",
        timeout_sec=3,
    )

    print("\n=== Test 2: HTTP 404 ===")
    fetch_json_safely(
        "https://httpbin.org/status/404",
        timeout_sec=5,
    )

    print("\n=== Test 3: non-JSON response ===")
    fetch_json_safely(
        "https://httpbin.org/html",
        timeout_sec=5,
    )

    print("\n=== Test 4: valid JSON response ===")
    data = fetch_json_safely(
        "https://httpbin.org/json",
        timeout_sec=5,
    )

    if data:
        print("[INFO] Top-level keys:", list(data.keys()))


if __name__ == "__main__":
    main()