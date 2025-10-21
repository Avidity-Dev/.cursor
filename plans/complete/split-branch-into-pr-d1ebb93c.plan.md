<!-- d1ebb93c-34d9-4f1c-9b7e-9c73fac79867 ac34e831-1d5c-4e2a-b0c8-34c04bee90fa -->
# Split Branch into Multiple PRs

## Analysis Summary

The branch contains **32 commits** spanning **3 distinct projects**:

1. **DBT 3-Layer Architecture** (6 commits): Original purpose - dbt model refactoring
2. **Overengineering Fixes - Phase 1** (20 commits): Python code simplification
3. **Package Modernization** (3 commits + merge + uncommitted): Namespace restructuring to `mastermind.*` plus integration of already-merged config changes from PR #59

## Proposed PR Split Strategy

### PR #1: DBT 3-Layer Architecture Refactoring

**Commits:** `4921938` through `9692985` (6 commits)

**Base branch:** Current base of `refactor/dbt-three-layer-architecture`

**Changes:**

- Remove `dim_` and `fct_` prefixes from mart models
- Improve address normalization with special character handling
- Add comprehensive column documentation to intermediate schemas
- Add unit tests for Address and HCP entities
- Add intermediate schema audit documentation

**Why first:** This is the original purpose of the branch and has no dependencies on other work.

**Git strategy:**

```bash
# Create new branch from current base
git checkout -b pr/dbt-three-layer-architecture origin/refactor/dbt-three-layer-architecture
git cherry-pick 4921938 3d5cfcc 42185f3 9e8ba95 33b4281 9692985
```

---

### PR #2: Python Simplification - Overengineering Fixes Phase 1

**Commits:** `438b281` through `770c24c` (20 commits)

**Base branch:** `main` (or whatever your default branch is)

**Changes:**

- Consolidate geocoding service v2 into main implementation
- Merge ServiceFactory into ApplicationRoot
- Delete unused repository interfaces and BaseRepository base class
- Remove hasattr() anti-patterns
- Add architecture compliance tests
- Remove `_cda` suffixes from AddressEntity fields
- Add comprehensive documentation in `overengineering_fixes/`

**Why second:** Independent of dbt work, can go directly to main. This is the major Python simplification effort.

**Git strategy:**

```bash
# Create new branch from main
git checkout -b pr/overengineering-fixes-phase1 main
git cherry-pick 438b281 8c0b740 f57a2d2 5211df4 728c851 f86629c cc7d35c 7447666 dea7a45 8a38d60 308de2f ee93407 9b4d856 f4d8fc8 d76b37e 039b4a2 dad2247 9c003a3 770c24c
```

---

### PR #3: Package Modernization & Namespace Restructuring

**Commits:** `f9dd4ac` through `ca90052` (3 commits)

**Base branch:** Result of PR #2 (overengineering fixes)

**Changes:**

- Modernize `pyproject.toml` configuration
- Restructure to `mastermind.*` namespace (move domain/application/infrastructure under `src/mastermind/`)
- Update all imports from `src.domain.*` and `domain.*` to `mastermind.domain.*`
- Add ADR-004 documenting namespace adoption

**Why third:** Depends on simplified structure from PR #2. Namespace changes will be easier to review after unnecessary code is removed.

**Git strategy:**

```bash
# After PR #2 merges, create branch from that merge commit
git checkout -b pr/package-modernization <PR2-merge-commit>
git cherry-pick f9dd4ac 9ed5820 ca90052
```

---

### PR #4: Config System Refactoring

**Commits:** `54af300` through `7dd0fe4` + uncommitted changes

**Base branch:** Result of PR #3 (namespace restructuring)

**Changes:**

- Move config from `src/domain/config/` to `src/config/` (new layer)
- Split config into `src/config/loader.py` and `src/config/settings.py`
- Add configurable matching settings and policies
- Update GitHub workflows for config changes
- Delete old `src/config/` files (shown in git status)
- Resolve merge conflicts

**Why fourth:** Depends on namespace restructuring from PR #3. These changes touch the new namespace structure.

**Git strategy:**

```bash
# After PR #3 merges, create branch from that merge commit
git checkout -b pr/config-system-refactoring <PR3-merge-commit>
git cherry-pick 54af300 7a9a11d b7f0740 7dd0fe4

# Then stage and commit the current uncommitted changes
git add src/mastermind/domain/config/
git add -u src/config/
git commit -m "Complete config layer separation and cleanup"
```

---

## Dependency Chain

```
main
 ├─ PR #1: DBT 3-Layer → [can merge independently]
 │
 └─ PR #2: Overengineering Fixes Phase 1
     │
     └─ PR #3: Package Modernization
         │
         └─ PR #4: Config System Refactoring
```

**Notes:**

- PR #1 (DBT) can merge anytime, it's independent
- PRs #2-4 must merge in sequence due to dependencies
- Each PR should be tested independently before merging
- Consider squashing commits within each PR for cleaner history

## Review Considerations

**PR #1 (DBT):** Focus on SQL logic, naming conventions, documentation quality

**PR #2 (Overengineering):** Focus on architecture improvements, deleted code justification

**PR #3 (Namespace):** Focus on import correctness, no functional changes

**PR #4 (Config):** Focus on new config layer design, separation of concerns

## ✅ Project Complete

All work from the `refactor/dbt-three-layer-architecture` branch has been successfully split and merged to main:

**Merged PRs:**

- ✅ **PR #75**: dbt Model Refactoring - Enriched/Extension Layer Separation (23 commits) - Merged 2025-10-07 23:08 UTC
- ✅ **PR #76**: Python Code Simplification - Overengineering Fixes Phase 1 (20 commits) - Merged 2025-10-07 23:48 UTC
- ✅ **PR #77**: Package Modernization & Namespace Restructuring (10+ commits) - Merged 2025-10-08 01:17 UTC

**Note on PR #4:** There is no PR #4. The config refactoring work was already completed and merged to main via PR #59. The commits on this branch related to config were integration work adapting those changes to the new namespace structure, which were included in PR #77.

### To-dos

- [x] Create PR #1 branch (DBT changes) - DONE
- [x] Create PR #2 branch (Overengineering fixes) - DONE
- [x] Abort current PR #3 rebase - DONE
- [x] Push PR #1 and PR #2 branches - DONE
- [x] Write detailed PR descriptions - DONE
- [x] Create PRs on GitHub - DONE
- [x] Update PR #75 to target main and include all dbt commits - DONE
- [x] Update PR #75 description to reflect full scope - DONE
- [x] Move suggestions.md from PR #75 to PR #76 - DONE
- [x] Review and merge PRs #75 and #76 to main - DONE (PR #75, PR #76 merged)
- [x] Pull main into pr/package-modernization branch - DONE
- [x] Cherry-pick PR #3 commits (f9dd4ac, 9ed5820, ca90052) - DONE
- [x] Resolve conflicts (config location, imports, tests) - DONE
- [x] Create PR #3 on GitHub - DONE (PR #77: https://github.com/Avidity-Dev/mastermind/pull/77)
- [x] Review and merge PR #77 to main - DONE (PR #77 merged 2025-10-08)
- [x] **Project Complete** - All three PRs successfully merged