import paramiko
import os
from common.logger import write_log

#SFTP Details
SFTP_HOSTNAME = "sftp.example.com"
PORT = 22
USERNAME = "your_username"  
PASSWORD = "your_password"

#File paths
REMOTE_DIRECTORY = "/remote/directory/path"
LOCAL_DIRECTORY = "local/directory/path"
remote_file_path = REMOTE_DIRECTORY + os.path.join(LOCAL_DIRECTORY)

try:
    transport = paramiko.Transport((SFTP_HOSTNAME, PORT))
    transport.connect(username=USERNAME, password=PASSWORD)
    
    #create SFTP client
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    #Upload file to SFTP server
    sftp.put(localpath=LOCAL_DIRECTORY, remotepath=remote_file_path)
    
    write_log(f"File {LOCAL_DIRECTORY} uploaded successfully to SFTP server at {remote_file_path}")
    
    #close the SFTP connection
    sftp.close()
    transport.close()
     
     
    
except Exception as e:
    write_log(f"SFTP upload failed: {str(e)}")   