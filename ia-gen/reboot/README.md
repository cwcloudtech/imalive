# Reboot endpoint

Create a endpoint like this:

```shell
POST /v1/reboot
```

The endpoint should trigger a reboot of the system. The response should be a JSON object with a message indicating that the reboot has been initiated.

```json
{
  "status": "ok",
  "message": "Reboot initiated"
}
```

Code http response: `202 Accepted`, indicating that the request has been accepted for processing, but the processing has not been completed.

The response must be sent before executing the reboot command in an asynchronous process.

Beware, the process is launch from a docker container, so the reboot command should be executed in a way that it reboots the host machine, not just the container. You can use the following command to reboot the host machine from within the container:

```shell
reboot
```

We also want an environment variable to configure a passphrase that must be provided in the request body to authorize the reboot. The environment variable should be named `IMALIVE_REBOOT_PASSPHRASE`.

The passphrase must be sent with a header `X-Reboot-Passphrase`.
Code response if not set or incorrect: `403 Forbidden`, with a JSON response:

```json
{
  "status": "ko",
  "message": "Forbidden: Incorrect or missing passphrase"
}
```

If the environment variable `IMALIVE_REBOOT_PASSPHRASE` is not set, the endpoint should be disabled and return a `503 Service Unavailable` response with a JSON message:

```json
{
  "status": "ko",
  "message": "Service Unavailable: Reboot endpoint is disabled"
}
```
