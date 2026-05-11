import reflex as rx
import bcrypt
import re


class UserStore:
    users: dict[str, dict] = {}


class AuthState(rx.State):
    """Handle all authentication logic and session management."""

    logged_in: bool = False
    current_user: str = ""
    user_id: str = ""
    username: str = ""
    email: str = ""
    password: str = ""
    confirm_password: str = ""

    @rx.event
    def logout(self):
        """Reset session and redirect to login."""
        self.logged_in = False
        self.current_user = ""
        self.user_id = ""
        return rx.redirect("/")

    def _validate_email(self, email: str) -> bool:
        return re.match("[^@]+@[^@]+\\.[^@]+", email) is not None

    @rx.event
    def handle_login(self, form_data: dict):
        """Verify credentials and start session."""
        username = form_data.get("username", "").strip()
        password = form_data.get("password", "").strip()
        if not username or not password:
            return rx.toast("Por favor, preencha todos os campos.")
        user = UserStore.users.get(username)
        if user and bcrypt.checkpw(
            password.encode("utf-8"), user["password_hash"]
        ):
            self.logged_in = True
            self.current_user = username
            self.user_id = user["user_id"]
            return rx.redirect("/app/perfil")
        else:
            return rx.toast("Usuário ou senha incorretos.")

    @rx.event
    def handle_register(self, form_data: dict):
        """Create new user with hashed password."""
        username = form_data.get("username", "").strip()
        email = form_data.get("email", "").strip()
        password = form_data.get("password", "").strip()
        confirm = form_data.get("confirm_password", "").strip()
        if not all([username, email, password, confirm]):
            return rx.toast("Todos os campos são obrigatórios.")
        if not self._validate_email(email):
            return rx.toast("E-mail inválido.")
        if len(password) < 6:
            return rx.toast("A senha deve ter pelo menos 6 caracteres.")
        if password != confirm:
            return rx.toast("As senhas não coincidem.")
        if username in UserStore.users:
            return rx.toast("Este nome de usuário já existe.")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        import uuid

        UserStore.users[username] = {
            "email": email,
            "password_hash": hashed,
            "user_id": str(uuid.uuid4()),
        }
        yield rx.toast("Conta criada com sucesso! Faça login.")
        yield rx.redirect("/")

    @rx.event
    def check_auth(self):
        """Protect routes by checking session."""
        if not self.logged_in:
            return rx.redirect("/")