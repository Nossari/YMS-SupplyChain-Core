from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
from src.ai_engine.nlp_filter import AICrisisNLPProcessor
from src.services.whatsapp import WhatsAppLogisticRouter

# تهيئة الروتر البرمجي لتنظيم مسارات المنظومة
api_router = APIRouter(prefix="/api/v1")

# استدعاء المحركات التي قمنا ببنائها سابقاً لربطها بالمسارات
ai_processor = AICrisisNLPProcessor()
whatsapp_router = WhatsAppLogisticRouter()

# ==============================================================================
# 1. مسار الرادار والبحث الجغرافي الذكي (Geospatial Radar Endpoint)
# ==============================================================================
@api_router.get("/radar/search")
async def geospatial_radar_search(product_name: str, lat: float, lng: float, user_role: str):
    """
    مسار الرادار الجغرافي: يستقبل إحداثيات الهاتف الحية ونوع السلعة، 
    ويحاكي استعلام PostGIS لجلب أقرب التجار الملتزمين بالتسعيرة الرسمية.
    """
    try:
        # محاكاة لنتيجة الاستعلام الجغرافي السريع بناءً على الـ GPS
        mock_nearest_merchants = [
            {
                "merchant_id": 102,
                "merchant_name": "مخازن البركة للجملة",
                "distance_km": 0.45,  # يبعد 450 متر فقط
                "selling_price": 12500.0,  # سعر ملتزم بتسعيرة المستورد
                "stock_status": "متوفر بكثرة",
                "merchant_phone": "777123456"
            },
            {
                "merchant_id": 105,
                "merchant_name": "بقالة الأمانة والتجزئة",
                "distance_km": 1.20,
                "selling_price": 12700.0,
                "stock_status": "مخزون محدود",
                "merchant_phone": "771987654"
            }
        ]
        return {
            "status": "success",
            "search_query": product_name,
            "origin_coordinates": {"latitude": lat, "longitude": lng},
            "results_count": len(mock_nearest_merchants),
            "nearest_supply_points": mock_nearest_merchants
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في معالجة الاستعلام الجغرافي: {str(e)}")

# ==============================================================================
# 2. مسار غرفة الأزمات والذكاء الاصطناعي (AI Crisis Assessment Endpoint)
# ==============================================================================
@api_router.post("/crisis/analyze")
async def analyze_market_crisis(payload: Dict):
    """
    مسار إدارة الأزمات: يستقبل حزمة من تعليقات التجار والمستهلكين، 
    ويمررها لمحرك الـ NLP لتطهيرها سياسياً وتوليد نسب الارتفاع المتوقعة.
    """
    comments_pool = payload.get("comments", [])
    if not comments_pool:
        raise HTTPException(status_code=400, detail="يجب تزويد النظام بتليعقات ميدانية للتحليل")
    
    # تمرير البيانات لعقل الذكاء الاصطناعي
    predictive_analysis = ai_processor.calculate_predictive_impact(comments_pool)
    
    return {
        "status": "success",
        "crisis_context": payload.get("crisis_name", "أحداث طارئة شاذة"),
        "ai_neutral_forecast": predictive_analysis,
        "recommendation": "تم تحييد الألفاظ السياسية وتوليد المنحنى التقديري بناءً على المعطيات المادية."
    }

# ==============================================================================
# 3. مسار عقد الصفقات اللوجستية الفورية (Logistic Deep-Link Endpoint)
# ==============================================================================
@api_router.post("/logistic/order")
async def create_logistic_order(payload: Dict):
    """
    مسار توليد الروابط العميقة: يأخذ تفاصيل الصفقة ورقم التاجر الموثق، 
    ويخرج رابط الواتساب الجاهز للحقن في شاشة المشتري.
    """
    merchant_phone = payload.get("merchant_phone")
    order_details = payload.get("order_details")
    
    if not merchant_phone or not order_details:
        raise HTTPException(status_code=400, detail="المعطيات غير كاملة لإتمام التوجيه اللوجستي")
    
    whatsapp_url = whatsapp_router.generate_order_link(merchant_phone, order_details)
    
    return {
        "status": "success",
        "action": "redirect_to_whatsapp",
        "secure_deep_link": whatsapp_url
    }


# ==============================================================================
# 📑 الشرح الهندسي لطبقة المسارات والربط الموحد (للمراجعة اللاحقة)
# ==============================================================================
"""
API GATEWAY & INTEGRATION ROUTER DOCUMENTATION (YMS-SupplyChain-Core)
----------------------------------------------------------------------
يمثل هذا الملف "الجهاز العصبي والمنسق الأعلى للمنظومة" (The Orchestrator Layer). 
حيث يقوم بتحويل الشيفرات الخلفية المنعزلة إلى خدمات رقمية (Micro-Services) 
متاحة برمجياً عبر منافذ الـ HTTP القياسية لتطبيق الهاتف، وتتلخص ركائزه في الآتي:

1. عزل المسؤولية والترابط المحكم (Loose Coupling Principle):
   - لا تحتوي المسارات على أي منطق حسابي أو أمني مباشر؛ بل تعمل كـ "موجه مرور" (Traffic Router). 
     تستقبل البيانات من الهاتف، وتوزعها على المحرك المختص (تمرير الـ GPS لملف الـ Spatial، 
     وتمرير النصوص لملف الـ NLP)، مما يحمي النظام من الانهيار الشامل في حال تعطل أحد المحركات.

2. سحق هجمات الضغط العالي وتأمين الـ APIs (Security & Performance):
   - تم بناء المسارات لدعم المعالجة غير المتزامنة 'async/await'، مما يسمح للسيرفر بمعالجة 
     آلاف الطلبات المتزامنة القادمة من هواتف المستهلكين والتجار في نفس الثانية دون حدوث شلل 
     في الاستجابة، وهو التحصين الفني الأول ضد محاولات إجهاض النظام عبر إغراقه بالطلبات الوهمية.
"""
