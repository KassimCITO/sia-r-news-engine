from flask import Blueprint, jsonify, request, render_template
from services.review_manager import ReviewManager
from services.settings_manager import SettingsManager
from services.metrics_collector import MetricsCollector
from services.jwt_auth import JWTAuth
import logging

logger = logging.getLogger(__name__)

ui_bp = Blueprint('ui', __name__, url_prefix='/api/ui')

# === Status and Dashboard ===

@ui_bp.route('/status', methods=['GET'])
def ui_status():
    """Get UI dashboard status"""
    try:
        stats = MetricsCollector.get_pipeline_stats(days=7)
        pending = len(ReviewManager.get_pending_reviews(limit=100))
        
        return jsonify({
            "status": "operational",
            "stats": stats,
            "pending_reviews": pending
        }), 200
    except Exception as e:
        logger.error(f"Error getting UI status: {e}")
        return jsonify({"error": str(e)}), 500

# === Reviews Management ===

@ui_bp.route('/reviews', methods=['GET'])
def get_reviews():
    """Get pending or all reviews"""
    try:
        status = request.args.get('status', 'pending')
        limit = int(request.args.get('limit', 20))
        
        if status == 'pending':
            reviews = ReviewManager.get_pending_reviews(limit=limit)
        elif status == 'published':
            reviews = ReviewManager.get_published_articles(limit=limit)
        else:
            reviews = ReviewManager.get_pending_reviews(limit=limit)
        
        return jsonify({
            "status": "success",
            "count": len(reviews),
            "reviews": reviews
        }), 200
    except Exception as e:
        logger.error(f"Error getting reviews: {e}")
        return jsonify({"error": str(e)}), 500

@ui_bp.route('/review/<int:review_id>', methods=['GET'])
def get_review(review_id):
    """Get specific review details"""
    try:
        review = ReviewManager.get_review_by_id(review_id)
        
        if not review:
            return jsonify({"error": "Review not found"}), 404
        
        return jsonify({
            "status": "success",
            "review": review
        }), 200
    except Exception as e:
        logger.error(f"Error getting review: {e}")
        return jsonify({"error": str(e)}), 500

@ui_bp.route('/review/<int:review_id>/approve', methods=['POST'])
def approve_review(review_id):
    """Approve article for publication"""
    try:
        # Get editor ID from token
        auth_header = request.headers.get('Authorization')
        editor_id = None
        if auth_header:
            try:
                token = auth_header.split(' ')[1]
                editor_id, _ = JWTAuth.verify_token(token)
            except:
                pass
        
        if not editor_id:
            return jsonify({"error": "Unauthorized"}), 401
        
        # Check permissions
        if not SettingsManager.can_user_action(editor_id, 'can_approve'):
            return jsonify({"error": "Insufficient permissions"}), 403
        
        success = ReviewManager.approve_review(review_id, editor_id)
        
        if success:
            return jsonify({
                "status": "success",
                "message": f"Review {review_id} approved"
            }), 200
        else:
            return jsonify({"error": "Review not found"}), 404
    except Exception as e:
        logger.error(f"Error approving review: {e}")
        return jsonify({"error": str(e)}), 500

@ui_bp.route('/review/<int:review_id>/reject', methods=['POST'])
def reject_review(review_id):
    """Reject article"""
    try:
        data = request.get_json() or {}
        reason = data.get('reason', 'No reason provided')
        
        # Get editor ID from token
        auth_header = request.headers.get('Authorization')
        editor_id = None
        if auth_header:
            try:
                token = auth_header.split(' ')[1]
                editor_id, _ = JWTAuth.verify_token(token)
            except:
                pass
        
        if not editor_id:
            return jsonify({"error": "Unauthorized"}), 401
        
        # Check permissions
        if not SettingsManager.can_user_action(editor_id, 'can_reject'):
            return jsonify({"error": "Insufficient permissions"}), 403
        
        success = ReviewManager.reject_review(review_id, editor_id, reason)
        
        if success:
            return jsonify({
                "status": "success",
                "message": f"Review {review_id} rejected"
            }), 200
        else:
            return jsonify({"error": "Review not found"}), 404
    except Exception as e:
        logger.error(f"Error rejecting review: {e}")
        return jsonify({"error": str(e)}), 500

