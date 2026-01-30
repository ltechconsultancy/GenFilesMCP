Generates a Word document for reports or academic papers, including headers, paragraphs, lists, tables, images, equations, and bold/italic text formatting.

The arguments `document_cover`, `columns_body`, `document_body_elements` and `file_name` are mandatory and have to be valid dictionaries. If any of these are missing or are not valid dictionaries, the function will raise a `ValueError`. 

# Arguments

- **file_name**: str - The desired name of the Word file (without extension).

- **document_cover**: A Cover object containing:
  - title: str - The main title of the document.
  - subtitle: str - The subtitle.
  - description: str - A brief description.
  - author: str - The author's name.
  - month: str - The month (e.g., "January").
  - year: str - The year (e.g., "2023").
  - page_break: bool - Whether to add a page break after the cover (default: false). 

- **columns_body**: int - Number of columns for the body sections (1 or 2). 1 is for general reports, 2 is for papers following academic formats.

- **document_body_elements**: A list of document elements, the order of elements defines their sequence in the document. Supported elements include:

  - **ParagraphHeader**: Use this element to create a heading.
    - paragraph_title: str - The heading text.
    - level: int (1-6) - The heading level (1 for main title, 2 for section, etc.).

  - **ParagraphBody**: Use this element to create a paragraph of text.
    - paragraph_text: str - The paragraph text. Use '\n\n' for paragraph breaks.
    - **Never user markdown formatting only plain text**.
    - **Never use bold or italic formatting in this element, use WordsWithBoldOrItalic instead**.

  - **WordsWithBoldOrItalic**: Use this element to add words or phrases with bold or italic formatting within a paragraph.
    - **Never user markdown formatting only plain text**.
    - bold_italic_text: str - The text content.
    - bold: bool - Whether the text is bold.
    - italic: bool - Whether the text is italic.

  - **ListItem**: Use this element to create a list (bulleted or numbered).
    - list_style: str - "List Number" for numbered list or "List Bullet" for bulleted list.
    - items: List[str] - The list of item texts.

  - **Table**: Use this element to create a table.
    - headers: List[str] - The table headers.
    - rows: List[List[str]] - The table rows, each as a list of cell values.
    - caption: Optional[str] - An optional caption for the table.

  - **Image**: Use this element to insert an image.
    - id: str - The image file ID (preloaded by the server).
    - caption: Optional[str] - An optional caption for the image.

  - **Equation**: Use this element to insert a mathematical equation. 
    - latex: str - The LaTeX code for the equation.
    - caption: Optional[str] - An optional caption for the equation.

Never use markdown syntax for bold or italic text formatting, use the respective keys to set bold or italic text. Never include equations in paragraphs, use the respective keys to set equations. Never list items in paragraphs, use the respective keys to set list items.