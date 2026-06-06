import os
from google import genai

def generate_bengali_script(topic):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[⚠️] GEMINI_API_KEY পাওয়া যায়নি! ডিফল্ট ব্যাকআপ স্ক্রিপ্ট লোড হচ্ছে।")
        return get_default_data()

    # যে মডেলগুলো ফ্রি এবং ক্লাউডে সচল থাকে তাদের তালিকা (অগ্রাধিকার ভিত্তিতে)
    models_to_try = [
        "gemini-1.5-flash",    # ক্লাউড সার্ভারে সবচেয়ে বেশি স্থিতিশীল ও ফ্রি
        "gemini-2.0-flash",    # লেটেস্ট জেমিনি ২.০
        "gemini-1.5-pro"       # হেভি ওয়েট ব্যাকআপ মডেল
    ]

    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    প্রসঙ্গ: {topic}
    কাজ: ওপরের প্রসঙ্গের ওপর একটি আকর্ষণীয় বাংলা শর্টস ভিডিওর স্ক্রিপ্ট তৈরি করো। দৈর্ঘ্য হবে ৩০-৪০ সেকেন্ড।
    একই সাথে ভিডিওর ফুটেজ খোঁজার জন্য ৫টি ইংরেজি কিওয়ার্ডস দাও।

    আউটপুটটি হুবহু নিচের ফরম্যাটে দাও, অন্য কোনো কথা লিখবে...
    TITLE: [শিরোনাম]
    KEYWORDS: [keyword1, keyword2, keyword3]
    SCRIPT: [বাংলা স্ক্রিপ্ট]
    """

    # স্মার্ট অটো-কানেক্ট লুপ
    for model_name in models_to_try:
        try:
            print(f"[🤖] {model_name} মডেলটি দিয়ে চেষ্টা করা হচ্ছে...")
            response = client.models.generate_content(
                model=model_name, 
                contents=prompt
            )
            
            # সফল হলে ডেটা পার্স করে রিটার্ন করবে
            if response.text:
                print(f"[✅] {model_name} দিয়ে সফলভাবে স্ক্রিপ্ট জেনারেট হয়েছে।")
                return parse_ai_output(response.text)
                
        except Exception as e:
            print(f"[⚠️] {model_name} মডেলে সমস্যা হয়েছে (কোটা বা লিমিট)। পরবর্তী মডেলে যাওয়া হচ্ছে...")
            continue # লুপের পরের মডেলে চলে যাবে

    # যদি সব মডেলই ব্যর্থ হয়, তবে কোড ক্র্যাশ না করে সেফটি নেট ব্যবহার করবে
    print("[🚨] গুগলের সবকটি ফ্রি মডেল সাময়িকভাবে ব্যস্ত। অটো-সেফটি স্ক্রিপ্ট সক্রিয় করা হলো।")
    return get_default_data()

def parse_ai_output(text):
    data = {"title": "আজকের ভাইরাল ইনফো", "keywords": ["technology", "future"], "script": ""}
    lines = text.split("\n")
    script_lines = []
    is_script = False

    for line in lines:
        if line.startswith("TITLE:"):
            data["title"] = line.replace("TITLE:", "").strip()
        elif line.startswith("KEYWORDS:"):
            kw_str = line.replace("KEYWORDS:", "").replace("[", "").replace("]", "").strip()
            data["keywords"] = [k.strip() for k in kw_str.split(",") if k.strip()]
        elif line.startswith("SCRIPT:"):
            is_script = True
            script_lines.append(line.replace("SCRIPT:", "").strip())
        elif is_script:
            script_lines.append(line.strip())

    data["script"] = " ".join(script_lines).strip()
    return data

def get_default_data():
    return {
        "title": "কৃত্রিম বুদ্ধিমত্তা ও ভবিষ্যৎ চাকরি",
        "keywords": ["artificial intelligence", "future of work", "technology"],
        "script": "২০২৬ সালে কৃত্রিম বুদ্ধিমত্তা বা এআই মানুষের কাজের ধরন সম্পূর্ণ বদলে দিচ্ছে। নিজেকে দক্ষ করে তোলাই এখন সময়ের দাবি।"
        }
    
