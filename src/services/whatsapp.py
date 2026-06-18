import urllib.parse
from typing import Dict

class WhatsAppLogisticRouter:
    def __init__(self):
        # النطاق الأساسي للروابط العميقة لـ WhatsApp API عابر المنصات (Android/iOS)
        self.base_url = "https://api.whatsapp.com/send"

    def generate_order_link(self, merchant_phone: str, order_details: Dict) -> str:
        """
        توليد رابط عميق ومحمي يوجه المشتري مباشرة إلى محادثة التاجر اللوجستية 
        مع صياغة نصية مشفرة ومجهرة للطلب لتسريع حركة الشحن.
        """
        # تنظيف رقم الهاتف وتجهيزه بالصيغة الدولية (مثل: 967)
        clean_phone = "".join(filter(str.isdigit, merchant_phone))
        if clean_phone.startswith("0"):
            clean_phone = "967" + clean_phone[1:]
        elif not clean_phone.startswith("967") and len(clean_phone) == 9:
            clean_phone = "967" + clean_phone

        # صياغة الرسالة التلقائية باحترافية لتوفير الوقت في الميدان
        templated_message = (
            f"📦 *طلب توريد لوجستي عبر منصة سوق رادار*\n"
            f"----------------------------------------\n"
            f"🔹 *المنتج المطلوب:* {order_details.get('product_name')}\n"
            f"🔹 *الكمية المقدرة:* {order_details.get('quantity')} كرتون/قطعة\n"
            f"🔹 *نوع المشتري:* {order_details.get('buyer_role')}\n"
            f"📍 *موقع الشحن (جغريافياً):* {order_details.get('buyer_address')}\n"
            f"----------------------------------------\n"
            f"💡 _يرجى تأكيد توفر الكمية وتحديد وقت الشحن الفوري._"
        )

        # ترميز النص برمجياً (URL Encoding) لضمان سلامة الحروف العربية أثناء النقل
        encoded_message = urllib.parse.quote(templated_message)
        
        # بناء الرابط النهائي الموجه عابر التطبيقات
        final_deep_link = f"{self.base_url}?phone={clean_phone}&text={encoded_message}"
        return final_deep_link

# اختبار المحرك محلياً بمثال لطلب حقيقي في السوق
if __name__ == "__main__":
    router = WhatsAppLogisticRouter()
    
    sample_order = {
        "product_name": "دقيق السعيد - 50 كيلو",
        "quantity": 20,
        "buyer_role": "تاجر تجزئة (بقالة الأمانة)",
        "buyer_address": "صنعاء - مديرية السبعين - جول مدرم"
    }
    
    # رقم هاتف تاجر الجملة المفترض في الميدان
    merchant_number = "777123456"
    
    generated_url = router.generate_order_link(merchant_number, sample_order)
    print("🚀 الرابط العميق الجاهز للحقن في زر التطبيق:")
    print(generated_url)


# ==============================================================================
# 📑 الشرح الهندسي لنظام التوجيه وعقد الصفقات اللوجستية (للمراجعة اللاحقة)
# ==============================================================================
"""
GEOSPATIAL ROUTING & DEEP-LINKING DOCUMENTATION (YMS-SupplyChain-Core)
----------------------------------------------------------------------
تم هندسة هذا الموديل ليكون شريان الربط الميداني السريع لإتمام الصفقات التجارية 
بأقل استهلاك ممكن للبيانات والشبكة، وتتلخص ركائزه الفنية في الآتي:

1. كسر البيروقراطية الرقمية واستهلاك الإنترنت (Data Ingestion & Lean UX):
   - بدلاً من إجبار المستخدمين على إتمام الدورة المالية (Transaction Layer) داخل التطبيق 
     مما يتطلب بنية تحتية بنكية معقدة وسرعات إنترنت عالية قد لا تتوفر للتجار في كافة المديريات، 
     يقوم التابع 'generate_order_link' بتحويل حركة المرور (Traffic) مباشرة إلى البنية التحتية 
     العملاقة لشركة WhatsApp عبر الروابط العميقة (Deep Links).
   - هذا يجعل التطبيق خفيفاً جداً ومقاوماً لانقطاع الإنترنت المحلي، حيث يعمل فقط كـ "دليل رادار ذكي" 
     يوجه الأطراف لبعضها، ويترك التنفيذ اللوجستي لمرونة السوق المعتادة.

2. حوكمة الصياغة وتأمين البيانات (Structured Communication):
   - صياغة الرسالة عبر قوالب صارمة 'templated_message' يضمن جدية الطلب ويوفر صياغة علمية 
     تتضمن (اسم السلعة، الكمية، موقع الـ GPS والمستندات)، مما يمنع العشوائية والرسائل الوهمية، 
     ويسهل على كبار المستوردين وتجار الجملة أرشفة وجرد الطلبات القادمة من رادار التطبيق بسهولة.
"""
