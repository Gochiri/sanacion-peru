"""Cliente del API público de GHL (services.leadconnectorhq.com).

Se usa `curl` en vez de urllib a propósito: **Cloudflare bloquea el user-agent
de Python con un 1010 «browser_signature_banned»**. Con un UA de navegador pasa
sin problema. Es la misma razón por la que conviene no cambiar el UA a la ligera.

El API interno (workflows) sigue viviendo en esb_lib.py; esto es solo lo público:
calendarios, custom values, productos, usuarios, campos.
"""
from __future__ import annotations

import json
import os
import subprocess

BASE = "https://services.leadconnectorhq.com"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def _credenciales() -> tuple[str, str]:
    pit = os.environ.get("GHL_API_KEY", "").strip()
    loc = os.environ.get("GHL_LOCATION_ID", "").strip()
    if not pit or not loc:
        raise SystemExit("Faltan GHL_API_KEY / GHL_LOCATION_ID (source tools/ghl-cli/.env)")
    return pit, loc


def pedir(metodo: str, ruta: str, cuerpo: dict | None = None) -> tuple[int, dict]:
    """Devuelve (código http, json). Nunca lanza por un status de error."""
    pit, _ = _credenciales()
    cmd = ["curl", "-s", "-m", "40", "-X", metodo, BASE + ruta, "-A", UA,
           "-H", f"Authorization: Bearer {pit}",
           "-H", "Version: 2021-07-28",
           "-H", "Accept: application/json",
           "-H", "Content-Type: application/json",
           "-w", "\n%{http_code}"]
    if cuerpo is not None:
        cmd += ["-d", json.dumps(cuerpo)]
    salida = subprocess.run(cmd, capture_output=True, text=True).stdout
    texto, _, code = salida.rpartition("\n")
    try:
        return int(code or 0), json.loads(texto or "{}")
    except Exception:
        return int(code or 0), {"raw": texto[:400]}


def location() -> str:
    return _credenciales()[1]


# ── Custom values ────────────────────────────────────────────────────────

def custom_values() -> list[dict]:
    _, r = pedir("GET", f"/locations/{location()}/customValues")
    return r.get("customValues", [])


def por_nombre() -> dict[str, dict]:
    return {v["name"]: v for v in custom_values()}


def crear_custom_value(nombre: str, valor: str) -> tuple[int, dict]:
    return pedir("POST", f"/locations/{location()}/customValues",
                 {"name": nombre, "value": valor})


def actualizar_custom_value(cv_id: str, nombre: str, valor: str) -> tuple[int, dict]:
    return pedir("PUT", f"/locations/{location()}/customValues/{cv_id}",
                 {"name": nombre, "value": valor})


# ── Calendarios ──────────────────────────────────────────────────────────

def calendarios() -> list[dict]:
    _, r = pedir("GET", f"/calendars/?locationId={location()}")
    return r.get("calendars", [])


def horas_por_dia(dias: list[int], desde: int = 9, hasta: int = 18) -> list[dict]:
    """openHours exige **una entrada por día**: un array con varios días en
    `daysOfTheWeek` responde "must be a valid day of week"."""
    return [{"daysOfTheWeek": [d],
             "hours": [{"openHour": desde, "openMinute": 0,
                        "closeHour": hasta, "closeMinute": 0}]}
            for d in dias]
