# 🍳 ChefAI - Smart Recipe Generator

**Transform your ingredients into culinary masterpieces with AI-powered recipe suggestions**

ChefAI is an intelligent recipe generation application that uses computer vision and natural language processing to analyze your fridge contents and create personalized recipes based on available ingredients and your cooking preferences.

![ChefAI Demo](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange)

## 🌟 Features

- **🔍 AI-Powered Ingredient Detection**: Upload photos of your fridge/pantry and let AI identify available ingredients
- **📝 Smart Recipe Generation**: Get personalized recipes based on detected ingredients and cooking preferences
- **🎯 Mood-Based Cooking**: Choose from different cooking styles (Quick & Easy, Comfort Food, Healthy, etc.)
- **🎨 Professional UI**: Modern, responsive interface with intuitive user experience
- **📱 Cross-Platform**: Works on desktop, tablet, and mobile devices
- **⚡ Real-Time Processing**: Fast ingredient detection and recipe generation

## 🏗️ Tech Stack

### **Frontend**
- **[Streamlit](https://streamlit.io/)** - Web application framework
- **HTML5/CSS3** - Custom styling and responsive design
- **JavaScript** - Interactive elements and animations

### **Backend & AI**
- **[Python 3.8+](https://python.org/)** - Core application language
- **[OpenAI GPT-4](https://openai.com/)** - Recipe generation and text processing
- **[OpenAI Vision API](https://platform.openai.com/docs/guides/vision)** - Image analysis and ingredient detection

### **Data Processing**
- **[NumPy](https://numpy.org/)** - Numerical computations
- **[OpenCV](https://opencv.org/)** - Image preprocessing
- **[Pillow](https://pillow.readthedocs.io/)** - Image manipulation
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** - Environment variable management

### **Development Tools**
- **Git** - Version control
- **Virtual Environment** - Dependency isolation
- **Environment Variables** - Secure configuration management

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Git (for cloning the repository)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/chefai-recipe-generator.git
   cd chefai-recipe-generator
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv fridge_env
   source fridge_env/bin/activate  # On Windows: fridge_env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your OpenAI API key
   ```

5. **Run the application**
   ```bash
   streamlit run main.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Optional: Custom model settings
# For vision tasks, gpt-4o is used automatically
# For text generation, you can use gpt-4o-mini for cost efficiency
```

### Model Configuration

- **Vision Analysis**: Uses `gpt-4o` for image processing and ingredient detection
- **Recipe Generation**: Uses `gpt-4o-mini` by default (configurable via environment)
- **Cost Optimization**: Different models for different tasks to balance performance and cost

## 📖 Usage Guide

### 1. **Upload Your Fridge Photo**
- Take a clear photo of your fridge, pantry, or ingredients
- Upload through the web interface
- AI will automatically detect and list available ingredients

### 2. **Select Ingredients**
- Review AI-detected ingredients
- Add additional items from common ingredient categories
- Include custom ingredients not detected by AI

### 3. **Choose Your Cooking Mood**
- 🚀 Quick & Easy (5-15 minutes)
- 🏠 Comfort Food Classics
- 🥗 Healthy & Nutritious
- 🍖 Hearty & Filling
- 🌟 Creative & Gourmet
- 👨‍👩‍👧‍👦 Family-Friendly

### 4. **Generate Recipes**
- Click "Create My Recipes" to generate personalized suggestions
- Get two different recipes using your selected ingredients
- Each recipe includes ingredients list, step-by-step instructions, and timing

## 🏗️ Project Structure

```
chefai-recipe-generator/
│
├── main.py                    # Main Streamlit application
├── recipe_utils.py           # Core recipe generation logic
├── grocery_detection_utils.py # Image analysis and ingredient detection
├── test_grocery_detection.py # Testing utilities
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── README.md                # Project documentation
│
├── prompts/
│   └── recipe_prompt.txt    # AI prompt templates
│
├── uploads/                 # Temporary image storage
│   └── .gitkeep
│
└── fridge_env/             # Virtual environment (not in git)
    └── ...
```

## 🧪 Testing

Run the ingredient detection test:

```bash
python test_grocery_detection.py
```

This will test the AI vision capabilities with sample images and display detection results.

## 🔧 Development

### Adding New Features

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with descriptive messages**
   ```bash
   git commit -m "feat: add new ingredient categorization"
   ```
6. **Push and create a Pull Request**

### Code Style

- Follow PEP 8 Python style guidelines
- Use descriptive variable and function names
- Add comprehensive docstrings to all functions
- Include type hints where appropriate
- Keep functions focused and modular

### Debugging

Enable debug mode by setting environment variable:
```bash
export DEBUG=true
streamlit run main.py
```

## 💰 Cost Considerations

### OpenAI API Usage

- **Image Analysis**: ~$0.01-0.03 per image (using GPT-4o)
- **Recipe Generation**: ~$0.001-0.005 per recipe (using GPT-4o-mini)
- **Monthly Budget**: Estimate $10-50 for moderate usage

### Optimization Tips

- Use `gpt-4o-mini` for text-only tasks
- Resize large images before processing
- Cache ingredient detection results
- Implement request rate limiting

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Areas for Contribution

- 🔍 Improve ingredient detection accuracy
- 🍳 Add more recipe categories and cuisines
- 🎨 Enhance UI/UX design
- 📱 Mobile app development
- 🌍 Internationalization support
- 🧪 Add comprehensive testing

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for providing powerful AI models
- **Streamlit** for the excellent web framework
- **Open Source Community** for various libraries and tools

## 📞 Support

- 📧 **Email**: support@chefai.com
- 💬 **Issues**: [GitHub Issues](https://github.com/yourusername/chefai-recipe-generator/issues)
- 📚 **Documentation**: [Wiki](https://github.com/yourusername/chefai-recipe-generator/wiki)

## 🗺️ Roadmap

### Version 2.0 (Coming Soon)
- [ ] User accounts and recipe history
- [ ] Shopping list generation
- [ ] Nutritional information
- [ ] Recipe rating and favorites
- [ ] Social sharing features

### Version 3.0 (Future)
- [ ] Mobile app (React Native)
- [ ] Voice commands integration
- [ ] Meal planning features
- [ ] Integration with grocery delivery services
- [ ] Multi-language support

---

**Made with ❤️ for food lovers everywhere**

*Transform your cooking experience with the power of AI!*

