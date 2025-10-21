<!-- 5a2f00a6-8f23-479e-b9f4-d4fc651626e8 012e9605-2b68-4c4f-936f-75139aeb23c4 -->
# Complete Configuration Refactoring - Phases 2, 3, and 4

## Overview

Complete the configuration refactoring started in PR #59 by removing legacy code, refactoring services for proper dependency injection, and creating a complete application entry point.

## Phase 2: Cleanup (Remove Legacy Code)

### 2.1 Migrate Pydantic Models to Centralized Config

**Move all models from `src/mastermind/domain/config/models.py` to `src/mastermind/config/settings.py`**

Current state:

- `config/settings.py` imports models from `domain/config/models.py`
- Violates Clean Architecture (domain shouldn't have config models)

Actions:

1. Copy all model classes from `domain/config/models.py` to `config/settings.py`:

   - `AuthMethod` enum
   - `AuthSettings`
   - `SnowflakeSettings`
   - `TableSettings`, `ColumnSettings`
   - `MatchingSettings`, `LoggingSettings`
   - `GeocodingSettings`, `EntityResolutionSettings`
   - `DbtSettings`

2. Update imports in `config/settings.py` to remove dependency on domain layer

3. Keep `AppSettings` model definition at the bottom

4. Add a `DbtSettings` model in `src/mastermind/config/settings.py` and include it on `AppSettings`:

   - `DbtSettings`: `project_dir`, `profiles_dir`, `target`, `timeout`
   - Extend `AppSettings` with `dbt: DbtSettings | None = None`
   - This aligns with `mastermind.infrastructure.config.dbt_config.DbtConfig`

### 2.2 Update All Import Statements

**Replace all imports of `mastermind.domain.config.config_loader` with centralized loader**

Current code contains multiple occurrences across application and infrastructure modules

(at least 16 implementation modules; docs may reference it too). Update all implementation

modules to use the centralized loader.

Change pattern:

```python
# OLD
from mastermind.domain.config.config_loader import config
value = config.snowflake_account

# NEW
from mastermind.config.loader import load_settings
settings = load_settings()
value = settings.snowflake.account
```

### 2.3 Remove Legacy Config Bridge

**Delete `src/mastermind/domain/config/` directory**

Files to delete:

- `domain/config/config_loader.py` (bridge pattern, no longer needed)
- `domain/config/models.py` (moved to config/settings.py)
- `domain/config/__init__.py`
- `domain/config/MIGRATION_GUIDE.md` (archive to docs/)

Actions:

1. Move `MIGRATION_GUIDE.md` to `docs/archive/config_migration_guide.md`
2. Delete entire `domain/config/` directory
3. Update any documentation references

### 2.4 Update Tests

**Update test files to use centralized config**

Files:

- `tests/conftest.py` - Update mocks
- `tests/unit/domain/config/test_config_loader.py` - Move to `tests/unit/config/`
- All integration tests that mock config

Change pattern:

```python
# OLD
patch("src.domain.config.config_loader.Config.snowflake_account")

# NEW
patch("src.config.loader.load_settings")
```

## Phase 3: Service Refactoring (Dependency Injection)

### 3.1 Refactor MatchingService

**File: `src/mastermind/application/use_cases/matching/matching_service.py`**

Current constructor:

```python
def __init__(self, session, query_service, dbt_orchestrator, ...):
    # Uses global config singleton internally
```

New constructor:

```python
def __init__(
    self,
    session: Session,
    query_service: MatchingQueryService,
    dbt_orchestrator: DbtOrchestrationService,
    matching_settings: MatchingSettings,
    hcp_repository: Optional[HCPRepository] = None,
    hco_repository: Optional[HCORepository] = None,
):
    self.session = session
    self.query_service = query_service
    self.dbt_orchestrator = dbt_orchestrator
    self.matching_settings = matching_settings  # Injected
    # ...
```

Update line 123:

```python
# OLD
policy = MatchingPolicy.legacy_defaults()

# NEW
policy = MatchingPolicy(
    assignment_priority=self.matching_settings.assignment_priority,
    tie_break_policy=self.matching_settings.tie_break_policy
)
```

### 3.2 Refactor DbtOrchestrationService

**File: `src/mastermind/application/services/dbt_orchestration_service.py`**

Update constructor to accept `DbtConfig`:

```python
def __init__(self, dbt_config: DbtConfig, session: Session):
    self.dbt_config = dbt_config
    self.session = session
    self.runner = DbtRunner(
        project_dir=dbt_config.project_dir,
        profiles_dir=dbt_config.profiles_dir,
        target=dbt_config.target
    )
```

### 3.3 Update ApplicationRoot (Composition Root)

**File: `src/mastermind/application/composition_root.py`**

Current (line 22):

```python
from mastermind.domain.config.config_loader import config
```

Changes:

1. Remove global config import
2. Load settings in `__init__`:
```python
def __init__(self, session: Session):
    self._session = session
    self._settings = load_settings()  # Load once
    self._repositories = None
    self._dbt_orchestrator = None
```

3. Create config objects for injection:
```python
def _get_dbt_config(self) -> DbtConfig:
    """Create DbtConfig from settings."""
    return DbtConfig(
        project_dir=self._settings.dbt.project_root,
        profiles_dir=self._settings.dbt.profiles_dir,
        target=self._settings.dbt.target,
        timeout=self._settings.dbt.compile_timeout,
        dbt_vars={
            "distance_threshold_km": self._settings.matching.distance_threshold
        }
    )
```

4. Update `create_matching_service()` (line 141):
```python
def create_matching_service(self) -> MatchingService:
    """Create the HCP-HCO matching service with all dependencies."""
    return MatchingService(
        session=self.session,
        hcp_repository=self.repositories.create_hcp_repository(),
        hco_repository=self.repositories.create_hco_repository(),
        data_validator=self.create_validation_service(),
        affiliation_repository=self.repositories.create_affiliation_repository(),
        dbt_orchestrator=self.dbt_orchestrator,
        matching_settings=self._settings.matching  # Inject config
    )
```


### 3.4 Update Repository Classes

**Files: `infrastructure/persistence/repositories/*.py`**

Pattern for all repositories that use config:

```python
# OLD
from mastermind.domain.config.config_loader import config

class HCPRepository:
    def __init__(self, session: Session):
        self.session = session
        self._table = config.tables.input["hcp"]  # Global access

# NEW
from mastermind.config.settings import TableSettings, ColumnSettings

class HCPRepository:
    def __init__(
        self,
        session: Session,
        table_settings: TableSettings,
        column_settings: ColumnSettings
    ):
        self.session = session
        self._table = table_settings.input["hcp"]  # Injected
```

Update `RepositoryFactory` to inject config objects.

### 3.5 Update Connection Classes

**File: `infrastructure/persistence/connection.py`**

```python
# OLD
from mastermind.domain.config.config_loader import config

def get_sso_session() -> Session:
    account = config.snowflake_account
    # ...

# NEW
from mastermind.config.loader import load_settings

def get_sso_session() -> Session:
    settings = load_settings()
    account = settings.snowflake.account
    # ...
```

## Phase 4: Complete Entry Point

### 4.1 Implement Full Main Entry Point

**File: `src/main.py`**

Replace minimal implementation with complete service wiring:

```python
"""
Main Application Entry Point

Orchestrates configuration loading, dependency injection, and application execution.
"""
import argparse
import logging
import sys
from typing import Optional

from mastermind.config.loader import load_settings
from mastermind.config.settings import AppSettings
from mastermind.infrastructure.config.dbt_config import DbtConfig
from mastermind.domain.value_objects.matching_policy import MatchingPolicy
from mastermind.application.composition_root import ApplicationRoot
from mastermind.infrastructure.observability.logging import setup_logging

logger = logging.getLogger(__name__)


def create_dbt_config(settings: AppSettings) -> DbtConfig:
    """Create DbtConfig from AppSettings."""
    return DbtConfig(
        project_dir=settings.dbt.project_root,
        profiles_dir=settings.dbt.profiles_dir,
        target=settings.dbt.target,
        timeout=settings.dbt.compile_timeout,
        dbt_vars={
            "distance_threshold_km": settings.matching.distance_threshold,
            "database": settings.snowflake.database,
            "schema": settings.snowflake.db_schema,
        }
    )


def create_matching_policy(settings: AppSettings) -> MatchingPolicy:
    """Create MatchingPolicy from AppSettings."""
    return MatchingPolicy(
        assignment_priority=settings.matching.assignment_priority,
        tie_break_policy=settings.matching.tie_break_policy
    )


def main(config_path: Optional[str] = None, command: str = "matching") -> int:
    """
    Main application entry point.

    Args:
        config_path: Optional path to config YAML file
        command: Command to execute (matching, geocoding, entity_resolution)

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    try:
        # Step 1: Load centralized configuration
        logger.info("Loading application configuration...")
        settings = load_settings(config_path)

        # Step 2: Setup logging
        setup_logging(level=settings.logging.level)

        # Step 3: Create layer-specific config objects
        dbt_config = create_dbt_config(settings)
        matching_policy = create_matching_policy(settings)

        # Step 4: Initialize application root with dependency injection
        logger.info("Initializing application services...")
        app = ApplicationRoot.from_sso()

        # Step 5: Execute requested command
        if command == "matching":
            logger.info("Starting HCP-HCO matching process...")
            matching_service = app.create_matching_service()
            results = matching_service.run_dbt_matching_process()
            logger.info(f"Matching complete. Generated {len(results)} matches.")

        elif command == "geocoding":
            logger.info("Starting geocoding process...")
            geocoding_service = app.create_geocoding_service()
            # Execute geocoding workflow

        elif command == "entity_resolution":
            logger.info("Starting entity resolution process...")
            er_service = app.create_entity_resolution_service()
            # Execute entity resolution workflow

        else:
            logger.error(f"Unknown command: {command}")
            return 1

        logger.info("Application execution completed successfully")
        return 0

    except Exception as e:
        logger.error(f"Application failed: {e}", exc_info=True)
        return 1
    finally:
        if 'app' in locals():
            app.close()


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Mastermind - HCP-HCO Matching System"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration YAML file"
    )
    parser.add_argument(
        "command",
        choices=["matching", "geocoding", "entity_resolution"],
        default="matching",
        help="Command to execute"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without persisting results"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    sys.exit(main(config_path=args.config, command=args.command))
```

### 4.2 Update Existing Entry Points

**Update `src/run_matching.py` to use new main**:

```python
"""Backward compatibility wrapper for run_matching."""
from main import main

def run_matching():
    """Legacy entry point - delegates to new main."""
    return main(command="matching")

if __name__ == "__main__":
    run_matching()
```

### 4.3 Fix DbtConfig Field Name Inconsistency

**File: `src/mastermind/config/default.yaml`**

Update field names to match `DbtConfig` dataclass:

```yaml
# OLD
dbt:
  project_root: "transforms"
  target_path: "target"
  cache_enabled: true
  cache_ttl: 3600
  compile_timeout: 600

# NEW
dbt:
  project_dir: "transforms"       # Match dataclass field
  profiles_dir: "transforms"      # Match dataclass field
  target: "dev"
  timeout: 600                    # Match dataclass field
  dbt_vars: {}
```

**Update `src/mastermind/domain/config/models.py` (to be moved):**

```python
class DbtSettings(BaseModel):
    """dbt runner configuration."""
    project_dir: str = "transforms"
    profiles_dir: str = "transforms"
    target: str = "dev"
    timeout: int = 600
```

## Testing Strategy

### Unit Tests

- Test config loading with new centralized loader
- Test service constructors with injected config
- Mock config objects instead of singleton

### Integration Tests

- Test full application flow with real config
- Verify backward compatibility during transition
- Test CLI argument parsing

### Migration Testing

1. Run tests with bridge pattern (current state)
2. Implement Phase 2, run tests again
3. Implement Phase 3, run tests again
4. All tests should pass at each phase

## Success Criteria

- [ ] `src/mastermind/domain/config/` directory deleted
- [ ] All Pydantic models in `src/mastermind/config/settings.py`
- [ ] No global `config` singleton usage
- [ ] All services receive config via constructor
- [ ] `src/main.py` demonstrates full application execution
- [ ] All 18 files updated to use centralized config
- [ ] All tests pass
- [ ] CLI works with argument parsing

## Rollout Order

1. **Phase 2 first** - Remove legacy code, update imports
2. **Phase 3 second** - Refactor services for DI
3. **Phase 4 third** - Complete entry point

Each phase should be committed separately for easy rollback if needed.

### To-dos

- [ ] Migrate Pydantic models from domain/config/models.py to config/settings.py
- [ ] Update 18 files to import from config.loader instead of domain.config.config_loader
- [ ] Delete src/mastermind/domain/config/ directory after archiving MIGRATION_GUIDE.md
- [ ] Update test mocks and fixtures to use centralized config
- [ ] Refactor MatchingService to accept MatchingSettings via constructor
- [ ] Refactor DbtOrchestrationService to accept DbtConfig via constructor
- [ ] Update ApplicationRoot to load settings once and inject config objects
- [ ] Refactor repository classes to accept config objects via constructor
- [ ] Update connection classes to use centralized config loading
- [ ] Implement complete main.py with CLI, service wiring, and command execution
- [ ] Fix DbtConfig field name inconsistency between YAML and dataclass
- [ ] Update run_matching.py to delegate to new main entry point
- [ ] Run full test suite and verify all tests pass