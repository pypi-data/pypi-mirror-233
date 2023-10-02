import os

from dotserve.logger import logger

# Default dotserve.md file created if none exists
DEFAULT_MARKDOWN_STR = """# Welcome to Dotserve! 🚀🤖

Hi there, Developer! 👋 We're excited to have you on board. Dotserve is a powerful tool designed to help you prototype, debug and share applications built on top of LLMs.

## Useful Links 🔗

- **Documentation:** Get started with our comprehensive [Dotserve Documentation](https://docs.dotagent.dev/serve) 📚
- **Discord Community:** Join our friendly [Dotserve Discord](https://discord.gg/k73SQ3FyUh) to ask questions, share your projects, and connect with other developers! 💬

We can't wait to see what you create with Dotserve! Happy coding! 💻😊

## Welcome screen

To modify the welcome screen, edit the `dotserve.md` file at the root of your project. If you do not want a welcome screen, just leave this file empty.
"""


def init_markdown(root: str):
    """Initialize the dotserve.md file if it doesn't exist."""
    dotserve_md_file = os.path.join(root, "dotserve.md")

    if not os.path.exists(dotserve_md_file):
        with open(dotserve_md_file, "w", encoding="utf-8") as f:
            f.write(DEFAULT_MARKDOWN_STR)
            logger.info(f"Created default dotserve markdown file at {dotserve_md_file}")


def get_markdown_str(root: str):
    """Get the dotserve.md file as a string."""
    dotserve_md_path = os.path.join(root, "dotserve.md")
    if os.path.exists(dotserve_md_path):
        with open(dotserve_md_path, "r", encoding="utf-8") as f:
            dotserve_md = f.read()
            return dotserve_md
    else:
        return None
