# Builds commands:

## Definitions :sunglasses:

| ARGUMENT       | DEFINITION              |
| -------------- | ----------------------- |
| `[server_ip]`  | ip of your computer     |
| `[port_ip]`    | identifier of your port |
| `[proxy_ip]`   | ip of central proxy     |
| `[proxy_port]` | port of central proxy   |
| `[id_client]`  | identifier of client    |

## First step:

Launch your proxy with `python3 proxy.py [proxy_port]`

## Second step:

Server up command

```shell
bash server.sh [server_ip] [port_ip] [proxy_ip] [proxy_port]
```

## Third step:

Client up command

```shell
bash client.sh [id_client] [proxy_ip] [proxy_port]
```
