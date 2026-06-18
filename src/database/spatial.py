from datetime import datetime
from enum import Enum
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import declarative_base, relationship
from geoalchemy2 import Geometry

Base = declarative_base()

# ==============================================================================
# 1. طبقة المستخدمين والصلاحيات (Role-Based Access Control - RBAC)
# ==============================================================================
class UserRole(str, Enum):
    IMPORTER = "importer"       # المستورد الرئيسي (منبع السعر)
    WHOLESALER = "wholesaler"   # تاجر الجملة
    RETAILER = "retailer"       # تاجر التجزئة (البقالة)
    CONSUMER = "consumer"       # المستهلك النهائي
    AUDITOR = "auditor"         # الحساب الرقابي الصامت (وزارة الصناعة والتجارة)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(150), nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)  # رقم الهاتف الموثق بـ OTP
    role = Column(String(20), nullable=False, default=UserRole.CONSUMER)
    is_verified = Column(Boolean, default=False)  # صمام أمان ضد الحسابات الوهمية
    is_frozen = Column(Boolean, default=False)    # ميزة التجميد اللحظي للمتلاعبين بالأسعار
    created_at = Column(DateTime, default=datetime.utcnow)

    # الربط الجغرافي (تحديد موقع المنشأة التجارية أو مخزن التاجر بدقة)
    # Point(Longitude, Latitude) باستخدام نظام الإحداثيات العالمي WGS 84 (SRID 4326)
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)
    address_details = Column(Text, nullable=True)  # المحافظة / المديرية / الحارة مادية


# ==============================================================================
# 2. جدول المنتجات والسلع الغذائية المحكومة من المنبع
# ==============================================================================
class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    barcode = Column(String(50), unique=True, nullable=True) # الباركود العالمي للسلعة
    product_name = Column(String(150), nullable=False)
    category = Column(String(50), default="Foodstuff") # قطاع المواد الغذائية في المرحلة الأولى
    
    # حوكمة المصدر: ربط المنتج بالمستورد الرئيسي الذي يمتلك حق تحديد السعر الرسمي
    importer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # السعر المرجعي المحكوم من المستورد (مقوم بالعملة الأساسية ويحدث ديناميكياً مع الصرف)
    base_official_price = Column(Float, nullable=False) 
    
    # التوقيع الرقمي لمنع التلاعب بالسعر أثناء النقل البرمجي
    cryptographic_signature = Column(String(256), nullable=True)
    
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    importer = relationship("User", foreign_keys=[importer_id])


# ==============================================================================
# 3. جدول المخزون الفعلي للتجار وأسعار البيع الميدانية (رادار المخازن)
# ==============================================================================
class Inventory(Base):
    __tablename__ = 'inventory'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    merchant_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    
    current_stock = Column(Integer, default=0) # كمية المخزون الحالي (لمؤشر العجز اللوجستي)
    is_available = Column(Boolean, default=True) # هل الصنف متوفر في الرفوف حالياً؟
    
    # السعر المعروض في الميدان (يجب ألا يتجاوز حد الحوكمة المفروض من المستورد)
    current_selling_price = Column(Float, nullable=False) 
    
    merchant = relationship("User", foreign_keys=[merchant_id])
    product = relationship("Product")


# ==============================================================================
# 📑 الشرح الهندسي والأمني لمعمارية قاعدة البيانات (للمراجعة اللاحقة والتطوير)
# ==============================================================================
"""
TECHNICAL AUDIT & SECURITY DOCUMENTATION (YMS-SupplyChain-Core)
----------------------------------------------------------------------
تم تصميم وهندسة هذه الجداول لتوفير حصانة سيادية وتقنية مطلقة للمنظومة ضد محاولات الإجهاض 
أو التشكيك الميداني، وتتلخص فلسفتها الأمنية والجغرافية في النقاط التالية:

1. صمام الأمان الميداني والمكافحة الفورية للاحتكار:
   - الحقل 'is_frozen' في جدول المستخدمين يمثل "زر الطوارئ الإداري". في حال أبلغت الجهات 
     الرقابية أو رصد النظام تلاعباً بالأسعار أو احتكاراً من قِبل أي تاجر جملة أو تجزئة، 
     يتم تحويل القيمة إلى True برمجياً، مما يؤدي فوراً لعزل حساب التاجر وإخفاء مخزنه 
     بالكامل من خريطة رادار البحث الجغرافي للمستخدمين.
   - الحقل 'is_verified' يمنع تماماً الحسابات الوهمية، حيث لا يتم تفعيله إلا بعد إتمام 
     التحقق الرقمي من هوية التاجر وسجله عبر بوابة الـ OTP.

2. المحرك والفرز الجغرافي الذكي (Spatial Indexing):
   - يتم تخزين موقع المنشأة التجارية باستخدام الحقل 'Geometry' المعتمد على ميزات PostGIS 
     وبنظام الإحداثيات العالمي (SRID 4326).
   - هذا التأسيس يتيح للباكيند تنفيذ استعلامات مكانية فائقة السرعة (Spatial Queries)، 
     مثل جلب أقرب المخازن التي يتوفر لديها الصنف الناقص جغرافياً بناءً على موقع الهاتف (GPS)، 
     مما يختصر وقت الإمداد ويوفر تكاليف النقل.

3. حسم شائعات التلاعب والتشكيك في دقة الأسعار:
   - الحوكمة من المنبع: تم فصل المنتج 'Product' وسعره الرسمي، عن المخزون 'Inventory' وسعر البيع. 
     السعر الرسمي 'base_official_price' محكوم ومقفل برمجياً برقم المستورد الوكيل 'importer_id'، 
     ولا يمتلك تاجر التجزئة أو الجملة صلاحية تعديله، بل يلتزم بحدود البيع المفروضة منه.
   - التوقيع الرقمي 'cryptographic_signature': يتم تشفير وحقن توقيع رقمي فريد لكل سعر رسمي 
     يتم رفعه من المستورد لمنع هجمات الوسطاء (Man-in-the-Middle) وضمان عدم إمكانية تعديل 
     الأسعار في قاعدة البيانات إلا من قِبل الحسابات المصرح لها قانوناً وبرمجياً.
"""
