import numpy as np
import tensorflow as tf
from pathlib import Path
import streamlit as st
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

image_base64 = get_base64_image("src/static/background/bg.png")

background_css = f"""
<style>
body {{
    background-image: url('data:image/jpg;base64,{image_base64}');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    font-family: 'Poppins', sans-serif;
    color: #ffffff;
    margin: 0;
    padding: 0;
}}
header {{
    text-align: center;
    padding: 20px;
    background: linear-gradient(90deg, rgba(0, 128, 128, 0.8), rgba(0, 191, 255, 0.8));
    color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    margin-bottom: 30px;
}}
section {{
    margin: 30px auto;
    padding: 20px;
    background: rgba(0, 0, 0, 0.85);
    border-radius: 15px;
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.3);
    max-width: 900px;
}}
button {{
    background: linear-gradient(90deg, #1e90ff, #32cd32);
    color: white;
    padding: 12px 25px;
    margin: 15px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 18px;
    transition: 0.3s;
}}
button:hover {{
    background: linear-gradient(90deg, #32cd32, #1e90ff);
}}
.file-upload-container {{
    text-align: center;
    margin-top: 20px;
}}
.results-container {{
    text-align: left;
    background: rgba(50, 50, 50, 0.9);
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}}
</style>
"""
st.markdown(background_css, unsafe_allow_html=True)

# Judul aplikasi
st.markdown("""
<header>
    <h1>Klasifikasi Citra Sampah Organik & Anorganik</h1>
    <p>Dengan teknologi modern untuk mendukung pengelolaan sampah yang berkelanjutan</p>
</header>
<section>
    <p>Model ini dirancang untuk mengidentifikasi dan mengklasifikasikan jenis sampah berdasarkan gambar. 
       Dengan tujuan mendukung pengelolaan sampah yang lebih efisien, ramah lingkungan, dan mempermudah daur ulang.</p>
    <p>Manfaatkan teknologi ini untuk meningkatkan kesadaran dan efisiensi dalam proses pemilahan sampah secara otomatis.</p>
</section>
""", unsafe_allow_html=True)

# Fungsi prediksi
def predict(uploaded_image, model_path):
    # Daftar kelas
    class_names = [
        "battery",
        "biological",
        "cardboard",
        "clothes",
        "glass",
        "metal",
        "paper",
        "plastic",
        "shoes",
        "trash"
    ]

    # Muat dan preprocess citra
    img = tf.keras.utils.load_img(uploaded_image, target_size=(224, 224))  # Pastikan ukuran sesuai dengan model
    img = tf.keras.utils.img_to_array(img) / 255.0  # Normalisasi
    img = np.expand_dims(img, axis=0)  # Tambahkan dimensi batch

    # Muat model
    model = tf.keras.models.load_model(model_path)

    # Prediksi
    output = model.predict(img)
    score = tf.nn.softmax(output[0])  # Hitung probabilitas
    return class_names[np.argmax(score)], 100 * np.max(score)  # Prediksi label dan confidence

# Pilihan model
st.markdown("<section>", unsafe_allow_html=True)
model_option = st.selectbox("Pilih model untuk prediksi:", ("InceptionV3", "MobileNetV2"))

# Tentukan path model berdasarkan pilihan
if model_option == "InceptionV3":
    model_path = Path(__file__).parent / "Model/Model_InceptionV3/model.h5"
else:
    model_path = Path(__file__).parent / "Model/Model_MobileNetV2/model.h5"

# Komponen file uploader untuk banyak file
st.markdown("""
<div class="file-upload-container">
    <h3>Unggah Gambar Anda</h3>
</div>
""", unsafe_allow_html=True)
uploads = st.file_uploader("Unggah citra untuk mendapatkan hasil prediksi", type=["png", "jpg"], accept_multiple_files=True)

# Tombol prediksi
if st.button("Predict", type="primary"):
    if uploads:
        st.markdown("""
        <div class="results-container">
        <h3>Hasil Prediksi:</h3>
        """, unsafe_allow_html=True)

        for upload in uploads:
            # Tampilkan setiap citra yang diunggah
            st.image(upload, caption=f"Citra yang diunggah: {upload.name}", use_container_width=True)

            with st.spinner(f"Memproses citra {upload.name} untuk prediksi..."):
                # Panggil fungsi prediksi
                try:
                    label, confidence = predict(upload, model_path)
                    st.markdown(f"<strong>Image:</strong> {upload.name}<br>", unsafe_allow_html=True)
                    st.markdown(f"<strong>Label :</strong> *{label}*<br>", unsafe_allow_html=True)
                    st.markdown(f"<strong>Confidence:</strong> *{confidence:.5f}%*<br>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat memproses {upload.name}: {e}")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("Unggah setidaknya satu citra terlebih dahulu!")
st.markdown("</section>", unsafe_allow_html=True)
