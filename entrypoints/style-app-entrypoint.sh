cd /applications || exit

python3 -m gunicorn -k uvicorn.workers.UvicornWorker \
  --workers 4 \
  --bind "0.0.0.0:${APP_PORT:-8080}" \
  style.main:app \
  "$@"
