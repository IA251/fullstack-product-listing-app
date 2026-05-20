#!/bin/sh

if [ -f /app/netfree-ca.crt ]; then
  echo "Installing NetFree CA..."
  cp /app/netfree-ca.crt /usr/local/share/ca-certificates/netfree.crt
  update-ca-certificates
fi

exec uvicorn main:app --host 0.0.0.0 --port 8000
