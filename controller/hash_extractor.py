import gzip
from pathlib import Path
from time import time
import hashlib
import os

from dotenv import load_dotenv

load_dotenv()
TEST_PATH = os.environ.get('ROOT_DIRECTORY_PATH')
BASE_DB_DIRECTORY = f'{TEST_PATH}.beaver'

if not os.path.isdir(BASE_DB_DIRECTORY):
    os.mkdir(BASE_DB_DIRECTORY, 0o777)

def _read_file_to_bytes(file_path: str) -> bytes:
    return Path(f'{TEST_PATH}{file_path}').read_bytes()

def _extract_sha1_hash_from_file_content(content: bytes) -> str:
    return hashlib.sha1(content).hexdigest()


def _compress_file_by_path(content: bytes) -> bytes:
    return gzip.compress(data=content)

def _save_compressed_file(file_name: str, content: bytes) -> None:
    with gzip.open(f'{BASE_DB_DIRECTORY}/{file_name}.gz', 'wb') as file:
        file.write(content)


def beaver_add(file_path: str) -> dict[str, float]:
    content = _read_file_to_bytes(file_path)
    file_hash = _extract_sha1_hash_from_file_content(content)
    compressed_content = _compress_file_by_path(content)
    _save_compressed_file(file_hash, compressed_content)
    return {file_hash: time()}


if __name__ == '__main__':
    base_path = f'dummy.py'
    db_value = beaver_add(base_path)
    print(db_value)
