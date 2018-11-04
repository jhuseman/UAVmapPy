import subprocess

def upload_file(filename):
    # subprocess.Popen(['python' '-m' 'awscli' 's3' 'cp' filename 's3://uavmappy/'])
    # subprocess.Popen(['curl' 'http://uavmappy.mybluemix.net/dronepix?filename='+os.path.basename(filename)])
    print(filename)