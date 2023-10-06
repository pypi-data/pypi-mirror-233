"""
click test
"""
import click


ticket_choices = ['high', 'medium', 'low']


@click.group()
def cli():
    pass

@click.command()
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def greet(name):
    """Greet NAME"""
    click.echo(f'Hello {name}!')


@click.command()
@click.option("--priority", type=click.Choice(ticket_choices), default='low')
@click.option("--todofile", prompt="Enter filename",type=click.Path(exists=True), required=1)
@click.option("-n",'--name', prompt='Enter todo name',help='Todo name.')
@click.option("-d",'--description', prompt='Todo description',help='Todo description.')
def add_todo(name, description, priority, todofile):
    """Add a todo to the todo list"""
    filename = todofile if todofile is not None else 'todo.txt'
    with open(filename, 'a+') as f:
        f.write(f'{name}: {description}, priority: {priority}\n')
    click.echo(f'Added todo {name}')


@click.command()
@click.argument("todofile", type=click.Path(exists=True), required=0)
def list_todos(todofile):
    filename = todofile if todofile is not None else 'todo.txt'
    """List all todos"""
    with open(filename, 'r') as f:
        todo_list = f.readlines()
        for todo in todo_list:
            print(todo)


cli.add_command(greet, name='greet')
cli.add_command(add_todo, name='add')
cli.add_command(list_todos, name='list')

if __name__ == '__main__':
    cli()