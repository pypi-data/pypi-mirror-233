"""Tabella API function definitions."""
__all__ = ("get_app",)

import asyncio
import importlib
import json
import shutil
import sys
from pathlib import Path
from typing import Any
from urllib import parse

import caseswitcher
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jsonrpcobjects.objects import (
    ErrorResponse,
    Notification,
    ParamsNotification,
    ParamsRequest,
    Request as RPCRequest,
    ResultResponse,
)
from openrpc import (
    OAuth2,
    OpenRPC,
    ParamStructure,
    RPCServer,
    Schema,
    SchemaType,
    Server,
)
from openrpcclientgenerator import generate, Language
from starlette.responses import FileResponse, JSONResponse, Response

# noinspection PyProtectedMember
from starlette.templating import _TemplateResponse
from starlette.websockets import WebSocket, WebSocketDisconnect

from tabella import _util as util
from tabella._cache import TabellaCache
from tabella._templating_engine import TemplatingEngine
from tabella._util import Middleware, OAuthChallengeHandler, RequestProcessor

try:
    httpx = importlib.import_module("httpx")
except ImportError:
    httpx = None  # type: ignore

RequestType = ParamsRequest | RPCRequest | ParamsNotification | Notification

root = Path(__file__).parent

app = FastAPI(docs_url="/swagger")
app.mount("/static", StaticFiles(directory=root / "static"), name="static")
templates = Jinja2Templates(
    directory=root / "templates", lstrip_blocks=True, trim_blocks=True
)

cache = TabellaCache.get_instance()
base_context: dict[str, Any] = {
    "len": len,
    "str": str,
    "id": lambda x: f"_{x}",
    "array_item_id": lambda x: f"_item{x}",
    "is_any": util.is_any,
    "is_str": lambda x: isinstance(x, str),
    "is_": lambda x, y: x is y,
    "ParamStructure": ParamStructure,
    "key_schema": Schema(type="string"),
    "httpx_missing": httpx is None,
}


def get_app(
    rpc: RPCServer | None,
    middleware: Middleware | None = None,
    oauth_challenge_handler: OAuthChallengeHandler | None = None,
    client_gen_directory: Path | None = None,
    favicon_url: str | None = None,
    icon_url: str | None = None,
) -> FastAPI:
    """Host the Given RPCServer.

    :param rpc: RPC server to host.
    :param middleware: Function to get RPCServer `depends` and
        `security` values from request headers.
    :param oauth_challenge_handler: Class to handle creating and getting
        OAuth verifiers from code challenges.
    :param client_gen_directory: Directory to write generated client
        files to.
    :param favicon_url: URL to favicon to use for docs site.
    :param icon_url: URL to icon to use in docs site.
    """
    if not rpc:
        return app

    async_middleware = util.get_middleware(middleware)

    # Determine request processor method.
    if async_middleware is None:
        # Ignore and noqa because signatures must be identical.
        # noinspection PyUnusedLocal
        async def _request_processor(
            request: str, headers: dict  # noqa: ARG001
        ) -> str | None:
            return await rpc.process_request_async(request) or ""

    else:

        async def _request_processor(request: str, headers: dict) -> str | None:
            return (
                await rpc.process_request_async(
                    request, *await async_middleware(headers)
                )
                or ""
            )

    servers = _get_servers(rpc)
    for server in servers:
        parsed_url = parse.urlparse(server.url)
        if parsed_url.scheme.startswith("http"):
            _add_ws_api_url(parsed_url.path, _request_processor)
        elif parsed_url.scheme.startswith("ws"):
            _add_http_api_url(parsed_url.path, _request_processor)

    api_path = servers[0].url
    cache.set_request_processor(_request_processor, api_path)
    if client_gen_directory:
        cache.client_gen_directory = client_gen_directory
    if favicon_url:
        base_context["favicon_url"] = favicon_url
    if icon_url:
        base_context["icon_url"] = icon_url
    if oauth_challenge_handler:
        cache.oauth_handler = oauth_challenge_handler
    if len(servers) > 1:
        cache.servers = servers
    return app


def _get_servers(rpc: RPCServer) -> list[Server]:
    servers = []
    if not isinstance(rpc.servers, Server):
        servers = rpc.servers
    else:
        parsed_url = parse.urlparse(rpc.servers.url)
        if not (not parsed_url.scheme and parsed_url.path == "localhost"):
            servers = [rpc.servers]
        else:
            port = "8000"
            for arg in sys.argv:
                if arg == "--port":
                    port = sys.argv[sys.argv.index(arg) + 1]
                    break
            servers.append(Server(name="HTTP API", url=f"http://localhost:{port}/api"))
            servers.append(
                Server(name="WebSocket API", url=f"ws://localhost:{port}/api")
            )
    return servers


