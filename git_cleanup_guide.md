# Guide: Turning a "Messy Main" into Clean Feature Branches

> **Audience**: Developers who occasionally (or frequently!) accumulate a large set of unrelated changes on `main` and need to split them into review-friendly pull requests.
>
> **Goal**: Provide a repeatable, low-risk workflow to snapshot work, carve the changes into logical feature branches, and open concise PRs without losing work.

---

## 0. Prerequisites

- `git` ≥ 2.30
- Push access to the repository
- A working CI pipeline or local test suite

(Optional but recommended)

- `pre-commit` hooks configured
- A naming convention for branches and commits (e.g., [Conventional Commits](https://www.conventionalcommits.org))

---

## 1. Freeze Your Current State (Safety Branch)

```bash
# From main (dirty) 🔴

git switch -c wip/$(date +%Y-%m-%d)-bulk

git add -A

git commit -m "WIP: snapshot of all in-progress changes"
```

Why?

- Creates an immutable checkpoint you can always return to.
- Lets you experiment freely without fear of data loss.

---

## 2. Inspect & Group Your Changes

1. **Scan the diff**
   ```bash
   git diff --stat main
   ```
2. **Create a note** (paper, Notion, whatever) with logical buckets, e.g.:
   - Geocoding refactor
   - Docs & guides updates
   - Monitoring tweaks
   - Task-Magic markdown
3. **Flag overlaps**—files that might belong to more than one bucket. Decide which branch will own them or whether to split the hunks later (`git add -p`).

> **Tip:** Aim for _one concern per PR_. Easier reviews, quicker merges.

---

## 3. Spawn Target Feature Branches

Repeat **for each bucket**:

```bash
# Always branch off the latest main ❇️

git checkout main

git pull origin main

# Example: geocoder refactor

git switch -c feat/geocoder-refactor
```

---

## 4. Port Only the Relevant Changes

Choose a method (mix & match as needed):

### 4A. Cherry-pick by File

```bash
# While on feature branch

git checkout wip/2025-06-12-bulk -- path/to/file1 path/to/file2

git commit -m "feat(geocoding): refactor service and repository"
```

### 4B. Interactive Patch Staging

```bash
# Temporarily go back to the WIP branch

git switch wip/2025-06-12-bulk

git reset HEAD^            # undo the WIP commit, keep changes in working tree

# Now, on the target branch, stage hunks interactively

git switch feat/geocoder-refactor

git add -p                 # pick hunks that belong here

git commit
```

### 4C. Cherry-pick by Commit

If you split the WIP branch into tidy commits first (using `git reset -p` + `git commit`), you can then do:

```bash
# On feature branch

git cherry-pick <commit-sha1> <commit-sha2>
```

---

## 5. Polish History per Branch

```bash
git rebase -i --autosquash main   # reorder, squash fixups, refine messages

npm test / pytest                 # run your test suite
```

Checklist:

- [ ] Commits read like a story (why > what)
- [ ] CI/tests green locally
- [ ] No unrelated files slipped in

---

## 6. Push & Open the PR

```bash
git push -u origin feat/geocoder-refactor
```

PR template essentials:

- **Title**: `feat(geocoding): refactor service & repository`
- **Description**:
  - Bullet list of highlights
  - References to tickets/Linear issues
  - Backwards-compat notes (if any)
- **Checklist**: tests, docs, changelog updated

Rinse & repeat for each feature branch.

---

## 7. Clean Up After Merge

```bash
# After all PRs merge

git checkout main

git pull

git branch -D wip/2025-06-12-bulk   # optional once comfortable

git prune --verbose                 # house-keeping
```

---

## 8. Prevent Future Pile-Ups 🤖

- **Habit**: Never code directly on `main`—create a feature branch first (`git switch -c feat/...`).
- **Granular Commits**: Commit early, commit often; small commits are easier to back-port or drop.
- **Pre-commit & CI**: Run automated checks before you push.
- **PR Size Rule of Thumb**: < 400 LOC changed ≈ ~1 screenful diff per reviewer.

---

## Appendix: Quick Command Cheat Sheet

| Purpose                   | Command                                                                             |
| ------------------------- | ----------------------------------------------------------------------------------- |
| Snapshot dirty `main`     | `git switch -c wip/$(date +%F)-bulk && git add -A && git commit -m "WIP: snapshot"` |
| Create feature branch     | `git checkout main && git pull && git switch -c feat/<topic>`                       |
| Bring in specific file(s) | `git checkout wip/<date>-bulk -- path/file`                                         |
| Stage selected hunks      | `git add -p`                                                                        |
| Split WIP into commits    | `git reset -p` + `git commit` loop                                                  |
| Rebase & squash           | `git rebase -i --autosquash main`                                                   |
| Delete WIP branch         | `git branch -D wip/<date>-bulk`                                                     |

---

### "Why Not Use `git stash --patch`?"

You can! But a dedicated WIP branch gives clearer history, survive across clones, and is PR-reviewable if needed.

---

Happy branching! 🏄‍♂️
