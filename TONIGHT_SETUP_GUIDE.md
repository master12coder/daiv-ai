# TONIGHT'S SETUP — Mac + Claude Max
# Copy-paste each command block one by one into Terminal
# Total time: ~15 minutes. Then sleep.

# =============================================
# STEP 1: Open Terminal
# =============================================
# Press: Cmd + Space
# Type: Terminal
# Press: Enter
# You'll see a window with a blinking cursor.

# =============================================
# STEP 2: Check what you already have
# =============================================

# Run these one by one. Note what you see.

python3 --version
# Need: 3.11 or higher. If you see 3.9+, that's fine too.
# If "command not found" → we'll install it in Step 3

git --version
# Need: any version. If "command not found" → it will prompt you to install Xcode tools. Say YES.

node --version
# If shows a number: great, skip Node install.
# If "command not found": we'll install in Step 3


# =============================================
# STEP 3: Install missing things
# =============================================

# --- Install Homebrew (if you don't have it) ---
# Check first:
brew --version
# If "command not found", install Homebrew:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# Follow the on-screen instructions. It may ask for your Mac password.
# IMPORTANT: After install, it shows 2 commands to add brew to your PATH. RUN THOSE.

# --- Install Python (if needed) ---
brew install python@3.12

# --- Install Node.js (needed for Claude Code) ---
brew install node

# --- Verify everything ---
python3 --version   # Should show 3.11+
node --version      # Should show 18+
git --version       # Should show any version
npm --version       # Should show any version


# =============================================
# STEP 4: Install Claude Code
# =============================================

# OPTION A: Native installer (recommended, auto-updates)
curl -fsSL https://cli.claude.com/install.sh | sh

# Close terminal and open a NEW terminal window (Cmd+Space → Terminal)
# Then verify:
claude --version

# If "command not found", try Option B instead:
# OPTION B: via npm
npm install -g @anthropic-ai/claude-code
# Then verify:
claude --version


# =============================================
# STEP 5: Authenticate Claude Code
# =============================================

# Just type:
claude

# What happens:
# 1. Your Chrome opens automatically
# 2. You see "Log in to Claude Code"
# 3. Click "Log in" → you're already logged into claude.ai in Chrome
# 4. It says "Authentication successful! You can close this tab."
# 5. Go back to Terminal → you'll see Claude Code ready with a ">" prompt
#
# IMPORTANT: Type /exit to quit Claude Code for now.
# We need to set up the project folder first.
/exit


# =============================================
# STEP 6: Create project folder
# =============================================

# Create folder on Desktop (easy to find)
mkdir -p ~/Desktop/vedic-ai-framework
cd ~/Desktop/vedic-ai-framework

# Initialize git
git init


# =============================================
# STEP 7: Save the BUILD_SPEC.md file
# =============================================
#
# Go back to your Claude.ai chat (this conversation).
# Find the BUILD_SPEC.md file I created.
# Click the download button on it.
# Save it to: Desktop → vedic-ai-framework folder
#
# Also download SYSTEM_DESIGN.md and save to same folder.
#
# Verify both files are there:
ls -la ~/Desktop/vedic-ai-framework/
# You should see:
#   BUILD_SPEC.md
#   SYSTEM_DESIGN.md


# =============================================
# STEP 8: Prevent Mac from sleeping
# =============================================

# OPTION A: Via System Settings
# Apple menu → System Settings → Displays → Advanced → check "Prevent automatic sleeping when display is off"

# OPTION B: Via terminal (simpler, lasts until you close terminal)
# Open a SECOND terminal tab (Cmd+T) and run:
caffeinate -d -i -s
# Leave this tab open. This prevents sleep.
# Switch back to your first terminal tab.


# =============================================
# STEP 9: Connect to GitHub (for later push)
# =============================================
#
# Go to github.com in Chrome
# Click "+" → "New repository"
# Name: vedic-ai-framework
# Description: AI-powered Vedic astrology framework with Swiss Ephemeris
# Visibility: Public
# Do NOT initialize with README (we're creating our own)
# Click "Create repository"
#
# Note the URL shown. It will be like:
# https://github.com/YOUR_USERNAME/vedic-ai-framework.git
#
# In terminal:
cd ~/Desktop/vedic-ai-framework
git remote add origin https://github.com/YOUR_USERNAME/vedic-ai-framework.git
# Replace YOUR_USERNAME with your actual GitHub username


