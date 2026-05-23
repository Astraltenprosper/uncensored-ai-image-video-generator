# 🎨 Image Generator Pro - Python Application

A full-featured application for safe image generation with a PyQt5-based GUI.

## 📋 Requirements

- Python 3.8+
- PyQt5
- Pillow
- requests

## 🚀 Installation

### 1. Clone or Download Files

```bash
# Download image_generator_app.py and requirements.txt
```

### 2. Create Virtual Environment (Optional but Recommended)

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Running the Application

```bash
python image_generator_app.py
```

Or:

```bash
python3 image_generator_app.py
```

## 🎯 Features

### Main Capabilities:
- ✅ **GUI Interface** - Beautiful dark design with PyQt5
- ✅ **Image Generation** - 6 styles (realistic, artistic, cartoon, abstract, vintage, cyberpunk)
- ✅ **Built-in Safety** - 4 content filters (NSFW, violence, hate speech, illegal content)
- ✅ **Content Verification** - Automatic check before generation
- ✅ **Quality Levels** - Standard, HD, 4K
- ✅ **Save & Download** - Export generated images
- ✅ **Multithreading** - Generation in separate thread (non-blocking UI)

### Available Styles:
- **Realistic** - Photorealistic style
- **Artistic** - Artistic style with line work
- **Cartoon** - Cartoon style with circles
- **Abstract** - Abstract style with geometric patterns
- **Vintage** - Vintage retro aesthetic
- **Cyberpunk** - Neon cyberpunk style

### Safety Filters:
- **NSFW** - Blocks adult content
- **Violence** - Blocks violent content
- **Hate** - Blocks hate speech and discriminatory content
- **Illegal** - Blocks illegal activity references

## 📁 Project Structure

```
image-generator/
├── image_generator_app.py        # Main application
├── image_generator_ai_advanced.py # Advanced version with AI
├── requirements.txt               # Dependencies
└── README.md                      # This file
```

## 💾 Where Images Are Saved

By default, images are saved in:
- **Linux/macOS**: `~/Pictures/ImageGenerator/`
- **Windows**: `C:\Users\YourUsername\Pictures\ImageGenerator\`

You can also manually select a location using the "⬇️ Download Image" button.

## 🔒 Security

The application uses built-in filters to verify content:

1. **Keyword Filtering** - Blocked words list for each category
2. **Filtered Categories**:
   - NSFW: nude, sex, porn, adult, erotic, etc.
   - Violence: kill, murder, blood, gun, bomb, etc.
   - Hate: hate, racism, nazi, terrorist, etc.
   - Illegal: bomb, drug, cocaine, heroin, etc.

3. **All Filters Enabled by Default** - Can be disabled if needed

## 🎨 AI API Integration (Optional)

To use real AI image generation:

### Using Hugging Face:

```python
from diffusers import StableDiffusionPipeline
import torch

pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
pipe = pipe.to("cuda")  # or "cpu" if no GPU
image = pipe(prompt).images[0]
```

### Using OpenAI DALL-E API:

```python
import openai

openai.api_key = "your-api-key"
response = openai.Image.create(
    prompt="your prompt",
    n=1,
    size="512x512"
)
```

## ⚙️ Customization

### Adding New Styles:

Edit the `_create_generative_image` method:

```python
elif style == 'your_style':
    self._draw_your_style(draw, size, color1, color2)

@staticmethod
def _draw_your_style(draw, size, color1, color2):
    # Your code here
    pass
```

### Adding New Filters:

Add to the `SafetyFilter` class:

```python
NEW_CATEGORY_KEYWORDS = {
    'keyword1', 'keyword2', 'keyword3'
}

# And in the check() method:
if filters.get('new_category', True):
    if SafetyFilter.NEW_CATEGORY_KEYWORDS & words:
        return False, "Error message"
```

## 🐛 Troubleshooting

### Error: "No module named 'PyQt5'"
```bash
pip install PyQt5
```

### Error: "No module named 'PIL'"
```bash
pip install Pillow
```

### Application Won't Start
- Check Python version: `python --version` (should be 3.8+)
- On Linux you may need: `sudo apt-get install python3-pyqt5`
- On macOS: `brew install qt5`

### Slow Image Generation
- This is normal for local generation
- For faster results, use GPU or cloud-based AI API

## 🚀 Advanced Version (AI-Powered)

For real AI-powered image generation, use `image_generator_ai_advanced.py`:

```bash
# Install additional dependencies
pip install diffusers torch transformers safetensors

# Run the advanced version
python image_generator_ai_advanced.py
```

Features:
- Real Stable Diffusion models from Hugging Face
- Automatic GPU/CPU detection
- 50+ inference steps for better quality
- Full safety filtering integration

## 📝 Code Structure

### SafetyFilter Class
Handles content verification with keyword-based filtering.

### ImageGeneratorWorker Thread
Performs image generation without blocking the UI.

### ImageGeneratorApp Class
Main PyQt5 window managing the user interface.

## 🎯 Usage Examples

### Basic Generation
1. Open the application
2. Describe the image you want (e.g., "a beautiful sunset over mountains")
3. Choose style and quality
4. Click "Generate"
5. Download when complete

### Safety in Action
- Try entering "nude" → Will be blocked by NSFW filter
- Try entering "kill" → Will be blocked by violence filter
- Filters can be disabled for testing

## 📊 Performance

### System Requirements
- **Minimum**: Intel i5, 8GB RAM, Python 3.8
- **Recommended**: GPU support, 16GB RAM, SSD storage
- **For AI Version**: NVIDIA CUDA support recommended

### Generation Times
- **Standard (512x512)**: 2-5 seconds
- **HD (768x768)**: 5-10 seconds
- **4K (1024x1024)**: 10-15 seconds

## 📄 License

This application was created for educational purposes.

## 🤝 Support

If you have questions or issues:
1. Check that all dependencies are installed
2. Verify Python 3.8+ is being used
3. Check console output for detailed error messages
4. On Linux systems, ensure PyQt5 system libraries are installed

## 🔄 Updates

Current Version: **1.0**  
Last Updated: **2024**  
Platform Support: **Windows, macOS, Linux**

---

### 🌟 Features Highlight

| Feature | Basic Version | AI Version |
|---------|---------------|-----------|
| GUI Interface | ✅ | ✅ |
| 6 Styles | ✅ | ✅ |
| Safety Filters | ✅ | ✅ |
| Multithreading | ✅ | ✅ |
| Real AI Generation | ❌ | ✅ |
| GPU Support | ❌ | ✅ |
| Higher Quality | ❌ | ✅ |

## 📖 Documentation

Full documentation is available in the code comments. Each class and method is documented with:
- Purpose description
- Parameters explanation
- Return value documentation

Happy generating! 🎨✨
