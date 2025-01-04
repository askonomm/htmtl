# HTMTL

HTMTL (HyperText Markup _Templating_ Language) is a templating language that uses HTML attributes for its rendering logic. 
It is both a subset and superset of HTML, meaning that valid HTML is also valid HTMTL and valid HTMTL is also valid HTML, allowing 
you to use any editor without needing any additional editor extensions.

## Features

- **Interpolation**: You can interpolate data from a data dictionary into your templates.
- **Modifiers**: You can modify the interpolated values using modifiers.
- **Conditionals**: You can show or hide blocks using expressions.
- **Partials**: You can include other templates inside your templates.
- **Loops**: You can loop over iterable data.
- **Extendable**: You can implement custom parsers and modifiers.

## Example syntax

```html
<!DOCTYPE html>
<html>
<head>
    <title inner-text="{title}"></title>
</head>
<body>
    <h1 inner-text="{title}"></h1>
    
    <div class="posts" when="posts">
        <div foreach="posts as post">
            <h2 class="post-title">
                <a :href="/blog/{post.url}" inner-text="{post.title | Capitalize}"></a>
            </h2>
            <div class="post-date" inner-text="{post.date | Date('yyyy-MM-dd')}"></div>
            <div class="post-content" inner-html="{post.body}"></div>
        </div>
    </div>
</body>
</html>
```

## Installation

```
pip install htmtl
```

## Usage

A simple example of how to use HTMTL with default configuration looks like this:

```python
from htmtl import Htmtl

htmtl = Htmtl('<p inner-text="Hello {who}"></p>', {'who': 'World'})
html = htmtl.html() # returns: <p>Hello World</p>
```

## Attributes

HTMTL works by parsing attributes in the template. 

### `inner-text`

Sets the inner text of the element to the value of the attribute.

HTMTL template where `title` key is `Hello, World!`:

```html
<h1 inner-text="{title}"></h1>
```

Results in:

```html
<h1>Hello, World!</h1>
```

### `inner-html`

Sets the inner HTML of the element to the value of the attribute.

HTMTL template where `content` key is `<p>Hello, World!</p>`:

```html
<div inner-html="{content}"></div>
```

Results in:

```html
<div>
    <p>Hello, World!</p>
</div>
```

### `inner-partial`

Sets the inner HTML of the element to the value of the parsed HTMTL template. Inherits all the same data 
as the parent template. 

HTMTL template with data such as:

```python
data = {
    'title': 'My Web Portal Thing',
    'header': '<div class="header"><h1 inner-text="title"></h1></div>'
}
```

And where the template is:

```html
<div inner-partial="header"></div>
```

Results in:

```html
<div>
    <div class="header">
        <h1>My Web Portal Thing</h1>
    </div>
</div>
```

### `outer-text`

Sets the outer text of the element to the value of the attribute.

HTMTL template where `title` key is `Hello, World!`:

```html
<h1 outer-text="{title}"></h1>
```

Results in:

```html
Hello, World!
```

### `outer-html`

Sets the outer HTML of the element to the value of the attribute.

HTMTL template where `content` key is `<p>Hello, World!</p>`:

```html
<div outer-html="{content}"></div>
```

Results in:

```html
<p>Hello, World!</p>
```

### `outer-partial`

Sets the outer HTML of the element to the value of the parsed Toretto template. Inherits all the same data
as the parent template.

HTMTL template with data such as:

```python
data = {
    'title': 'My Web Portal Thing',
    'header': '<div class="header"><h1 inner-text="title"></h1></div>'
}
```

And where the template is:

```html
<div outer-partial="header"></div>
```

Results in:

```html
<div class="header">
    <h1>My Web Portal Thing</h1>
</div>
```

### `when`

Removes the element if the attribute is false-y.

HTMTL template where `show` key is `False`:

```html
<div when="show">Hello, World!</div>
```

Results in:

```html
<!-- Empty -->
```

### `when-not`

Removes the element if the attribute is truthy.

HTMTL template where `hide` key is `True`:

```html
<div when-not="hide">Hello, World!</div>
```

Results in:

```html
<!-- Empty -->
```

### `foreach`

Loops anything iterable. 

For example, to loop over a collection of `posts` and then use `post` as the variable of each iteration, you can do something 
like this:

```php
<div foreach="posts as post">
    <h2 inner-text="post.title"></h2>
</div>
```

If you do not care about using any of the iteration data, you can also entirely omit `as ...` from the expression, 
like so:

```php
<div foreach="posts">
    ...
</div>
```

And, you can also assign the key of the iteration to a variable, like so:

