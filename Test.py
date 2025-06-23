"""import f5_tts
import os

print("✅ f5_tts imported successfully")

# Print the package path
print("📁 f5_tts path:", f5_tts.__path__)

# Explore all sub-files/folders in the package
print("\n🔍 Listing files inside f5_tts package:\n")
for path in f5_tts.__path__:
    for root, dirs, files in os.walk(path):
        for file in files:
            print(os.path.join(root, file))



print("🔍 Trying to import infer_cli from f5_tts...")

try:
    from f5_tts.infer import infer_cli
    print("✅ Successfully imported infer_cli from f5_tts.infer")
except ImportError as e:
    print("❌ Failed to import infer_cli:")
    print(e)"""




import importlib.util

spec = importlib.util.find_spec("f5_tts.infer.infer_cli")
if spec is not None:
    print("✅ infer_cli module is available inside f5_tts.infer")
else:
    print("❌ infer_cli module not found")
