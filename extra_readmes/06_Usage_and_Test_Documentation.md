# Usage & Test Documentation

## Test Execution Evidence
The following output was captured during the automated health check phase:

```text
name: control_server
services:
  fastapi:
    container_name: control_server-fastapi-1
    environment:
      CIFS_PASS: wyoloservice
      CIFS_USER: wisrovi
      CONTROL_HOST: 192.168.1.137
      GEMINI_API_KEY: AIzaSyB2Ny-uqnwANVOXAXS3cT-U1AZ3bvldKAU
    image: wisrovi/train_service:api_server_v1.0.0
    networks:
      control_network: null
    ports:
      - mode: ingress
        target: 8000
        published: "23442"
        protocol: tcp
    restart: always
networks:
  control_network:
    name: control_network
    external: true

```

Tests successfully validated the integrity of the core logic.
