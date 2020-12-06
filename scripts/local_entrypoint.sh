
source ~/.bashrc
conda activate app
conda install -c conda-forge -y --file /app/requirements.txt

source /root/google-cloud-sdk/path.bash.inc

# apt-get update
# apt-get install golang-go
# GO111MODULE=on go get github.com/GoogleCloudPlatform/cloudsql-proxy/cmd/cloud_sql_proxy

## NOTE: the above line installs the cloud sql proxy, but keeping the below lines for later debugging if needed
wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64
mv cloud_sql_proxy.linux.amd64 cloud_sql_proxy
chmod +x cloud_sql_proxy

mkdir -p /cloudsql
chmod 777 /cloudsql
gcloud auth login
gcloud config set project hackduke-2020-brohke
export PATH=$PATH:$GOPATH/bin
./cloud_sql_proxy -dir=/cloudsql &

bash scripts/start.sh