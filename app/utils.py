import requests
import time
import logging


def _request_with_retry(url, headers=None, timeout=10, retries=2):
    """Helper to fetch an URL with exponential backoff on failure."""
    for attempt in range(retries + 1):
        try:
            res = requests.get(url, headers=headers, timeout=timeout)
            if res.status_code == 200:
                return res
            logging.warning(
                f"Request failed with status {res.status_code} for {url}"
            )
        except Exception as e:
            logging.exception("Unexpected error")
            logging.warning(
                f"Request exception on attempt {attempt + 1}/{retries + 1} for {url}: {e}"
            )
        if attempt < retries:
            time.sleep(1 * 2**attempt)
    raise Exception(f"Failed to fetch {url} after {retries + 1} attempts")