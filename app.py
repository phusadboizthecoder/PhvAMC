import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tensorflow as tf
import librosa
import pandas as pd
import io
import os
from utils.media_detector import MediaDetector
from utils.vietnamese_labels import VietnameseLabels

# Khởi tạo detector và labels
@st.cache_resource
def load_detector():
    return MediaDetector()

@st.cache_resource
def load_labels():
    return VietnameseLabels()

def main():
    st.set_page_config(
        page_title="Phát hiện Media bằng AI",
        page_icon="🎯",
        layout="wide"
    )
    
    detector = load_detector()
    labels = load_labels()
    
    # Header với links
    col_title, col_links = st.columns([3, 1])
    
    with col_title:
        st.title("AI Media Checker \"PhvAMC\"")
        st.markdown("Tiện ích kiểm tra nội dung AI chân thật vl do PhvsadboizDEV")
    
    with col_links:
        st.markdown("**Liên kết:**")
        st.markdown("[📺 Phv YouTube](https://www.youtube.com/@Phvsadboiz)")
        st.markdown("[📘 Phv Facebook](https://www.facebook.com/phu.phamthiem/)")
    
    # Sidebar cho các tùy chọn
    st.sidebar.header("Tùy chọn")
    media_type = st.sidebar.selectbox(
        "Chọn loại media:",
        ["Hình ảnh", "Video", "Âm thanh"]
    )
    
    confidence_threshold = st.sidebar.slider(
        "Ngưỡng độ tin cậy:",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.05,
        help="Giảm ngưỡng để xem nhiều kết quả hơn"
    )
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📁 Tải lên Media")
        
        if media_type == "Hình ảnh":
            uploaded_file = st.file_uploader(
                "Chọn file hình ảnh:",
                type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
                help="Các định dạng được hỗ trợ: JPG, JPEG, PNG, BMP, TIFF"
            )
        elif media_type == "Video":
            uploaded_file = st.file_uploader(
                "Chọn file video (tối đa 300MB):",
                type=['mp4', 'avi'],
                help="Định dạng được hỗ trợ: MP4, AVI (video ngắn, tối đa 300MB)"
            )
        else:  # Audio
            uploaded_file = st.file_uploader(
                "Chọn file âm thanh:",
                type=['mp3', 'wav', 'flac', 'm4a', 'ogg'],
                help="Các định dạng được hỗ trợ: MP3, WAV, FLAC, M4A, OGG"
            )
        
        if uploaded_file is not None:
            # Kiểm tra kích thước file
            file_size_mb = uploaded_file.size / (1024 * 1024)  # Convert to MB
            
            if media_type == "Video" and file_size_mb > 300:
                st.error(f"❌ File quá lớn: {file_size_mb:.1f}MB. Vui lòng chọn video dưới 300MB")
                return
            
            st.success(f"✅ Đã tải lên: {uploaded_file.name} ({file_size_mb:.1f}MB)")
            
            # Hiển thị preview
            if media_type == "Hình ảnh":
                image = Image.open(uploaded_file)
                st.image(image, caption="Hình ảnh đã tải lên", use_container_width=True)
            elif media_type == "Video":
                if file_size_mb <= 50:  # Only show preview for smaller videos
                    st.video(uploaded_file)
                else:
                    st.info("📹 Video đã tải lên (không hiển thị preview do kích thước lớn)")
            else:  # Audio
                st.audio(uploaded_file)
            
            # Nút phân tích
            if st.button("🔍 Bắt đầu phân tích", type="primary"):
                analyze_media(uploaded_file, media_type, detector, labels, confidence_threshold, col2)
    
    with col2:
        st.header("📊 Kết quả phân tích")
        if 'analysis_results' not in st.session_state:
            st.info("👆 Vui lòng tải lên media và nhấn 'Bắt đầu phân tích' để xem kết quả")

def analyze_media(uploaded_file, media_type, detector, labels, confidence_threshold, results_column):
    with results_column:
        with st.spinner("🔄 Đang phân tích media..."):
            try:
                if media_type == "Hình ảnh":
                    results = detector.detect_image(uploaded_file)
                elif media_type == "Video":
                    results = detector.detect_video(uploaded_file)
                else:  # Audio
                    results = detector.detect_audio(uploaded_file)
                
                if results:
                    st.session_state.analysis_results = results
                    display_results(results, labels, confidence_threshold)
                else:
                    st.error("❌ Không thể phân tích media. Vui lòng thử lại.")
                    
            except Exception as e:
                st.error(f"❌ Lỗi trong quá trình phân tích: {str(e)}")

