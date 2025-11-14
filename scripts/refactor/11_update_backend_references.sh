#!/bin/bash
set -e

echo "Updating backend references after src/ move..."

# Update Python imports in moved scripts
echo "  Updating sys.path references in scripts..."
find scripts/ -name "*.py" -type f -exec sed -i.bak \
    's|Path(__file__).parent.parent.parent / "backend"|Path(__file__).parent.parent.parent / "src" / "backend"|g' {} \;

# Cleanup backup files
find scripts/ -name "*.py.bak" -delete

# Update shell scripts
if [[ -f ".bahr_aliases.sh" ]]; then
    sed -i.bak 's|cd "$BAHR_ROOT/backend|cd "$BAHR_ROOT/src/backend|g' .bahr_aliases.sh
    rm .bahr_aliases.sh.bak
    echo "  Updated: .bahr_aliases.sh"
fi

# Update setup scripts
if [[ -f "scripts/setup/verify_setup.sh" ]]; then
    sed -i.bak 's|backend/app/main.py|src/backend/app/main.py|g' scripts/setup/verify_setup.sh
    rm scripts/setup/verify_setup.sh.bak
    echo "  Updated: scripts/setup/verify_setup.sh"
fi

# Update Docker files
if [[ -f "Dockerfile" ]]; then
    sed -i.bak 's|COPY backend/|COPY src/backend/|g' Dockerfile
    sed -i.bak 's|WORKDIR /app/backend|WORKDIR /app/src/backend|g' Dockerfile
    rm Dockerfile.bak
    echo "  Updated: Dockerfile"
fi

if [[ -f "docker-compose.yml" ]]; then
    sed -i.bak 's|./backend:|./src/backend:|g' docker-compose.yml
    rm docker-compose.yml.bak
    echo "  Updated: docker-compose.yml"
fi

echo "✓ Backend references updated"
