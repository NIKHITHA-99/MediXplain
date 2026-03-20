from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FakeEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

MEDICAL_KNOWLEDGE = """
HEMOGLOBIN:
Normal range for men: 13.5-17.5 g/dL
Normal range for women: 12.0-15.5 g/dL
Low hemoglobin means anemia - causes fatigue, weakness, pale skin
High hemoglobin may indicate dehydration or lung disease

BLOOD SUGAR (GLUCOSE):
Fasting normal: 70-100 mg/dL
Pre-diabetes: 100-125 mg/dL
Diabetes: above 126 mg/dL
Low blood sugar: below 70 mg/dL

CHOLESTEROL:
Total cholesterol normal: below 200 mg/dL
Borderline high: 200-239 mg/dL
High: above 240 mg/dL
LDL normal: below 100 mg/dL
HDL normal: above 40 mg/dL

WHITE BLOOD CELLS (WBC):
Normal range: 4.5-11.0 K/uL
Low WBC means weak immune system
High WBC means infection or inflammation

PLATELETS:
Normal range: 150-400 K/uL
Low platelets causes bleeding problems
High platelets increases clotting risk

CREATININE:
Normal for men: 0.7-1.3 mg/dL
Normal for women: 0.6-1.1 mg/dL
High creatinine indicates kidney problems

THYROID (TSH):
Normal range: 0.4-4.0 mIU/L
Low TSH means overactive thyroid
High TSH means underactive thyroid

VITAMIN D:
Deficient: below 20 ng/mL
Normal: 30-100 ng/mL
Low vitamin D causes bone weakness

VITAMIN B12:
Normal range: 200-900 pg/mL
Low B12 causes nerve damage and anemia

URIC ACID:
Normal for men: 3.4-7.0 mg/dL
Normal for women: 2.4-6.0 mg/dL
High uric acid causes gout

BILIRUBIN:
Total normal: 0.1-1.2 mg/dL
High bilirubin causes jaundice

SGPT/ALT:
Normal: 7-56 units/L
High SGPT indicates liver damage

SGOT/AST:
Normal: 10-40 units/L
High SGOT indicates liver or heart problems
"""

def create_rag_chain():
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.create_documents([MEDICAL_KNOWLEDGE])

    embeddings = FakeEmbeddings(size=384)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = ChatGroq(
        model="llama3-8b-8192",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3
    )

    prompt = PromptTemplate(
        template="""You are a friendly medical assistant explaining medical reports to normal people.
Use the medical knowledge below to explain the report accurately.

Medical Knowledge:
{context}

Medical Report:
{question}

Instructions:
1. Explain each test value in very simple English
2. Say NORMAL, HIGH or LOW for each value with emojis
3. Explain what HIGH or LOW means for their health
4. Suggest 3-5 questions to ask the doctor
5. Be friendly and reassuring

Explanation:""",
        input_variables=["context", "question"]
    )

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain
