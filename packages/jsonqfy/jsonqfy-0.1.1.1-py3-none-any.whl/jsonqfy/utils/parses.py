from bs4 import BeautifulSoup, NavigableString
import pandoc

# pandoc.configure(auto=True)
# pandoc.configure(read=True)

def html_to_dict(tag, path=[], path_counts={}):
    """
    Função recursiva para converter uma estrutura HTML em uma lista de dicionários.

    Args:
    - tag (Tag): Tag do BeautifulSoup a ser processada.
    - path (list): Lista mantendo o caminho atual até a tag.
    - path_counts (dict): Um dicionário para rastrear a contagem de ocorrências de um caminho específico.

    Returns:
    list: Estrutura HTML convertida em lista de dicionários.
    """
    tag_name = tag.name
    if tag_name == "[document]":
        tag_name = "document"

    # Se já encontramos essa tag antes neste caminho, atualizamos seu nome.
    if path_counts.get("/".join(path + [tag_name])):
        path_counts["/".join(path + [tag_name])] += 1
        tag_name = f"{tag_name}[{path_counts['/'.join(path + [tag_name])]}]"
    else:
        path_counts["/".join(path + [tag_name])] = 1

    # Atualizamos o caminho.
    path.append(tag_name)

    results = []

    # Chamada recursiva para todas as subtags.
    for child in tag.children:
        if isinstance(child, NavigableString) and child.strip():
            results.append({'path': '/'.join(path), 'value': child.strip()})
        elif not isinstance(child, NavigableString):
            results.extend(html_to_dict(child, path.copy(), path_counts))

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

    # global result
    result = []
    path_counts = {}

    def update_path_counts(current_path):
        if current_path in path_counts:
            path_counts[current_path] += 1
            current_path += f"[{path_counts[current_path]}]"
        else:
            path_counts[current_path] = 1
        return current_path

    def process_block(block, current_path, Text = None):
        nonlocal result


        # Header
        if isinstance(block, pandoc.types.Header):
            current_path = f"{current_path}/H{block[0]}"
            current_path = update_path_counts(current_path)
            result.append({
                "text": pandoc.write(block[2]),
                "meta": block[1],
                "path": current_path
            })

       # Para
        elif isinstance(block, pandoc.types.Para):
            current_path = f"{current_path}/P"
            current_path = update_path_counts(current_path)
            result.append({
                "text": pandoc.write(block),
                "path": current_path
            })

        # Plain
        elif isinstance(block, pandoc.types.Plain):
            current_path = f"{current_path}/Plain"
            current_path = update_path_counts(current_path)
            result.append({
                "text": pandoc.write(block),
                "path": current_path
            })

       # OrderedList
        elif isinstance(block, pandoc.types.OrderedList):
            current_path = f"{current_path}/OrderedList"
            for idx, item in enumerate(block[1]):
                item_path = f"{current_path}/Item[{idx+1}]"
                for subblock in item:
                    process_block(subblock, item_path)

        # BulletList
        elif isinstance(block, pandoc.types.BulletList):
            current_path = f"{current_path}/BulletList"
            for idx, item in enumerate(block):
                item_path = f"{current_path}/Item[{idx+1}]"

                for subblock in item:
                    for subsubblock in subblock:
                        process_block(subsubblock, item_path)


       # LineBlock
        elif isinstance(block, pandoc.types.LineBlock):
            current_path = f"{current_path}/LineBlock"
            current_path = update_path_counts(current_path)
            for line in block:
                result.append({
                    "text": pandoc.write(line),
                    "path": current_path
                })

        # RawBlock
        elif isinstance(block, pandoc.types.RawBlock):
            current_path = f"{current_path}/RawBlock"
            current_path = update_path_counts(current_path)
            result.append({
                "text": block[1],
                "Format": block[0],
                "path": current_path
            })


        # CodeBlock
        elif isinstance(block, pandoc.types.CodeBlock):
            current_path = f"{current_path}/CodeBlock"
            current_path = update_path_counts(current_path)
            result.append({
                "text": block[1],
                "path": current_path
            })

        # BlockQuote
        elif isinstance(block, pandoc.types.BlockQuote):
            current_path = f"{current_path}/BlockQuote"
            for subblock in block:
                process_block(subblock, current_path)

        # DefinitionList
        elif isinstance(block, pandoc.types.DefinitionList):
            current_path = f"{current_path}/DefinitionList"
            for term, definitions in block:
                term_path = f"{current_path}/Term-{pandoc.write(term)}"
                for idx, definition in enumerate(definitions):
                    def_path = f"{term_path}/Definition[{idx+1}]"
                    for subblock in definition:
                        process_block(subblock, def_path)

        # HorizontalRule
        elif isinstance(block, pandoc.types.HorizontalRule):
            current_path = f"{current_path}/HorizontalRule"
            result.append({"path": current_path,
                           "type": "HorizontalRule",
                           "text": "---------\n"})

        # Table
        elif isinstance(block, pandoc.types.Table):
            current_path = f"{current_path}/Table"
            current_path = update_path_counts(current_path)
            # Aqui você pode adicionar processamento adicional para os elementos específicos da tabela,
            # como legendas, cabeçalho, corpo, etc.
            result.append({"path": current_path, "Caption": pandoc.write(block[1])})

        # Figure
        elif isinstance(block, pandoc.types.Image):
            current_path = f"{current_path}/Figure"
            current_path = update_path_counts(current_path)
            for subblock in block[2]:
                process_block(subblock, current_path)

        # Div
        elif isinstance(block, pandoc.types.Div):
            current_path = f"{current_path}/Div"
            current_path = update_path_counts(current_path)
            for subblock in block[1]:
                process_block(subblock, current_path)

    current_path = "Document"
    for block in doc:
        process_block(block, current_path)

    return result



# # Use como antes, assumindo que 'doc' seja um documento pandoc.
# dict_pandoc = pandoc_to_dict(doc[1])
# dict_pandoc




from bs4 import BeautifulSoup, Tag

def dict_to_html(data):
    """
    Convert a list of dictionaries (from html_to_dict) back into an HTML string.

    Args:
    - data (list): List of dictionaries containing path and value keys.

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

        # Assign the value (text) to the innermost tag
        current.string = item['value']

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
