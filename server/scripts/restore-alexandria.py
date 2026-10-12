"""Rebuild an exact Alexandria stream with bounded intermediate disk usage.

Reuse the established record normalizer and pinned raw/normalized digests. At
most three archive outputs coexist with the final stream, rather than retaining
all archive outputs until concatenation.
"""
import argparse
import concurrent.futures
import hashlib
import itertools
import json
from pathlib import Path
import shutil
import sqlite3

from alexandria_reader import normalize_file

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / 'data/downloads/open-sources'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(4 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def normalize_verified(arguments):
    path, expected_hash, masses = arguments
    path = Path(path)
    if digest(path) != expected_hash:
        raise ValueError(f'Raw archive checksum mismatch: {path.name}')
    return normalize_file((path, masses))


def restore(key):
    from pymatgen.core import Element
    manifest = json.loads((ROOT / 'data/open-sources-manifest.json').read_text())
    entry = next(source for source in manifest['sources'] if source['key'] == key)
    acquisition = json.loads((ROOT / 'data/alexandria-acquisition-manifest.json').read_text())
    files = [item for item in acquisition['files'] if (item['file'] == 'convex_hull.json.bz2') == (key == 'alexandria-pbe-hull')]
    target = CACHE / f'{key}.jsonl'
    if target.exists():
        if digest(target) != entry['normalizedSha256']:
            raise ValueError('Existing normalized stream differs from its pinned digest; preserved.')
        print(f'{key}: existing stream matches its pinned digest', flush=True)
        return
    if shutil.disk_usage(CACHE).free < (4_300_000_000 if key == 'alexandria-pbe' else 300_000_000):
        raise ValueError('Insufficient free space for the bounded restoration.')
    source = {field: entry[field] for field in ['key', 'name', 'url', 'license', 'kind', 'version', 'checksum', 'note']}
    masses = {str(element): float(element.atomic_mass) for element in Element}
    partial = target.with_suffix('.restore.partial')
    ids_path = target.with_suffix('.restore-ids.sqlite')
    if partial.exists() or ids_path.exists():
        raise ValueError('An earlier restoration partial exists; preserve and inspect it before retrying.')
    identifiers = sqlite3.connect(ids_path)
    identifiers.execute('CREATE TABLE ids (accession TEXT PRIMARY KEY)')
    count, coverage = 0, {}
    try:
        with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor, partial.open('wb') as output:
            output.write((json.dumps({'source': source, 'records': entry['records']}) + '\n').encode())
            pending = []
            next_file = iter(files)
            def submit(item):
                return executor.submit(normalize_verified, (str(CACHE / 'alexandria' / item['file']), item['sha256'], masses))
            for item in itertools.islice(next_file, 3):
                pending.append(submit(item))
            while pending:
                result = pending.pop(0).result()
                with open(result['ids']) as accessions:
                    while batch := list(itertools.islice(accessions, 10000)):
                        identifiers.executemany('INSERT INTO ids VALUES (?)', [(line.strip(),) for line in batch])
                identifiers.commit()
                with open(result['path'], 'rb') as records:
                    shutil.copyfileobj(records, output)
                count += result['count']
                for field, value in result['coverage'].items():
                    coverage[field] = coverage.get(field, 0) + value
                Path(result['path']).unlink()
                Path(result['ids']).unlink()
                print(f'{key}: {count:,}/{entry["records"]:,} records reconstructed', flush=True)
                item = next(next_file, None)
                if item is not None:
                    pending.append(submit(item))
        if count != entry['records'] or coverage != entry['coverage']:
            raise ValueError('Reconstructed counts/coverage differ from the pinned manifest.')
        if digest(partial) != entry['normalizedSha256']:
            raise ValueError('Reconstructed normalized SHA-256 differs from the pinned manifest.')
        partial.replace(target)
        print(f'{key}: restored with exact original SHA-256; {count:,} unique source accessions', flush=True)
    finally:
        identifiers.close()
        ids_path.unlink()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', choices=['alexandria-pbe', 'alexandria-pbe-hull'])
    restore(parser.parse_args().source)
