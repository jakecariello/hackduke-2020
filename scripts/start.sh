conda init bash
source ~/.bashrc
conda activate app
gunicorn -t 300 --bind $HOST:$PORT wsgi:app --log-level debug
