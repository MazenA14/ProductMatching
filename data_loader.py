import pandas as pd
import re
from tqdm import tqdm

def normalize_text(text):
    """
    Normalize text by converting to lowercase, removing special characters, and applying custom rules.
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and symbols
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    text = re.sub(r'[#=/-]', ' ', text)  # Replace specific symbols with spaces
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing spaces
    text = text.strip()
    
    # Handle common typos or variations
    replacements = {
        'دانسيت': 'دانست',
        'الفانوفا بللللس': 'الفانوفا بلس',
        'الفانوفا بلاس': 'الفانوفا بلس',
        'الفا نوفا': 'الفانوفا',
        'داونوبرزول': 'داونوبرازول',
        'داونوبرازوال': 'داونوبرازول',
        'اقراص': 'كبسول',
        'امبولة': 'امبول',
        'امبولات': 'امبول',
        'امبووول': 'امبول',
        'امبوله': 'امبول',
        'قطره': 'قطرة',
        'كبسوول': 'كبسول',
        'كبسولة': 'كبسول',
        'كبسوله': 'كبسول',
        'قرص': 'كبسول',
        'اقراااص': 'كبسول',
        'جديد': '',
        'س ج': '',
        'س.ج': '',
        'سعر جديد': '',
        'ادويا': '',
        'حقن': '',
        'يوتوبيا': '',
        'يوتيوبيا': '',
        'س.ق': '',
        'تورسيريتك': 'تورستيريتك',
        'تورستوريتك': 'تورستيريتك',
        'تورستريتك': 'تورستيريتك',
        'تورسوريتك': 'تورستيريتك',
        'تورسيرتيك': 'تورستيريتك',
        'تورستورتيك': 'تورستيريتك',
        'تروستورتيك': 'تورستيريتك',
        'اماريل': 'امريل',
        'امريل1': 'امريل 1',
        'اماريل1': 'امريل 1',
        '3شريط': '3 شريط',
        '3شرائط': '3 شريط',
        '3شرررريط': '3 شريط',
        '3شريطططط': '3 شريط',
        'فنتال مركب': 'فنتال مركب',
        'فينتال مركب': 'فنتال مركب',
        'فنتال مركب*سبراى': 'فنتال مركب بخاخ',
        'فنتال مركب للاستنشاق': 'فنتال مركب بخاخ',
        'بيتاديرم': 'بيتاديرم',
        'فوليك اسيد': 'فوليك اسيد',
        'الفيولين-بى': 'الفيولين-بى',
        'ماء غريب بامبينو': 'ماء غريب بامبينو',
        'جراليبنتين': 'جراليبنتين',
        'جرالبتين': 'جراليبنتين',
        'جرالبنتين': 'جراليبنتين',
        'جرالبينتين': 'جراليبنتين',
        'جراليبانتين': 'جراليبنتين',
        'جراليبتين': 'جراليبنتين',
        'جراليبينتين': 'جراليبنتين',
        'ابيمول': 'ابيمول',
        'زيستريل': 'زيستريل',
        'زيستوريتك': 'زيستريل',
        'باي-كيتوجيسيك': 'باي-كيتوجيسيك',
        'باى كيتوجيسك': 'باي-كيتوجيسيك',
        'باى كيتوجيستك': 'باي-كيتوجيسيك',
        'باى كيتوجسيك': 'باي-كيتوجيسيك',
        'باى كيتوجسك': 'باي-كيتوجيسيك',
        'سويتال': 'سويتال',
        'لاميكتال': 'لاميكتال',
        'اماجلوست': 'اماجلوست',
        'اموجلويست': 'اماجلوست',
        'اموجلاويست': 'اماجلوست',
        'اموجلوست': 'اماجلوست',
        'فابوزول': 'فابوزول',
        'بكتيكلور': 'بكتيكلور',
        'باكتيكلور': 'بكتيكلور',
        'جويبوكس': 'جويبوكس',
        'جوى بوكس': 'جويبوكس',
        'اديمكس': 'اديمكس',
        'ايديمكس': 'اديمكس',
        'ريفاروسبير': 'ريفاروسبير',
        'ريفاروسبيرو': 'ريفاروسبير',
        'اليير': 'اليير',
        'الير': 'اليير',
        'اللير': 'اليير',
        'جولد بلس': 'جولد بلس',
        'جولد كلنزر': 'جولد بلس',
        'جولد كلنسر': 'جولد بلس',
        'اليفو': 'اليفو',
        'رينكس': 'رينكس',
        'تومكس بلس': 'تومكس بلس',
        'تومكس بلاس': 'تومكس بلس',
        'سيريتايد': 'سيريتايد',
        'سيريتيد': 'سيريتايد',
        'سيرتايد': 'سيريتايد',
        'سيريتد': 'سيريتايد',
        'ميكروسيرك': 'ميكروسيرك',
        'اولابكس': 'اولابكس',
        'اولابيكس': 'اولابكس',
        'اوتريفين': 'اوتريفين',
        'اوتروفين': 'اوتريفين',
        'اوترفين': 'اوتريفين',
        'اوترافين': 'اوتريفين',
        'نيزابيكس': 'نيزابيكس',
        'نيوروباتكس': 'نيوروباتكس',
        'نيورباتيكس': 'نيوروباتكس',
        'نيورباتكس': 'نيوروباتكس',
        'تارجوفلوكسين': 'تارجوفلوكسين',
        'تارجو': 'تارجوفلوكسين',
        'ار اكس': 'ار اكس',
        'فاروفيجا': 'فاروفيجا',
        'فارو فيجا': 'فاروفيجا',
        'ديكسافلوكس': 'ديكسافلوكس',
        'ماكسيلاز': 'ماكسيلاز',
        'يونيزيثرين': 'ماكسيلاز',
        'اليكويس': 'اليكويس',
        'ايليكويس': 'اليكويس',
        'اليكوايس': 'اليكويس',
        'اليكوس': 'اليكويس',
        'ايلى كويس': 'اليكويس',
        'ايلكويس': 'اليكويس',
        'شوجارلو': 'شوجارلو',
        'شوجالرو': 'شوجارلو',
        'شوجارلوبلس': 'شوجارلو بلس',
        'سبانيلا': 'سبانيلا',
        'استوهالت': 'استوهالت',
        'اوستوهالت': 'استوهالت',
        'اوتريفين سالاين': 'اوتريفين',
        'اماريل': 'امريل',
        'اماريل3': 'امريل 3',
        'اماريل3ملى': 'امريل 3',
        'دانست': 'دانست',
        'دانيست': 'دانست',
        'دانسيت': 'دانست',
        'تريتاس': 'تريتاس',
        'تورسيريتك': 'تورستيريتك',
        'توريسيريتك': 'تورستيريتك',
        'سيلدافا': 'سيلدافا',
        'سلدافا': 'سيلدافا',
        'فلاجيل': 'فلاجيل',
        'اريك': 'اريك',
        'ايريك': 'اريك',
        'سيمباتكس': 'سيمباتكس',
        'سيمباتيكس': 'سيمباتكس',
        'بيبون': 'بيبون',
        'بيبون بلاس': 'بيبون بلس',
        'بليتال': 'بليتال',
        'بيليتال': 'بليتال',
        'بريمبران': 'بريمبران',
        'ديمرا': 'ديمرا',
        'ديميرا': 'ديمرا',
        'انتيكوكس': 'انتيكوكس',
        'انتى كوكس': 'انتيكوكس',
        'تلفاست': 'تلفاست',
        'ادابالين': 'ادابالين',
        'اوكاربون': 'اوكاربون',
        'دورميفال': 'دورميفال',
        'افازير': 'افازير',
        'امريزول': 'امريزول',
        'توينزول': 'توينزول',
        'جابتن': 'جابتن',
        'جابتين': 'جابتن',
        'تريب جولد': 'تريب جولد',
        'موبيتيل': 'موبيتيل',
        'موبيتل': 'موبيتيل',
        'داونوبرازول': 'داونوبرازول',
        'داونيبرازول': 'داونوبرازول',
        'داون بيرازول': 'داونوبرازول',
        'داونبرازول': 'داونوبرازول',
        'الفانوفا بلس': 'الفانوفا بلس',
        'دانست': 'دانست',
        'فنتال مركب': 'فنتال مركب',
        'فنتال مركب*سبراى': 'فنتال مركب بخاخ',
        'بيتاديرم': 'بيتاديرم',
        'فوليك اسيد': 'فوليك اسيد',
        'الفيولين-بى': 'الفيولين-بى',
        'ماء غريب بامبينو': 'ماء غريب بامبينو',
        'جراليبنتين': 'جراليبنتين',
        'جرالبتين': 'جراليبنتين',
        'جرالبيتين': 'جراليبنتين',
        'جراليبتين': 'جراليبنتين',
        'جرالينتين': 'جراليبنتين',
        'جراليبنتين300ممتد المفعول': 'جراليبنتين 300 مجم ممتد المفعول',
        'جراليبنتين300اكس ار': 'جراليبنتين 300 مجم اكس ار',
        'جراليبنتين300 بديل جابتن': 'جراليبنتين 300 مجم',
        'ابيمول': 'ابيمول',
        'ابيكوسيللين': 'ابيمول',
        'زيستريل': 'زيستريل',
        'زيستريل20مجم': 'زيستريل 20 مجم',
        'باي-كيتوجيسيك': 'باي-كيتوجيسيك',
        'باى كيتوجيسك': 'باي-كيتوجيسيك',
        'باى كيتو جيسك': 'باي-كيتوجيسيك',
        'سويتال': 'سويتال',
        'لاميكتال': 'لاميكتال',
        'اماجلوست': 'اماجلوست',
        'فابوزول': 'فابوزول',
        'بكتيكلور': 'بكتيكلور',
        'جويبوكس': 'جويبوكس',
        'جوى بوكس': 'جويبوكس',
        'اديمكس': 'اديمكس',
        'اوميكاربكس': 'اديمكس',
        'ريفاروسبير': 'ريفاروسبير',
        'ريفاروسبيرو': 'ريفاروسبير',
        'اليير': 'اليير',
        'جولد بلس': 'جولد بلس',
        'جولد كلنزر': 'جولد بلس',
        'اليفو': 'اليفو',
        'رينكس': 'رينكس',
        'تومكس بلس': 'تومكس بلس',
        'سيريتايد': 'سيريتايد',
        'سيريتيد': 'سيريتايد',
        'سيرتايد': 'سيريتايد',
        'سيراتيد': 'سيريتايد',
        'ميكروسيرك': 'ميكروسيرك',
        'اولابكس': 'اولابكس',
        'اوتريفين': 'اوتريفين',
        'نيزابيكس': 'نيزابيكس',
        'نيوروباتكس': 'نيوروباتكس',
        'نيوروباتيكس': 'نيوروباتكس',
        'تارجوفلوكسين': 'تارجوفلوكسين',
        'تارجو': 'تارجوفلوكسين',
        'ار اكس': 'ار اكس',
        'فاروفيجا': 'فاروفيجا',
        'ديكسافلوكس': 'ديكسافلوكس',
        'ماكسيلاز': 'ماكسيلاز',
        'اليكويس': 'اليكويس',
        'ايليكويس': 'اليكويس',
        'اليكوس': 'اليكويس',
        'ايلكيوس': 'اليكويس',
        'شوجارلو': 'شوجارلو',
        'شوجار لو': 'شوجارلو',
        'سبانيلا': 'سبانيلا',
        'بيوفيت': 'بيوفيت',
        'بيوفيت امبول': 'بيوفيت امبول',
        'املوديبين': 'املوديبين',
        'املوديبيبن': 'املوديبين',
        'املودبين': 'املوديبين',
        'نانازوكسيد': 'نانازوكسيد',
        'نانا زوكسيد': 'نانازوكسيد',
        'نانوزوكسيد': 'نانازوكسيد',
        'برونتوجيست': 'برونتوجيست',
        'برونتوجيست امبول': 'برونتوجيست امبول',
        'موزابرايد': 'موزابرايد',
        'موزابريد': 'موزابرايد',
        'بريستافلام': 'بريستافلام',
        'زيثروماكس': 'زيثروماكس',
        'دولفين': 'دولفين',
        'دولفن': 'دولفين',
        'كيتولاك': 'كيتولاك',
        'فليكس': 'فليكس',
        'فلكس': 'فليكس',
        'اوميز': 'اوميز',
        'جليميبرايد': 'جليميبرايد',
        'جليمابرايد': 'جليميبرايد',
        'جليما برايد': 'جليميبرايد',
        'ديكساميثازون': 'ديكساميثازون',
        'ديكثاميسازون': 'ديكساميثازون',
        'زيرتك': 'زيرتك',
        'زيرتيك': 'زيرتك',
        'برافوتين': 'برافوتين',
        'تاروليمس': 'تاروليمس',
        'تيراتام': 'تيراتام',
        'ترايتام': 'تيراتام',
        'افيكسور': 'افيكسور',
        'ايفوكسر': 'افيكسور',
        'ايفكسور': 'افيكسور',
        'ايفيكسور': 'افيكسور',
        'ازموراب': 'ازموراب',
        'ايزوموراب': 'ازموراب',
        'افيميو': 'افيميو',
        'افميو': 'افيميو',
        'لى-فلوكس': 'لى-فلوكس',
        'لى فلوكس': 'لى-فلوكس',
        'كلوباترا': 'كلوباترا',
        'رومارين': 'رومارين',
        'ديفلوستيرو': 'ديفلوستيرو',
        'ديفليسترو': 'ديفلوستيرو',
        'ستاركوبريكس': 'ستاركوبريكس',
        'ستاركوبركس': 'ستاركوبريكس',
        'داونستيرولين': 'داونستيرولين',
        'داونوستورلين': 'داونستيرولين',
        'داونوسترولين': 'داونستيرولين',
        'داونسترولين': 'داونستيرولين',
        'وينديبين': 'وينديبين',
        'ويندبين': 'وينديبين',
        'هاي فريش': 'هاي فريش',
        'كونترولوك': 'كونترولوك',
        'كونترالوك': 'كونترولوك',
        'كونترلوك': 'كونترولوك',
        'بيبرا': 'بيبرا',
        'ببرا': 'بيبرا',
        'ديبافالي': 'ديبافالي',
        'ديبافلى': 'ديبافالي',
        'رجكور': 'رجكور',
        'فيافاج': 'فيافاج',
        'فيفاج': 'فيافاج',
        'دايت سويت': 'دايت سويت',
        'اكتوفنت': 'اكتوفنت',
        'اوكتوفنت': 'اكتوفنت',
        'اوكتوفينت': 'اكتوفنت',
        'اكتيفنت': 'اكتوفنت',
        'كوديلاترول': 'كوديلاترول',
        'كو ديلاترول': 'كوديلاترول',
        'مايوديورا': 'مايوديورا',
        'مايودورا': 'مايوديورا',
        'ايزوجاست': 'ايزوجاست',
        'كانزارتان': 'كانزارتان',
        'كانزرتان': 'كانزارتان',
        'اجركس': 'اجركس',
        'اجريكس': 'اجركس',
        'ريفاروسبير': 'ريفاروسبير',
        'ريفارو اسبير': 'ريفاروسبير',
        'ايزيس نعناع': 'ايزيس نعناع',
        'فيلداجلوز': 'فيلداجلوز',
        'فلداجلوس': 'فيلداجلوز',
        'بولي فريش': 'بولي فريش',
        'بولى فريش': 'بولي فريش',
        'لازيلاكتون': 'لازيلاكتون',
        'لازلكتون': 'لازيلاكتون',
        'لازيلكتون': 'لازيلاكتون',
        'ستارفيل': 'ستارفيل',
        'ستار فيل': 'ستارفيل',
        'نورمو تيرز': 'نورمو تيرز',
        'نورموتيرز': 'نورمو تيرز',
        'فلدين': 'فلدين',
        'دوسباتالين': 'دوسباتالين',
        'دوسبيتالين': 'دوسباتالين',
        'دوسبتالين': 'دوسباتالين',
        'دوسباتلين': 'دوسباتالين',
        'سيردالود': 'سيردالود',
        'لوفير': 'لوفير',
        'جينوزول': 'جينوزول',
        'سوفيناسين': 'سوفيناسين',
        'تريتاس كومب': 'تريتاس كومب',
        'زيثروكان': 'زيثروكان',
        'زيثرون': 'زيثروكان',
        'جليسرين': 'جليسرين',
        'جلسرين': 'جليسرين',
        'سيبروفلوكساسين': 'سيبروفلوكساسين',
        'سيبرو': 'سيبروفلوكساسين',
        'اوكيوجارد': 'اوكيوجارد',
        'سويتال': 'سويتال',
        'ليليبيل': 'ليليبيل',
        'ليليبل': 'ليليبيل',
        'لى لى بل': 'ليليبيل',
        'ليلى بل': 'ليليبيل',
        'ليلى بيل': 'ليليبيل',
        'فنتال مركب': 'فنتال مركب',
        'فنتال كومب': 'فنتال مركب',
        'فنتال كومبوزيتوم': 'فنتال مركب',
        'فنتال كومبيزيتم': 'فنتال مركب',
        'بيتاديرم': 'بيتاديرم',
        'فوليك اسيد': 'فوليك اسيد',
        'الفيولين-بى': 'الفيولين-بى',
        'ماء غريب بامبينو': 'ماء غريب بامبينو',
        'فلوكسينيز': 'فليكسونيز',
        'فاست فلام': 'فاستافلام',
        'فاستيفلام': 'فاستافلام',
        'برفاماكس': 'برافاماكس',
        'برافامكس': 'برافاماكس',
        'اتاكند': 'اتاكاند',
        'نيفلوب': 'نيفيلوب',
        'ايفى برونت': 'ايفيبرونت',
        'اوندلينزا': 'اوندالينز',
        'اوندالينزا': 'اوندالينز',
        'اوندلينز': 'اوندالينز',
        'سبازموديجستين': 'سبازمو ديجستين',
        'سبازمودايجستين': 'سبازمو ديجستين',
        'كرباميد': 'كارباميد',
        'افيفا فاسك': 'افيفافاسك',
        'افيفاسك': 'افيفافاسك',
        'روتاسى': 'روتاسي',
        'ليفوهستام': 'ليفوهيستام',
        'كال برج': 'كال بريج',
        'ادويفلام6امبول': 'ادويفلام 6 امبول',
        'توسيفان ان': 'توسيفان-ان',
        'تادانيرفى': 'تادانيرفي',
        'تادنرفى': 'تادانيرفي',
        'تادانيرافى': 'تادانيرفي',
        'تادانرفي': 'تادانيرفي',
        'ديلاترول25': 'ديلاترول 25',
        'تريفيستال': 'تريفاستال',
        'براديباكت': 'براديبيكت',
        'براديبكت': 'براديبيكت',
        'نوفيستوريك10': 'نوفيستوريك 10',
        'نوفى ستوريك': 'نوفيستوريك',
        'فلدين20': 'فلدين 20',
        'دولسيل3': 'دولسيل 3',
        'اترابيكس': 'اترابكس',
        'بلنديل': 'بلينديل',
        'كتافلام6': 'كتافلام 6',
        'ماكسييكال': 'ماكسيكال',
        'نازوكورت': 'نازاكورت',
        'نازا كورت': 'نازاكورت',
        'نازو كورت': 'نازاكورت',
        'تافسين': 'تافاسين',
        'سيتا برونكس': 'سيتابرونكس',
        'فليكسونيز': 'فليكسونيز',
        'جلاريل': 'نيوروفيت',
        'سيراتايد': 'سيريتايد',
        'سيريتيد': 'سيريتايد',
        'سيرتايد': 'سيريتايد',
        'فيبراميسن': 'فيبراميسين',
        'توب مود': 'توبمود',
        'كارنيفيتاادفانس': 'كارنيفيتا ادفانس',
        'كارنفيتا': 'كارنيفيتا',
        'فيسيرالجين': 'فيسرالجين',
        'سويتال50': 'سويتال 50',
        'جليبتس50': 'جليبتس 50',
        'بون كير1': 'بون كير 1',
        'كريستولب': 'كريستوليب',
        'كرستوليب': 'كريستوليب',
        'فيروجلوبين': 'فيروجلوبين',
        'ريكوكسى برايت': 'ريكوكسيبرايت',
        'ريكوكس برايد': 'ريكوكسيبرايت',
        'فيرسيرك16': 'فيرسيرك 16',
        'ريفاريست': 'ريفارست',
        'فلاكسو برايد': 'فلاكسوبرايد',
        'فلاكسوبريد': 'فلاكسوبرايد',
        'رومن تيجرا': 'رومانتيجرا',
        'روما نتيجيرا': 'رومانتيجرا',
        'ميتا كارديا': 'ميتاكارديا',
        'هيلسك': 'هيلسيك',
        'اريك تاليس': 'اريكتاليس',
        'اريك تيالس': 'اريكتاليس',
        'اريكتاماكس': 'اريكتاليس',
        'برونشيكام': 'برونشيكم',
        'بروش كريم': 'برونشيكم',
        'بروش برطمان': 'برونشيكم',
        'بانادول داى': 'بانادول داي',
        'بنادول': 'بانادول',
        'توسيستوب': 'توسيستوب',
        'لوبريفسك': 'لوبريفيسك',
        'كلوزابكس25': 'كلوزابكس 25',
        'دايجست ايز': 'دايجيست ايزى',
        'جاتى ستار': 'جاتيستار',
        'داونوبرازل': 'داونوبرازول',
        'داونى برازول': 'داونوبرازول',
        'سالبوفنت120': 'سالبوفنت 120',
        'سالبوفنت شــراب': 'سالبوفنت شراب',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Remove price references
    text = re.sub(r'\d+جنيه', '', text)
    text = re.sub(r'\d+ج', '', text)
    
    # Standardize dosage and concentration
    text = re.sub(r'(\d+)\s*مجم', r'\1 مجم', text)
    text = re.sub(r'(\d+)\s*مل', r'\1 مل', text)
    text = re.sub(r'(\d+)\s*امبول', r'\1 امبول', text)
    text = re.sub(r'(\d+)\s*كبسول', r'\1 كبسول', text)
    
    return text

def load_data(master_file, seller_file):
    # Load data with progress bar
    print("Loading master sheet...")
    master_df = pd.read_excel(master_file)
    print("Loading seller sheet...")
    seller_df = pd.read_excel(seller_file)

    # Normalize text using vectorized operations
    print("Normalizing master sheet product names...")
    master_df['product_name_normalized'] = master_df['product_name'].apply(normalize_text)
    master_df['product_name_ar_normalized'] = master_df['product_name_ar'].apply(normalize_text)
    
    print("Normalizing seller sheet product names...")
    seller_df['seller_item_name_normalized'] = seller_df['seller_item_name'].apply(normalize_text)

    return master_df, seller_df