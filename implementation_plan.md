# Phase 3: Enhancements & SEO

## Goal Description
Enhance the SEO capabilities of the SIA-R News Engine by replacing heuristic-based optimization with LLM-based generation for Meta Descriptions and H2 tags. Additionally, implement JSON-LD Schema Markup generation to improve search engine visibility.

## User Review Required
> [!NOTE]
> This update involves more LLM calls per article (for Meta Description and H2s), which may increase API costs/latency slightly but will significantly improve quality.

## Proposed Changes

### Core Services

#### [MODIFY] [seo_optimizer.py](file:///d:/Prj/sia-r-news-engine/services/seo_optimizer.py)
- **Refactor `_generate_meta_description`**: Replace regex/slicing with an LLM prompt to generate compelling, keyword-rich meta descriptions.
- **Refactor `_generate_h2_suggestions`**: Replace first-sentence logic with LLM analysis to suggest semantic subheadings based on content structure.
- **Implement `_generate_schema_markup`**: Add a new method to generate JSON-LD schema (NewsArticle type) including headline, date, author, and image placeholders.
- **Update `optimize` method**: Include schema markup in the returned dictionary.

#### [MODIFY] [pipeline/run_pipeline.py](file:///d:/Prj/sia-r-news-engine/pipeline/run_pipeline.py)
- **Update Stage 7**: logic to extract and store the new `schema_markup` field from the SEO optimizer.
- **Update Final Output**: Ensure `final_schema_markup` is included in the returned pipeline output.

## Phase 4: Maintenance & Bugfixes

### Maintenance
#### [MODIFY] [services/trend_harvester.py](file:///d:/Prj/sia-r-news-engine/services/trend_harvester.py)
- **Implement Caching**: Increase `_cache_ttl` to 3 hours (10800 seconds).
- **Optimize Fetch**: Ensure `fetch_all_trends` relies on cache by default.

#### [MODIFY] [services/scheduler.py](file:///d:/Prj/sia-r-news-engine/services/scheduler.py)
- **Optimize Schedule**: Change `update_trends` interval from 1 hour to 3 hours.

## Verification Plan

### Automated Tests
- Run `test_seo_optimizer.py` (will create if needed or run manual python script).
- Verify the output contains valid JSON-LD.

### Manual Verification
- Generate an article using `article_generator.py` (via a script or REPL).
- Inspect the logs to see the generated H1, Meta Description, and Schema Markup.
- Check that H2 suggestions make semantic sense.
