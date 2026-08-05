import streamlit as st
from groq import Groq
import base64
import re

# Set to "wide" mode so it looks like a real software dashboard
st.set_page_config(page_title="AI Creator Studio", layout="wide")

st.title("🎬 AI Creator Studio")
st.write("Your all-in-one suite for viral content creation.")

api_key = st.text_input("Enter your Groq API Key to unlock:", type="password")

# This creates three interactive tabs!
tab1, tab2, tab3 = st.tabs(["📸 Vision Captioner", "💡 Idea Brainstormer", "📋 Reel Storyboard"])


# --- TAB 1: Image Upload ---
with tab1:
    st.write("### Customize Your Caption")
    
    # The Dropdowns
    col1, col2 = st.columns(2)
    with col1:
        language = st.selectbox("Language:", ["Hinglish", "English", "Hindi", "Punjabi", "Gen-Z Slang"])
    with col2:
        tone = st.selectbox("Vibe:", ["Storytelling & Emotional", "Viral & Punchy", "Funny & Sarcastic", "Aesthetic & Poetic"])

    # --- NEW FEATURE: The Creator's Context Box ---
    st.write("### Add Your Own Spark (Optional)")
    user_context = st.text_area(
        "Tell the AI what to focus on:", 
        placeholder="e.g., Make sure to mention the jhumkas my bestie gave me, or focus on the storytelling aspect of this memory..."
    )

    st.write("### Upload a photo")
    uploaded_photo = st.file_uploader("Upload an image (JPG/PNG)", type=["jpg", "jpeg", "png"])
    
    if uploaded_photo is not None:
        st.image(uploaded_photo, caption="Image ready for AI analysis", width=400)
        
        if st.button("Generate Custom Caption"):
            if not api_key:
                st.error("Please enter your API Key first.")
            else:
                with st.spinner(f"Writing a {tone} caption in {language}..."):
                    try:
                        base64_image = base64.b64encode(uploaded_photo.getvalue()).decode('utf-8')
                        client = Groq(api_key=api_key)
                        
                    # --- SUPERCHARGED PROMPT ENGINEERING ---
                        dynamic_prompt = f"""You are a top-tier viral social media manager. The creator needs a massive batch of highly engaging content for this image in {language}, focusing on a {tone} vibe. 
                        
                        Creator's specific instructions: {user_context}
                        
                        STRICT RULES - YOU MUST OBEY:
                        1. Generate EXACTLY 20 different Instagram captions. Number them 1 to 20. 
                        2. DO NOT STOP EARLY. You must reach number 20.
                        3. STOP BEING GENERIC. Make them high-quality, relatable, and scroll-stopping. Mix up the lengths (some short hooks, some deep storytelling).
                        4. EVERY single caption MUST include emojis and 4-5 high-reach, trending hashtags.
                        5. After the 20th caption, generate EXACTLY 2 interactive Instagram Story concepts based on the image.
                        """
                        
                        completion = client.chat.completions.create(
                            model="qwen/qwen3.6-27b",
                            messages=[
                                {
                                    "role": "user",
                                    "content": [
                                        {"type": "text", "text": dynamic_prompt},
                                        {
                                            "type": "image_url",
                                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                                        },
                                    ],
                                }
                            ],
                            temperature=0.8,  # Bumped up slightly for more creativity!
                            max_tokens=3000,  # Forces the AI to keep writing until it finishes
                        )
                        
                        # --- THE REGEX PARSER FIX ---
                        raw_text = completion.choices[0].message.content
                        
                        # This finds <think>...</think> and replaces it with nothing ('')
                        clean_text = re.sub(r'<think>.*?</think>', '', raw_text, flags=re.DOTALL).strip()
                        
                        st.success("Custom Caption Generated!")
                        # We display the clean text instead of the raw text
                        st.write(clean_text)
                        
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
# --- TAB 2: Idea Generator ---
with tab2:
    st.write("### Brainstorm Viral Concepts")
    
    # --- NEW FEATURE: Idea Dropdowns ---
    col1, col2 = st.columns(2)
    with col1:
        idea_language = st.selectbox("Idea Language:", ["Hinglish", "English", "Hindi", "Punjabi", "Gen-Z Slang"])
    with col2:
        idea_tone = st.selectbox("Content Vibe:", ["Storytelling & Emotional", "Funny & Sarcastic", "Aesthetic & Poetic", "Educational & Value", "High-Energy & Fast-Paced"])

    niche = st.text_input("What is your niche? (e.g., Fashion storytelling, CS Engineering Student life)")
    
    if st.button("Generate Ideas"):
        if not api_key:
            st.error("Please enter your API Key first.")
        elif not niche:
            st.warning("Please tell me your niche to generate ideas!")
        else:
            with st.spinner(f"Brainstorming {idea_tone} ideas in {idea_language}..."):
                try:
                    client = Groq(api_key=api_key)
                    
                    # --- SUPERCHARGED IDEA PROMPT ---
                    prompt = f"""You are an elite, highly creative social media strategist. The creator's niche is: {niche}.
                    Generate 3 highly engaging, viral Reel/Short video concepts focusing on a {idea_tone} vibe in {idea_language}. 
                    
                    STRICT RULES - YOU MUST OBEY:
                    1. Make the formatting visually appealing. Use bold text, bullet points, and heavy emojis (🎨🔥✨) throughout!
                    2. DO NOT be boring or generic. Use catchy, viral hooks.
                    3. For EACH concept, you MUST provide a full, word-for-word voiceover (VO) script that would take 1 to 2 minutes to speak out loud. 
                    
                    Format EXACTLY like this for each concept:
                    ### 🎬 Concept [Number]: [Extremely Catchy Title]
                    * **🔥 The Hook (0-3s)**: Exactly what happens visually and audibly to stop the scroll.
                    * **🎥 Visual Action**: A detailed breakdown of the camera angles, B-roll, and actions to film.
                    * **🎵 Audio Vibe**: Trending sound or music style to use in the background.
                    * **🗣️ Full 1-2 Min Script**: [Provide the exact, long, highly engaging word-for-word script here].
                    ---
                    """
                    
                    completion = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": "You are a creative social media expert."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.8,
                        max_tokens=3000, # Increased memory so it can write the long scripts!
                    )
                    
                    st.success("Viral Concepts Generated!")
                    st.write(completion.choices[0].message.content)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