```php
<div foreach="posts as index:post">
    <h2 :class="post-{post.index}" inner-text="post.title"></h2>
</div>
```

This would add the key of the iteration to as `post.index` variable, but you can name it whatever you want.

### `:*` (Generic Value Attributes)

You can use the `:*` attribute to set any attribute on an element to the interpolated value of the generic value attribute.

For example, to set the `href` attribute of an element, you can use the `:href` attribute:

```html
<a :href="/blog/{slug}">Hello, World!</a>
```

Results in:

```html
<a href="/blog/hello-world">Hello, World!</a>
```

If the `slug` key is `hello-world`.

## Modifiers

All interpolated expressions can be modified using modifiers. Modifiers are applied to the value of the attribute, and they can be chained, like so:

```html
<h1 inner-text="{title | Uppercase | Reverse}"></h1>
```

Note that if you have nothing other than the interpolated variable in the attribute, then you can omit the curly brackets, and so this would also work:

```html
<h1 inner-text="title | Uppercase | Reverse"></h1>
```

Modifiers can also take arguments which are passed within
parentheses `(` and `)`, and can be either `int`, `float`, `str` or `bool`. For example:

```html
<h1 inner-text="some_var | SomeModifier(123, 'asd', true)"></h1>
```

### `Date`

Parses the value into a formatted date string.

```html
<p inner-text="published_at | Date('YYYY-mm-dd')"></p>
```

### `Truncate`

Truncates the value to the specified length.

```html
<p inner-text="{title | Truncate(10)}"></p>
```

This also works on collections, so you can use `truncate` to limit items in an array as well.

## Extending

### Parsers

You can add (or replace) parsers in HTMTL when creating a new instance of the `Htmtl` class, like so:

```python
from htmtl import Htmtl
from htmtl.parsers import InnerText

htmtl = Htmtl('<p inner-text="Hello {who}"></p>', {'who': 'World'})
htmtl.set_parsers([
    InnerText,
])

html = htmtl.html() # returns: <p>Hello World</p>
```

Prsers must extend the `Parser` class, like so:

```python
from typing import Optional
from dompa.nodes import Node, TextNode
from htmtl import Parser


class InnerText(Parser):
    def traverse(self, node: Node) -> Optional[Node]:
        if "inner-text" in node.attributes:
            node.children = [TextNode(value=self.expression(node.attributes["inner-text"]))]
            node.attributes.pop("inner-text")

        return node
```

All parsers traverse the entire DOM tree to do whatever DOM manipulation they want. It's important to know that
a parser must have the `traverse` method, and it must return a `Node`, or `None` if you want to remove the `Node`.

HTMTL is built upon the [Dompa](https://github.com/askonomm/dompa) HTML parser, so check that out for more granular info on things.

#### List of built-in parsers

- `htmtl.parsers.GenericValue` - Parser the `:*` attributes.
- `htmtl.parsers.When` - Parser the `when` attributes.
- `htmtl.parsers.WhenNot` - Parser the `when-not` attributes.
- `htmtl.parsers.InnerPartial` - Parser the `inner-partial` attributes.
- `htmtl.parsers.InnerHtml` - Parser the `inner-html` attributes.
- `htmtl.parsers.InnerText` - Parser the `inner-text` attributes.
- `htmtl.parsers.OuterPartial` - Parser the `outer-partial` attributes.
- `htmtl.parsers.OuterHtml` - Parser the `outer-html` attributes.
- `htmtl.parsers.OuterText` - Parser the `outer-text` attributes.
- `htmtl.parsers.Foreach` - Parses the `foreach` attributes. (**soon**)

### Modifiers

You can add (or replace) modifiers in HTMTL when creating a new instance of the `Htmtl` class, like so:

```python
from htmtl import Htmtl
from htmtl.modifiers import Truncate

htmtl = Htmtl('<p inner-text="Hello {who}"></p>', {'who': 'World'})
htmtl.set_modifiers([
    Truncate,
])

html = htmtl.html() # returns: <p>Hello World</p>
```

Mdifiers must extend the `Modifier` class, like so:

```python
from typing import Any
from htmtl import Modifier


class Truncate(Modifier):
    def modify(self, value: Any, opts: list[Any]) -> Any:
        if isinstance(value, str) and len(opts) > 0:
            if all([x in "1234567890" for x in opts[0]]):
                char_limit = int(opts[0])

                if len(value) > char_limit:
                    return f"{value[:char_limit - 3]}..."

        return value
```

#### List of built-in modifiers

- `htmtl.modifiers.Truncate` - Truncates the value (both strings and collections).
