#!/usr/bin/env python3
from huggingface_hub import HfApi
import time

# ==== Configuration ====

REPO_ID = ""   # Your HF repo, for example: cortexso/qwen3
BRANCH = ""                         # Branch to clean, for example: 14b
FILES_TO_KEEP = [                     # Files to keep (exact match, at root)
    ".gitattributes",
    "metadata.yml",
    "model.gguf",
    "model.yml"
]

# ========================

def clean_branch_via_api(repo_id: str, branch: str, files_to_keep: list):
    api = HfApi()

    print(f"\nListing files in branch '{branch}' of repo '{repo_id}'...")
    all_files = api.list_repo_files(repo_id=repo_id, revision=branch)
    print(f"✓ Found {len(all_files)} files")

    # Delete all files not in the keep list
    for file in all_files:
        if file not in files_to_keep:
            print(f"Deleting: {file}")
            try:
                api.delete_file(
                    path_in_repo=file,
                    repo_id=repo_id,
                    repo_type="model",
                    revision=branch,
                )
                time.sleep(0.5)  # small delay to avoid rate limiting
            except Exception as e:
                print(f"✗ Failed to delete {file}: {e}")
    
    print(f"\n✓ Cleanup complete for branch '{branch}'.")

if __name__ == "__main__":
    clean_branch_via_api(REPO_ID, BRANCH, FILES_TO_KEEP)
