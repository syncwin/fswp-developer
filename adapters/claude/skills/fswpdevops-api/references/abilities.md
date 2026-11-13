# Abilities API: register, audit, verify

The Abilities API is recent and still evolving; read the current developer documentation (search "Abilities API" on developer.wordpress.org and the Core news blog) for exact function names, hooks, and minimum WordPress version before writing code. The procedures below do not depend on those details.

## Register

Per ability: a unique namespaced name, label and description written for humans and for AI clients, an input JSON Schema, an output JSON Schema, a permission callback that checks a real capability (and object access when an ID is involved), an execute callback, and metadata including whether it is exposed over REST and its safety annotations.

Design rules: one ability = one clear action; explicit inputs and outputs; validate input against the schema before acting; return structured errors; never expose an ability more widely than the underlying action allows.

## Audit an existing plugin (propose, do not register)

For each REST route, AJAX action, and public function worth exposing, record: name, purpose in one sentence, HTTP method or trigger, required capability today, inputs (types, limits), outputs, side effects (writes, deletes, sends email, spends money, calls external services), idempotency, and a suggested annotation. Group into candidates (safe to register), needs-work (weak permission or unclear schema), and not-suitable (too dangerous or too internal). Deliver as a table plus a short migration order. Registering anything requires approval.

## Verify a registration

For every registered ability check that behavior matches its claim:

1. **Read-only claims:** execute path performs no writes (options, meta, posts, users, files, external calls with side effects, cache-busting side effects that change state). A callback that writes while annotated read-only is a defect (Critical).
2. **Destructive claims:** anything that deletes or irreversibly changes data is annotated as destructive.
3. **Idempotent claims:** running twice gives the same end state.
4. **Permissions:** the permission callback checks a specific capability, not just login; object-level checks exist where IDs are inputs; failing returns the right error.
5. **Schemas:** input schema rejects unexpected shapes; output matches the declared schema on success and error.
6. **Exposure:** REST exposure is intentional; sensitive abilities are not public.
7. **Naming and docs:** unique prefix, clear descriptions, no misleading wording.

Report each ability as PASS, FAIL, or NOT RUN (for example, no site to execute it on), with the file and line for failures.