# --- TAB 3: Storyboarder ---
with tab3:
    st.write("### 🎬 Ultimate Reel Storyboard Generator")
    st.write("Plan your video second-by-second before you even press record.")
    
    # --- ROW 1: Language & Vibe ---
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        story_language = st.selectbox("Storyboard Language:", ["Hinglish", "English", "Hindi", "Punjabi", "Gen-Z Slang"])
    with row1_col2:
        story_tone = st.selectbox("Overall Vibe:", ["Storytelling & Emotional", "Funny & Sarcastic", "Aesthetic & Poetic", "Educational & Value", "High-Energy & Fast-Paced"])

    # --- ROW 2: Director's Logistics ---
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    with row2_col1:
        video_length = st.selectbox("Target Length:", ["Under 15 seconds (Viral hook)", "15-30 seconds (Standard)", "30-60 seconds (Deep dive)"])
    with row2_col2:
        editing_style = st.selectbox("Editing Style:", ["Fast-paced & Trendy (CapCut style)", "Slow & Cinematic (Aesthetic)", "Vlog / Follow Me", "Direct to Camera (Storytelling)"])
    with row2_col3:
        platform = st.selectbox("Primary Platform:", ["Instagram Reels", "YouTube Shorts", "TikTok"])

    st.write("### What is your concept?")
    concept = st.text_area(
        "Describe the video you want to film:", 
        placeholder="e.g., A transition video showcasing a new jhumka given by my bestie, blending CS college life with traditional vibes..."
    )
    
    if st.button("Generate Master Storyboard"):
        if not api_key:
            st.error("Please enter your API Key first.")
        elif not concept:
            st.warning("Please tell me your concept!")
        else:
            with st.spinner(f"Directing your {story_tone} masterpiece in {story_language}..."):
                try:
                    client = Groq(api_key=api_key)
                    
                    # --- THE DIRECTOR'S PROMPT ---
                    prompt = f"""You are a master video director and viral content editor. 
                    Create a highly detailed, scene-by-scene storyboard for a {platform} video. 
                    
                    Creator's Concept: {concept}
                    Language for Text/Speech: {story_language}
                    Overall Vibe: {story_tone}
                    Target Length: {video_length}
                    Editing Style: {editing_style}
                    
                    STRICT RULES - YOU MUST OBEY:
                    1. Break the video down second-by-second (or scene-by-scene).
                    2. For EACH scene, you MUST include these exact bullet points:
                       - ⏱️ **Timestamp** (e.g., 0:00 - 0:03)
                       - 🎥 **Camera Angle & Movement** (e.g., Close-up, pan left, phone on tripod)
                       - 🎬 **Visual Action** (Exactly what the creator is doing on screen)
                       - 🔠 **On-Screen Text / Voiceover** (Provide exact text or script in {story_language} matching the {story_tone} vibe!)
                       - 🎵 **Audio / SFX** (e.g., 'Whoosh transition', 'Bass drop', or background track vibe)
                    3. Add a section at the very end called "💡 Pro-Filming Tips" with quick advice on lighting and angles for this specific video.
                    4. Format beautifully using Markdown, bold text, and emojis.
                    """
                    
                    completion = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": "You are a professional video director and editor."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=3000,
                    )
                    
                    st.success("Storyboard Complete! Ready for production. 🎬")
                    st.write(completion.choices[0].message.content)
                except Exception as e:
                    st.error(f"An error occurred: {e}")