import subprocess

cmd = ['python', '-c', 'import sys;sys.path.append("/home/rmslick/PointCloudBrowser/sandbox_testing/pcdprocessor"); from PointCloudAPI import *;print("Hello, world!");test_api();']

result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10, check=True)
output = result.stdout.decode('utf-8')
print(output)