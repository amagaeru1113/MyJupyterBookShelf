# Markdown Files

<!-- Whether you write your book's content in Jupyter Notebooks (`.ipynb`) or
in regular markdown files (`.md`), you'll write in the same flavor of markdown
called **MyST Markdown**. -->

本の内容をJupyter Notebooks (.ipynb)で書く場合でも、通常のmarkdownファイル(.md)で書く場合でも、
**MyST Markdown**と呼ばれる同じフレーバーのmarkdownで書くことになります。



## What is MyST?

<!-- MyST stands for "Markedly Structured Text". It
is a slight variation on a flavor of markdown called "CommonMark" markdown,
with small syntax extensions to allow you to write **roles** and **directives**
in the Sphinx ecosystem. -->

MySTは "Markedly Structured Text "の略です。
これは、"CommonMark" markdownと呼ばれるマークダウンのフレーバーのわずかなバリエーションで、
Sphinxのエコシステムでロールとディレクティブを書くことができるように、小さな構文拡張をしています。



## What are roles and directives?

<!-- Roles and directives are two of the most powerful tools in Jupyter Book. They
are kind of like functions, but written in a markup language. They both
serve a similar purpose, but **roles are written in one line**, whereas
**directives span many lines**. They both accept different kinds of inputs,
and what they do with those inputs depends on the specific role or directive
that is being called. -->

ロールとディレクティブは Jupyter Book の中で最も強力なツールです。
これらは関数のようなものですが、マークアップ言語で書かれています。
どちらも同じような目的を果たしますが、ロールは一行で書かれているのに対し、ディレクティブは何行にもわたって書かれています。
どちらも異なる種類の入力を受け付け、それらの入力で何をするかは呼び出される特定のロールやディレクティブに依存します。



### Using a directive

<!-- At its simplest, you can insert a directive into your book's content like so: -->

もっとも単純に言えば、このように本の内容にディレクティブを挿入することができます:

````
```{mydirectivename}
My directive content
```
````

<!-- This will only work if a directive with name `mydirectivename` already exists
(which it doesn't). There are many pre-defined directives associated with
Jupyter Book. For example, to insert a note box into your content, you can
use the following directive: -->

これは `mydirectivename` という名前のディレクティブが既に存在する場合にのみ動作します (存在しない場合は動作しない)。Jupyter Book には多くの定義済みディレクティブがあります。例えば、コンテンツにノートボックスを挿入するには、次のようなディレクティブを使うことができます。

````
```{note}
Here is a note
```
````

結果として、貴方の本の上では次のようになります。

This results in:

```{note}
Here is a note
```

より詳細な情報については[MyST documentation](https://myst-parser.readthedocs.io/)を参照してください。


### Using a role

<!-- Roles are very similar to directives, but they are less-complex and written
entirely on one line. You can insert a role into your book's content with
this pattern: -->

ロールはディレクティブと非常に似ていますが、より複雑ではなく、すべて1行で書かれています。このパターンでは、ロールをブックの内容に挿入することができます:

```
Some content {rolename}`and here is my role's content!`
```

<!-- Again, roles will only work if `rolename` is a valid role's name. For example,
the `doc` role can be used to refer to another page in your book. You can
refer directly to another page by its relative path. For example, the
role syntax `` {doc}`intro` `` will result in: {doc}`intro`. -->

繰り返しになりますが、ロールはrolenameが有効なロール名である場合にのみ機能します。例えば、docロールは、あなたの本の別のページを参照するために使用することができます。別のページを相対パスで直接参照することができます。例えば、{doc}`intro`というロール構文は次のようになります: Welcome to Iron Ball Run.

より詳細な情報については[MyST documentation](https://myst-parser.readthedocs.io/)を参照してください。

### Adding a citation

<!-- You can also cite references that are stored in a `bibtex` file. For example,
the following syntax: `` {cite}`holdgraf_evidence_2014` `` will render like
this: {cite}`holdgraf_evidence_2014`.

Moreoever, you can insert a bibliography into your page with this syntax:
The `{bibliography}` directive must be used for all the `{cite}` roles to
render properly.
For example, if the references for your book are stored in `references.bib`,
then the bibliography is inserted with: -->

また、`bibtex` ファイルに保存されている参照を引用することもできます。例えば、次のような構文です。<br>
`` {cite}`holdgraf_evidence_2014` `` はこのようにレンダリングされます:{cite}`holdgraf_evidence_2014`.

また、この構文でページに書誌を挿入することもできます。`{bibliography}` は、すべての `{cite}` ロールで正しく表示されるように使用されなければなりません。例えば、あなたの本の参照が `references.bib` に保存されている場合、書誌は次のように挿入されます。


````
```{bibliography} references.bib
```
````

結果として、次のようにレンダリングされます：
<!-- Resulting in a rendered bibliography that looks like: -->

```{bibliography} references.bib
```

### Executing code in your markdown files

<!-- If you'd like to include computational content inside these markdown files,
you can use MyST Markdown to define cells that will be executed when your
book is built. Jupyter Book uses *jupytext* to do this.

First, add Jupytext metadata to the file. For example, to add Jupytext metadata
to this markdown page, run this command: -->

これらのマークダウンファイルの中に計算コンテンツを含めたい場合、MyST Markdownを使用して、ブックがビルドされたときに実行されるセルを定義することができます。Jupyter Bookはこれを行うためにjupytextを使用します。

まず、ファイルにJupytextメタデータを追加します。例えば、このマークダウンページにJupytextメタデータを追加するには、次のコマンドを実行します：

```
jupyter-book myst init markdown.md
```

<!-- Once a markdown file has Jupytext metadata in it, you can add the following
directive to run the code at build time: -->
マークダウンファイルにJupytextのメタデータが入っていると、以下のようなディレクティブを追加してビルド時にコードを実行することができます：

````
```{code-cell}
print("Here is some code to execute")
```
````

<!-- When your book is built, the contents of any `{code-cell}` blocks will be
executed with your default Jupyter kernel, and their outputs will be displayed
in-line with the rest of your content.

For more information about executing computational content with Jupyter Book,
see [The MyST-NB documentation](https://myst-nb.readthedocs.io/). -->

ブックがビルドされると、`{code-cell}` ブロックの内容はデフォルトの Jupyter カーネルで実行され、その出力は残りの内容と並んで表示されます。

Jupyter Book で計算コンテンツを実行する方法の詳細については、[The MyST-NB documentation](https://myst-nb.readthedocs.io/)を参照してください。
