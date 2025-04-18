# %%
#! pip install gitpython
# %% [markdown]
# 

# %%
def format_text_file(input_file, output_file):
    """
    Reads a .txt file, replaces escaped '\n' with actual new lines, and writes the formatted text to a new file.

    :param input_file: Path to the input .txt file
    :param output_file: Path to the output .txt file
    """
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            content = file.read()

        # Replace literal "\n" (not actual new lines) with real new lines
        formatted_content = content.replace("\\n", "\n")

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(formatted_content)

        print(f"Formatted text saved to {output_file}")
    except Exception as e:
        print(f"Error formatting text file: {e}")


# %%
def save_dict_to_txt(data, file_path):
    """
    Saves a dictionary to a text file in JSON format.

    :param data: Dictionary to save
    :param file_path: Path to the .txt file
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print(f"Dictionary saved successfully to {file_path}")
    except Exception as e:
        print(f"Error saving dictionary: {e}")


# %%
import git
import os

def clone_repository(repo_url, local_dir="repo_clone"):
    """Clones a GitHub repository to a local directory."""
    if os.path.exists(local_dir):
        print("Repository already cloned.")
    else:
        git.Repo.clone_from(repo_url, local_dir)
        print(f"Cloned repository to {local_dir}")

repo_url = "https://github.com/SmitMaurya23/InstInc.git"  # Replace with an actual repo
clone_repository(repo_url)


# %%
import os
import json

def extract_code(file_path):
    """
    Extract code content from a repository and structure it in a dictionary format.

    Args:
        file_path (str): Path to the cloned repository

    Returns:
        dict: A dictionary representing the project structure with code content
    """
    project_content_code = {}

    # List of directories/files to ignore (common config and non-developer files)
    ignore_list = [
        'node_modules', '.git', '.github', '.vscode', 'build', 'dist', 'coverage',
        '.DS_Store', 'package-lock.json', 'yarn.lock', '.gitignore', '.env',
        '.env.local', '.env.development', '.env.test', '.env.production',
        'venv', '__pycache__', '.pytest_cache', '.idea', '.project'
    ]

    # Common binary file extensions to avoid reading their content
    binary_extensions = [
        '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', '.pdf', '.zip',
        '.tar', '.gz', '.rar', '.exe', '.dll', '.so', '.pyc', '.class'
    ]

    def is_binary_file(file_path):
        """Check if a file is binary based on its extension"""
        _, ext = os.path.splitext(file_path)
        return ext.lower() in binary_extensions

    def should_include(path):
        """Check if a file or directory should be included"""
        name = os.path.basename(path)
        # Skip hidden files/folders and those in ignore_list
        if name.startswith('.') or name in ignore_list:
            return False
        return True

    def process_directory(path, current_dict):
        """Process directory recursively and populate the dictionary"""

        # Get all items in the directory
        items = os.listdir(path)

        for item in items:
            item_path = os.path.join(path, item)

            # Skip if item should be ignored
            if not should_include(item_path):
                continue

            if os.path.isdir(item_path):
                # If it's a directory, create a new dictionary entry with metadata
                current_dict[item] = {
                    "type": "directory",
                    "content": {}
                }
                # Process the subdirectory
                process_directory(item_path, current_dict[item]["content"])
            else:
                # If it's a file, determine its type and add content
                _, ext = os.path.splitext(item)
                file_type = ext.lstrip('.') if ext else "unknown"

                file_content = ""
                # Read the file content if it's not a binary file
                if not is_binary_file(item_path):
                    try:
                        with open(item_path, 'r', encoding='utf-8') as file:
                            file_content = file.read()
                    except UnicodeDecodeError:
                        # If we encounter an error, it might be a binary file not in our list
                        file_content = "Binary file content not included"
                else:
                    file_content = "Binary file content not included"

                # Add the file information to the dictionary
                current_dict[item] = {
                    "type": "file",
                    "file_type": file_type,
                    "content": file_content
                }

    # Start processing from the root directory
    if os.path.exists(file_path) and os.path.isdir(file_path):
        process_directory(file_path, project_content_code)
    else:
        raise ValueError(f"The path '{file_path}' does not exist or is not a directory")

    return project_content_code

# Example usage:
# project_structure = extract_code("path/to/repo_clone")
#
# # Save to JSON file (optional)
# with open("project_structure.json", "w", encoding="utf-8") as f:
#     json.dump(project_structure, f, indent=2)

# %%
project_content_code = extract_code("repo_clone")
project_content_code

# %%
import re
import copy

def create_chunked_project_code(project_content_code):
    """
    Convert project_content_code into a chunked version where code files are split into meaningful snippets.

    Args:
        project_content_code (dict): Dictionary containing the project structure with code content

    Returns:
        dict: A dictionary with the same structure but with code content chunked into snippets
    """
    chunked_project_code = copy.deepcopy(project_content_code)

    def process_node(node):
        """Process a node in the project structure recursively"""
        if isinstance(node, dict):
            if node.get("type") == "file" and "content" in node:
                if node.get("file_type") in ["js", "jsx", "ts", "tsx", "py", "java", "c", "cpp", "cs", "php", "go", "rb"]:
                    # Process code files
                    node["snippets"] = create_code_snippets(node["content"], node["file_type"])
                    # Keep the original content for reference
                    node["original_content"] = node["content"]
                    # Remove content as it's now in snippets
                    del node["content"]
                    return

            # Process directories or non-code files
            for key, value in list(node.items()):
                if key != "type" and key != "file_type" and key != "content":
                    process_node(value)
                elif key == "content" and isinstance(value, dict):
                    process_node(value)

    def create_code_snippets(content, file_type):
        """Break down code content into logical snippets"""
        snippets = {}

        if file_type in ["js", "jsx", "ts", "tsx"]:
            return create_javascript_snippets(content)
        elif file_type == "py":
            return create_python_snippets(content)
        elif file_type in ["java", "c", "cpp", "cs"]:
            return create_c_style_snippets(content)
        elif file_type == "php":
            return create_php_snippets(content)
        elif file_type in ["go", "rb"]:
            return create_generic_snippets(content)
        else:
            # Default chunking for other types
            snippets["snip1"] = {
                "type": "complete_file",
                "content": content
            }
            return snippets

    def create_javascript_snippets(content):
        """Create snippets for JavaScript/TypeScript code"""
        snippets = {}

        # Split imports and global declarations
        import_pattern = r'^(import\s+.*?;|const\s+.*?=\s+require\(.*?\);|export\s+.*?;)\s*$'
        imports = re.findall(import_pattern, content, re.MULTILINE)

        if imports:
            imports_text = "\n".join(imports)
            snippets["snip1"] = {
                "type": "imports",
                "content": imports_text
            }

        # Match functions, classes, and methods
        function_pattern = r'((?:async\s+)?(?:function\s+\w+|\w+\s*=\s*(?:async\s+)?function|\w+\s*=\s*\(.*?\)\s*=>)\s*\{[^{}]*(?:\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}[^{}]*)*\})'
        class_pattern = r'(class\s+\w+(?:\s+extends\s+\w+)?\s*\{[^{}]*(?:\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}[^{}]*)*\})'
        method_pattern = r'(\w+\s*\(.*?\)\s*\{[^{}]*(?:\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}[^{}]*)*\})'
        arrow_func_pattern = r'(const\s+\w+\s*=\s*(?:\(.*?\))?\s*=>\s*(?:\{[^{}]*(?:\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}[^{}]*)*\}|[^;]+;))'

        patterns = [
            ("function", function_pattern),
            ("class", class_pattern),
            ("method", method_pattern),
            ("arrow_function", arrow_func_pattern)
        ]

        snip_count = 2 if imports else 1

        # Find and store all code blocks
        for pattern_type, pattern in patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            for match in matches:
                snippets[f"snip{snip_count}"] = {
                    "type": pattern_type,
                    "content": match.strip()
                }
                snip_count += 1

        # Get remaining code that doesn't fit patterns
        remaining_code = content
        for _, snip_data in snippets.items():
            remaining_code = remaining_code.replace(snip_data["content"], "")

        # Clean up remaining code and store meaningful chunks
        remaining_code = re.sub(r'\s+', ' ', remaining_code).strip()
        if remaining_code and len(remaining_code) > 10:  # Only include if it's not just whitespace
            snippets[f"snip{snip_count}"] = {
                "type": "other_code",
                "content": remaining_code
            }

        # If no snippets were found, store the whole content
        if not snippets:
            snippets["snip1"] = {
                "type": "complete_file",
                "content": content
            }

        return snippets

    def create_python_snippets(content):
        """Create snippets for Python code"""
        snippets = {}

        # Split imports and global declarations
        import_pattern = r'^((?:import|from).*?)$'
        imports = re.findall(import_pattern, content, re.MULTILINE)

        if imports:
            imports_text = "\n".join(imports)
            snippets["snip1"] = {
                "type": "imports",
                "content": imports_text
            }

        # Match classes and functions
        class_pattern = r'(class\s+\w+(?:\(.*?\))?\s*:(?:.*?)(?:(?:^[ \t]*def|\Z)|\n\s*\n))'
        function_pattern = r'(def\s+\w+\s*\(.*?\)\s*:(?:.*?)(?:(?:^[ \t]*def|\Z)|\n\s*\n))'

        snip_count = 2 if imports else 1

        # Find classes
        for match in re.finditer(class_pattern, content, re.DOTALL | re.MULTILINE):
            class_content = match.group(1).strip()
            snippets[f"snip{snip_count}"] = {
                "type": "class",
                "content": class_content
            }

            # Find methods within the class
            method_pattern = r'([ \t]+def\s+\w+\s*\(.*?\)\s*:(?:.*?)(?:(?:[ \t]+def|\Z)|\n\s*\n))'
            method_count = 1

            for method_match in re.finditer(method_pattern, class_content, re.DOTALL | re.MULTILINE):
                method_content = method_match.group(1).strip()
                snippets[f"snip{snip_count}snip{method_count}"] = {
                    "type": "method",
                    "content": method_content
                }
                method_count += 1

            snip_count += 1

        # Find standalone functions
        for match in re.finditer(function_pattern, content, re.DOTALL | re.MULTILINE):
            func_content = match.group(1).strip()
            # Skip if this is a method (indented)
            if not func_content.startswith(" ") and not func_content.startswith("\t"):
                snippets[f"snip{snip_count}"] = {
                    "type": "function",
                    "content": func_content
                }
                snip_count += 1

        # Get remaining code
        if not snippets:
            snippets["snip1"] = {
                "type": "complete_file",
                "content": content
            }

        return snippets

    def create_c_style_snippets(content):
        """Create snippets for C-style languages (Java, C, C++, C#)"""
        snippets = {}

        # Split imports/includes
        import_pattern = r'^((?:import|#include|using).*?;)\s*$'
        imports = re.findall(import_pattern, content, re.MULTILINE)

        if imports:
            imports_text = "\n".join(imports)
            snippets["snip1"] = {
                "type": "imports",
                "content": imports_text
            }

        # Match classes, interfaces, and functions
        class_pattern = r'((?:public|private|protected)?\s*(?:abstract|final)?\s*class\s+\w+(?:\s+(?:extends|implements)\s+[\w,\s]+)?\s*\{[^{}]*(?:\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}[^{}]*)*\})'
        interface_pattern = r'((?:public|private|protected)?\s*interface\s+\w+(?:\s+(?:extends)\s+[\w,\s]+)?\s*\{[^{}]*(?:\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}[^{}]*)*\})'
        method_pattern = r'((?:public|private|protected)?\s*(?:static)?\s*(?:final)?\s*\w+(?:<[\w,\s<>]+>)?\s+\w+\s*\(.*?\)\s*(?:throws\s+[\w,\s]+)?\s*\{[^{}]*(?:\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}[^{}]*)*\})'

        patterns = [
            ("class", class_pattern),
            ("interface", interface_pattern),
            ("method_or_function", method_pattern)
        ]

        snip_count = 2 if imports else 1

        # Find and store all code blocks
        for pattern_type, pattern in patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            for match in matches:
                snippets[f"snip{snip_count}"] = {
                    "type": pattern_type,
                    "content": match.strip()
                }
                snip_count += 1

        # If no snippets were found, store the whole content
        if not snippets:
            snippets["snip1"] = {
                "type": "complete_file",
                "content": content
            }

        return snippets

    def create_php_snippets(content):
        """Create snippets for PHP code"""
        snippets = {}

        # PHP files might start with <?php tag
        if "<?php" in content:
            snippets["snip1"] = {
                "type": "php_opening",
                "content": "<?php"
            }
            snip_count = 2
        else:
            snip_count = 1

        # Match functions and classes
        function_pattern = r'(function\s+\w+\s*\(.*?\)\s*\{[^{}]*(?:\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}[^{}]*)*\})'
        class_pattern = r'(class\s+\w+(?:\s+extends\s+\w+)?(?:\s+implements\s+[\w,\s]+)?\s*\{[^{}]*(?:\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}[^{}]*)*\})'

        patterns = [
            ("function", function_pattern),
            ("class", class_pattern)
        ]

        # Find and store all code blocks
        for pattern_type, pattern in patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            for match in matches:
                snippets[f"snip{snip_count}"] = {
                    "type": pattern_type,
                    "content": match.strip()
                }
                snip_count += 1

        # If no snippets were found, store the whole content
        if not snippets:
            snippets["snip1"] = {
                "type": "complete_file",
                "content": content
            }

        return snippets

    def create_generic_snippets(content):
        """Generic snippet creation for other languages"""
        snippets = {}

        # Try to identify functions and blocks
        function_pattern = r'((?:func|def|function)\s+\w+\s*\(.*?\).*?\{[^{}]*(?:\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}[^{}]*)*\})'
        block_pattern = r'(\w+\s*\{[^{}]*(?:\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}[^{}]*)*\})'

        snip_count = 1

        # Find functions
        functions = re.findall(function_pattern, content, re.DOTALL)
        for func in functions:
            snippets[f"snip{snip_count}"] = {
                "type": "function_or_method",
                "content": func.strip()
            }
            snip_count += 1

        # Find other code blocks
        if not functions:
            blocks = re.findall(block_pattern, content, re.DOTALL)
            for block in blocks:
                snippets[f"snip{snip_count}"] = {
                    "type": "code_block",
                    "content": block.strip()
                }
                snip_count += 1

        # If no snippets were found, store the whole content
        if not snippets:
            snippets["snip1"] = {
                "type": "complete_file",
                "content": content
            }

        return snippets

    # Start processing the project structure
    process_node(chunked_project_code)

    return chunked_project_code

# Example usage:
# chunked_project_code = create_chunked_project_code(project_content_code)

# %%
chunked_project_code = create_chunked_project_code(project_content_code)
chunked_project_code

# %%
import subprocess
import json
import os

def create_summarized_project_code(chunked_project_code):
    """
    Create a summarized version of the chunked project code, recursively summarizing from bottom up.

    Args:
        chunked_project_code (dict): Dictionary containing the chunked project structure

    Returns:
        dict: A dictionary with the same structure but with added summaries
    """
    summarized_project_code = copy.deepcopy(chunked_project_code)

    # Define prompts for different types of content
    SNIPPET_PROMPT = """You are a code-summarizer now, summarize this code snippet in one to three lines such that:
1) logic of the summary and code remains the same.
2) try to minimize the number of characters in summary.
3) make sure that no crucial information is lost
4) summary should be good enough such that any other LLM can regenerate the same code snippet from the summary.
5) Mention all the variables, functions, input-output used so that the summary is sufficient to regenerate the exact code.

CODE:
{code}
"""

    FILE_PROMPT = """You are a code-summarizer now, summarize this file based on its snippets summaries in three to five lines such that:
1) the summary explains the overall purpose and functionality of the file.
2) highlight the key components, functions, or classes in the file.
3) mention how these components interact with each other.
4) the summary should provide enough context for someone to understand what this file does without reading the actual code.

SNIPPETS SUMMARIES:
{summaries}
"""

    DIRECTORY_PROMPT = """You are a code-summarizer now, summarize this directory based on its contained files and subdirectories in five to seven lines such that:
1) explain the overall purpose of this directory in the project.
2) highlight the key files and their roles.
3) explain how the files in this directory work together.
4) mention any important dependencies or relationships with other parts of the project if evident.
5) provide a high-level architectural view of this part of the project.

CONTAINED FILES AND DIRECTORIES SUMMARIES:
{summaries}
"""

    def generate_summary_with_mistral(prompt):
        """
        Generate summary using Ollama Mistral model.

        Args:
            prompt (str): The prompt to send to the model

        Returns:
            str: The generated summary
        """
        try:
            # Call Ollama with Mistral model
            result = subprocess.run(
                ["ollama", "run", "mistral", prompt],
                capture_output=True,
                text=True,
                check=True
            )
            # Clean and return the output
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error calling Ollama: {e}")
            # Fallback message if Ollama isn't available
            return "Summary generation failed. Please ensure Ollama is installed and the Mistral model is available."
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "An unexpected error occurred during summary generation."

    def summarize_node(node, path=""):
        """
        Recursively summarize nodes in the project structure from bottom up.

        Args:
            node: The current node to summarize
            path: Current path in the structure (for debugging)

        Returns:
            str: Summary of the current node
        """
        if not isinstance(node, dict):
            return ""

        # Handle different node types
        if "type" in node:
            # For files
            if node["type"] == "file":
                # First summarize all snippets if they exist
                if "snippets" in node:
                    # Process all snippets
                    for snippet_key, snippet_data in node["snippets"].items():
                        if "content" in snippet_data:
                            # Generate prompt for this snippet
                            prompt = SNIPPET_PROMPT.format(code=snippet_data["content"])

                            # Add the prompt to the snippet data
                            snippet_data["prompt"] = prompt

                            # Generate the summary
                            summary = generate_summary_with_mistral(prompt)

                            # Add the summary to the snippet data
                            snippet_data["summary"] = summary

                    # Now summarize the file based on its snippets
                    snippet_summaries = []
                    for snippet_key, snippet_data in node["snippets"].items():
                        if "summary" in snippet_data:
                            snippet_summaries.append(f"{snippet_key} ({snippet_data.get('type', 'unknown')}): {snippet_data['summary']}")

                    all_snippets_summary = "\n".join(snippet_summaries)
                    file_prompt = FILE_PROMPT.format(summaries=all_snippets_summary)

                    # Add the prompt to the file data
                    node["prompt"] = file_prompt

                    # Generate file summary
                    file_summary = generate_summary_with_mistral(file_prompt)
                    node["summary"] = file_summary

                    return file_summary
                else:
                    # Handle files with no snippets (like binary files or simple text)
                    node["summary"] = f"File with no code content or binary file."
                    return node["summary"]

            # For directories
            elif node["type"] == "directory" and "content" in node:
                # First summarize all contained items
                item_summaries = []

                for key, value in node["content"].items():
                    if isinstance(value, dict):
                        item_summary = summarize_node(value, f"{path}/{key}")
                        if item_summary:
                            item_type = "Directory" if value.get("type") == "directory" else "File"
                            item_summaries.append(f"{key} ({item_type}): {item_summary}")

                # If there are summaries, generate a directory summary
                if item_summaries:
                    all_items_summary = "\n".join(item_summaries)
                    dir_prompt = DIRECTORY_PROMPT.format(summaries=all_items_summary)

                    # Add the prompt to the directory data
                    node["prompt"] = dir_prompt

                    # Generate directory summary
                    dir_summary = generate_summary_with_mistral(dir_prompt)
                    node["summary"] = dir_summary

                    return dir_summary
                else:
                    node["summary"] = "Empty directory or directory with no summarizable content."
                    return node["summary"]

        return ""

    # Start the summarization process from the root
    summarize_node(summarized_project_code)

    return summarized_project_code

# Example usage:
# summarized_project_code = create_summarized_project_code(chunked_project_code)


