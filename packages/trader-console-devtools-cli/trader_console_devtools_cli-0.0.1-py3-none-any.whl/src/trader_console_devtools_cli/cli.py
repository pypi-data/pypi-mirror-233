import fire # Alternative: [Click](click.palletsprojects.com)
from rich.console import Console

console = Console()

console.print("Hello", "World!")

class App(object):
  """A simple calculator class."""

  def double(self, number):
    return 2 * number

if __name__ == '__main__':
  fire.Fire(App)