def _add_ws_api_url(api_path: str, request_processor: RequestProcessor) -> None:
    @app.websocket(api_path)
    async def ws_process_rpc(websocket: WebSocket) -> None:
        """Process RPC requests through websocket."""
        try:
            await websocket.accept()

            async def _process_rpc(request: str) -> None:
                rpc_response = await request_processor(request, {**websocket.headers})
                if rpc_response is not None:
                    await websocket.send_text(rpc_response)

            while True:
                data = await websocket.receive_text()
                asyncio.create_task(_process_rpc(data))
        except WebSocketDisconnect:
            pass


def _add_http_api_url(api_path: str, request_processor: RequestProcessor) -> None:
    @app.post(api_path, response_model=ErrorResponse | ResultResponse | None)
    async def http_process_rpc(request: Request, rpc_request: RequestType) -> Response:
        """Process RPC request through HTTP server."""
        rpc_response = await request_processor(
            rpc_request.model_dump_json(), {**request.headers}
        )
        return Response(content=rpc_response, media_type="application/json")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> _TemplateResponse:
    """Get interactive docs site."""
    scheme = None
    enabled_scopes = []
    client_id = None

    # If state is provided this is redirect from OAuth server.
    state = request.query_params.get("state")
    if not state:
        te = await cache.get_templating_engine()
    else:
        code = request.query_params.get("code")
        hash_, scheme, scopes, client_id, api_url = state.split("@")
        enabled_scopes = scopes.split(" ")
        if not (verifier := cache.oauth_handler.get_verifier(hash_)):
            return _error(request, "Server Error", "OAuth 2.0 verifier is missing.")

        te = await cache.get_templating_engine(api_url)
        # This shouldn't happen but needed for type safety.
        if te.rpc.components is None:
            return _error(
                request,
                "Server Error",
                "This server does not have an OAuth 2.0. security scheme",
            )

        schemes = te.rpc.components.x_security_schemes or {}
        for i, name in enumerate(schemes):
            if i != int(scheme):
                continue
            security_scheme = schemes[name]
            if not isinstance(security_scheme, OAuth2):
                continue
            token_url = security_scheme.flows[0].token_url
            client = httpx.AsyncClient()
            result = await client.post(
                f"{token_url}?code={code}&code_verifier={verifier}&grant_type=token"
            )
            te.headers = {"Authorization": f"Bearer {result.json()['access_token']}"}
            break

    context = {
        "request": request,
        "disable_api_input": cache.api_url is not None,
        "api_url": te.api_url,
        "te": te,
        "examples": util.get_examples(te.rpc.methods),
        "servers": cache.servers,
        "code_challenge": cache.oauth_handler.create_verifier(),
        "enabled_scheme": scheme,
        "enabled_scopes": enabled_scopes,
        "client_id": client_id,
    }
    return templates.TemplateResponse("index.html", {**context, **base_context})


@app.get("/docs/discover-{trigger}", response_class=HTMLResponse)
async def discover(request: Request) -> _TemplateResponse:
    """Get OpenRPC docs."""
    api_url = request.query_params.get("api-url")
    trigger = request.path_params["trigger"]
    te = await cache.get_templating_engine(api_url, refresh=trigger == "click")

    context = {
        "request": request,
        "te": te,
        "examples": util.get_examples(te.rpc.methods),
        "code_challenge": cache.oauth_handler.create_verifier(),
    }
    return templates.TemplateResponse("openrpc_docs.html", {**context, **base_context})


@app.get("/docs/try-it-modal/{method_idx}", response_class=HTMLResponse)
async def try_it(request: Request) -> _TemplateResponse:
    """Get "Try it out" modal for a method."""
    api_url = request.query_params.get("api-url")
    method_idx = request.path_params["method_idx"]
    te = await cache.get_templating_engine(api_url)
    method = te.get_method(int(method_idx))
    context = {
        "request": request,
        "method": method,
        "method_id": method_idx,
        "get_any_default": util.get_any_default,
    }
    return templates.TemplateResponse("modals/try_it.html", {**context, **base_context})


