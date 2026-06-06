import os
import sys
import inspect
import shutil
from uuid import uuid4

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

def patch_config_toml():
    """
    ম্যাজিক ফাংশন ২: এটি রান-টাইমে config.toml ফাইলটি স্ক্যান করে 
    GitHub Secrets থেকে আসা PEXELS_API_KEY এবং অন্যান্য কীগুলো স্বয়ংক্রিয়ভাবে বসিয়ে দেয়।
    """
    config_path = os.path.join(root_dir, "config.toml")
    example_path = os.path.join(root_dir, "config.example.toml")
    
    # যদি config.toml না থাকে, উদাহরণ ফাইল থেকে কপি করবে
    if not os.path.exists(config_path) and os.path.exists(example_path):
        shutil.copy(example_path, config_path)
        print("[🔧] config.example.toml থেকে config.toml তৈরি করা হয়েছে।")
        
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        pexels_key = os.environ.get("PEXELS_API_KEY", "").strip()
        pixabay_key = os.environ.get("PIXABAY_API_KEY", "").strip()
        gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
        
        new_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("pexels_api_keys") and pexels_key:
                new_lines.append(f'pexels_api_keys = ["{pexels_key}"]\n')
            elif stripped.startswith("pixabay_api_keys") and pixabay_key:
                new_lines.append(f'pixabay_api_keys = ["{pixabay_key}"]\n')
            elif stripped.startswith("gemini_api_key") and gemini_key:
                new_lines.append(f'gemini_api_key = "{gemini_key}"\n')
            else:
                new_lines.append(line)
                
        with open(config_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print("[✅] config.toml ফাইলে এপিআই কী-সমূহ ডাইনামিকালি আপডেট করা হয়েছে।")

# আগে কনফিগারেশন প্যাচ করতে হবে, তারপর অ্যাপ ইমপোর্ট করতে হবে
patch_config_toml()

from automation.core_brain import generate_bengali_script

def dynamic_engine_caller(func, **kwargs):
    sig = inspect.signature(func)
    filtered_kwargs = {}
    
    aliases = {
        "video_subject": kwargs.get("title"),
        "video_script": kwargs.get("script"),
        "script": kwargs.get("script"),
        "video_terms": kwargs.get("keywords_str"),
        "search_keywords": kwargs.get("keywords_list"),
        "voice_name": "bn-BD-PradeepNeural",
        "video_aspect": "9:16",
        "bgm_name": "random"
    }

    for param_name in sig.parameters:
        if param_name in aliases and aliases[param_name] is not None:
            filtered_kwargs[param_name] = aliases[param_name]
        elif param_name == "task_id":
            filtered_kwargs[param_name] = kwargs.get("task_id")
        elif param_name == "params":
            try:
                from app.models.schema import VideoParams
                filtered_kwargs[param_name] = VideoParams(
                    video_subject=kwargs.get("title"),
                    video_script=kwargs.get("script"),
                    video_terms=kwargs.get("keywords_str"),
                    voice_name="bn-BD-PradeepNeural",
                    video_aspect="9:16"
                )
            except:
                pass

    return func(**filtered_kwargs)

def main():
    print("[🚀] কন্টেন্ট ফ্যাক্টরি সচল হচ্ছে...")
    
    topic = "কৃত্রিম বুদ্ধিমত্তা (AI) কীভাবে ২০২৬ সালে মানুষের চাকরি পাল্টাচ্ছে"
    ai_data = generate_bengali_script(topic)
    
    title = ai_data.get("title", "আজকের ভাইরাল ইনফো")
    keywords = ai_data.get("keywords", ["technology", "future"])
    script = ai_data.get("script", "")
    keywords_str = ",".join(keywords)
    
    print(f"\n[🎬] প্রস্তুতি সম্পন্ন: {title}")
    print("[⏳] ভিডিও রেন্ডারিং মডিউল স্ক্যান করা হচ্ছে...")

    target_function = None
    try:
        from app.services import task as task_service
        target_function = task_service.start
        print("[ℹ️] টার্গেট সনাক্তকরণ: task_service.start")
    except:
        try:
            from app.services import video as video_service
            target_function = video_service.generate_video
            print("[ℹ️] টার্গেট সনাক্তকরণ: video_service.generate_video")
        except Exception as e:
            print("[❌] মূল প্রজেক্টের কোনো রেন্ডারিং ফাংশন খুঁজে পাওয়া যায়নি।")
            return

    try:
        task_id = str(uuid4())
        dynamic_engine_caller(
            target_function,
            task_id=task_id,
            title=title,
            script=script,
            keywords_str=keywords_str,
            keywords_list=keywords
        )
        print("[✅] কন্টেন্ট ফ্যাক্টরি সফলভাবে রান সম্পন্ন করেছে!")
        
    except Exception as e:
        print(f"/n[❌] ডাইনামিক রেন্ডারিং এরর: {str(e)}")

if __name__ == "__main__":
    main()
    