# =============================================
# STEP 10: LAUNCH CLAUDE CODE AND START THE BUILD
# =============================================

# Make sure you're in the project folder:
cd ~/Desktop/vedic-ai-framework

# Launch Claude Code:
claude

# Wait for the ">" prompt to appear.
# Then paste this EXACT text (copy everything between the --- lines):

# ---START PASTE---
Read BUILD_SPEC.md completely from start to finish. This is a complete specification for a Python-based Vedic astrology AI framework. Build the entire project following every instruction exactly.

Work through this order:
1. First create pyproject.toml, config.yaml, CLAUDE.md, .gitignore, LICENSE (MIT)
2. Then create jyotish/utils/constants.py with all astrological constants
3. Then build the entire compute layer: chart.py, dasha.py, divisional.py, yoga.py, dosha.py, panchang.py, matching.py, transit.py, muhurta.py, strength.py
4. Then create ALL knowledge YAML files with COMPLETE data — all 12 lagnas in lordship_rules.yaml, all 27 nakshatras in nakshatra_data.yaml, all 9 gemstones in gemstone_logic.yaml, all 30+ yogas in yoga_definitions.yaml, and every other YAML file specified
5. Then build interpret layer: llm_backend.py with Ollama/Groq/Claude/OpenAI backends, interpreter.py, formatter.py, and ALL prompt template .md files
6. Then build learn layer: corrections.py, validator.py, rule_extractor.py, audio_processor.py
7. Then build deliver layer: markdown_report.py, json_export.py
8. Then build cli.py using click library with ALL commands specified
9. Then create ALL test files and run pytest — fix any failures
10. Then create comprehensive README.md with architecture diagram, quick start, examples
11. Then create all example JSON/MD files in examples/
12. Finally run the full test suite one more time to verify everything works

Use pip install as needed for dependencies. After building each layer, verify it works before moving to the next. Do not ask me questions — make reasonable decisions based on the spec and keep building autonomously. I am going to sleep and will check in the morning.
# ---END PASTE---

# Press Enter.
# Watch for ~1 minute to make sure it starts reading BUILD_SPEC.md
# and creating files. You should see it working.
#
# Once confirmed it's building → GO TO SLEEP.
# Keep Terminal open. Keep Mac plugged in. Keep caffeinate running.


# =============================================
# MORNING: Wake up and verify
# =============================================

# Go to Terminal. Claude Code should be finished or close to it.
# If it shows ">" prompt, it's done.

# Install the project:
cd ~/Desktop/vedic-ai-framework
pip3 install -e ".[dev]"

# Run tests:
python3 -m pytest

# Test with your own chart:
python3 -m jyotish.cli chart --name "Manish Chaurasia" --dob "13/03/1989" --tob "12:17" --place "Varanasi" --gender Male

# If everything works, push to GitHub:
git add .
git commit -m "feat: initial commit — Vedic AI Framework"
git push -u origin main

# DONE! Check github.com/YOUR_USERNAME/vedic-ai-framework


# =============================================
# IF SOMETHING GOES WRONG
# =============================================

# Claude Code stopped/crashed:
cd ~/Desktop/vedic-ai-framework
claude
# Paste: "Continue building from BUILD_SPEC.md. Check what already exists and build what's missing. Run tests when done."

# Can't install pyswisseph:
brew install swig
pip3 install pyswisseph

# "Permission denied" errors:
pip3 install --user -e ".[dev]"

# Git push asks for password:
# Use GitHub Personal Access Token instead of password
# Go to: github.com → Settings → Developer settings → Personal access tokens → Generate new token
# Use the token as your password when git push asks

# Rate limit (unlikely with Max plan but just in case):
# Claude Code auto-waits and resumes. Just leave it running.
