conda init bash
source ~/.bashrc
conda activate app
gunicorn --bind $HOST:$PORT wsgi:app --log-level debug
