#!/usr/bin/env python3
import hashlib
import os
import sys

START_PATH = "."
if len(sys.argv) > 1:
    START_PATH = sys.argv[1]
EXTENSIONS = ["png", "jpg", "jpeg", "bmp"]
EXISTING_HASHES = set()
HASH_TO_PATH = dict()


def crawl(path: str) -> list:
    duplicates = []
    for rel_path, dirs, files in os.walk(path):
        for f in files:
            if f[f.find(".") + 1:] in EXTENSIONS:
                full_path = os.path.join(rel_path, f)
                print(full_path)
                file = open(full_path, "rb")
                hash = hashlib.md5(file.read()).hexdigest()
                file.close()
                if hash in EXISTING_HASHES:
                    existing = HASH_TO_PATH[hash]
                    if existing != full_path:
                        duplicates.append((full_path, existing))
                else:
                    EXISTING_HASHES.add(hash)
                    HASH_TO_PATH[hash] = full_path
    return duplicates


duplicates = crawl(START_PATH)

if len(duplicates) == 0:
    print("No duplicates found")

for case in duplicates:
    print("\"" + case[0] + "\"", "is a duplicate of", "\"" + case[1] + "\"")
