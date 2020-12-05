conda init bash
source ~/.bashrc
conda activate app
conda install -c conda-forge --file requirements.txt
python -u app.py
