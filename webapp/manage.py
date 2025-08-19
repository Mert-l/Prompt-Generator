# webui/manage.py
import os
import sys
from pathlib import Path

# add repo root to sys.path so we can import `core`
REPO_ROOT = Path(__file__).resolve().parent.parent  # .../webui
REPO_PARENT = REPO_ROOT.parent                      # repo root
sys.path.append(str(REPO_PARENT))

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
