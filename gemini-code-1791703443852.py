import streamlit as st
from script_generator import generate_comic_script
from image_generator import create_comic_panel_image
from pdf_exporter import export_comic_to_pdf

st.set_page_config(page_title="ComicCraft: AI Comic Creator", page_icon="🎨", layout="centered")

st.title("🎨 ComicCraft - AI Comic Story Creator")
st.markdown("Transform any simple idea or text prompt into a multi-panel structured comic book using Google Gemini models.")

user_prompt = st.text_area("Enter your comic story concept:", placeholder="e.g., A stray cat discovers it has superhero flying powers and saves a falling ice cream cone.")

if st.button("Generate Comic Story", type="primary"):
    if not user_prompt.strip():
        st.warning("Please enter a valid story description first.")
    else:
        with st.spinner("🤖 Gemini is writing your script and choreographing panels..."):
            try:
                script_data = generate_comic_script(user_prompt)
                st.success(f"Comic Script Generated: **{script_data.get('title')}**")
            except Exception as e:
                st.error(f"Error generating script: {e}")
                st.stop()

        panel_images = []
        progress_bar = st.progress(0)
        total_panels = len(script_data["panels"])

        for index, panel in enumerate(script_data["panels"]):
            with st.spinner(f"Rendering Panel {panel['panel_number']}..."):
                img = create_comic_panel_image(
                    visual_prompt=panel["visual_description"],
                    caption=panel["caption"],
                    dialogue=panel["dialogue"],
                    panel_num=panel["panel_number"]
                )
                panel_images.append(img)
                progress_bar.progress((index + 1) / total_panels)

        st.subheader("📖 Preview Your Generated Comic Panels")
        cols = st.columns(2)
        for i, img in enumerate(panel_images):
            with cols[i % 2]:
                st.image(img, caption=f"Panel {i+1}", use_container_width=True)

        # PDF Compilation
        pdf_path = export_comic_to_pdf(panel_images, output_filename="comiccraft_output.pdf")
        
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📥 Download Final Comic as PDF",
                data=pdf_file,
                file_name="comiccraft_story.pdf",
                mime="application/pdf"
            )