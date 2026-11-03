from openai import OpenAI
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

# or 
# client = ai.client()     import aisute as ai first

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_BASE_URL')
)

def generate_draft(topic:str, tone:str, model_name:str) -> str: 
  
  instruction = f"""
   write a well adjusted content for a persian LinkedIn post, with 300 characters at max, consisting only 3 to 5 of the most trended hashtags related to the asked topic.
     And at last, write it based on the asked topic and tone:
    Topic: {topic}
     Tone: {tone}
  """
  response = client.chat.completions.create(
      model=model_name,
      messages=[
          {"role":"user","content":instruction},
          ]
  )
  
  return response.choices[0].message.content


def reflect_on_draft(draft:str, model_name:str) -> str:
  instruction = f"""
   reflect critically on the following draft Linkedin post. 
   Identify areas for improvement in structure, clarity, the attractiveness, or style.

   draft:
   {draft}

  """
  response = client.chat.completions.create(
      model=model_name,
      messages=[
          {"role":"user","content":instruction}
          ]
  )
  
  return response.choices[0].message.content

def revise_draft(original_draft:str, reflection:str, model_name:str) ->str:
  instruction= f"""
  Revise the following Linkedin Post draft using the feedback provided.
  Make improvements in clarity, coherence, augmentation and flow.
  Original draft:
  {original_draft}
   
  feedback:
  {reflection}
  """

  response = client.chat.completions.create(
      model=model_name,
      messages=[
          {"role":"user","content":instruction}
      ],
      temperature=1.0
  )

  return response.choices[0].message.content

def run_linkedin_work(topic:str, tone:str, model_name:str) -> str:
   
   draft = generate_draft(topic, tone, model_name)
   feedback = reflect_on_draft(draft, model_name)
   revised_post = revise_draft(draft, feedback, model_name)

   return revised_post, feedback, draft

st.set_page_config(page_title="خوداصلاحی هوش مصنوعی", layout="centered")
st.title("سیستم خودکار تولید و اصلاح پست لینکدین")
st.write("این برنامه بر اساس موضوع مشخص شده با لحنی حرفه‌ای محتوای لینکدین شما را تولید می‌کند")

st.info(
       "**موضوع:** معرفی دوره شبکه عصبی جدید \n\n **لحن انتخابی:** حرفه‌ای"
)

if st.button("اجرای فرآیند تولید و ارزیابی"):
  with st.spinner(
    "Generating draft, receiving feedback and final optimization..."
  ):
    final_post, reflect, first_draft = run_linkedin_work(topic="معرفی دوره آموزشی شبکه عصبی جدید", tone="حرفه‌ای", model_name="gpt-4o-mini")
    st.success("Operation done successfully.")

    tab1, tab2, tab3 = st.tabs(
      ["پست نهایی", "پیش‌نویس اولیه", "Model Feedback"]
    )

    with tab1:
       st.markdown("پیش‌نویس اولیه:")
       st.markdown(first_draft)
    with tab2:
      st.markdown("نقد و بررسی مدل:")
      st.markdown(reflect)

    with tab3:
          st.markdown("پست نهایی:")
          st.markdown(final_post)