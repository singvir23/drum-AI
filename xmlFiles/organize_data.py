import os
import json
import openai
import time
from dotenv import load_dotenv

load_dotenv()

def read_musicxml(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            xml_str = f.read()
        return xml_str
    except Exception as e:
        print(f"An error occurred while reading {file_path}: {e}")
        return None

def read_baseline_descriptions(description_file_path):
    try:
        descriptions = {}
        with open(description_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if "=" in line:
                    filename, desc = line.split("=", 1)
                    descriptions[filename.strip()] = desc.strip()
        return descriptions
    except Exception as e:
        print(f"Failed to read baseline descriptions: {e}")
        return {}

from openai import OpenAI
import time

client = OpenAI()

def generate_descriptions(xml_content, baseline_description):
    try:
        descriptions = []
        for i in range(5):
            specificity = ["ultra-specific", "very specific", "specific", "general", "generic"][i]
            if baseline_description:
                prompt = f"Based on this baseline description: '{baseline_description}', provide a {specificity} description of the following MusicXML content:\n{xml_content}"
            else:
                prompt = f"Provide a {specificity} description of the following MusicXML content:\n{xml_content}"

            stream = client.chat.completions.create(
                model="gpt-4o", 
                messages=[
                    {"role": "user", "content": prompt}
                ],
                stream=True,  
            )

            description = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    description += chunk.choices[0].delta.content

            descriptions.append(description.strip())
            print(f"Generated {specificity} description: {description.strip()}")
            
            time.sleep(1)  

        return descriptions
    except client.error.RateLimitError as e:
        print(f"Rate limit exceeded: {e}")
        return []
    except client.error.APIError as e:
        print(f"API error: {e}")
        return []
    except client.OpenAIError as e: 
        print(f"An OpenAI API error occurred: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        raise


def append_to_jsonl(data, output_path):
    """
    Appends the given data to a JSONL file.
    """
    try:
        with open(output_path, 'a', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)
            file.write('\n')
        print(f"Appended data to {output_path}")
    except Exception as e:
        print(f"Failed to write to file: {e}")
        raise

def process_all_xml_files(xml_root_path, output_path, description_file_path):
    """
    Processes all XML files in the given directory and its subdirectories,
    generates descriptions, and appends them to the JSONL file.
    """
    print(f"Starting to process XML files in {xml_root_path}")
    file_count = 0  

    baseline_descriptions = read_baseline_descriptions(description_file_path)

    for root, dirs, files in os.walk(xml_root_path):
        for file in files:
            if file.lower().endswith('.xml'):
                file_count += 1
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")
                xml_content = read_musicxml(file_path)
                if not xml_content:
                    print(f"Failed to read {file_path}")
                    continue

                baseline_description = baseline_descriptions.get(file, None)

                descriptions = generate_descriptions(xml_content, baseline_description)
                if not descriptions:
                    print(f"No descriptions generated for {file_path}")
                    continue
                print(f"Generated {len(descriptions)} descriptions for {file}")
                
                for description in descriptions:
                    record = {
                        "messages": [
                            {
                                "role": "system",
                                "content": "Drum-Lick-Generator is an AI that can produce MusicXML code according to your input."
                            },
                            {
                                "role": "user",
                                "content": description
                            },
                            {
                                "role": "assistant",
                                "content": xml_content
                            }
                        ]
                    }
                    append_to_jsonl(record, output_path)

    if file_count == 0:
        print("No XML files found in the specified directory or its subdirectories.")
    print("Finished processing XML files.")


if __name__ == "__main__":
    print("Starting the data organization script...")
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable")
    else:
        print("API key loaded successfully.")

    openai.api_key = api_key

    xml_root_path = '/Users/viraajsingh/Desktop/drum-AI/xmlFiles/triplets'
    description_file_path = '/Users/viraajsingh/Desktop/drum-AI/xmlFiles/descriptions.txt'
    output_path = os.path.join(xml_root_path, 'allData.jsonl')

    process_all_xml_files(xml_root_path, output_path, description_file_path)
    print("Script completed successfully.")
