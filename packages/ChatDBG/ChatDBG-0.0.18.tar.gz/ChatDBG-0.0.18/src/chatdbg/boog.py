import textwrap

def word_wrap_except_code_blocks(text: str) -> str:
    """
    Wraps text except for code blocks.

    Splits the text into paragraphs and wraps each paragraph,
    except for paragraphs that are inside of code blocks denoted
    by ` ``` `. Returns the updated text.

    Args:
        text: The text to wrap.

    Returns:
        The wrapped text.
    """
    # Split text into paragraphs
    paragraphs = text.split("\n\n")
    wrapped_paragraphs = []
    # Check if currently in a code block.
    in_code_block = False
    # Loop through each paragraph and apply appropriate wrapping.
    for paragraph in paragraphs:
        # Check for the presence of triple quotes in the paragraph
        if "```" in paragraph:
            # Split paragraph by triple quotes
            parts = paragraph.split("```")
            for i, part in enumerate(parts):
                # If we are inside a code block, do not wrap the text
                if in_code_block:
                    wrapped_paragraphs.append(part)
                else:
                    # Otherwise, apply text wrapping to the part
                    wrapped_paragraphs.append(textwrap.fill(part))
                # Toggle the in_code_block flag for each triple quote encountered
                if i < len(parts) - 1:
                    wrapped_paragraphs.append("```")
                    in_code_block = not in_code_block
        else:
            # If the paragraph does not contain triple quotes and is not inside a code block, wrap the text
            if not in_code_block:
                wrapped_paragraphs.append(textwrap.fill(paragraph))
            else:
                wrapped_paragraphs.append(paragraph)
    # Join all paragraphs into a single string
    wrapped_text = "\n\n".join(wrapped_paragraphs)
    return wrapped_text

# Example usage:
input_text = '''The root cause of this error is that the variable `x` is initialized
to 1.0, and then iteratively multiplied by `i` in the `for` loop in
the `fact` function. However, the loop starts from `i = 0.0`, which
means that `x` will always be multiplied by 0 in the first iteration,
resulting in `x` being 0.0. The subsequent `assert` statement checks
if `x` is not equal to 0.0, which will always fail.

To fix this error, we need to initialize `x` to 1.0 instead of 0.0.
This can be done by changing the initialization of `i` in the `for`
loop to start from 1.0 instead of 0.0.

Fixed source code: ``` /* frame 0 */ /* frame 1 */ /* frame 2 */ /*
frame 3 */ /* frame 4 */ #include <assert.h> #include <iostream>

float fact(float n) {   auto x = 1.0;   for (auto i = 1.0; i < n; i++)
{     x *= i;   }   assert(x != 0.0);   ^-----------------------------
------------------------------------------------ /* frame 5 */   for
(auto i = 1.0; i < n; i++) {     x *= i;   }   assert(x != 0.0);
return x; }


int main()
{
  std::cout << fact(100) << std::endl;
  ^-----------------------------------------------------------------------------
      ```

With this fix, `x` will correctly accumulate the product of `i`
values, starting from 1 instead of 0, and the `assert` statement will
not fail.'''

print(word_wrap_except_code_blocks(input_text))
