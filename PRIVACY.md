# Privacy Policy

**Last Updated:** February 19, 2026 **Plugin Name:** DateTime Tool **Version:**
0.0.1 **Author:** cazziwork

## Overview

This privacy policy describes how the DateTime Tool plugin handles data within
your Dify instance. We are committed to protecting your privacy and ensuring
transparency about our data practices.

## Data Collection and Processing

### What Data Does This Plugin Access?

The DateTime Tool plugin processes data that you explicitly provide to it
through Dify workflows:

- **Date Strings**: Date values passed to the tools in `YYYY-MM-DD` or ISO 8601
  format
- **Format Patterns**: Format strings used for date formatting
- **Parameters**: Tool parameters such as timezone, unit, amount, and edge
  values

### How Is Data Processed?

- **Local Processing**: All date calculation and formatting occurs locally
  within your Dify instance
- **In-Memory Processing**: Data is processed in memory and is not persisted to
  disk by the plugin itself
- **External Holiday Data**: The `date_check_holiday_jp` and `date_add`
  (business days mode) tools fetch Japanese public holiday data from the
  official Japanese Cabinet Office website
  (`https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv`). This data is
  cached locally in `/tmp/dify_holiday_jp_cache.csv` with a 24-hour TTL.

### Data Storage

- **Holiday Cache**: Holiday data is temporarily cached at
  `/tmp/dify_holiday_jp_cache.csv` for performance. This cache contains only the
  official public holiday list published by the Japanese government — no user
  data is stored.
- **No Other Persistent Storage**: The plugin does not store, cache, or persist
  any of the date or parameter data it processes.
- **Dify-Managed Storage**: Any logging or persistence beyond the holiday cache
  is handled by the Dify platform according to your Dify configuration.

## Data Sharing

- **Holiday Data Source**: The plugin fetches public holiday data from the
  Japanese Cabinet Office
  (`https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv`). This is a one-way
  fetch of publicly available government data — no user data is sent to this
  server.
- **No Other Third-Party Sharing**: The plugin does not share any user data with
  third parties.
- **No Analytics**: We do not collect analytics, usage statistics, or telemetry
  data.
- **No User Tracking**: The plugin does not track users or their behavior.

## Security

### Security Measures

- **Sandboxed Execution**: The plugin runs within Dify's plugin sandbox
  environment
- **Limited Permissions**: The plugin only processes the input data provided to
  it
- **Input Validation**: Date strings and format patterns are validated before
  processing
- **Controlled External Access**: The only external network request is to fetch
  publicly available Japanese holiday data from the official government source

### Best Practices for Users

1. **Input Data**: Avoid passing sensitive information as date strings or format
   patterns
2. **Network Access**: Ensure your Dify instance can reach
   `https://www8.cao.go.jp` for holiday data fetching
3. **Access Control**: Use Dify's built-in access controls to restrict who can
   use workflows containing this plugin

## Data Retention

- **Holiday Cache**: Cached for up to 24 hours in `/tmp`. This is a system
  temporary directory that is cleared on restart.
- **No User Data Retention**: The plugin does not retain any user-provided data
  beyond the execution lifecycle.
- **Workflow Context**: Data may be retained as part of Dify's workflow
  execution logs according to your Dify instance configuration.

## User Rights

As a user of this plugin, you have the following rights:

- **Access**: You can access all data that flows through the plugin via Dify's
  workflow logs
- **Control**: You have full control over what data is passed to the plugin
- **Transparency**: You can review the plugin's source code to understand
  exactly how data is processed

## Compliance

### GDPR Compliance

This plugin is designed to be GDPR-compliant:

- **Data Minimization**: Only processes data explicitly provided by the user
- **Purpose Limitation**: Data is used only for date calculation and formatting
  purposes
- **No Profiling**: The plugin does not create user profiles or make automated
  decisions
- **User Control**: Users have complete control over data processing

### Other Regulations

The plugin's minimal-storage design makes it compatible with most data
protection regulations including:

- CCPA (California Consumer Privacy Act)
- PIPEDA (Canadian Personal Information Protection and Electronic Documents Act)
- Other regional data protection laws

## Children's Privacy

This plugin is part of the Dify platform and is intended for business and
professional use. It is not designed for or targeted at children under the age
of 13.

## Changes to This Privacy Policy

We may update this privacy policy from time to time. When we do:

- The "Last Updated" date at the top of this document will be revised
- Significant changes will be noted in the plugin's changelog

## Open Source

This plugin's source code is available for review, allowing you to:

- Verify the privacy practices described in this policy
- Audit the code for security and privacy concerns
- Understand exactly how your data is processed

## Contact Information

For questions, concerns, or requests regarding this privacy policy or the
plugin's data practices, please contact:

**Author:** cazziwork **Issue Tracker:** Please submit issues through the
repository's issue tracker

## Summary

**In Plain English:**

- ✅ Date calculations happen locally on your Dify instance
- ✅ No user data is sent to external servers
- ✅ The only external request is fetching the public Japanese holiday list from
  the government
- ✅ Holiday data is cached temporarily and contains no user information
- ✅ You have complete control over your data
- ✅ The code is open for you to review

**What We DON'T Do:**

- ❌ We don't collect personal information
- ❌ We don't send your date data to external servers
- ❌ We don't store user data after processing
- ❌ We don't track or analyze usage
- ❌ We don't share user data with third parties

---

_This plugin is designed with privacy as a core principle. If you have any
questions or concerns about how your data is handled, please don't hesitate to
reach out._
