
### **SMART_IVR**

---

#### **Description**:

This repository structures and manages AI queries necessary for the frontend_ivr application. It aids in generating similar text prompts for intelligent prompt engineering.

#### **Prerequisites**:

- Python 3.9 (will not work with higher versions of python)
- A virtual environment tool of your choice (e.g., venv, virtualenv)

#### **Installation and Setup**:

1. Clone the repository.

   ```bash
   git clone https://github.com/Nikhilesh-B/smart_IVR.git
   ```

2. Navigate to the project directory.

   ```bash
   cd SMART_IVR
   ```

3. Set up a virtual environment:

   ```bash
   # For venv
   python3 -m venv venv_name
   source venv_name/bin/activate   # On Windows, use venv_name\Scripts\activate
   ```

4. Install the required Python packages:
   ```bash
   pip3 install -r requirements.txt
   ```

#### **Running the Application**:

1. Start the server:

   ```bash
   python3 manage.py runserver
   ```

2. The server should be up and running. Navigate to the displayed link in your web browser.

#### **Features**:

In the `audio_app` directory, you'll find all functionalities needed to run OpenAI queries for generating similar text prompts.

---

This README should be placed in the root directory of the `SMART_IVR` repository for clarity.
