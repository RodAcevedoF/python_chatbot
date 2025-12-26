#!/usr/bin/env python
import argparse
import subprocess
import sys
import os
from pathlib import Path


def reindex(dry_run: bool = False):
    """Re-index hotel data into Supabase."""
    cmd = [sys.executable, "-m", "app.scripts.embeddings_test"]
    if dry_run:
        cmd.append("--dry-run")
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


def check_env():
    """Check if required environment variables are set."""
    required_vars = [
        "SUPABASE_URL",
        "SUPABASE_KEY",
        "OPENAI_API_KEY"
    ]
    
    print("Checking environment variables...\n")
    
    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            masked = value[:8] + "..." if len(value) > 8 else "***"
            print(f"✓ {var}: {masked}")
        else:
            print(f"✗ {var}: NOT SET")
            all_set = False
    
    if all_set:
        print("\n✓ All required environment variables are set!")
        sys.exit(0)
    else:
        print("\n✗ Some environment variables are missing. Check your .env file.")
        sys.exit(1)


def run_server():
    """Start the FastAPI server."""
    cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--host", "127.0.0.1", "--port", "8000"]
    print(f"Starting server: {' '.join(cmd)}")
    subprocess.run(cmd)


def main():
    parser = argparse.ArgumentParser(description="Hotel Chatbot CLI Management Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    reindex_parser = subparsers.add_parser("reindex", help="Re-index hotel data into Supabase")
    reindex_parser.add_argument("--dry-run", action="store_true", help="Preview documents without indexing")
    
    subparsers.add_parser("check-env", help="Check if environment variables are set")
    
    subparsers.add_parser("run-server", help="Start the FastAPI server")
    
    args = parser.parse_args()
    
    if args.command == "reindex":
        reindex(dry_run=args.dry_run)
    elif args.command == "check-env":
        check_env()
    elif args.command == "run-server":
        run_server()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
