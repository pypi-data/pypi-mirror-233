# Tabella Integration Test HTTP Client

Tabella Integration Test TypeScript HTTP client.

## Example Usage

```typescript
import {TabellaIntegrationTestClient} from "tabella_integration_test_client"


async function main() {
  // Get an instance of the client.
  const client = new TabellaIntegrationTestClient(headers={});
  // Use client method calls...
}

main().then(() => {});
```

## Build Installable Tarball Locally

```shell
npm i
npm run build
npm pack
```
