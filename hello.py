import os
import click
from flask_migrate import Migrate
from dotenv import load_dotenv
from app import create_app, db
from app.models import User, Role

# Configuração do ambiente
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print(".env is missing.")

# Criação da aplicação a partir da factory function
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    """Configuração de contexto do shell."""
    return dict(db=db, User=User, Role=Role)

@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Executa testes unitários."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == "__main__":
    app.run(debug=True)
