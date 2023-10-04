from bs4 import BeautifulSoup, NavigableString
import pandoc

# pandoc.configure(auto=True)
# pandoc.configure(read=True)


def html_to_dict(tag, current_path=None, path_occurrences=None):
    """
    Recursively convert an HTML structure into a list of dictionaries.

    This function traverses the HTML tags and generates a dictionary entry for each unique path and value.
    
    Args:
    - tag (Tag): The BeautifulSoup tag to be processed.
    - current_path (list, optional): List maintaining the current path to the tag.
                                    Defaults to an empty list.
    - path_occurrences (dict, optional): A dictionary tracking the count of occurrences of a specific path.
                                        Defaults to an empty dictionary.

    Returns:
    list: The HTML structure converted into a list of dictionaries.
    """

    # If the arguments are None, initialize them
    if current_path is None:
        current_path = []
    if path_occurrences is None:
        path_occurrences = {}

    tag_name = tag.name
    if tag_name == "[document]":
        tag_name = "document"

    # Check if we've encountered this tag before in the current path and update its name if we have.
    path_str = "/".join(current_path + [tag_name])
    tag_count = path_occurrences.get(path_str, 0)
    
    if tag_count:
        tag_count += 1
        tag_name = f"{tag_name}[{tag_count}]"
    else:
        tag_count = 1
    
    path_occurrences[path_str] = tag_count

    # Update the current path
    current_path.append(tag_name)

    results = []

    # Recursively process all child tags
    for child in tag.children:
        if isinstance(child, NavigableString) and child.strip():
            results.append({'path': '/'.join(current_path), 'value': child.strip()})
        elif not isinstance(child, NavigableString):
            results.extend(html_to_dict(child, current_path.copy(), path_occurrences))

    return results


# Exemplo de uso

# html_doc = """
# <h1 id="titulo-1">Titulo 1</h1>
# <h1 id="titulo-2">Titulo 2</h1>
# <h2 id="subtitulo">Subtitulo</h2>
# <h3 id="subtitulo-1">Subtitulo</h3>
# <ol start="3" type="1">
# <li>Amortização ou liquidação de saldo devedor</li>
# </ol>
# <p>É possível amortizar (abater) parte do saldo devedor ou liquidar toda
# a dívida.</p>
# <p><span class="math inline"><em>x</em><sup>2</sup></span></p>
# <pre class="importante!"><code>Não é possível usar o FGTS para amortizar ou quitar o consórcio
# cujo crédito tenha sido utilizado para aquisição de imóvel.</code></pre>
# <ul>
# <li>Teste
# <ul>
# <li>Teste 1</li>
# <li>Teste 2</li>
# <li>Teste 3 Alguma coisa aqui</li>
# </ul>
# </li>
# </ul>
# """

# dict_html = html_to_dict(html)
# dict_html


