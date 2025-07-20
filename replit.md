# AI Media Detection Application

## Overview

This is a Streamlit-based AI media detection application that can analyze and classify images, videos, and audio files. The application is built in Python and uses TensorFlow for machine learning capabilities, with Vietnamese language support for user interface and classification labels.

## User Preferences

Preferred communication style: Simple, everyday language.
App Branding: "AI Media Checker PhvAMC" with Vietnamese interface
Social Media Integration: YouTube (@Phvsadboiz) and Facebook links in header

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application
- **Language**: Python with Vietnamese UI
- **Layout**: Wide layout with sidebar for configuration options
- **Caching**: Uses Streamlit's `@st.cache_resource` for model loading optimization

### Backend Architecture
- **Core Logic**: Object-oriented design with separate utility classes
- **AI Models**: TensorFlow-based models for different media types
- **Media Processing**: OpenCV for video/image processing, librosa for audio analysis
- **File Handling**: PIL for image manipulation, temporary file handling for uploads

## Key Components

### 1. Main Application (`app.py`)
- **Purpose**: Entry point and UI orchestration
- **Responsibilities**: 
  - Streamlit page configuration and layout
  - User interface components (file upload, confidence threshold slider)
  - Model initialization with caching
  - Media type selection (Image, Video, Audio)

### 2. Media Detector (`utils/media_detector.py`)
- **Purpose**: Core AI detection functionality
- **Architecture**: 
  - Singleton pattern with cached model loading
  - Separate methods for each media type
  - Uses pre-trained MobileNetV2 for image classification
  - Video processing through frame-by-frame analysis
  - Audio processing capabilities (placeholder implementation)

### 3. Vietnamese Labels (`utils/vietnamese_labels.py`)
- **Purpose**: Localization support for classification results
- **Implementation**: Dictionary-based mapping from English ImageNet labels to Vietnamese translations
- **Coverage**: Extensive animal classification labels with Vietnamese equivalents

## Data Flow

1. **User Input**: File upload through Streamlit interface
2. **Media Type Detection**: Automatic or manual selection of processing pipeline
3. **Model Processing**: 
   - Images: MobileNetV2 classification
   - Videos: Frame extraction and image processing
   - Audio: Librosa-based feature extraction (planned)
4. **Label Translation**: English labels converted to Vietnamese using mapping dictionary
5. **Result Display**: Confidence scores and localized labels presented to user

## External Dependencies

### Core Libraries
- **streamlit**: Web application framework
- **tensorflow**: Machine learning models
- **opencv-python**: Computer vision and video processing
- **PIL (Pillow)**: Image processing
- **librosa**: Audio analysis
- **numpy**: Numerical computations
- **pandas**: Data manipulation

### Pre-trained Models
- **MobileNetV2**: ImageNet pre-trained model for image classification
- **Future models**: Placeholder architecture for video and audio models

## Deployment Strategy

### Current Setup
- **Platform**: Designed for Replit deployment
- **Resource Management**: Model caching to optimize memory usage
- **File Handling**: Temporary file system usage for uploaded media
- **Scalability**: Single-instance design suitable for development/demo environments

### Architectural Decisions

1. **Streamlit Framework Choice**
   - **Problem**: Need for rapid prototyping of AI application with minimal frontend development
   - **Solution**: Streamlit for automatic UI generation from Python code
   - **Pros**: Fast development, built-in caching, easy deployment
   - **Cons**: Limited customization, single-user sessions

2. **MobileNetV2 Model Selection**
   - **Problem**: Need for efficient image classification
   - **Solution**: Pre-trained MobileNetV2 from ImageNet
   - **Pros**: Good accuracy-to-size ratio, fast inference, no training required
   - **Cons**: Limited to ImageNet classes, may not cover domain-specific objects

3. **Modular Architecture**
   - **Problem**: Separation of concerns for different media types
   - **Solution**: Separate utility classes for detection logic and localization
   - **Pros**: Maintainable, extensible, testable
   - **Cons**: Slight complexity overhead for simple use cases

4. **Vietnamese Localization**
   - **Problem**: Need for local language support
   - **Solution**: Dictionary-based label mapping
   - **Pros**: Simple implementation, easy to extend
   - **Cons**: Manual maintenance, limited to predefined mappings

### Recent Changes
- **2025-07-19**: Customized app branding to "AI Media Checker PhvAMC" 
- **2025-07-19**: Added social media integration (YouTube and Facebook links)
- **2025-07-19**: Created local installation scripts (run_app.py, install.bat, install.sh)
- **2025-07-19**: Updated description to Vietnamese with custom messaging

### Future Considerations
- Database integration for storing detection results
- User authentication for multi-user support
- Advanced video and audio model implementations
- API endpoints for programmatic access
- Enhanced error handling and logging