# Housing-Check 🏠🔍

An AI-powered image analysis tool that uses Google's Gemini Vision model to analyze photos and provide detailed descriptions of what's visible inside them. Perfect for housing inspections, property analysis, or any scenario where you need comprehensive visual understanding.

## Features ✨

- 🤖 **Advanced AI Vision**: Powered by Google's Gemini 1.5 Flash multi-modal model
- 📸 **Multiple Image Formats**: Supports JPEG, PNG, WebP, and other common formats
- 🎯 **Detailed Analysis**: Provides comprehensive descriptions including objects, colors, lighting, and spatial relationships
- 💬 **Custom Prompts**: Use custom prompts for specific analysis needs
- 🛡️ **Robust Error Handling**: Graceful handling of API failures and invalid inputs
- 🖥️ **User-Friendly CLI**: Simple command-line interface with helpful examples

## Quick Start 🚀

### 1. Installation

First, make sure you have conda activated, then install the required packages:

```bash
# Install required packages
conda install -c conda-forge google-generativeai pillow python-dotenv

# Or using pip with requirements file
pip install -r requirements.txt
```

### 2. Get Google AI API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key

### 3. Configure API Key

Create a `.env` file in the project directory:

```bash
# Copy the example file
cp .env.example .env
```

Then edit `.env` and add your API key:

```
GOOGLE_AI_API_KEY=your_actual_api_key_here
```

### 4. Run Analysis

```bash
# Basic analysis
python process-image.py path/to/your/image.jpg

# With custom prompt
python process-image.py image.jpg --prompt "What safety issues do you see in this room?"

# With verbose logging
python process-image.py image.jpg --verbose

# Provide API key directly (alternative to .env file)
python process-image.py image.jpg --api-key your_api_key_here
```

## Usage Examples 📝

### Basic Image Analysis
```bash
python process-image.py house_interior.jpg
```

### Housing Inspection Analysis
```bash
python process-image.py kitchen.jpg --prompt "Analyze this kitchen for potential safety issues, cleanliness, and maintenance needs"
```

### Property Features Analysis
```bash
python process-image.py living_room.jpg --prompt "Describe the style, condition, and notable features of this living space"
```

### Custom Analysis
```bash
python process-image.py exterior.jpg --prompt "What architectural features and landscaping elements do you notice?"
```

## Command Line Options 🔧

```
positional arguments:
  image_path            Path to the image file to analyze

options:
  -h, --help            show this help message and exit
  --prompt PROMPT, -p PROMPT
                        Custom prompt for image analysis
  --api-key API_KEY, -k API_KEY
                        Google AI API key (can also be set via GOOGLE_AI_API_KEY env variable)
  --verbose, -v         Enable verbose logging
```

## API Usage 🔌

You can also use the `ImageAnalyzer` class programmatically:

```python
from process_image import ImageAnalyzer

# Initialize analyzer
analyzer = ImageAnalyzer()

# Basic analysis
result = analyzer.analyze_image("path/to/image.jpg")
print(result)

# Custom analysis
custom_result = analyzer.analyze_with_custom_prompt(
    "path/to/image.jpg", 
    "What furniture and decorations do you see?"
)
print(custom_result)
```

## Supported Image Formats 🖼️

- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)
- BMP (.bmp)
- TIFF (.tiff, .tif)
- And other formats supported by PIL

## Error Handling 🛠️

The tool includes comprehensive error handling for:

- ❌ Missing or invalid image files
- 🔑 Invalid or missing API keys
- 🌐 Network connection issues
- 📝 API response errors
- 🖼️ Unsupported image formats

## Privacy & Security 🔒

- Images are sent to Google's AI services for processing
- No images are stored permanently by this tool
- API keys should be kept secure and not committed to version control
- Consider privacy implications when analyzing sensitive images

## Troubleshooting 🔧

### Common Issues

**Import Error for google-generativeai:**
```bash
conda install -c conda-forge google-generativeai
# or
pip install google-generativeai
```

**API Key Not Found:**
- Ensure your `.env` file exists and contains `GOOGLE_AI_API_KEY`
- Or pass the API key directly with `--api-key`

**Image Loading Error:**
- Check that the image file exists and is readable
- Ensure the image format is supported
- Try converting the image to a standard format (JPEG/PNG)

**Network/API Errors:**
- Check your internet connection
- Verify your API key is valid and has quota remaining
- Try again later if there are temporary service issues

## Contributing 🤝

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License 📄

This project is open source. Please check the repository for license details.

## Acknowledgments 🙏

- Built with Google's Gemini Vision AI model
- Uses PIL for image processing
- Powered by Python and love ❤️