import sys,json,glob,os
from termcolor import colored

class Options:
    @staticmethod
    def generate_patterns_all(app_namespace):
        return [
            f'{app_namespace}/views/*.py', f'{app_namespace}/views/**/*.py',f'{app_namespace}/views.py',
            f'{app_namespace}/serializers/*.py', f'{app_namespace}/serializers/**/*.py',
            f'{app_namespace}/forms/*.py', f'{app_namespace}/forms/**/*.py',
            f'{app_namespace}/services/*.py', f'{app_namespace}/services/**/*.py',
            f'{app_namespace}/models/*.py', f'{app_namespace}/models/**/*.py',f'{app_namespace}/models.py',
            f'{app_namespace}/templatetags/*.py', f'{app_namespace}/templatetags/**/*.py',
            f'{app_namespace}/context_processors/*.py', f'{app_namespace}/context_processors/**/*.py',f'{app_namespace}/context_processors.py',
            f'{app_namespace}/templates/{app_namespace}/*.html',f'{app_namespace}/templates/{app_namespace}/**/*.html',
            f'static/css/base/*.css',f'static/css/base/**/*.css'
        ]
    
    @staticmethod
    def generate_patterns_html(app_namespace):
        return [
            f'{app_namespace}/views/*.py', f'{app_namespace}/views/**/*.py',f'{app_namespace}/views.py',
            f'{app_namespace}/forms/*.py', f'{app_namespace}/forms/**/*.py',
            f'{app_namespace}/templatetags/*.py', f'{app_namespace}/templatetags/**/*.py',
            f'{app_namespace}/context_processors/*.py', f'{app_namespace}/context_processors/**/*.py',
            f'{app_namespace}/templates/{app_namespace}/*.html',f'{app_namespace}/templates/{app_namespace}/**/*.html',
            f'static/css/base/*.css',f'static/css/base/**/*.css'
        ]

    @staticmethod
    def generate_patterns_views(app_namespace):
        return [f'{app_namespace}/views/*.py',f'{app_namespace}/views/**/*.py',f'{app_namespace}/views.py'
                f'{app_namespace}/**/*.html',f'static/css/base/*.css',f'static/css/base/**/*.css']
    
    @staticmethod
    def generate_patterns_base(app_namespace):
        return [
            f'{app_namespace}/**/*.py', f'{app_namespace}/**/*.html'
               ]
    @staticmethod
    def generate_patterns_root():
        return [f'./*.py',f'./*.sh',f'./*.js',f'./*.toml',f'./README.md',]            

    patterns = {
        'django-all': {
            'include': generate_patterns_all('baseapp') + generate_patterns_all('alignity') + ['base/*.py'],
            'exclude': ['**/__init__.py']
        },
        'django-html': {
            'include': generate_patterns_html('baseapp') + generate_patterns_html('alignity') + ['base/settings.py'],
            'exclude': ['**/__init__.py']
        },
        'django-views': {
            'include': generate_patterns_views('baseapp') + generate_patterns_views('alignity') + ['base/settings.py'],
            'exclude': ['**/__init__.py']
        },
        'django-base': {
            'include': generate_patterns_base('base') + generate_patterns_base('baseapp'),
            'exclude': ['**/__init__.py']
        },
        'django-root': {
            'include': generate_patterns_root(),
            'exclude': ['**/__init__.py','**/llm-collector.py']
        }
    }
def count_tokens_and_size(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        tokens = len(content.split())
        size_bytes = os.path.getsize(file_path)
        size_mb = size_bytes / (1024 * 1024)
        return tokens, size_mb
    except Exception as e:
        print(colored(f"Error reading {file_path}: {e}", "red"))
        return 0, 0

def collect_files(include_patterns, exclude_patterns):
    collected_files = []
    total_size_mb = 0
    for pattern in include_patterns:
        for file_path in glob.glob(pattern, recursive=True):
            if not any(glob.fnmatch.fnmatch(file_path, ex) for ex in exclude_patterns):
                tokens, size_mb = count_tokens_and_size(file_path)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                file_info = {
                    'file_path': file_path,
                    'tokens': tokens,
                    'size_mb': size_mb,
                    'directory': os.path.dirname(file_path),
                    'extension': os.path.splitext(file_path)[1],
                    'content': content  # Include the file content
                }
                collected_files.append(file_info)
                total_size_mb += size_mb
                print(colored(f'Collecting file: {file_path} - Tokens: {tokens} - Size: {size_mb:.2f} MB', 'green'))
    return collected_files, total_size_mb

def get_next_sequenced_filename(output_dir, base_filename, extension=""):
    os.makedirs(output_dir, exist_ok=True)
    sequence = 0
    existing_files = glob.glob(os.path.join(output_dir, f"{base_filename}_*{extension}"))
    for existing_file in existing_files:
        parts = os.path.basename(existing_file).replace(base_filename + '_', '').replace(extension, '')
        try:
            num = int(parts)
            if num > sequence:
                sequence = num
        except ValueError:
            # If conversion to int fails, it means it's not a properly sequenced file, so we ignore it
            pass
    return os.path.join(output_dir, f"{base_filename}_{sequence + 1}{extension}")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in Options.patterns:
        print(colored('Usage: python3 script.py [option]', 'yellow'))
        print(colored('Available options:', 'yellow'), colored(', '.join(Options.patterns.keys()), 'cyan'))
        sys.exit(1)

    option = sys.argv[1]
    print(colored(f'Using pattern group: {option}', 'green'))

    include_patterns = Options.patterns[option]['include']
    exclude_patterns = Options.patterns[option]['exclude']

    # Collect files and count tokens and size
    files_info, total_size_mb = collect_files(include_patterns, exclude_patterns)

    output_dir = "results"
    base_filename = "collected_contents"
    jsonl_output_file = get_next_sequenced_filename(output_dir, base_filename, ".jsonl")
    stats_output_file = get_next_sequenced_filename(output_dir, "result", ".stats")

    # Write the files to the sequenced output file and stats
    total_tokens = 0
    with open(jsonl_output_file, 'w', encoding='utf-8') as jsonlfile, open(stats_output_file, 'w', encoding='utf-8') as statsfile:
        file_count = 0
        for file_info in files_info:
            total_tokens += file_info['tokens']
            file_count += 1
            # Write each file's JSON object to a single line in the .jsonl file
            jsonlfile.write(json.dumps(file_info) + '\n')
            # Write file stats
            statsfile.write(f"{file_info['file_path']}: {file_info['tokens']} tokens, {file_info['size_mb']:.2f} MB\n")

        statsfile.write(f"Total files: {file_count}\n")
        statsfile.write(f"Total tokens: {total_tokens}\n")
        statsfile.write(f"Total size: {total_size_mb:.2f} MB\n")

    print(colored(f'All file information has been collected into {jsonl_output_file}', 'green'))
    print(colored(f'Token counts and file stats have been saved to {stats_output_file}', 'green'))
    print(colored(f'Total files: {file_count}', 'green'))
    print(colored(f'Total size: {total_size_mb:.2f} MB', 'green'))
    print(colored(f'Total tokens: {total_tokens}', 'green'))

if __name__ == "__main__":
    main()