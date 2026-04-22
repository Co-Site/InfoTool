#!/bin/sh
set -e

# Start the original PostgreSQL entrypoint in the background
/usr/local/bin/docker-entrypoint.sh postgres &

echo "[WRAPPER] ---"
echo "[WRAPPER] Waiting for PostgreSQL to be ready..."
echo "[WRAPPER] ---"
until pg_isready -h localhost -U "$POSTGRES_USER" -d "$POSTGRES_DB" -q; do
  sleep 1
done
echo "[WRAPPER] ---"
echo "[WRAPPER] PostgreSQL is up. Starting user synchronization..."
echo "[WRAPPER] ---"
# Remove all users before adding only the configured
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOF
    DELETE FROM public."USERS" CASCADE;
EOF
echo "$FROST_USERS" | jq -c '.[]' | while read -r row; do
    USER_NAME=$(echo "$row" | jq -r '.name')
    USER_PASSWORD=$(echo "$row" | jq -r '.password')
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOF
        INSERT INTO public."USERS" ("USER_NAME", "USER_PASS")
        VALUES ('$USER_NAME', crypt('$USER_PASSWORD', gen_salt('bf')))
        ON CONFLICT ("USER_NAME")
        DO UPDATE SET "USER_PASS" = EXCLUDED."USER_PASS";
EOF
    echo "$row" | jq -r '.roles[]' | while read -r USER_ROLE; do
        psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOF
            INSERT INTO public."USER_ROLES" ("USER_NAME", "ROLE_NAME")
            VALUES ('$USER_NAME', '$USER_ROLE')
            ON CONFLICT DO NOTHING;
EOF
    done
done
echo "[WRAPPER] ---"
echo "[WRAPPER] User synchronization complete. Only users from ENV are present."
echo "[WRAPPER] ---"
wait
