import streamlit as st
from PIL import Image
from langchain_community.llms import Ollama
import io
import base64

st.set_page_config(page_title="AI Image + Chat Assistant", layout="centered")
st.title("📸 AI Image + Chat Assistant")
st.write("Analyze images and chat with a local multimodal vision intelligence system.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader("Upload an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=400)
    
    st.subheader("💬 Chat Log")
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"**👤 You:** {chat['content']}")
        else:
            st.markdown(f"**🤖 Assistant:** {chat['content']}")
            st.markdown("---")

    with st.form(key="chat_form", clear_on_submit=True):
        user_prompt = st.text_input("Ask a question about this image:")
        submit_button = st.form_submit_button(label="Send Message")
        
    if submit_button and user_prompt:
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})
        with st.spinner("Thinking locally..."):
            try:
                # Convert image format to RGB automatically to handle screenshots cleanly
                image_rgb = image.convert("RGB")
                buffered = io.BytesIO()
                image_rgb.save(buffered, format="JPEG")
                img_bytes = buffered.getvalue()
                img_b64 = base64.b64encode(img_bytes).decode('utf-8')
                
                llm = Ollama(model="llava")
                response = llm.bind(images=[img_b64]).invoke(user_prompt)
                
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
else:
    st.session_state.chat_history = []
    st.info("👈 Please upload an image file to begin.")
