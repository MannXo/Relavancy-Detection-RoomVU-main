python -m venv venv
if (!$?)
{
    exit 1
}

venv/scripts/activate.ps1
if (!$?)
{
    exit 1
}
python -m pip install --upgrade pip
pip install -e .[build]
python -m spacy download en_core_web_trf