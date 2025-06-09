# Clone your repo
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo

# Create a fresh virtual environment (recommended)
python -m venv myenv

# Activate the environment
# Windows
myenv\Scripts\activate
# macOS/Linux
source myenv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run your script
python your_script.py
