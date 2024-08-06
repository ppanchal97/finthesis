#!/bin/bash

ENV_FILE="../finance-co-pilot-backend/.env"

REPO="GenerAIve/ia-poc-backend"

while IFS= read -r line; do
  IFS='=' read -ra KV <<< "$line"
  NAME="${KV[0]}"
  VALUE="${KV[1]}"

  echo "Processing secret for $NAME with value: $VALUE"

  echo "$VALUE" | gh secret set "$NAME" --repo "$REPO" --body -
  
done < "$ENV_FILE"

echo "All secrets processed ✅."