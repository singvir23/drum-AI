import xml.etree.ElementTree as ET
import json

def read_musicxml(file_path):
    """
    Reads a MusicXML file and returns its contents as a string.
    The output string is escaped to maintain XML structure when embedding in JSON.
    """
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Convert the XML tree back to a string
        xml_str = ET.tostring(root, encoding='unicode')

        # Escape double quotes to ensure valid JSON string
        escaped_str = xml_str.replace('"', '\\"')

        return escaped_str
    except ET.ParseError as e:
        return f"Parse error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

def append_to_jsonl(data, output_path):
    """
    Appends the given data to a JSONL file.
    """
    try:
        with open(output_path, 'a') as file:
            json_record = json.dumps({"xml_content": data})
            file.write(json_record + '\n')
    except Exception as e:
        print(f"Failed to write to file: {e}")

# Example usage
file_path = '/Users/viraajsingh/drum-lick-generator/xmlFiles/flams/flam.xml'
output_path = '/Users/viraajsingh/drum-lick-generator/allData.jsonl'
musicxml_content = read_musicxml(file_path)

if musicxml_content:
    append_to_jsonl(musicxml_content, output_path)
    print("XML content has been appended to JSONL file.")
else:
    print("No data to append.")
