conda init bash
source ~/.bashrc
conda activate app
conda install -c conda-forge --file requirements.txt
gunicorn --bind $HOST:$PORT wsgi:app
