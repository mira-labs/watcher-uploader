# Mira watcher

This script is a file watcher which uploads file through SFTP to the remote location defined in the `.env` file or environmental variables``

It should solve the problem of instant changes to files on remote servers when the IDE or text editor does not provide sftp transfer functionality. 

### `.env` file structure
`PATTERNS=["*.py", "*.txt", ".flaskenv"]` - array of file name patterns to track

`IGNORE_PATTERNS=None` - array of patterns to ignore

`CASE_SENSITIVE=True` - should the watcher be case-sensitive?

`PATH="."` - which folder should be watched

`REMOTE_PATH="/remote/path/on/the/server"` - path on the server the files will be uploaded to

`KEY_FILE="/home/my_user_name/.ssh/id_ed25519"` - location of the private key for sftp connection - this feature has not been fully implemented yet as `pysftp` has problems with `ed25519` ssh keys. 

`KNOWN_HOSTS="/home/my_user_name/.ssh/known_hosts"` - location of known hosts file.

`HOST="host.example.com"` - SFTP host

`PORT=22` - SFTP port

`USER="username"` - SFTP user name

`PASSWORD="MyPaSsWoRd"` - SFTP password