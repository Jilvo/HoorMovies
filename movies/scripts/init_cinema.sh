set -e

echo "Running Django migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Filling database with initial data..."
python manage.py fill_db

echo "Creating superuser (if not exists)..."
python manage.py create_superuser --username admin --email admin@mail.com --password admin

echo "Init script completed."