import os
import re

ext_dict = {
  'cpp': 'C++',
  'py': 'Python',
  'c': 'C',
  'java': 'Java',
  'js': 'JavaScript',
}

def on_page_markdown(markdown, page, **kwargs):
  '''
  {{ codes }}
    : 
  {{ codes name }}
  '''
  pattern = re.compile(r"\{\{[ \t]*codes.*\}\}")
  matched = re.findall(pattern, markdown)

  if not matched:
    return markdown

  for m in matched:
    target = None
    signature = m.split()

    if len(signature) != 3:
      target = signature[2]

    result = ''
    dir_path = os.path.dirname(f'{page.file.src_dir}/{page.file.src_uri}')

    if 'md' in page.file.src_uri:
      list_dir = os.listdir(dir_path)
      list_dir = sort_list(list_dir)

      for item in list_dir:
        name, extension = item.split('.')
        if os.path.isdir(os.path.join(dir_path, item)):
          continue

        if target == name or target is None:
          result += f'''=== "{ext_dict[extension]}"

    ``` {extension}
    --8<-- "{item}"
    ```

'''
    markdown = markdown.replace(m, result)

  return markdown

def sort_list(file_list):
  result = []
  for k, v in ext_dict.items():
    for file in file_list:
      if file.endswith(k):
        result.append(file)

  return result