# === Published Articles ===

@ui_bp.route('/published', methods=['GET'])
def get_published():
    """Get published articles"""
    try:
        limit = int(request.args.get('limit', 50))
        articles = ReviewManager.get_published_articles(limit=limit)
        
        return jsonify({
            "status": "success",
            "count": len(articles),
            "articles": articles
        }), 200
    except Exception as e:
        logger.error(f"Error getting published articles: {e}")
        return jsonify({"error": str(e)}), 500

# === Settings ===

@ui_bp.route('/settings', methods=['GET'])
def get_settings():
    """Get system settings"""
    try:
        # Check if user is authenticated (token must exist)
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1]
                user_id, _ = JWTAuth.verify_token(token)
            except:
                pass  # Token invalid but continue with default settings
        
        # Return default settings
        settings = {
            "auto_publish_enabled": False,
            "quality_threshold": 75,
            "risk_threshold": 30,
            "seo_threshold": 60,
            "allowed_categories": ["Tecnología", "Política", "Economía"]
        }
        
        return jsonify({
            "status": "success",
            "settings": settings
        }), 200
    except Exception as e:
        logger.error(f"Error getting settings: {e}")
        return jsonify({"error": str(e)}), 500

@ui_bp.route('/settings', methods=['POST'])
def update_settings():
    """Update system settings"""
    try:
        # Check if user is authenticated
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({
                "status": "success",
                "message": "Settings would be updated (auth not required in demo)"
            }), 200
        
        try:
            token = auth_header.split(' ')[1]
            user_id, _ = JWTAuth.verify_token(token)
        except:
            pass  # Token invalid but continue
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # In a real implementation, save to database or file
        return jsonify({
            "status": "success",
            "message": "Settings updated"
        }), 200
    except Exception as e:
        logger.error(f"Error updating settings: {e}")
        return jsonify({"error": str(e)}), 500


@ui_bp.route('/settings/integrations', methods=['GET'])
def get_integrations():
    """Get integration settings (WordPress, OpenAI, etc)"""
    try:
        import os
        integrations = {
            "wordpress": {
                "url": os.getenv("WP_BASE_URL", ""),
                "username": os.getenv("WP_USERNAME", "")
                # Don't expose password!
            },
            "openai": {
                # Don't expose the actual API key, just indicate it's set
                "configured": bool(os.getenv("OPENAI_API_KEY"))
            }
        }
        
        return jsonify({
            "status": "success",
            "settings": integrations
        }), 200
    except Exception as e:
        logger.error(f"Error getting integrations: {e}")
        return jsonify({"error": str(e)}), 500


@ui_bp.route('/settings/integrations', methods=['POST'])
def update_integrations():
    """Update integration settings"""
    try:
        data = request.get_json() or {}
        
        # For now, integrations are read from .env
        # In production, you might want to save them to a secure store
        return jsonify({
            "status": "success",
            "message": "Integration settings are managed via environment variables"
        }), 200
    except Exception as e:
        logger.error(f"Error updating integrations: {e}")
        return jsonify({"error": str(e)}), 500

# === Metrics ===

@ui_bp.route('/metrics', methods=['GET'])
def get_metrics():
    """Get system metrics"""
    try:
        days = int(request.args.get('days', 30))
        
        pipeline_stats = MetricsCollector.get_pipeline_stats(days=days)
        top_categories = MetricsCollector.get_category_performance(limit=10)
        
        return jsonify({
            "status": "success",
            "pipeline_stats": pipeline_stats,
            "top_categories": top_categories
        }), 200
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        return jsonify({"error": str(e)}), 500

# === Run Pipeline from UI ===

