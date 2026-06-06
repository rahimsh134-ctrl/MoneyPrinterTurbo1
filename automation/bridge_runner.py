import os
import sys
import inspect
from uuid import uuid4

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from automation.core_brain import generate_bengali_script

def dynamic_engine_caller(func, **kwargs):
    """
    ম্যাজিক ফাংশন: এটি টার্গেট ফাংশনের সিগনেচার লাইভ চেক করে 
    শুধু গ্রহণযোগ্য আর্গুমেন্টগুলোই পাস করবে। ফলে এরর আসার সুযোগ নেই।
    """
    sig = inspect.signature(func)
    filtered_kwargs = {}
    
    # ম্যাপিং ডিকশনারি: ওদের প্রজেক্টের ভিন্ন ভিন্ন ভার্সনে যে নামগুলো থাকতে পারে
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
            # যদি ফাংশনটি সরাসরি অবজেক্ট খোঁজে
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

    # একের অধিক সম্ভাব্য সোর্স ফাংশন চেক করা (ভার্সন সেফটি)
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
        # ডাইনামিক ফিল্টারিং কল
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
        print(f"[❌] ডাইনামিক রেন্ডারিং এরর: {str(e)}")

if __name__ == "__main__":
    main()
            
