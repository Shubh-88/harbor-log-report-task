There is an Apache-style access log at `/app/access.log`. Each line is one HTTP
request in Combined Log Format (IP, timestamp, method, path, status, bytes).

Read the log and write a JSON report to `/app/report.json` containing exactly
three keys:

- `total_requests` — integer count of all log lines
- `unique_ips` — integer count of distinct client IP addresses
- `top_path` — string, the URL path that appears most often in the log

Success criteria:

1. `/app/report.json` exists and is valid JSON containing the three keys above.
2. `total_requests` is the correct integer count of all requests in the log.
3. `unique_ips` is the correct integer count of distinct client IP addresses.
4. `top_path` is the string URL path with the highest request count in the log.
