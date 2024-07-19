import hashlib
import os
import shutil

def get_hash(filepath):
    """Calculates MD5 and SHA-256 hashes for a file."""
    with open(filepath, 'rb') as f:
        data = f.read()
        md5_hash = hashlib.md5(data).hexdigest()
        sha256_hash = hashlib.sha256(data).hexdigest()
        return md5_hash, sha256_hash

def find_duplicates(directory):
    """Finds duplicate files in a directory based on size, MD5, and SHA-256."""
    duplicates = {}  # Dictionary to store duplicates, key: hash tuple, value: list of filepaths
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            filesize = os.path.getsize(filepath)
            md5_hash, sha256_hash = get_hash(filepath)
            file_hash = (filesize, md5_hash, sha256_hash)

            if file_hash not in duplicates:
                duplicates[file_hash] = []
            duplicates[file_hash].append(filepath)

    # Filter duplicates (remove entries with only one file)
    actual_duplicates = {key: values for key, values in duplicates.items() if len(values) > 1}

    return actual_duplicates

def print_duplicates(duplicates):
    """Prints information about duplicate files and automatically deletes duplicates (except the first)."""
    if duplicates:
        print("\nDuplicate Files:")
        for file_hash, filepaths in duplicates.items():
            filesize, md5_hash, sha256_hash = file_hash
            print(f"File size: {filesize} bytes")
            print(f"MD5 hash: {md5_hash}")
            print(f"SHA-256 hash: {sha256_hash}")
            print(f"Duplicate Files:")
            for i, filepath in enumerate(filepaths):
                print(f"\t- File {i + 1}: {filepath}")

            # Automatically delete duplicates (except the first one)
            for filepath in filepaths[1:]:
                os.remove(filepath)
                print(f"Deleted: {filepath}")
            print("-" * 40)
    else:
        print("No duplicate files found.")


if __name__ == "__main__":
    # Get the directory path from the user
    directory = input("Enter the directory path: ")

    # Find and print duplicate files
    duplicates = find_duplicates(directory)
    print_duplicates(duplicates)
