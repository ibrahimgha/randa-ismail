# LLM Read This First: SprintFlow for randa-ismail

Read `project-memory.md` first, then come back to this file before touching code.

## Live SprintFlow Access
- Base URL: `https://tech-tasks.sastouma.com`
- Username: `vm2`
- Password: `vm2worker`
- Use the API, not the browser UI.

## Project Match
- SprintFlow project id: `18`
- SprintFlow project name: `randa-ismail`
- GitHub repository: `git@github.com:ibrahimgha/randa-ismail.git`
- Staging branch: `staging`
- Known SprintFlow columns: `backlog_1, backlog_2, current_sprint, in_progress, pending_review, accepted, archived`

## API Calls
- Token login: `POST /api/auth/token/` with `{ "username": "...", "password": "..." }`
- Assigned projects: `GET /api/projects/assigned/`
- Move task: `POST /api/tasks/<task_id>/move/` with `{ "column": "in_progress" }` or `{ "column": "pending_review" }`

- Update `llm_output`: `POST /api/tasks/<task_id>/move/` with the current `column` plus `llm_output`

## Required Worker Flow
1. Log in with `POST /api/auth/token/`.
2. Fetch assigned projects with `GET /api/projects/assigned/`.
3. Match the current repo to the SprintFlow project.
4. Only work tasks in the `current_sprint` column.
5. Move the chosen task to `in_progress`.
6. Implement the change locally.
7. Run tests and checks.
8. Commit and push.
9. If deployment instructions are provided, deploy using `staging-deploy-instructions.md` and any extra notes in `project-memory.md`.
10. Verify the live environment directly if the task depends on server, DB, user, or permissions state.
11. Move the task to `pending_review` only after push, deploy, and live verification succeed.

## Guardrail
- If there are no `current_sprint` tasks for this project, do not invoke LLM work for it.
