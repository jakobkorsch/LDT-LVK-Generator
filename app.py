import streamlit as st
from pathlib import Path
import tempfile

from lvk_generator import generate_lvk

st.set_page_config(
    page_title="LVK Generator",
    page_icon="💡",
    layout="centered"
)

st.title("💡 LDT → LVK Generator")
st.markdown(
    """
    Lade eine **LDT (EULUMDAT)**-Datei hoch und erstelle automatisch:

    - 📷 PNG
    - 📄 PDF
    """
)

uploaded_file = st.file_uploader(
    "LDT-Datei auswählen",
    type=["ldt"]
)

if uploaded_file:

    with tempfile.TemporaryDirectory() as tmp:

        tmp = Path(tmp)

        ldt_path = tmp / uploaded_file.name
        output_dir = tmp / "output"

        output_dir.mkdir(exist_ok=True)

        with open(ldt_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if st.button("🚀 LVK erstellen", use_container_width=True):

            with st.spinner("LVK wird erzeugt..."):

                png_path, pdf_path = generate_lvk(
                    ldt_path,
                    output_dir
                )

            st.success("LVK erfolgreich erstellt!")

            st.image(
                str(png_path),
                caption="LVK Vorschau",
                use_container_width=True
            )

            col1, col2 = st.columns(2)

            with col1:
                with open(png_path, "rb") as f:
                    st.download_button(
                        "📷 PNG herunterladen",
                        data=f,
                        file_name=png_path.name,
                        mime="image/png",
                        use_container_width=True
                    )

            with col2:
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "📄 PDF herunterladen",
                        data=f,
                        file_name=pdf_path.name,
                        mime="application/pdf",
                        use_container_width=True
                    )

st.markdown("---")
st.caption(
    "LVK Generator • Python • Streamlit • Matplotlib • EULUMDAT (LDT)"
)


