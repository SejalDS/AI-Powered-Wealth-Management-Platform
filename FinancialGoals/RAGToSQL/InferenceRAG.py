from Helper.VannaObject import MyVanna
from Helper.Credentials import Credentials
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

vn = MyVanna(config={'api_key': Credentials.open_ai_key, 'model': Credentials.model})

print("Generating SQL for: 'Tell me the top client with highest portfolio value'")
print("=" * 50)
print(vn.generate_sql("Tell me the top client with highest portfolio value."))