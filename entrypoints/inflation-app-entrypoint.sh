cd /applications || exit

export PYTHONUNBUFFERED=TRUE

python3 -m gunicorn -k uvicorn.workers.UvicornWorker \
  --workers 2 \
  --bind "0.0.0.0:${APP_PORT:-8000}" \
  inflation.main:app \
  --log-level debug \
  "$@"
