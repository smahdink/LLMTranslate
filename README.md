# 🌍 LLM Translate: Your Smart PDF Translator! 🚀

Translate your large PDF files with ease using the power of Large Language Models! This project leverages OpenAI-compatible and Mistral APIs to provide accurate, context-aware translations to your language of choice.
* You can see an example OCR and translation result in [Example.md](https://github.com/smahdink/LLMTranslate/blob/main/Example.md)

---

## ✨ Key Features

* **OCR Integration:** Processes PDF files by first performing Optical Character Recognition to extract text. 📄➡️💻
* **Specialized Translation:** Leveraging the power of LLMs, the translations done by this method are highly specialized and context-aware! 🧠
* **Structure Preservation:** Maintains the original document's formatting, numbers, measurements, and proper nouns. 📏
* **Configurable API:** Supports both OpenAI-compatible and Mistral API endpoints, with API key management through a local configuration file, so that you can use your favourite LLM or even self-host! ⚙️
* **Cost Reduction:** By using services like **OpenRouter** that provide free APIs for some models like the new `deepseek-r1-0528`, you can get great results with almost no expenses! 🤑


---

## 🛠️ Installation Guide
  * The commands you see in this guide can be executed inside a command line interface regardless of the OS (Linux, Windows, MacOS). But you need Python3 and pip installed beforehand.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/LLM-Translate.git
    cd LLM-Translate
    ```
    * You can use the download zip button instead of cloning

2.  **Install dependencies:**
    * You may want to create a Python virtual environment for this project to manage dependencies.
    ```bash
    pip install openai mistralai
    ```

---

## 🚀 How to Use

1.  **Customize URL and System Prompt:**
    Before running the application, open the `LLMTranslate.py` file in a text editor and customize the `system_prompt` and `base_url` parameters.

    * I highly recommend using **OpenRouter** which is the default URL. You only need to create an account on their website and generate an API key.
    * Customize the system prompt to provide the model with your **target language** and any additional contextual information relevant to your document. This helps ensure more accurate and tailored translations!

2.  **Run the script for the first time:**
    The first time you execute `LLMTranslate.py`, it will prompt you to enter your API keys for OpenAI-compatible and Mistral servers. These keys will be securely saved in `LLM-translate-config.ini`.

    ```bash
    python LLMTranslate.py your_document.pdf
    ```

    * *Remember to replace `your_document.pdf` with the actual path to your PDF file.*

3.  **Specify the LLM Model (Optional):**
    You have the flexibility to choose between `openai-compatible` (the default) and `mistral` models for translation. Use the `-m` or `--model` flag:

    ```bash
    python LLMTranslate.py your_document.pdf -m mistral
    ```

    *Alternatively:*

    ```bash
    python LLMTranslate.py your_document.pdf --model openai-compatible
    ```

4.  **Check the Output:**
    The translated content will be saved in a new Markdown file. The filename will follow the pattern `[original_filename] [model] translated.md` and will be located in the same directory as your input PDF. For example: `your_document mistral translated.md`. 📄✨

---

## 🤝 Contribute to LLM Translate!

I welcome contributions to LLM Translate! If you have suggestions, found a bug, or want to contribute to the code, please feel free to:

* Open a new issue for bug reports or feature requests.
* Submit a pull request with your improvements.

Let's build a better translation tool together! Your input is highly valued. 🎉

---

## 📝 TODO

* [ ] Improve code structre. This wasn't meant to be released at first :P
* [ ] Seperate the system prompt and move it somewhere easier to edit
* [ ] Implement an intermediate data structure (maybe json) to keep track of pages and different translations
* [ ] GUI and packaging into an installable app