@app.get(
    "/docs/add-{item_type}-item/{method_id}/{param_id}/{input_id}/{is_even}",
    response_class=HTMLResponse,
)
async def add_item(request: Request) -> _TemplateResponse:
    """Get "Try it out" modal for a method."""
    api_url = request.query_params.get("api-url")
    item_count = request.query_params.get("item-count")
    method_id = request.path_params["method_id"]
    param_id = int(request.path_params["param_id"])
    input_id = request.path_params["input_id"]
    item_type = request.path_params["item_type"]
    is_even = int(request.path_params["is_even"])
    te = await cache.get_templating_engine(api_url)
    method = te.get_method(int(method_id))

    # Get schema for this param.
    schema: SchemaType = Schema()
    for i, param in enumerate(method.params):
        if i == param_id:
            schema = param.schema_
            break

    # We already got param schema from method, remove those ids.
    input_tree_path = input_id.removeprefix(f"{method_id}_{param_id}")
    # Get input ids to get proper schema in schema tree.
    input_ids = [id_.removeprefix("item") for id_ in input_tree_path.split("_") if id_]
    schema = util.get_schema_from_input_ids(schema, map(int, input_ids))

    if item_type == "array" and not isinstance(schema, bool) and schema.items:
        schema = schema.items
    if item_type != "recursive":
        input_id = f"{input_id}_item{item_count}"

    context = {
        "request": request,
        "method_id": method_id,
        "param_id": str(param_id),
        "schema": schema,
        "input_id": input_id,
        "minimalize": True,
        "required": True,
        "get_any_default": util.get_any_default,
        "is_even": 0 if is_even else 1,
    }
    if item_type == "object":
        return templates.TemplateResponse(
            "schema_form/object.html", {**context, **base_context}
        )
    return templates.TemplateResponse(
        "schema_form/form.html", {**context, **base_context}
    )


# FIXME: Re-add response model when Pydantic is fixed.
@app.get("/openrpc.json")
async def openrpc_doc(request: Request) -> JSONResponse:
    """Get raw OpenRPC JSON document."""
    api_url = request.query_params.get("api-url")
    te = await cache.get_templating_engine(api_url)
    return JSONResponse(content=await _discover(te))


@app.post("/rpc-api")
async def api_pass_through(request: Request) -> Response:
    """Pass RPC requests to RPC server and get response."""
    api_url = request.query_params.get("api-url")
    te = await cache.get_templating_engine(api_url)

    # Set request headers based on security scheme.
    components = te.rpc.components
    scheme_is_set = False
    if components and components.x_security_schemes:
        for i, name in enumerate(components.x_security_schemes):
            if value := request.headers.get(f"scheme{i}"):
                scheme_is_set = True
                scheme = components.x_security_schemes[name]
                if scheme.type == "bearer":
                    te.headers = {scheme.name: f"Bearer {value}"}
                elif scheme.type == "apikey":
                    te.headers = {scheme.name: value}
                break
    # If no scheme is set clear any existing headers.
    if not scheme_is_set:
        te.headers = {}

    response = await te.process_request(await request.json())
    return Response(content=response, media_type="application/json")


@app.get("/download-client")
async def download_client(request: Request) -> FileResponse:
    """Download a generated client for this API."""
    # Get RPC data and target language.
    api_url = request.query_params["api-url"]
    language = request.query_params["language"]
    te = await cache.get_templating_engine(api_url)
    rpc = OpenRPC(**await _discover(te))
    lang_option = Language.PYTHON if language == "Python" else Language.TYPESCRIPT

    # Make generated out directories if they don't exist.
    out = cache.client_gen_directory or root.joinpath("static/out")
    out.mkdir(exist_ok=True)
    lang_out = out.joinpath(language.lower())
    lang_out.mkdir(exist_ok=True)
    transport = "http" if api_url.startswith("http") else "ws"
    client_name = caseswitcher.to_kebab(rpc.info.title) + f"-{transport}-client"
    client_dir = lang_out.joinpath(client_name)
    filename = f"{client_name}-{rpc.info.version}-{lang_option.value}.zip"
    zip_file = lang_out.joinpath(filename)

    # If client doesn't exist, generate and zip it.
    if not zip_file.exists():
        generate(rpc, lang_option, api_url, out)
        shutil.make_archive(zip_file.as_posix().removesuffix(".zip"), "zip", client_dir)

    # Serve the client zipfile.
    return FileResponse(zip_file, headers={"Content-Disposition": filename})


async def _discover(te: TemplatingEngine) -> dict[str, Any]:
    discover_request = {"id": 1, "method": "rpc.discover", "jsonrpc": "2.0"}
    response = await te.process_request(discover_request)
    return json.loads(response)["result"]


def _error(request: Request, error_title: str, error_message: str) -> _TemplateResponse:
    context = {
        "request": request,
        "error_title": error_title,
        "error_message": error_message,
    }
    return templates.TemplateResponse("error.html", context)
