# Security Policy

## Supported Versions

The following table lists the security support status for releases of this project:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0.0 | :x:                |

## Reporting a Vulnerability

We take the security of our distributed systems and AI infrastructure seriously. If you discover a vulnerability or security flaw, please report it responsibly.

### Disclosure Process

1. **Do not create a public GitHub issue.**
2. Send an email to **tayyabmasood911@gmail.com** with the subject line:
   `[SECURITY VULNERABILITY] vllm-high-throughput-inference-server - <Brief Description>`
3. Include the following details:
   - Impacted component and version
   - Detailed steps to reproduce or Proof of Concept (PoC)
   - Potential impact and severity assessment
   - Any suggested mitigations or patches
4. You will receive an initial response acknowledging receipt within 48 hours.
5. A remediation timeline and coordinated public disclosure plan will be established once the vulnerability is verified and resolved.

## Security Best Practices

- Always run production deployments behind a hardened reverse proxy or API gateway with TLS 1.3 termination.
- Ensure sensitive environment variables and credentials are not hardcoded or committed to version control.
- Apply the principle of least privilege to network ingress/egress rules and container runtime permissions.