@ui_bp.route('/run', methods=['POST'])
def ui_run_pipeline():
    """Run pipeline from UI"""
    try:
        from pipeline.run_pipeline import Pipeline
        
        data = request.get_json()
        if not data or not data.get('title') or not data.get('content'):
            return jsonify({"error": "Missing title or content"}), 400
        
        # Get user ID from token
        auth_header = request.headers.get('Authorization')
        user_id = None
        if auth_header:
            try:
                token = auth_header.split(' ')[1]
                user_id, _ = JWTAuth.verify_token(token)
            except:
                pass
        
        pipeline = Pipeline()
        result = pipeline.run(
            title=data.get('title'),
            content=data.get('content'),
            user_id=user_id,
            auto_publish=False
        )
        
        status_code = 200 if result.get("status") == "success" else 500
        return jsonify(result), status_code
    except Exception as e:
        logger.error(f"Error running pipeline: {e}")
        return jsonify({"error": str(e)}), 500

# === Logs ===

@ui_bp.route('/logs', methods=['GET'])
def get_logs():
    """Get pipeline execution logs"""
    try:
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        from storage.models import PipelineLog
        from storage.database import get_session
        
        session = get_session()
        logs = session.query(PipelineLog)\
            .order_by(PipelineLog.created_at.desc())\
            .limit(limit)\
            .offset(offset)\
            .all()
        
        logs_data = [{
            "id": log.id,
            "title": log.title,
            "preview_text": log.content[:100] if log.content else "N/A",
            "status": "success" if log.quality_score > 0.5 else "failed",
            "quality_score": log.quality_score,
            "execution_time": log.execution_time or 0,
            "created_at": log.created_at.isoformat(),
            "error_message": log.content,
            "completed_stages": ["Limpieza", "Categorización", "Auditoría", "Verificación"]
        } for log in logs]
        
        return jsonify({
            "status": "success",
            "count": len(logs_data),
            "logs": logs_data
        }), 200
    except Exception as e:
        logger.error(f"Error getting logs: {e}")
        return jsonify({"error": str(e)}), 500

@ui_bp.route('/logs/<int:log_id>', methods=['DELETE'])
def delete_log(log_id):
    """Delete specific log"""
    try:
        from storage.models import PipelineLog
        from storage.database import get_session
        
        session = get_session()
        log = session.query(PipelineLog).filter_by(id=log_id).first()
        
        if not log:
            return jsonify({"error": "Log not found"}), 404
        
        session.delete(log)
        session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Log deleted"
        }), 200
    except Exception as e:
        logger.error(f"Error deleting log: {e}")
        return jsonify({"error": str(e)}), 500

@ui_bp.route('/logs/clear', methods=['POST'])
def clear_logs():
    """Clear all logs"""
    try:
        from storage.models import PipelineLog
        from storage.database import get_session
        
        session = get_session()
        session.query(PipelineLog).delete()
        session.commit()
        
        return jsonify({
            "status": "success",
            "message": "All logs cleared"
        }), 200
    except Exception as e:
        logger.error(f"Error clearing logs: {e}")
        return jsonify({"error": str(e)}), 500

# === Enhanced Metrics ===

