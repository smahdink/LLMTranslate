from openai import OpenAI
from openai.types.chat.chat_completion import Choice
from mistralai import Mistral
import argparse
from pathlib import Path
import time
import configparser
import MistralOCR

parser = argparse.ArgumentParser(prog='LLM Translate', description='Translates the input file, to the target language in page chunks.')
parser.add_argument('filename', help='Input file path')
parser.add_argument('-m', '--model', help="Specify the model to use for translation", choices=['openai-compatible', 'mistral'], default='openai-compatible')


max_retries = 3
content = ""

args = parser.parse_args()


# Init config file
config = configparser.ConfigParser()
config_file = Path("LLM-translate-config.ini")

#    Read or create config file if it doesn't exist
if config_file.exists():
       print(f"Config file '{config_file}' found. Reading configuration...")
       config.read(config_file)
else:
    print(f"Config file '{config_file}' not found. Creating new configuration...")
    # Ask user for parameter values
    param1 = input("Enter API Key for OPENAI compatible server: ")
    param2 = input("Enter API Key for Mistral: ")
    # Set configuration values
    config['DEFAULT'] = {
        'openai': param1,
        'mistral': param2
    }

    # Write configuration to file
    try:
        config_file.write_text('')  # Create the file first
        with open(config_file, 'w') as f:
            config.write(f)
        print(f"Configuration saved to '{config_file}'")
    except IOError as e:
        print(f"Error writing config file: {e}")


# instantiate apis
openai_client = OpenAI(
base_url="https://openrouter.ai/api/v1",
api_key=config["DEFAULT"].get("openai"),
)

mistral_client = Mistral(api_key = config["DEFAULT"].get("mistral"))


system_prompt = (
        "You are a professional medical translator from English to فارسی ایران. Translate by following these rules and DO NOT HALLUCINATE.:\n"
        "1. Maintain strict technical accuracy\n"
        "2. Preserve numbers and measurements\n"
        "3. Use formal medical terminology\n"
        "4. Keep original document formatting, You may translate ordered list numbers and characters\n"
        "5. Maintain consistent terminology\n"
        "6. Preserve proper nouns and Latin terms\n"
        "7. با حفظ دقیق معنی جملات ترجمه را انجام بده. می‌توانی بدون تغییر در معنی کمی ساختار جمله را تغییر دهی تا معنی آن در فارسی رسا تر شود.\n"
        "8. Output language is Persian (Iran) and RTL\n"
        "9. Preserve ICD-10 codes unchanged\n"
        "10. Use WHO-approved terminology\n"
        "11. Maintain original measurement units\n"
        "12. Highlight uncertain translations with [غیر مطمئن]\n"
        "13. Return only the translated text without any descriptions\n"
        "14. Expect markdown format in the prompt and return markdown, while keeping the structure intact\n"
        "15. فاصله و نیم فاصله بین کلمات را رعایت کن\n."
        "16. کاراکترهای راست نویس و چپ نویس یونیکد را در جاهای مقتضی رعایت کن."
    )


def parseFromFile(filepath):
    parsedListFromFile = []
    with open(filepath) as fp:
        for line in fp:
            if line.strip() != "---":
                parsedListFromFile.append(line)
            else:
                content = ""
                for index, item in enumerate(parsedListFromFile):
                    content = content + item + '\n'
                parsedListFromFile = []
                apiCall(content, filepath, args.model)


def apiCall(content, path, model):
    for tries in range(max_retries):
        try:
            if model == "mistral":
                completion = mistral_client.chat.complete(
                    model= "mistral-large-latest",
                    messages = [
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                        "role": "user",
                        "content": "Here is the text to translate:\n\"" + content + '\"'
                        }
                    ]
                )
            else:
                completion = openai_client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
                    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
                },
                extra_body={
                    #"provider": {
                    #    "order": ["Targon", "Chutes"]
                    #}
                },
                model="deepseek/deepseek-r1-0528:free",
                #model="google/gemma-3-27b-it:free",
                #model="tngtech/deepseek-r1t-chimera:free",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                    "role": "user",
                    "content": content
                    }
                ]
                )



            translated_content = ""
            # Validate response structure
            if (completion and
                completion.choices and
                len(completion.choices) > 0 and
                completion.choices[0].message and
                completion.choices[0].message.content):

                translated_content = completion.choices[0].message.content

            # Check if content meets minimum requirements
            if len(translated_content.strip()) >= 1:  # At least 1 non-whitespace character
                break  # Successful response, exit retry loop

            print(f"Attempt {tries+1}: Received empty or invalid response structure")
            time.sleep(1)

        except Exception as e:
            print(f"Attempt {tries+1} failed with error: {str(e)}")


    with open(filenameFromPath(path) + ' ' + model +" translated.md", "a") as output:
        output.write(str(translated_content) + '\n')


def filenameFromPath(path):
    name = path.replace(Path(path).suffix, "")
    return name

def main():
    if(args.filename.endswith(".pdf")):
        MistralOCR.ocrCall(args.filename, mistral_client)
        print("OCR done.")
    else:
        print("ERROR: Only pdf files are supported for now!")
        return False
    print("Starting translation. This might take a while depending on the LLM and file size. Go make some Tea!")

    # This does the upload to api and handles writing the answers to file
    # the file name is what the ocrCall function generates
    parseFromFile(filenameFromPath(args.filename) + " ocred.md")


if __name__ == "__main__": main()
