from typer_shell import make_typer_shell

app = make_typer_shell(
    prompt="meu-app> ",
    intro="Bem-vindo ao modo interativo!"
)