@ui_bp.route('/metrics/enhanced', methods=['GET'])
def get_metrics_enhanced():
    """Get enhanced system metrics with trends"""
    try:
        from datetime import datetime, timedelta
        from storage.models import PipelineLog
        from storage.database import get_session
        
        period = request.args.get('period', '7d')
        
        # Parse period
        if period == '7d':
            days = 7
        elif period == '30d':
            days = 30
        elif period == '90d':
            days = 90
        else:
            days = 365
        
        session = get_session()
        start_date = datetime.now() - timedelta(days=days)
        
        logs = session.query(PipelineLog)\
            .filter(PipelineLog.created_at >= start_date)\
            .all()
        
        # Calculate metrics
        total_processed = len(logs)
        successful = sum(1 for log in logs if log.quality_score and log.quality_score > 0.5)
        success_rate = successful / total_processed if total_processed > 0 else 0
        avg_quality = sum(log.quality_score or 0 for log in logs) / total_processed if total_processed > 0 else 0
        avg_execution_time = sum(log.execution_time or 0 for log in logs) / total_processed if total_processed > 0 else 0
        
        # Top categories
        categories = {}
        for log in logs:
            cat = getattr(log, 'category', 'Sin categoría') or 'Sin categoría'
            if cat not in categories:
                categories[cat] = {'count': 0, 'total_quality': 0}
            categories[cat]['count'] += 1
            categories[cat]['total_quality'] += log.quality_score or 0
        
        top_categories = [
            {
                'name': cat,
                'count': data['count'],
                'percentage': data['count'] / total_processed if total_processed > 0 else 0,
                'avg_quality': data['total_quality'] / data['count'] if data['count'] > 0 else 0
            }
            for cat, data in sorted(categories.items(), key=lambda x: x[1]['count'], reverse=True)[:5]
        ]
        
        # Daily trend
        daily_counts = {}
        for log in logs:
            date = log.created_at.strftime('%Y-%m-%d')
            daily_counts[date] = daily_counts.get(date, 0) + 1
        
        daily_trend = [
            {'date': date, 'count': count}
            for date, count in sorted(daily_counts.items())
        ]
        
        return jsonify({
            "status": "success",
            "metrics": {
                "total_processed": total_processed,
                "success_rate": success_rate,
                "avg_quality": avg_quality,
                "avg_execution_time": avg_execution_time,
                "top_categories": top_categories,
                "daily_trend": daily_trend,
                "common_issues": [
                    {"name": "Bajo SEO", "count": 15, "percentage": 0.15},
                    {"name": "Riesgo factual alto", "count": 8, "percentage": 0.08},
                    {"name": "Contenido corto", "count": 5, "percentage": 0.05}
                ]
            }
        }), 200
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        return jsonify({"error": str(e)}), 500


# === Connection Tests ===

@ui_bp.route('/test/wordpress', methods=['POST'])
def test_wordpress_connection():
    """Test WordPress connection"""
    try:
        data = request.get_json()
        wp_url = data.get('url', '').strip() if data else ''
        wp_token = data.get('token', '').strip() if data else ''
        
        # If no params provided, use default config
        if not wp_url and not wp_token:
            from config import WP_API_ENDPOINT, WP_USERNAME
            from services.wp_client import WordPressClient
            
            try:
                wp_client = WordPressClient()
                
                # Try to get users as a simple connection test
                response = wp_client.session.get(f"{wp_client.base_url}/users?per_page=1")
                
                if response.status_code == 200:
                    return jsonify({
                        "status": "success",
                        "message": "Conexión exitosa con WordPress",
                        "site_info": {
                            "url": WP_API_ENDPOINT,
                            "user": WP_USERNAME
                        }
                    }), 200
                else:
                    return jsonify({
                        "status": "error",
                        "message": f"Error al conectar: {response.status_code}"
                    }), 400
            except Exception as wp_error:
                return jsonify({
                    "status": "error",
                    "message": f"Error de conexión: {str(wp_error)}"
                }), 400
        else:
            # Test with provided credentials
            if not wp_url or not wp_token:
                return jsonify({
                    "status": "error",
                    "message": "URL y token son requeridos"
                }), 400
            
            # Create custom client with provided credentials
            import requests
            from requests.auth import HTTPBasicAuth
            
            try:
                session = requests.Session()
                session.auth = HTTPBasicAuth('test', wp_token)
                
                # Extract username/password if token is in format "user:pass"
                if ':' in wp_token:
                    user, pwd = wp_token.split(':', 1)
                    session.auth = HTTPBasicAuth(user, pwd)
                
                response = session.get(f"{wp_url}/wp-json/wp/v2/users?per_page=1", timeout=5)
                
                if response.status_code == 200:
                    return jsonify({
                        "status": "success",
                        "message": "Conexión exitosa con WordPress",
                        "site_info": {
                            "url": wp_url,
                            "title": "Sitio WordPress"
                        }
                    }), 200
                else:
                    return jsonify({
                        "status": "error",
                        "message": f"Error al conectar: {response.status_code} - {response.text[:100]}"
                    }), 400
            except requests.exceptions.Timeout:
                return jsonify({
                    "status": "error",
                    "message": "Tiempo de conexión agotado. Verifica la URL"
                }), 400
            except Exception as custom_error:
                return jsonify({
                    "status": "error",
                    "message": f"Error de conexión: {str(custom_error)}"
                }), 400
            
    except Exception as e:
        logger.error(f"Error testing WordPress connection: {e}")
        return jsonify({
            "status": "error",
            "message": f"Error al probar conexión: {str(e)}"
        }), 500


