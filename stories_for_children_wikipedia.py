import streamlit as st
import openai
from langchain.utilities import WikipediaAPIWrapper

# Enter your OpenAI API key here
openai.api_key = ""

# Streamlit app page title
st.title('📚💫 Stories for children using Wikipedia knowledge (and AI).')

# Streamlit input field for chat
query = st.chat_input('Write a story about...')

# Langchain Wikipedia content retriever (here we keep only the first result)
wiki = WikipediaAPIWrapper(top_k_results=1)

# When user query, perform the search and write the story with GPT
if query:
    # Wikipedia search (with a temporary message during the search)
    with st.spinner("⏳ Writing the story ..."):
        wiki_research = wiki.run(query)

    # Choose the GPT model (here gpt-3.5-turbo)
    GPT_MODEL = "gpt-3.5-turbo"

    # Write the query before writing the story
    st.markdown(f"### {query}")

    # Prompt and call of the model
    prompt_template = f"""
    Write a short story for children about {query}. Maximum 300 words.
    Using this Wikipedia content: {wiki_research}
    """
    completion = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "You're a children story teller."},
                {"role": "user", "content": f"{prompt_template}"},
            ],
            temperature=0.5,
            stream = True
        )

    # Display the story as a stream (character by character)
    res_box = st.empty()
    report = []
    for line in completion:
        token = ""
        response_obj = dict(line.choices[0].delta)
        if "content" in response_obj:
            token = response_obj["content"]
            report.append(token)
            result = "".join(report).strip()
            res_box.write(result)

    # Show the original Wikipedia content (in a Streamlit expander)
    with st.expander('Original Wikipedia content'):
        st.info(wiki_research)
