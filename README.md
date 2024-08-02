# backend

## Setup

1. Set 2 environment variables:
- `ICL_USERNAME` - Imperial shortname
- `ICL_PASSWORD` - Password used for authenticating into the GPU cluster

2. Upload the `remote/start-api.sh` to the home (`~/`) directory on the remote server.

3. Allow execution: `chmod +x ~/start-api.sh`

4. Start an interactive GPU job on the cluster: `salloc --gres=gpu:1` and keep the terminal alive.

5. **In another terminal**: `run-api.sh -p {JUPYTER_PORT} -s (SERVER_PORT)`
- `JUPYTER_PORT` - port of the jupyter notebook which is different than the port that the server is running
- `SERVER_PORT` - exposed port of the API (Optional, `default=5000`). Need to update the notebook to listen to the same port in case it is changed

6. Run the cell in `server.ipynb` to start up the server.
