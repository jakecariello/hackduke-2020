source /root/google-cloud-sdk/path.bash.inc
wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64
mv cloud_sql_proxy.linux.amd64 cloud_sql_proxy
chmod +x cloud_sql_proxy
mkdir -p /cloudsql
chmod 777 /cloudsql
gcloud auth login
gcloud config set project hackduke-2020-brohke
./cloud_sql_proxy -dir=/cloudsql &
bash scripts/start.sh