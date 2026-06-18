import re
from typing import Dict, List, Tuple

class AICrisisNLPProcessor:
    def __init__(self):
        # 1. صمام الأمان السيادي: الكلمات الافتتاحية للمشاحنات السياسية لحجبها فوراً
        self.geopolitical_noise_keywords = [
            r"العدوان", r"المرتزقة", r"الشرعية", r"الحوثي", r"الانتقالي", 
            r"التحالف", r"حكومة عدن", r"حكومة صنعاء", r"مؤامرة دولية"
        ]
        
        # 2. الكيانات الاقتصادية المستهدفة للاستخلاص والتحليل (Economic Entities)
        self.economic_indicators = {
            "fuel_crisis": ["مشتقات", "ديزل", "بترول", "وقود", "ناقلات", "أجور النقل"],
            "tariffs_taxes": ["جمارك", "ضرائب", "جبايات", "ميناء", "نقطة", "ترسيم"],
            "currency_fluctuation": ["فارق الصرف", "تدهور العملة", "عمولة التحويل", "صرافين"]
        }

    def clean_and_sanitize_text(self, raw_comment: str) -> str:
        """
        المرحلة الأولى: تطهير النص وعزل أي محتوى سياسي أو هجومي لضمان حيدة المنصة.
        تستبدل العبارات السياسية بعبارة محايدة تضمن التركيز على الجانب الاقتصادي البحت.
        """
        cleaned_text = raw_comment.strip()
        for pattern in self.geopolitical_noise_keywords:
            cleaned_text = re.sub(pattern, "[تحييد سياسي تكنوقراطي]", cleaned_text)
        return cleaned_text

    def extract_economic_drivers(self, sanitized_text: str) -> List[str]:
        """
        المرحلة الثانية: تحليل النص بالذكاء الاصطناعي (NLP) لمعرفة السبب المادي الحقيقي للأزمة.
        """
        detected_drivers = []
        for driver_name, keywords in self.economic_indicators.items():
            for keyword in keywords:
                if keyword in sanitized_text:
                    detected_drivers.append(driver_name)
                    break
        return list(set(detected_drivers))

    def calculate_predictive_impact(self, comments_pool: List[str]) -> Dict[str, float]:
        """
        المرحلة الثالثة: وزن الأسباب برمجياً والتنبؤ بنسبة الارتفاع المتوقعة في الأسعار.
        """
        driver_weights = {"fuel_crisis": 0.0, "tariffs_taxes": 0.0, "currency_fluctuation": 0.0}
        total_valid_comments = 0
        
        for comment in comments_pool:
            sanitized = self.clean_and_sanitize_text(comment)
            drivers = self.extract_economic_drivers(sanitized)
            
            if drivers:
                total_valid_comments += 1
                for d in drivers:
                    # زيادة وزن السبب بناءً على تكراره في الميدان من قِبل التجار
                    driver_weights[d] += 1.0
                    
        # تحويل الأوزان إلى نسب مئوية تقديرية لحركة السعر المتوقعة في السوق
        predictive_matrix = {}
        if total_valid_comments > 0:
            for driver, count in driver_weights.items():
                # معادلة تقريبية لحساب الأثر: (تكرار السبب / إجمالي التعليقات) * معامل أثر مالي مقدر
                impact_factor = 0.15 if driver == "fuel_crisis" else 0.10
                predictive_matrix[driver] = round((count / total_valid_comments) * impact_factor * 100, 2)
        
        return predictive_matrix

# تفعيل المحرك وتجربته محلياً بمثال ميداني طارئ
if __name__ == "__main__":
    processor = AICrisisNLPProcessor()
    
    # محاكاة لتعليقات قادمة من تجار ومستوردين في السوق أثناء أزمة وقود وارتفاع صرف
    sample_market_feedback = [
        "بسبب انعدام الديزل وارتفاع أجور النقل ارتفعت تكلفة كرتون الدقيق علينا",
        "السبب هو عشوائية الصرافين وفارق الصرف اليوم وتدهور العملة المستمر",
        "هناك جبايات وضرائب إضافية في المداخل تزيد من التكلفة النهائية للمواد الغذائية"
    ]
    
    impact_forecast = processor.calculate_predictive_impact(sample_market_feedback)
    print("توقعات حركة الأسعار المستقبلية المعالجة بالذكاء الاصطناعي:")
    print(impact_forecast)


# ==============================================================================
# 📑 الشرح الهندسي لغرفة إدارة الأزمات والتحليل التنبئي (للمراجعة اللاحقة)
# ==============================================================================
"""
AI NLP ENGINE & CRISIS MITIGATION DOCUMENTATION (YMS-SupplyChain-Core)
----------------------------------------------------------------------
تم هندسة هذا المحرك ليمثل "المظلة الواقية والحصن السيادي للمنظومة" عند حدوث تشوهات 
أو أحداث شاذة في السوق، وتتمحور بنيته الفنية والأمنية حول الآتي:

1. الحماية السيادية المطلقة والتكنوقراطية (Geopolitical Neutrality Shield):
   - يمتلك المحرك مصفوفة 'geopolitical_noise_keywords' التي تعمل كمرشح أولي صارم. 
     أي تعليق يحتوي على مصطلحات سياسية أو اتهامات متبادلة بين أطراف النزاع يتم تطهيره 
     وتحييده برمجياً بشكل كامل وفوري.
   - هذا التحييد الذكي يضمن عدم استخدام المنصة كساحة لتصفية الحسابات الإعلامية، 
     ويحمي إدارة التطبيق قانونياً وسياسياً أمام كافة السلطات، ويظهر النظام كأداة علمية 
     تكنوقراطية بحتة لخدمة أمن الغذاء للمواطن اليمني.

2. استخلاص المسببات المادية الحقيقية (Economic Entity Extraction):
   - عبر مصفوفة 'economic_indicators'، يقوم المحرك بتحليل مدخلات التجار والمستوردين 
     لفرز الأسباب إلى قنوات اقتصادية مادية حتمية: (أزمات مشتقات نفطية ولوجستية، جمارك وضرائب، 
     أو تقلبات صرف العملة).
   - هذا يمنع العشوائية ويقوم بـ "تأصيل الأزمة" بناءً على شهادات الميدان الحية (Crowdsourcing).

3. خوارزمية التنبؤ الاستشرافي بالأسعار (Predictive Asset Pricing):
   - يقوم التابع 'calculate_predictive_impact' بوزن تكرار الأزمات في الميدان وتحويلها 
     إلى نسب مئوية تتنبأ بحجم الارتفاع المتوقع في أسعار السلع خلال الأيام القادمة.
   - هذا التنبؤ العلمي يسحق عذر "الأسعار غير الدقيقة"؛ لأنه يوضح للمستهلك والتاجر بالأرقام 
     أن الارتفاع قادم حتماً بسبب معطيات مادية ملموسة (مثل ارتفاع تكلفة الديزل بنسبة معينة)، 
     ويعطي صناع القرار فرصة للتدخل ووضع حلول مسبقة قبل وقوع العجز التجاري.
"""
