import reflex as rx
import bcrypt
import re
from sqlalchemy import text
import uuid
import os
import logging


class AuthState(rx.State):
    """Handle all authentication logic and session management."""

    logged_in: bool = False
    is_admin: bool = False
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
        self.username = ""
        self.email = ""
        self.is_admin = False
        return rx.redirect("/")

    @rx.event
    def init_google_oauth(self):
        """Build the OAuth URL and redirect to Google."""
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        if not client_id:
            return rx.toast(
                "Login com Google não está configurado neste ambiente."
            )

        import urllib.parse

        # Use current page URL to build absolute callback URL
        host = getattr(self.router.page, "host", "localhost:3000")

        if "build.reflexsandbox.com" in host:
            redirect_uri = "https://8080-331b29ba-aebd-41c3-8bbc-0531b291adc1.build.reflexsandbox.com"
        else:
            protocol = "https" if "build.reflexsandbox.com" in host else "http"
            redirect_uri = f"{protocol}://{host}"

        state_val = str(uuid.uuid4())

        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "select_account",
            "state": state_val,
        }

        query = urllib.parse.urlencode(params)
        auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{query}"

        return rx.redirect(auth_url, is_external=True)

    @rx.event
    async def handle_google_callback(self):
        """Process Google callback query parameters."""
        query_params = self.router.page.params
        error = query_params.get("error")
        code = query_params.get("code")

        if not error and not code:
            return

        if error:
            yield rx.toast("Autenticação cancelada ou falhou.")
            yield rx.redirect("/")
            return

        if not code:
            yield rx.toast("Código de autorização não encontrado.")
            yield rx.redirect("/")
            return

        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

        if not client_id or not client_secret:
            yield rx.toast(
                "Credenciais do Google não configuradas no servidor."
            )
            yield rx.redirect("/")
            return

        host = getattr(self.router.page, "host", "localhost:3000")
        path = getattr(self.router.page, "path", "/")

        if "build.reflexsandbox.com" in host:
            if path == "/auth/google/callback":
                redirect_uri = "https://8080-331b29ba-aebd-41c3-8bbc-0531b291adc1.build.reflexsandbox.com/auth/google/callback"
            else:
                redirect_uri = "https://8080-331b29ba-aebd-41c3-8bbc-0531b291adc1.build.reflexsandbox.com"
        else:
            protocol = "https" if "build.reflexsandbox.com" in host else "http"
            if path == "/auth/google/callback":
                redirect_uri = f"{protocol}://{host}/auth/google/callback"
            else:
                redirect_uri = f"{protocol}://{host}"

        import httpx

        try:
            token_resp = httpx.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code",
                },
                timeout=15,
            )
            if token_resp.status_code != 200:
                yield rx.toast("Falha ao validar código de autorização.")
                yield rx.redirect("/")
                return

            tokens = token_resp.json()
            access_token = tokens.get("access_token")

            userinfo_resp = httpx.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=15,
            )
            if userinfo_resp.status_code != 200:
                yield rx.toast("Falha ao recuperar dados do perfil.")
                yield rx.redirect("/")
                return

            user_info = userinfo_resp.json()
            email = user_info.get("email", "")
            verified_email = user_info.get("verified_email", False)
            name = user_info.get("name", "Google User")

            if not email or not verified_email:
                yield rx.toast(
                    "E-mail não fornecido ou não verificado pelo Google."
                )
                yield rx.redirect("/")
                return

            import uuid
            import bcrypt
            from sqlalchemy import text

            async with rx.asession() as session:
                result = await session.execute(
                    text(
                        "SELECT id, username, is_admin FROM users WHERE email = :email LIMIT 1"
                    ),
                    {"email": email},
                )
                user = result.first()

                if user:
                    self.logged_in = True
                    self.user_id = user[0]
                    self.current_user = user[1]
                    self.username = user[1]
                    self.email = email
                    self.is_admin = bool(user[2]) if user[2] else False
                    yield rx.redirect("/app/perfil")
                else:
                    uid = str(uuid.uuid4())
                    random_pass = str(uuid.uuid4())
                    salt = bcrypt.gensalt()
                    hashed = bcrypt.hashpw(
                        random_pass.encode("utf-8"), salt
                    ).decode("utf-8")

                    base_username = email.split("@")[0]
                    username = base_username
                    u_res = await session.execute(
                        text(
                            "SELECT id FROM users WHERE username = :u LIMIT 1"
                        ),
                        {"u": username},
                    )
                    if u_res.first():
                        username = f"{base_username}_{str(uuid.uuid4())[:6]}"

                    await session.execute(
                        text(
                            "INSERT INTO users (id, username, email, password_hash, is_admin) VALUES (:id, :username, :email, :hash, 0)"
                        ),
                        {
                            "id": uid,
                            "username": username,
                            "email": email,
                            "hash": hashed,
                        },
                    )
                    await session.execute(
                        text(
                            "INSERT INTO profiles (user_id, nome, email, dias_semana, horas_dia, km_dia) VALUES (:id, :nome, :email, 6, 8, 150.0)"
                        ),
                        {"id": uid, "nome": name, "email": email},
                    )
                    await session.commit()

                    self.logged_in = True
                    self.user_id = uid
                    self.current_user = username
                    self.username = username
                    self.email = email
                    self.is_admin = False
                    yield rx.redirect("/app/perfil")

        except Exception as e:
            import logging

            logging.exception(f"Google auth error: {e}")
            yield rx.toast("Erro ao autenticar com o Google.")
            yield rx.redirect("/")

    def _validate_email(self, email: str) -> bool:
        return re.match("[^@]+@[^@]+\\.[^@]+", email) is not None

    @rx.event
    async def handle_login(self, form_data: dict):
        """Verify credentials and start session."""
        username = form_data.get("username", "").strip()
        password = form_data.get("password", "").strip()
        if not username or not password:
            return rx.toast("Por favor, preencha todos os campos.")
        try:
            async with rx.asession() as session:
                result = await session.execute(
                    text(
                        "SELECT id, password_hash, is_admin FROM users WHERE username = :username"
                    ),
                    {"username": username},
                )
                user = result.first()
                if user and bcrypt.checkpw(
                    password.encode("utf-8"), user[1].encode("utf-8")
                ):
                    self.logged_in = True
                    self.current_user = username
                    self.user_id = user[0]
                    self.is_admin = bool(user[2]) if user[2] else False
                    return rx.redirect("/app/perfil")
                else:
                    return rx.toast("Usuário ou senha incorretos.")
        except Exception as e:
            import logging

            logging.exception(f"Login error: {e}")
            return rx.toast("Erro ao conectar com o servidor. Tente novamente.")

    @rx.event
    async def handle_register(self, form_data: dict):
        """Create new user with hashed password."""
        username = form_data.get("username", "").strip()
        email = form_data.get("email", "").strip()
        password = form_data.get("password", "").strip()
        confirm = form_data.get("confirm_password", "").strip()
        if not all([username, email, password, confirm]):
            yield rx.toast("Todos os campos são obrigatórios.")
            return
        if not self._validate_email(email):
            yield rx.toast("E-mail inválido.")
            return
        if len(password) < 6:
            yield rx.toast("A senha deve ter pelo menos 6 caracteres.")
            return
        if password != confirm:
            yield rx.toast("As senhas não coincidem.")
            return
        try:
            async with rx.asession() as session:
                result = await session.execute(
                    text("SELECT id FROM users WHERE username = :username"),
                    {"username": username},
                )
                if result.first():
                    yield rx.toast("Este nome de usuário já existe.")
                    return
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(password.encode("utf-8"), salt).decode(
                    "utf-8"
                )
                uid = str(uuid.uuid4())
                await session.execute(
                    text(
                        "INSERT INTO users (id, username, email, password_hash) VALUES (:id, :username, :email, :hash)"
                    ),
                    {
                        "id": uid,
                        "username": username,
                        "email": email,
                        "hash": hashed,
                    },
                )
                await session.execute(
                    text(
                        "INSERT INTO profiles (user_id, nome, email, dias_semana, horas_dia, km_dia) VALUES (:id, :nome, :email, 6, 8, 150.0)"
                    ),
                    {"id": uid, "nome": username, "email": email},
                )
                await session.commit()
            yield rx.toast("Conta criada com sucesso! Faça login.")
            yield rx.redirect("/")
        except Exception as e:
            import logging

            logging.exception(f"Registration error: {e}")
            yield rx.toast("Erro ao criar conta. Tente novamente.")

    @rx.event
    def check_auth(self):
        """Protect routes by checking session."""
        if not self.logged_in:
            return rx.redirect("/")

    @rx.event
    def check_admin(self):
        """Protect admin routes."""
        if not self.logged_in or not self.is_admin:
            return rx.redirect("/app/perfil")