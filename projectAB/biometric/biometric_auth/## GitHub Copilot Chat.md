## GitHub Copilot Chat

- Extension Version: 0.23.2 (prod)
- VS Code: vscode/1.96.2
- OS: Windows

## Network

User Settings:
```json
  "github.copilot.advanced.debug.useElectronFetcher": true,
  "github.copilot.advanced.debug.useNodeFetcher": false,
  "github.copilot.advanced.debug.useNodeFetchFetcher": true
```

Connecting to https://api.github.com:
- DNS ipv4 Lookup: 20.207.73.85 (207 ms)
- DNS ipv6 Lookup: Error (136 ms): getaddrinfo ENOTFOUND api.github.com
- Proxy URL: None (0 ms)
- Electron fetch (configured): HTTP 200 (975 ms)
- Node.js https: HTTP 200 (2159 ms)
- Node.js fetch: HTTP 200 (1585 ms)
- Helix fetch: HTTP 200 (1974 ms)

Connecting to https://api.individual.githubcopilot.com/_ping:
- DNS ipv4 Lookup: 140.82.113.21 (667 ms)
- DNS ipv6 Lookup: Error (320 ms): getaddrinfo ENOTFOUND api.individual.githubcopilot.com
- Proxy URL: None (0 ms)
- Electron fetch (configured): HTTP 200 (1041 ms)
- Node.js https: HTTP 200 (2209 ms)
- Node.js fetch: HTTP 200 (1752 ms)
- Helix fetch: HTTP 200 (1751 ms)

## Documentation

In corporate networks: [Troubleshooting firewall settings for GitHub Copilot](https://docs.github.com/en/copilot/troubleshooting-github-copilot/troubleshooting-firewall-settings-for-github-copilot).