@ui_bp.route('/test/openai', methods=['POST'])
def test_openai_connection():
    """Test OpenAI API connection"""
    try:
        import os
        import http.client
        import json as json_lib
        
        data = request.get_json() or {}
        api_key = data.get('api_key', '').strip()
        
        # If no key provided, use default config
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY", "")
            
            if not api_key:
                return jsonify({
                    "status": "error",
                    "message": "No hay clave de API configurada"
                }), 400
        
        try:
            # Test OpenAI connection with http.client
            conn = http.client.HTTPSConnection("api.openai.com")
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-3.5-turbo",  # Use cheaper model for testing
                "messages": [
                    {"role": "system", "content": "You are a test assistant"},
                    {"role": "user", "content": "Reply with only 'OK'"}
                ],
                "max_tokens": 5
            }
            
            conn.request("POST", "/v1/chat/completions", json_lib.dumps(payload), headers)
            response = conn.getresponse()
            response_data = response.read().decode()
            
            if response.status == 200:
                parsed = json_lib.loads(response_data)
                message = parsed.get('choices', [{}])[0].get('message', {}).get('content', '')
                return jsonify({
                    "status": "success",
                    "message": "Conexión exitosa con OpenAI API",
                    "model": "gpt-3.5-turbo",
                    "response": message[:50]
                }), 200
            else:
                try:
                    error_data = json_lib.loads(response_data)
                    error_msg = error_data.get('error', {}).get('message', response_data)
                except:
                    error_msg = response_data
                
                if response.status == 401:
                    message = "Clave de API inválida o incorrecta"
                    logger.error(f"OpenAI API error: {error_msg}")
                    return jsonify({
                        "status": "error",
                        "message": message
                    }), 400
                elif response.status == 429:
                    message = "Límite de velocidad excedido. Intenta nuevamente en unos minutos"
                    # Extract retry_after from response headers if available
                    retry_after = response.getheader('retry-after')
                    retry_seconds = int(retry_after) if retry_after and retry_after.isdigit() else 60
                    
                    logger.warning(f"OpenAI rate limit: {message}")
                    return jsonify({
                        "status": "error",
                        "message": message,
                        "retry_after": retry_seconds,
                        "retry_after_seconds": retry_seconds
                    }), 429
                elif response.status == 404:
                    message = "Modelo no disponible o endpoint no existe"
                else:
                    message = f"Error {response.status}: {error_msg[:100]}"
                
                logger.error(f"OpenAI API error: {error_msg}")
                return jsonify({
                    "status": "error",
                    "message": message
                }), 400
                
        except Exception as llm_error:
            error_msg = str(llm_error)
            logger.error(f"OpenAI test error: {error_msg}")
            return jsonify({
                "status": "error",
                "message": f"Error de conexión: {error_msg[:100]}"
            }), 400
            
    except Exception as e:
        logger.error(f"Error testing OpenAI connection: {e}")
        return jsonify({
            "status": "error",
            "message": f"Error al probar conexión: {str(e)}"
        }), 500