def display_results(results, labels, confidence_threshold):
    st.success("✅ Phân tích hoàn thành!")
    
    # Hiển thị thông tin debug
    if results:
        max_confidence = max([r.get('confidence', 0) for r in results])
        st.info(f"🔍 Tìm thấy {len(results)} kết quả. Độ tin cậy cao nhất: {max_confidence:.2%}")
    
    # Lọc kết quả theo ngưỡng confidence
    filtered_results = [r for r in results if r.get('confidence', 0) >= confidence_threshold]
    
    if not filtered_results:
        st.warning(f"⚠️ Không có kết quả nào đạt ngưỡng độ tin cậy {confidence_threshold:.1%}")
        if results:
            st.info("💡 Thử giảm ngưỡng độ tin cậy ở thanh bên để xem thêm kết quả")
            # Hiển thị top 3 kết quả dù không đạt ngưỡng
            st.subheader("📋 Top 3 kết quả (dưới ngưỡng):")
            for i, result in enumerate(results[:3]):
                st.write(f"{i+1}. {labels.get_vietnamese_label(result.get('label', 'Unknown'))} - {result.get('confidence', 0):.2%}")
        return
    
    st.subheader("🎯 Kết quả phát hiện")
    
    # Hiển thị kết quả dưới dạng dataframe
    df_data = []
    for i, result in enumerate(filtered_results):
        df_data.append({
            "STT": i + 1,
            "Đối tượng": labels.get_vietnamese_label(result.get('label', 'Unknown')),
            "Độ tin cậy": f"{result.get('confidence', 0):.2%}",
            "Vị trí": result.get('position', 'N/A')
        })
    
    if df_data:
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        
        # Form chỉnh sửa thông tin
        st.subheader("✏️ Chỉnh sửa thông tin")
        
        with st.form("edit_results_form"):
            selected_index = st.selectbox(
                "Chọn kết quả để chỉnh sửa:",
                range(len(filtered_results)),
                format_func=lambda x: f"{x+1}. {labels.get_vietnamese_label(filtered_results[x].get('label', 'Unknown'))}"
            )
            
            if selected_index is not None:
                selected_result = filtered_results[selected_index]
                
                # Các trường có thể chỉnh sửa
                new_label = st.text_input(
                    "Tên đối tượng:",
                    value=labels.get_vietnamese_label(selected_result.get('label', ''))
                )
                
                new_confidence = st.slider(
                    "Độ tin cậy (thủ công):",
                    min_value=0.0,
                    max_value=1.0,
                    value=selected_result.get('confidence', 0.5),
                    step=0.01
                )
                
                new_description = st.text_area(
                    "Mô tả thêm:",
                    value=selected_result.get('description', ''),
                    height=100
                )
                
                tags = st.text_input(
                    "Thẻ (phân cách bằng dấu phẩy):",
                    value=', '.join(selected_result.get('tags', []))
                )
                
                notes = st.text_area(
                    "Ghi chú:",
                    value=selected_result.get('notes', ''),
                    height=80
                )
                
                submitted = st.form_submit_button("💾 Lưu thay đổi", type="primary")
                
                if submitted:
                    # Cập nhật kết quả
                    filtered_results[selected_index].update({
                        'label': new_label,
                        'confidence': new_confidence,
                        'description': new_description,
                        'tags': [tag.strip() for tag in tags.split(',') if tag.strip()],
                        'notes': notes
                    })
                    
                    st.session_state.analysis_results = filtered_results
                    st.success("✅ Đã lưu thay đổi!")
                    st.rerun()
        
        # Xuất kết quả
        st.subheader("📤 Xuất kết quả")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Xuất CSV"):
                csv_data = pd.DataFrame([
                    {
                        'Đối tượng': labels.get_vietnamese_label(r.get('label', '')),
                        'Độ tin cậy': r.get('confidence', 0),
                        'Vị trí': r.get('position', ''),
                        'Mô tả': r.get('description', ''),
                        'Thẻ': ', '.join(r.get('tags', [])),
                        'Ghi chú': r.get('notes', '')
                    } for r in filtered_results
                ]).to_csv(index=False)
                
                st.download_button(
                    label="⬇️ Tải CSV",
                    data=csv_data,
                    file_name="ket_qua_phat_hien.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📋 Xuất JSON"):
                json_data = {
                    'metadata': {
                        'timestamp': pd.Timestamp.now().isoformat(),
                        'confidence_threshold': confidence_threshold,
                        'total_detections': len(filtered_results)
                    },
                    'results': filtered_results
                }
                
                st.download_button(
                    label="⬇️ Tải JSON",
                    data=pd.io.json.dumps(json_data, indent=2),
                    file_name="ket_qua_phat_hien.json",
                    mime="application/json"
                )
        
        with col3:
            if st.button("🔄 Phân tích lại"):
                if 'analysis_results' in st.session_state:
                    del st.session_state.analysis_results
                st.rerun()

if __name__ == "__main__":
    main()
