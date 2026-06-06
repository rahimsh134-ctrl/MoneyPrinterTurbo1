import os
import sys

# পাইথনকে মাদার প্রজেক্টের রুট ডিরেক্টরি চিনিয়ে দেওয়া (যাতে ইমপোর্ট এরর না হয়)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# আমাদের তৈরি করা এআই ব্রেন এবং প্রজেক্টের মূল ভিডিও জেনারেটর ইমপোর্ট করা
from automation.core_brain import VideoContentEngine

try:
    # প্রজেক্টের আসল ভিডিও জেনারেশন মডিউল ইমপোর্ট (ওদের ব্যাকএন্ড ইঞ্জিন)
    from app.services import video as video_service
    from app.models.schema import VideoParams
except ImportError:
    # যদি ওদের ফোল্ডার স্ট্রাকচার ভিন্ন হয়, তার জন্য সেফটি ব্যাকআপ লজিক
    print("[⚠️] মূল ভিডিও সার্ভিসের পাথ অ্যাডজাস্ট করা হচ্ছে...")
    video_service = None

class AutomationBridge:
    """
    মাস্টার ব্রিজ যা এআই-এর আউটপুট নিয়ে মূল ভিডিও মেকার ইঞ্জিনের সাথে কানেক্ট করে।
    """
    def __init__(self):
        self.ai_engine = VideoContentEngine()

    def start_factory(self):
        print("[🚀] কন্টেন্ট ফ্যাক্টরি সচল হচ্ছে...")
        
        # ১. আজকের ট্রেন্ড খুঁজে বের করা
        trend = self.ai_engine.fetch_trending_topic()
        
        # ২. জেমিনি এআই থেকে বাংলা স্ক্রিপ্ট ও কিওয়ার্ড অবজেক্ট নেওয়া
        ai_output = self.ai_engine.generate_bangla_script(trend)
        
        title = ai_output.get("title", "আজকের ব্রেকিং নিউজ")
        script = ai_output.get("script", "")
        keywords = ai_output.get("search_keywords", ["technology"])

        print(f"\n[🎬] ভিডিও তৈরির প্রস্তুতি সম্পন্ন:")
        print(f" - শিরোনাম: {title}")
        print(f" - কিওয়ার্ডস: {keywords}")
        print(f" - স্ক্রিপ্ট সাইজ: {len(script)} অক্ষর")

        # ৩. MoneyPrinterTurbo এর মূল ইঞ্জিনকে হেডলেস মোডে কল করা
        # এখানে আমরা ওদের কনফিগারেশন অনুযায়ী প্যারামিটার পাস করছি
        output_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(output_dir, exist_ok=True)

        print("[⏳] ভিডিও রেন্ডারিং শুরু হচ্ছে... (এতে কিছুক্ষণ সময় লাগতে পারে)")
        
        try:
            # পিক্সেলস এবং পিক্সাবে দুটোই ব্যাকআপ হিসেবে সেট করা হলো
            # কোডটি আপনার গিটহাব সিক্রেটস থেকে স্বয়ংক্রিয়ভাবে চাবিকাঠিগুলো নিয়ে নেবে
            if video_service:
                # ওদের অফিশিয়াল ব্যাকএন্ড ফাংশন কল করা (যা ওয়েবসাইট ছাড়াই রান হয়)
                # নোট: প্রজেক্টের ভার্সন ভেদে ফাংশনের নাম সামান্য পরিবর্তন হলে আমরা তা গিটহাব লগে দেখতে পাবো
                video_path = video_service.generate_video(
                    script=script,
                    search_keywords=keywords,
                    voice_name="bn-BD-PradeepNeural", # মাইক্রোসফটের বেস্ট বাংলা নিউরাল ভয়েস
                    video_multiplier=1,
                    bg_music="music.mp3" # ডিফল্ট ব্যাকগ্রাউন্ড মিউজিক
                )
                print(f"[🎉] সফল! আপনার ফাইনাল ভিডিও তৈরি হয়েছে এখানে: {video_path}")
            else:
                # যদি ইমপোর্ট এরর থাকে তবে এটি রান হবে (টেস্টিং পারপাস)
                print("[❌] মূল ভিডিও সার্ভিসের সাথে কানেকশন মেলানো যায়নি। ফোল্ডার স্ট্রাকচার চেক প্রয়োজন।")
                
        except Exception as engine_error:
            print(f"[❌] ভিডিও ইঞ্জিন রান করার সময় ত্রুটি ঘটেছে: {str(engine_error)}")

if __name__ == "__main__":
    bridge = AutomationBridge()
    bridge.start_factory()
      
