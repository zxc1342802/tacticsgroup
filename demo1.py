import os
from langchain_community.llms import OpenAI
os.environ["OPENAI_API_KEY"] = "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"
llm = OpenAI(temperature=0.9)
text = "如果我有10万本金，按照复利投入，如果每个月涨幅10% ，那么本金到1个亿需要多久?"
print(llm(text))