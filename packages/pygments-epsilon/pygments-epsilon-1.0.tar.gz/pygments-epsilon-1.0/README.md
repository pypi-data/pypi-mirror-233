# Epsilon Plugin for Pygments 
[Pygments](https://pygments.org/) lexer support for Epsilon languages (ready to use with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/))

## Installation

```
git clone https://github.com/iNafey/pygments-epsilon.git
cd pygments-epsilon
sudo python setup.py install 
```
Could also replace the last line for (``sudo python setup.py develop``) if you will make changes to the code.

If you want to install it from PyPI:

```
pip install pygments-epsilon
```

## Usage

To use the Epsilon lexers, you need to have Pygments installed (so you can use the ``pygmentize`` command). Then, you can perform syntax highlighting using the following command:

```
 pygmentize -l <LexerAlias> -x <RelativePathToFile>
```

Where ``LexerAlias`` is the alias of the lexer you want to use (e.g. ``emf`` for Emfatic) and ``RelativePathToFile`` is the relative path to the file you want to highlight.

For example, if you want to highlight the file ``test.egl`` using the EGL lexer, you would use:

```
 pygmentize -l etl -x test_scripts/test.etl
```

### MkDocs Material Support

If you want to use the lexers with MkDocs Material, simply call the ``LexerAlias`` in the code blocks of your Markdown files. For example, if you want to highlight an ETL code block using the ETL lexer, you would use:

```
    ``` etl
        //MT definition containing rules
    ```
```

## Color Customization

You can select from various pygments [styles](https://pygments.org/styles/) already available for highlighting within the terminal:

```
 pygmentize -O <StyleName>  -l <LexerAlias> -x <RelativePathToFile>
```
    
Where ``StyleName`` is the name of the style you want to use (e.g. ``monokai``). The default style is ``default``.

To change the style for MkDocs Material, you will need to find the token types of the keywords you want to highlight (Inspect Element via your browser). Then, follow the instructions [here](https://squidfunk.github.io/mkdocs-material/reference/code-blocks/#custom-syntax-theme) to add the custom style to your documentation site.


## Available Epsilon lexers

* ETL: ``etl``
* EOL: ``eol``
* Emfatic: ``emf``