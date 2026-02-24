#!/usr/bin/env python
"""Simple seed helper for local development."""

import os
import subprocess
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    commands = [
        [sys.executable, 'manage.py', 'migrate'],
        [sys.executable, 'manage.py', 'loaddata', 'modules/store/fixtures/store_data.json'],
    ]

    for cmd in commands:
        print('Running:', ' '.join(cmd))
        result = subprocess.run(cmd, check=False)
        if result.returncode != 0:
            return result.returncode

    print('Seed completed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
