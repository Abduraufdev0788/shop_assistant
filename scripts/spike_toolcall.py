import sys
import time
from pathlib import Path
import os

# Add root directory to sys.path to allow importing shop_assistant
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from anthropic import Anthropic
from shop_assistant import config

CAPTION_DVOYKA = (
    "🍂Kuz mavsumi uchun🍂\n🔥Yangi model Dvoyka🔥\nRazmer:M.L.XL.2XL.3XL\nNarx:980.000ming"
    "\n\n📍Manzil: Samarqand, Siyob bozori\n📞 +998 90 123 45 67\n@status_dokon\n🚚 Dastavka bor"
)

def main():
    ollama_url = getattr(config, "OLLAMA_URL", "http://192.168.0.218:11434")
    model_name = getattr(config, "MODEL", "gemma4:31b")
    
    client = Anthropic(
        base_url=ollama_url,
        api_key="ollama",
        
    )
    
    tools = [
        {
            "name": "record_product",
            "description": "Record product details from a caption",
            "input_schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "price": {"type": "integer"},
                    "sizes": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["name", "price", "sizes"]
            }
        }
    ]
    
    for i in range(3):
        print(f"\n--- Run {i+1} ---")
        start_time = time.time()
        
        try:
            response = client.messages.create(
                model=model_name,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": CAPTION_DVOYKA}
                ],
                tools=tools,
                tool_choice={"type": "tool", "name": "record_product"}
            )
            
            wall_time = time.time() - start_time
            
            tool_use = next((block for block in response.content if block.type == "tool_use"), None)
            
            if tool_use:
                print("Tool Input:")
                print(tool_use.input)
            else:
                print("No tool_use block returned!")
                print("Raw response:", response.content)
                
            print(f"Wall time: {wall_time:.3f} seconds")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
