from langchain_aws import ChatBedrock
from dotenv import load_dotenv
load_dotenv()

model = ChatBedrock(
    model_id="amazon.nova-lite-v1:0",
    region_name="us-east-1"   # REQUIRED
)

response = model.invoke("Who is arun")
print(response.content)