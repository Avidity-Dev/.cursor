<!-- 5dcb440f-22ae-43db-8fb3-f6276d83116f 2494a7fb-1110-4a5c-93fa-df367f0f4dde -->
# Add Schema Parent Boxes to Data Flow Diagrams

## Files to Update
- `docs/architecture/hco_ownership_data_flow.mmd`
- `docs/architecture/primary_affiliation_data_flow.mmd`

## Changes Required

### 1. HCO Ownership Diagram (`hco_ownership_data_flow.mmd`)

**Remove Downstream Usage section entirely:**
- Delete the "Downstream Usage" subgraph including `INT_AFF_EXT` and `MARTS` boxes
- Remove the flow arrows: `INT_OWN_RES --> INT_AFF_EXT` and `INT_OWN_RES --> MARTS`
- Remove styling class references for downstream boxes

**Restructure with schema parent boxes:**

Replace current flat "Sources" subgraph with nested schema boxes:
```mermaid
subgraph Sources ["Source Tables"]
    subgraph SRC_INGEST_VN ["INGEST.VEEVA_NETWORK"]
        SRC_VN_HCO["hco<br/>Veeva Network HCOs"]
    end
    subgraph SRC_INGEST_OD ["INGEST.VEEVA_OPENDATA"]
        SRC_OD_HCO["hco<br/>OpenData HCOs"]
        SRC_ADDR["address<br/>Addresses with Geocoding"]
        SRC_AFFILS["affils<br/>HCP→HCO Affiliations"]
        SRC_HCO_HIER["hco_hierarchy<br/>HCO Parent-Child Relationships"]
    end
    subgraph SRC_ADHOC ["EDW.ADHOC"]
        SRC_HCO_PROG["hco_program_flags<br/>MDA/COE/PPMD Flags"]
    end
end
```

Replace "Staging" subgraph with EDW.SILVER parent:
```mermaid
subgraph Silver ["EDW.SILVER"]
    subgraph Staging ["Staging Layer"]
        STG_HCO_HIER["stg_hco_hierarchy"]
        STG_VN_HCO["stg_vn_hco"]
        STG_HCO["stg_hco"]
        STG_ADDR["stg_addresses"]
        STG_AFFILS["stg_affiliations"]
        STG_PROG["stg_hco_program_flags"]
    end
    
    subgraph Unified ["Unified"]
        INT_HCO_UNI["mdm_hco_unified"]
    end
    
    subgraph Enriched ["Enriched"]
        INT_HCO_ENR["mdm_hco_enriched"]
    end
    
    subgraph Candidates ["Candidates"]
        INT_OWN_CAND["mdm_hco_top_ownership_candidates"]
    end
    
    subgraph Results ["Results"]
        INT_OWN_RES["mdm_hco_ownership_resolved"]
    end
end
```

### 2. Primary Affiliation Diagram (`primary_affiliation_data_flow.mmd`)

**Restructure with schema parent boxes:**

Replace current flat "Sources" subgraph with nested schema boxes:
```mermaid
subgraph Sources ["Source Tables"]
    subgraph SRC_INGEST_VN ["INGEST.VEEVA_NETWORK"]
        SRC_VN_HCP["hcp<br/>Veeva Network HCPs"]
        SRC_VN_HCO["hco<br/>Veeva Network HCOs"]
    end
    subgraph SRC_INGEST_OD ["INGEST.VEEVA_OPENDATA"]
        SRC_OD_HCP["hcp<br/>OpenData HCPs"]
        SRC_OD_HCO["hco<br/>OpenData HCOs"]
        SRC_AFFILS["affils<br/>HCP→HCO Affiliations"]
        SRC_ADDR["address<br/>Addresses with Geocoding"]
        SRC_HCO_HIER["hier<br/>HCO Hierarchy/Ownership"]
    end
    subgraph SRC_GOLD ["EDW.GOLD"]
        SRC_CRM_KOL["crm_kol_flags<br/>KOL Disease Flags"]
    end
    subgraph SRC_ADHOC ["EDW.ADHOC"]
        SRC_HCO_PROG["hco_program_flags<br/>MDA/COE/PPMD Flags"]
    end
end
```

Replace all intermediate layer subgraphs with single EDW.SILVER parent:
```mermaid
subgraph Silver ["EDW.SILVER"]
    subgraph Staging ["Staging Layer"]
        STG_VN_HCP["stg_vn_hcp"]
        STG_OD_HCP["stg_od_hcp"]
        STG_VN_HCO["stg_vn_hco"]
        STG_OD_HCO["stg_od_hco"]
        STG_AFFILS["stg_affiliations"]
        STG_ADDR["stg_addresses"]
        STG_OD_HCO_HIER["stg_od_hco_hierarchy"]
        STG_CRM["stg_crm_kol_flags"]
        STG_PROG["stg_od_hco_program_flags"]
    end
    
    subgraph Unified ["Unified"]
        INT_HCP_UNI["mdm_hcp_unified"]
        INT_HCO_UNI["mdm_hco_unified"]
    end
    
    subgraph Enriched ["Enriched"]
        INT_HCP_ENR["mdm_hcp_enriched"]
        INT_HCO_ENR["mdm_hco_enriched"]
    end
    
    subgraph Ownership ["Ownership"]
        INT_HCO_OWN_CAND["mdm_hco_top_ownership_candidates"]
        INT_HCO_OWN_RES["mdm_hco_ownership_resolved"]
    end
    
    subgraph Extension ["Extension"]
        INT_AFF_ENR["mdm_affiliations_enriched"]
        INT_AFF_EXT["mdm_affiliations_extension"]
    end
    
    subgraph Aggregation ["Aggregation"]
        INT_STATS["mdm_hcp_match_stats"]
    end
    
    subgraph Candidates ["Candidates"]
        INT_MATCH_CAND["mdm_match_candidates"]
        INT_PA_CAND_DBT["mdm_primary_affiliation_candidates"]
    end
    
    subgraph