def pandoc_to_dict(doc):
    """
    Convert a pandoc document structure into a list of dictionaries.

    This function traverses the pandoc document and generates a dictionary entry
    for each unique path and value.
    
    Args:
    - doc (list): The pandoc document to be processed.

    Returns:
    list: The pandoc document structure converted into a list of dictionaries.
    """

    results = []
    path_occurrences = {}

    def update_path_occurrences(current_path):
        """Update and return the path with its occurrence count."""
        if current_path in path_occurrences:
            path_occurrences[current_path] += 1
            current_path += f"[{path_occurrences[current_path]}]"
        else:
            path_occurrences[current_path] = 1
        return current_path

    def process_block(block, current_path):
        """Recursively process a pandoc block."""
        nonlocal results

        # Define behavior for each block type
        # This structure allows for easy expansion and modification
        # for different pandoc block types.
        # Define behavior for each block type
        block_type_handlers = {
            pandoc.types.Header: handle_header,
            pandoc.types.Para: handle_para,
            pandoc.types.Plain: handle_plain,
            pandoc.types.OrderedList: handle_ordered_list,
            pandoc.types.BulletList: handle_bullet_list,
            pandoc.types.LineBlock: handle_line_block,
            pandoc.types.RawBlock: handle_raw_block,
            pandoc.types.CodeBlock: handle_code_block,
            pandoc.types.BlockQuote: handle_block_quote,
            pandoc.types.DefinitionList: handle_definition_list,
            pandoc.types.HorizontalRule: handle_horizontal_rule,
            pandoc.types.Table: handle_table,
            pandoc.types.Image: handle_image,
            pandoc.types.Div: handle_div
        }


        # Get the handler for the block type and call it
        # print(type(block))
        handler = block_type_handlers.get(type(block))
        if handler:
            handler(block, current_path)
        else:
            # Handle default or unknown block types here, if necessary
            pass

    def handle_header(block, current_path):
        """Handle the Header block type."""
        current_path = f"{current_path}/H{block[0]}"
        current_path = update_path_occurrences(current_path)
        results.append({
            "path": current_path,
            "text": pandoc.write(block[2]),
            "meta": block[1]
        })

    def handle_para(block, current_path):
        """Handle the Para block type."""
        current_path = f"{current_path}/P"
        current_path = update_path_occurrences(current_path)
        results.append({
            "path": current_path,
            "text": pandoc.write(block)
        })

    def handle_plain(block, current_path):
        current_path = f"{current_path}/Plain"
        current_path = update_path_occurrences(current_path)
        results.append({
            "path": current_path,
            "text": pandoc.write(block)
        })

    def handle_ordered_list(block, current_path):
        current_path = f"{current_path}/OrderedList"
        for idx, item in enumerate(block[1]):
            item_path = f"{current_path}/Item[{idx+1}]"
            for subblock in item:
                process_block(subblock, item_path)

    def handle_bullet_list(block, current_path):
        current_path = f"{current_path}/BulletList"
        for idx, item in enumerate(block):
            item_path = f"{current_path}/Item[{idx+1}]"
            for subblock in item:
                for subsubblock in subblock:
                    process_block(subsubblock, item_path)

    def handle_line_block(block, current_path):
        current_path = f"{current_path}/LineBlock"
        current_path = update_path_occurrences(current_path)
        for line in block:
            results.append({
                "path": current_path,
                "text": pandoc.write(line)
            })

    def handle_raw_block(block, current_path):
        current_path = f"{current_path}/RawBlock"
        current_path = update_path_occurrences(current_path)
        results.append({
            "path": current_path,
            "text": block[1],
            "Format": block[0]
        })

    def handle_code_block(block, current_path):
        current_path = f"{current_path}/CodeBlock"
        current_path = update_path_occurrences(current_path)
        results.append({
            "path": current_path,
            "text": block[1]
        })

    def handle_block_quote(block, current_path):
        current_path = f"{current_path}/BlockQuote"
        for subblock in block:
            process_block(subblock, current_path)

    def handle_definition_list(block, current_path):
        current_path = f"{current_path}/DefinitionList"
        for term, definitions in block:
            term_path = f"{current_path}/Term-{pandoc.write(term)}"
            for idx, definition in enumerate(definitions):
                def_path = f"{term_path}/Definition[{idx+1}]"
                for subblock in definition:
                    process_block(subblock, def_path)

    def handle_horizontal_rule(block, current_path):
        current_path = f"{current_path}/HorizontalRule"
        results.append({
            "path": current_path,
            "type": "HorizontalRule",
            "text": "---------\n"
        })

    def handle_table(block, current_path):
        current_path = f"{current_path}/Table"
        current_path = update_path_occurrences(current_path)
        # Here you can add additional processing for specific table elements,
        # such as captions, headers, body, etc.
        results.append({
            "path": current_path,
            "Caption": pandoc.write(block[1])
        })

    def handle_image(block, current_path):
        current_path = f"{current_path}/Image"
        current_path = update_path_occurrences(current_path)
        for subblock in block[2]:
            process_block(subblock, current_path)

    def handle_div(block, current_path):
        current_path = f"{current_path}/Div"
        current_path = update_path_occurrences(current_path)
        for subblock in block[1]:
            process_block(subblock, current_path)

    # Start processing from the root "Document" path
    current_path = "Document"
    for block in doc:
        process_block(block, current_path)

    return results



# # Use como antes, assumindo que 'doc' seja um documento pandoc.
# dict_pandoc = pandoc_to_dict(doc[1])
# dict_pandoc




from bs4 import BeautifulSoup, Tag

def dict_to_html(data):
    """
    Convert a list of dictionaries (from html_to_dict) back into an HTML string.

    Args:
    - data (list): List of dictionaries containing path and content keys.

    Returns:
    str: Reconstructed HTML string.
    """

    root = BeautifulSoup('', 'html.parser')

    for item in data:
        # Split the path into individual tags and their indices (if present)
        parts = item['path'].split('/')
        current = root
        for part in parts:
            # Split part into tag and index (if present)
            tag_name, *index = part.split('[')
            if index:
                index = int(index[0].rstrip(']'))
            else:
                index = None

            # Try to get the tag by its name and (optional) index
            found = None
            for idx, child in enumerate(current.children):
                if isinstance(child, Tag) and child.name == tag_name:
                    if index is None or idx == index - 1:
                        found = child
                        break

            # If not found, create the tag
            if not found:
                new_tag = root.new_tag(tag_name)
                current.append(new_tag)
                current = new_tag
            else:
                current = found

        # Assign the content (text) to the innermost tag
        current.string = item['content']

    return str(root)


# Exemplo de uso
# data = [
#     {'path': 'html/head/title', 'value': 'My title'},
#         {'path': 'document/ul/li[1]', 'value': 'Item 1'},
#         {'path': 'document/ul/li[1]/ul/li', 'value': 'Subitem 1.1'},
#         {'path': 'document/ul/li[2]', 'value': 'Item 2'}]

# html_trns = dict_to_html(dict_html[0:13])

# # print(BeautifulSoup(html_trns, 'html.parser').prettify())

# pandoc_parse_html = pandoc.read(html_trns, format = "html")

# print(pandoc.write(pandoc_parse_html, format="markdown"))
