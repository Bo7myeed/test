# Directory Comparison Tool

مقارنة شاملة بين محتوى مجلدي ModelEngine و ModelEngine2

## Overview / نظرة عامة

This tool provides a comprehensive comparison between the contents of two directories, specifically designed to compare `ModelEngine` and `ModelEngine2` folders completely.

يوفر هذا البرنامج مقارنة شاملة بين محتويات مجلدين، مصمم خصيصاً لمقارنة مجلدي ModelEngine و ModelEngine2 بشكل كامل.

## Features / المميزات

- **Complete File Structure Analysis**: Compares all files and subdirectories
- **Content Comparison**: Uses MD5 hashing for efficient content comparison  
- **Size Comparison**: Identifies files with different sizes
- **Text File Diff**: Provides line-by-line differences for text files
- **Binary File Support**: Handles all file types including images, archives, and models
- **Detailed Reports**: Generates both console output and detailed JSON/text reports

## Files / الملفات

### Main Tools / الأدوات الرئيسية
- `directory_comparison.py` - Main comparison tool
- `generate_comparison_report.py` - Detailed report generator

### Generated Reports / التقارير المُنتجة
- `comparison_summary.txt` - Quick summary in text format
- `comparison_report.json` - Detailed JSON report with all data

## Usage / الاستخدام

### Basic Comparison / المقارنة الأساسية
```bash
python directory_comparison.py ModelEngine ModelEngine2
```

### Generate Detailed Reports / إنتاج التقارير المفصلة
```bash
python generate_comparison_report.py
```

## Comparison Results / نتائج المقارنة

### Summary / الملخص
- **ModelEngine**: 559 files / ملف
- **ModelEngine2**: 131 files / ملف  
- **Identical files**: 128 files / ملف متطابق
- **Different files**: 3 files / ملفات مختلفة
- **Files only in ModelEngine**: 428 files / ملف موجود فقط في ModelEngine
- **Files only in ModelEngine2**: 0 files / لا يوجد

### Key Differences / الاختلافات الرئيسية

1. **Size Difference**: ModelEngine contains 428 additional files not present in ModelEngine2
2. **Content Changes**: 3 files have different content between the directories:
   - `resource pack.zip` - Different archive contents
   - `resource pack/assets/minecraft/models/item/leather_horse_armor.json` - Model mappings reordered
   - `.data/cache.json` - Cache data differences

3. **Model Sets**: ModelEngine contains additional model sets:
   - `icon` collection (beta games logo)
   - `last` collection (dragon/creature models)  
   - `tough` collection (dragon/creature models)

## Technical Details / التفاصيل التقنية

### Comparison Method / طريقة المقارنة
- **File Existence**: Checks if files exist in both directories
- **Hash Comparison**: Uses MD5 hashing for content verification
- **Size Verification**: Compares file sizes for quick difference detection
- **Text Analysis**: Line-by-line diff for configuration and JSON files

### Supported File Types / أنواع الملفات المدعومة
- Configuration files (`.yml`, `.json`)
- Model files (`.bbmodel`)
- Texture files (`.png`)  
- Archive files (`.zip`)
- Shader files (`.fsh`, `.vsh`)
- All other binary and text formats

## Conclusion / الخلاصة

The comparison reveals that **ModelEngine2 is a subset of ModelEngine**, containing only the essential files needed for the `lesgo` model, while ModelEngine contains additional collections (`icon`, `last`, `tough`) and extended functionality.

تُظهر المقارنة أن **ModelEngine2 هو مجموعة فرعية من ModelEngine**، يحتوي فقط على الملفات الأساسية اللازمة لنموذج `lesgo`، بينما يحتوي ModelEngine على مجموعات إضافية ووظائف موسعة.

### Recommendations / التوصيات
- If you need only the `lesgo` model, ModelEngine2 is sufficient
- For complete functionality with all models, use ModelEngine
- The differences in cache files are expected and don't affect functionality
- Model mapping order differences in `leather_horse_armor.json` may affect custom model data IDs

إذا كنت تحتاج فقط لنموذج `lesgo`، فإن ModelEngine2 كافٍ
للوظائف الكاملة مع جميع النماذج، استخدم ModelEngine