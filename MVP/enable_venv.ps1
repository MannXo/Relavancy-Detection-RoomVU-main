venv/scripts/activate.ps1
if (!$?)
{
    exit 1
}

pip install -e '.[build]'
