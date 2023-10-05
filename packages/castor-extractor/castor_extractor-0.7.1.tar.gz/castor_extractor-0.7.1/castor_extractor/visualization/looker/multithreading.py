import logging
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import List, Set

from tqdm import tqdm  # type: ignore

from . import ApiClient
from .api.sdk import Folder
from .assets import LookerAsset

logger = logging.getLogger(__name__)


def _make_api_request(
    client: ApiClient,
    asset: LookerAsset,
    folder_id: str,
) -> List:
    """
    Calls the appropriate Looker API endpoint to retrieve either Looks or
    Dashboards withered by the given folder ID.
    """
    if asset == LookerAsset.LOOKS:
        return client.looks(folder_id=folder_id)
    return client.dashboards(folder_id=folder_id)


def fetch_assets_with_parallelization(
    folder_ids: Set[str],
    client: ApiClient,
    asset: LookerAsset,
    thread_pool_size: int,
) -> List:
    """
    Fetches Looks or Dashboards with a request per folder ID. Requests are
    parallelised.
    """
    final_assets = []
    total_folders = len(folder_ids)
    _fetch = partial(_make_api_request, client, asset)

    with ThreadPoolExecutor(max_workers=thread_pool_size) as executor:
        fetch_results = executor.map(_fetch, folder_ids)

        for result in tqdm(fetch_results, total=total_folders):
            final_assets.extend(result)

    logger.info(f"Fetched {len(final_assets)} {asset.value}")
    return final_assets
