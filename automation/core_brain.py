import os
import json
from google import genai
from google.genai import types

class VideoContentEngine:
    """
    ওয়ার্ল্ড-ক্লাস এআই ইঞ্জিন যা ট্রেন্ড অ্যানালাইসিস করে সোশাল মিডিয়ার জন্য 
    নিখুঁত বাংলা স্ক্রিপ্ট এবং ভিডিও কিওয়ার্ড তৈরি করে।
    """
    def __init__(self):
        # গিটহাব সিক্রেটস থেকে জেমিনি এপিআই কি নেওয়া হচ্ছে
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Error: GEMINI_API_KEY খুঁজে পাওয়া যায়নি! গিটহাব সিক্রেটস চেক করুন।")
        
        # ২০২৬ সালের লেটেস্ট জেমিনি ক্লায়েন্ট ইনিশিয়েট করা
        self.client = genai.Client(api_key=self.api_key)

    def fetch_trending_topic(self) -> str:
        """
        ইন্টারনেটের ব্রেকিং বা ভাইরাল টপিক সিলেক্ট করার মেকানিজম।
        (প্রাথমিকভাবে এটি গিটহাব অ্যাকশনের মাধ্যমে ডাইনামিক টপিক ফিড করবে)
        """
        try:
            # এখানে আমরা পরবর্তীতে আরএসএস ফিড বা গুগল ট্রেন্ডস যুক্ত করব
            # আপাতত টেস্ট করার জন্য একটি গ্লোবাল ট্রেন্ডিং টপিক ডিফল্ট রাখা হলো
            return "কৃত্রিম বুদ্ধিমত্তা (AI) কীভাবে ২০২৬ সালে মানুষের চাকরি পাল্টাচ্ছে"
        except Exception as e:
            print(self._log_error("Trend Fetching", e))
            return "প্রযুক্তির নতুন বিস্ময়"

    def generate_bangla_script(self, topic: str) -> dict:
        """
        জেমিনি ২.০ ফ্ল্যাশ ব্যবহার করে স্ট্রাকচার্ড বাংলা স্ক্রিপ্ট এবং কিওয়ার্ড জেনারেট করা।
        """
        prompt = f"""
        You are an expert viral content creator for YouTube Shorts, Facebook Reels, and TikTok.
        Analyze this topic: '{topic}' and generate a highly engaging structured response.
        
        Requirements:
        1. Script must be in natural, emotional, and catchy Bangla.
        2. Duration must be strictly under 50 seconds when spoken (approx. 100-120 words).
        3. Provide 3-4 specific English keywords for video clip searching (e.g., 'robot working', 'future city').
        
        You MUST respond ONLY in the following JSON format:
        {{
            "title": "A catchy viral Bangla title",
            "script": "The full voiceover script in Bangla without any brackets or scene descriptions",
            "search_keywords": ["keyword1", "keyword2", "keyword3"]
        }}
        """
        
        try:
            print(f"[🤖] জেমিনি এআই ব্রেন সচল হচ্ছে... টপিক: {topic}")
            
            # স্ট্রাকচার্ড জেসন ডেটা পাওয়ার জন্য লেটেস্ট কনফিগারেশন
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                ),
            )
            
            # এআই-এর দেওয়া জেসন ডেটা পার্স করা
            content_data = json.loads(response.text)
            print("[✅] সফলভাবে ইউনিক বাংলা স্ক্রিপ্ট এবং কিওয়ার্ড তৈরি হয়েছে।")
            return content_data

        except Exception as e:
            print(self._log_error("Gemini Script Generation", e))
            return {
                "title": "আজকের ভাইরাল ইনফো",
                "script": "বন্ধুরা, প্রযুক্তির দুনিয়ায় প্রতিদিন ঘটে চলেছে অদ্ভুত সব পরিবর্তন। যা আমাদের জীবনকে বদলে দিচ্ছে।",
                "search_keywords": ["technology", "future"]
            }

    def _log_error(self, phase: str, error: Exception) -> str:
        return f"[❌] এরর ঘটেছে {phase} ধাপে! বিস্তারিত: {str(error)}"

# গিটহাব অ্যাকশন বা রানার ফাইল দিয়ে টেস্ট করার মেইন মেথড
if __name__ == "__main__":
    try:
        engine = VideoContentEngine()
        current_trend = engine.fetch_trending_topic()
        final_output = engine.generate_bangla_script(current_trend)
        
        # ফলাফল প্রিন্ট করে দেখা (গিটহাব রানারে লগ দেখার জন্য)
        print("\n--- 📄 জেনারেটেড কন্টেন্ট ডেটা ---")
        print(json.dumps(final_output, indent=4, ensure_ascii=False))
        
    except Exception as main_error:
        print(f"[🚨] রানার ক্র্যাশ করেছে: {str(main_error)}")
  
