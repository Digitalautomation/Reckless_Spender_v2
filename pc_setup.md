This document summarizes the current state of this development machine, configured specifically for AI learning and development on Ubuntu Linux. It serves as a reference for AI to understand the development limitations. 

## I. Current System Summary (As of: [Enter Today's Date, e.g., 2025-03-30])

*   **Operating System:** Ubuntu 24.04 LTS (Verify specific point release if desired: `lsb_release -a`)
*   **GPU:** NVIDIA GeForce RTX 3060 Ti
*   **NVIDIA Driver:** [Enter Driver Version Here - Run: `nvidia-smi | grep 'Driver Version'`]
*   **CUDA Toolkit:** 12.8 (Verified with `nvcc --version`)
*   **cuDNN:** 9.8.0 (Installed via apt packages, verified library presence)
*   **Node.js Environment:**
    *   Manager: nvm v0.39.7
    *   Node.js Version: v22.14.0 (LTS)
    *   npm Version: v10.9.2
    *   **Tailwind CSS Test Result:**
        *   Initial goal was to resolve failure creating `tailwindcss.cmd` / `postcss.cmd` on Windows.
        *   Test on fresh Ubuntu Linux confirmed the OS/environment was **NOT** the cause.
        *   Issue isolated to **`tailwindcss` v4.0.17** (currently tagged as `@latest`) failing to create its `.bin` link via `npm install`.
        *   Installing stable **`tailwindcss@^3.0.0`** (with `postcss@^8` and `autoprefixer@^10`) **succeeded** in creating `.bin` links.
    *   **Recommendation:** Use Tailwind CSS v3 (`npm install -D tailwindcss@^3.0.0 ...`) for reliable builds until the v4 package issue is resolved by Tailwind Labs. Monitor Tailwind v4 releases if v4 features are needed.
    *   *Note:* `tailwindcss` v4.0.17 had `.bin` link issues; using `tailwindcss@^3` is recommended for now.
*   **Python Environment:**
    *   System Python 3: [Enter Version Here - Run: `python3 --version`]
    *   `pip` for Python 3: Installed (`sudo apt install python3-pip`)
    *   `venv` for Python 3: Installed (`sudo apt install python3-venv`)
*   **Version Control:**
    *   Git Version: [Enter Version Here - Run: `git --version`]
    *   Git User Configured: Yes (Name: [Your Name], Email: [Your Email])
*   **Primary Editor:** Cursor v0.47.9 (AppImage, requires `--no-sandbox` flag).
    *   Launch command (if not integrated): `~/Applications/Cursor-0.47.9-x86_64.AppImage --no-sandbox` (Adjust path if different)
    *   Essential Extensions Installed: Python, Jupyter, Pylance (Microsoft)
*   **Default Browser:** Google Chrome

## II. Standard Python Project Workflow Reminder

To keep dependencies isolated and avoid conflicts:

1.  **Create Project Folder:** `mkdir my_project && cd my_project`
2.  **Initialize Git:** `git init` (Create/add `.gitignore` for `__pycache__`, `.venv`, `.env`, etc.)
3.  **Create Virtual Environment:** `python3 -m venv .venv`
4.  **Activate Environment:** `source .venv/bin/activate` (Look for `(.venv)` in prompt)
5.  **Install Packages:** `pip install <package_name>`
6.  **Select Interpreter in Editor:** Use Ctrl+Shift+P -> "Python: Select Interpreter" -> Choose the `.venv` one.
7.  **Work on Project.**
8.  **Deactivate Environment:** `deactivate` (When finished working in that terminal session) 