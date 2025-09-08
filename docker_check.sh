#!/bin/bash

echo "=== Docker Verification Checklist (macOS) ==="
echo ""

# Function to check if command succeeded
check_success() {
    if [ $? -eq 0 ]; then
        echo "✔️ PASS"
    else
        echo "❌ FAIL"
    fi
}

echo "1. Check Docker Daemon (docker info)"
echo "Command: docker info"
docker info > /tmp/docker_info_output.txt 2>&1
if grep -q "Containers:" /tmp/docker_info_output.txt; then
    echo "✔️ PASS"
elif grep -q "Cannot connect to the Docker daemon" /tmp/docker_info_output.txt; then
    echo "❌ FAIL - Docker daemon not running"
else
    echo "❌ FAIL - Unexpected output"
fi
echo ""

echo "2. Check Docker Version"
echo "Command: docker --version"
docker --version > /tmp/docker_version_output.txt 2>&1
if grep -q "Docker version" /tmp/docker_version_output.txt; then
    echo "✔️ PASS"
    cat /tmp/docker_version_output.txt
else
    echo "❌ FAIL"
fi
echo ""

echo "3. Check Docker Compose Version"
echo "Command: docker-compose --version"
docker-compose --version > /tmp/docker_compose_output.txt 2>&1
if grep -q "Docker Compose version" /tmp/docker_compose_output.txt; then
    echo "✔️ PASS"
    cat /tmp/docker_compose_output.txt
elif grep -q "command not found" /tmp/docker_compose_output.txt; then
    echo "❌ FAIL - docker-compose not installed"
else
    echo "❌ FAIL"
fi
echo ""

echo "4. Run Hello World Test"
echo "Command: docker run hello-world"
docker run hello-world > /tmp/hello_world_output.txt 2>&1
if grep -q "Hello from Docker!" /tmp/hello_world_output.txt; then
    echo "✔️ PASS"
else
    echo "❌ FAIL"
fi
echo ""

echo "5. Check Running Containers"
echo "Command: docker ps"
docker ps > /tmp/docker_ps_output.txt 2>&1
if grep -q "CONTAINER ID" /tmp/docker_ps_output.txt; then
    echo "✔️ PASS"
else
    echo "❌ FAIL"
fi
echo ""

echo "=== Summary ==="
echo "Check the outputs above. If any FAIL, note it for fixes."
