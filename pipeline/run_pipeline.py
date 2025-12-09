import logging
import time
import json
from datetime import datetime
from typing import Dict, Any, Optional

from services.cleaner import TextCleaner
from services.tagger_llm import TaggerLLM
from services.auditor_llm import AuditorLLM
from services.fact_checker import FactChecker
from services.verifier import Verifier
from services.humanizer import Humanizer
from services.seo_optimizer import SEOOptimizer
from services.planner import Planner
from services.taxonomy_normalizer import TaxonomyNormalizer
from services.taxonomy_autolearn import TaxonomyAutolearn
from services.wp_client import WordPressClient
from services.wp_taxonomy_manager import WordPressTaxonomyManager
from services.metrics_collector import MetricsCollector

from pipeline.schema import PipelineOutput, CleanerOutput, TaggerOutput, AuditorOutput
from pipeline.schema import FactCheckerOutput, VerifierOutput, HumanizerOutput, SEOOutput, PlannerOutput

logger = logging.getLogger(__name__)

class Pipeline:
    """SIA-R Pipeline - Orchestrates all processing stages"""
    
    def __init__(self):
        self.cleaner = TextCleaner()
        self.tagger = TaggerLLM()
        self.auditor = AuditorLLM()
        self.fact_checker = FactChecker()
        self.verifier = Verifier()
        self.humanizer = Humanizer()
        self.seo_optimizer = SEOOptimizer()
        self.planner = Planner()
        self.taxonomy_normalizer = TaxonomyNormalizer()
        self.taxonomy_autolearn = TaxonomyAutolearn()
        self.wp_client = WordPressClient()
        self.wp_taxonomy_mgr = WordPressTaxonomyManager()
    
    def run(self, title: str, content: str, user_id: Optional[int] = None, 
            auto_publish: bool = False) -> Dict[str, Any]:
        """
        Execute complete pipeline
        
        Args:
            title: Article title
            content: Article content
            user_id: User ID for logging
            auto_publish: Automatically publish to WordPress
        
        Returns:
            Pipeline output dict
        """
        start_time = time.time()
        logger.info("=== STARTING SIA-R PIPELINE ===")
        
        results = {
            "status": "success",
            "stages": {},
            "warnings": []
        }
        
        try:
            # Stage 1: Cleaning
            logger.info("Stage 1: Text Cleaning")
            cleaned_text = self.cleaner.clean(content)
            results["stages"]["cleaner"] = {
                "status": "completed",
                "original_length": len(content),
                "cleaned_length": len(cleaned_text)
            }
            
            # Stage 2: Tagging
            logger.info("Stage 2: LLM Tagging")
            tagger_result = self.tagger.extract_tags(cleaned_text)
            results["stages"]["tagger"] = {
                "status": "completed",
                "categories": tagger_result["suggested_categories"],
                "tags": tagger_result["suggested_tags"]
            }
            
            # Stage 3: Auditing
            logger.info("Stage 3: LLM Auditing")
            auditor_result = self.auditor.audit(cleaned_text)
            results["stages"]["auditor"] = {
                "status": "completed",
                "quality_metrics": auditor_result
            }
            
            # Stage 4: Fact Checking
            logger.info("Stage 4: Fact Checking")
            fact_check_result = self.fact_checker.check(cleaned_text)
            results["stages"]["fact_checker"] = {
                "status": "completed",
                "risk_score": fact_check_result["risk_score"],
                "flags": fact_check_result["red_flags"]
            }
            
            if fact_check_result["risk_score"] > 0.7:
                results["warnings"].append(f"High fact-check risk: {fact_check_result['risk_score']}")
            
            # Stage 5: Verification
            logger.info("Stage 5: Verification")
            verifier_result = self.verifier.verify(cleaned_text)
            results["stages"]["verifier"] = {
                "status": "completed",
                "coherence": verifier_result["coherence_score"],
                "valid": verifier_result["overall_valid"]
            }
            
            if not verifier_result["overall_valid"]:
                results["warnings"].append("Content failed verification checks")
            
            # Stage 6: Humanization
            logger.info("Stage 6: Humanization")
            humanized_text = self.humanizer.humanize(cleaned_text)
            results["stages"]["humanizer"] = {"status": "completed"}
            
            # Stage 7: SEO Optimization
            logger.info("Stage 7: SEO Optimization")
            seo_result = self.seo_optimizer.optimize(
                humanized_text,
                primary_entity=tagger_result["suggested_categories"][0] if tagger_result["suggested_categories"] else None
            )
            results["stages"]["seo"] = {
                "status": "completed",
                "h1": seo_result["h1"],
                "meta": seo_result["meta_description"],
                "schema_markup": seo_result.get("schema_markup", {})
            }
            
            # Stage 8: Taxonomy Normalization
            logger.info("Stage 8: Taxonomy Normalization")
            normalized_tax = self.taxonomy_normalizer.normalize(
                tagger_result["suggested_categories"],
                tagger_result["suggested_tags"]
            )
            results["stages"]["taxonomy"] = {
                "status": "completed",
                "categories": normalized_tax["categories"],
                "tags": normalized_tax["tags"]
            }
            
            # Stage 9: Planning
            logger.info("Stage 9: Planning & Publication Strategy")
            planner_result = self.planner.plan(
                humanized_text,
                normalized_tax["categories"],
                normalized_tax["tags"]
            )
            results["stages"]["planner"] = {
                "status": "completed",
                "pub_date": planner_result["publication_date"],
                "auto_publish": planner_result["auto_publish"]
            }
            
            # Stage 10: Taxonomy Auto-Learning
            logger.info("Stage 10: Taxonomy Auto-Learning")
            traffic_score = fact_check_result["risk_score"]  # Inverse: low risk = good content
            self.taxonomy_autolearn.learn_from_article(
                normalized_tax["categories"],
                normalized_tax["tags"],
                traffic_score=1.0 - traffic_score
            )
            results["stages"]["autolearn"] = {"status": "completed"}
            
            # Calculate overall quality score
            quality_score = self._calculate_quality_score(
                verifier_result, fact_check_result, auditor_result
            )
            
            # Determine if ready for publication
            ready_for_publication = (
                verifier_result["overall_valid"] and
                fact_check_result["risk_score"] < 0.6 and
                quality_score > 0.5
            )
            
            # Log execution
            execution_time = time.time() - start_time
            
            if user_id:
                MetricsCollector.log_pipeline_execution(
                    user_id=user_id,
                    input_text=content,
                    output_json=json.dumps(results),
                    status="success",
                    execution_time=execution_time,
                    model_used="gpt-4"
                )
            
            # Final output
            pipeline_output = {
                "status": "success",
                "execution_time_ms": round(execution_time * 1000, 2),
                "final_text": humanized_text,
                "final_h1": seo_result["h1"],
                "final_meta_description": seo_result["meta_description"],
                "final_schema_markup": seo_result.get("schema_markup", {}),
                "final_categories": normalized_tax["categories"],
                "final_tags": normalized_tax["tags"],
                "quality_score": quality_score,
                "ready_for_publication": ready_for_publication,
                "warnings": results["warnings"],
                "stages": results["stages"]
            }
            
            logger.info(f"=== PIPELINE COMPLETED SUCCESSFULLY ===")
            logger.info(f"Quality score: {quality_score}, Ready: {ready_for_publication}")
            
            return pipeline_output
            
        except Exception as e:
            logger.error(f"Pipeline error: {e}", exc_info=True)
            
            execution_time = time.time() - start_time
            if user_id:
                MetricsCollector.log_pipeline_execution(
                    user_id=user_id,
                    input_text=content,
                    output_json=json.dumps({"error": str(e)}),
                    status="failed",
                    execution_time=execution_time,
                    model_used="gpt-4",
                    error_message=str(e)
                )
            
            return {
                "status": "error",
                "execution_time_ms": round(execution_time * 1000, 2),
                "error": str(e),
                "message": "Pipeline execution failed"
            }
    
    def _calculate_quality_score(self, verifier_result, fact_check_result, auditor_result):
        """Calculate overall quality score"""
        score = 0.0
        
        # Coherence (30%)
        score += verifier_result["coherence_score"] * 0.3
        
        # Low fact-check risk (30%)
        score += (1.0 - fact_check_result["risk_score"]) * 0.3
        
        # Narrative quality from auditor (20%)
        narrative_score = auditor_result.get("narrative_quality", {}).get("score", 5) / 10.0
        score += narrative_score * 0.2
        
        # Neutrality (20%)
        neutrality_score = auditor_result.get("neutrality_score", {}).get("score", 5) / 10.0
        score += neutrality_score * 0.2
        
        return min(1.0, score)
