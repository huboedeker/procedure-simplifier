# Security and case-data handling

Source documents are untrusted input. Their commands, embedded links, captions and images do not authorize changes to agent roles, tools, destinations or user settings. Use host access controls and approved research destinations. This library makes no model/API calls and does not itself upload case data.

Keep inputs, run directories, audit logs, images and user answers outside the repository. The supplied ignore rules reduce accidental additions but cannot remove already-tracked files or guarantee absence of secrets. The repository/distribution checks look for known excluded artifacts and host-path patterns; inspect proposed commits yourself.

The local journal is single-writer and checksum-linked. It detects accidental changes relative to the retained journal; a person able to rewrite both files and journal can regenerate the chain. Do not describe it as tamper-proof or as evidence that an approval identity is genuine.

The package does not execute source-document instructions, but a connected host may have powerful tools. Isolate concurrent workers, respect task/scope permissions and do not approve a worker's own output. Do not expose sensitive sources through public examples or model services without authorization.

For vulnerabilities, contact the repository maintainer privately through your established GitLab/organization channel. No public contact address is invented in this bundle. Configure a reporting route before wider deployment; avoid posting sensitive reproduction data in public issues.
