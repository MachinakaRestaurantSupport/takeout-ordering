# ruff: noqa: E501
"""HTML UI router for takeout-ordering."""

from html import escape
from typing import Any

import httpx
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from takeout_ordering.clients import MenuClient, OrderClient
from takeout_ordering.store import TakeoutStore

PORTAL_LINKS = [
    ("portal", "ポータル", "/ui/portal"),
    ("product", "商品管理", "/ui/products"),
    ("menu", "メニュー", "/ui/menus"),
    ("guest", "座席・顧客", "/ui/tables"),
    ("order", "注文かんばん", "/ui/orders/kanban"),
    ("accounting", "会計", "/ui/accounting/checkout"),
    ("sales", "売上", "/ui/sales/daily"),
    ("dine_in", "店内QR", "/ui/dine-in/session"),
    ("takeout", "持ち帰り", "/ui/takeout/login"),
]

PROVIDER_BADGES = {
    "google": ("Google", "#ea4335"),
    "facebook": ("Facebook", "#1877f2"),
    "line": ("LINE", "#06c755"),
}


def _safe_takeout_menus(menu_client: MenuClient) -> list[dict[str, Any]]:
    try:
        res = menu_client.get_takeout_menus()
    except (httpx.HTTPError, TypeError, ValueError):
        return []
    if isinstance(res, list):
        return res
    if isinstance(res, dict) and isinstance(res.get("items"), list):
        return [{"title": "持ち帰りメニュー", "categories": [{"name": "弁当", "items": res["items"]}]}]
    return []


def _safe_takeout_orders(order_client: OrderClient) -> list[dict[str, Any]]:
    try:
        res = order_client.list_orders()
        if isinstance(res, list):
            return [o for o in res if o.get("source") == "takeout"]
        return []
    except (httpx.HTTPError, TypeError, ValueError):
        return []


def _render_shell(*, title: str, subtitle: str, active_subtab: str, body_html: str) -> str:
    nav_html = "".join(
        f'<a class="nav-pill{" active" if key == "takeout" else ""}" href="{href}">{escape(label)}</a>'
        for key, label, href in PORTAL_LINKS
    )
    subtabs = [
        ("login", "1. SNS認証ログイン", "/ui/takeout/login"),
        ("reserve", "2. メニュー・受取時刻予約", "/ui/takeout/reserve"),
        ("status", "3. 注文状況・受取通知", "/ui/takeout/status"),
    ]
    subtab_html = "".join(
        f'<a class="subtab{" active" if key == active_subtab else ""}" href="{href}">{escape(label)}</a>'
        for key, label, href in subtabs
    )
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)} | まちなか飲食店サポート</title>
  <style>
    :root {{ --bg:#f8fafc; --surface:#fff; --navy:#0f172a; --slate:#334155; --muted:#64748b; --border:#e2e8f0; --accent:#ea580c; --accent-soft:#fff7ed; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:var(--bg); color:var(--navy); line-height:1.5; font-family:"Noto Sans CJK JP","Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif; }}
    .topbar {{ background:var(--navy); color:#fff; padding:0 24px; height:54px; display:flex; align-items:center; justify-content:space-between; gap:16px; }}
    .brand {{ display:flex; align-items:center; gap:10px; font-weight:700; font-size:15px; white-space:nowrap; }}
    .brand-badge {{ background:var(--accent); color:#fff; padding:2px 8px; border-radius:6px; font-size:11px; }}
    .nav-links {{ display:flex; gap:4px; overflow-x:auto; }}
    .nav-pill {{ color:#cbd5e1; text-decoration:none; font-size:12px; font-weight:600; padding:6px 10px; border-radius:6px; white-space:nowrap; }}
    .nav-pill.active {{ background:var(--accent); color:#fff; }}
    .subbar {{ background:var(--surface); border-bottom:1px solid var(--border); padding:12px 24px; display:flex; align-items:center; justify-content:space-between; gap:16px; }}
    .subbar h1 {{ margin:0; font-size:18px; }}
    .subbar .subtitle {{ margin:2px 0 0; font-size:12px; color:var(--muted); }}
    .subtabs {{ display:flex; gap:8px; }}
    .subtab {{ text-decoration:none; color:var(--slate); font-size:13px; font-weight:600; padding:7px 14px; border-radius:8px; border:1px solid var(--border); background:#fff; }}
    .subtab.active {{ background:var(--accent-soft); color:var(--accent); border-color:#fdba74; }}
    .container {{ max-width:1220px; margin:0 auto; padding:20px 24px 28px; }}
    .grid-2 {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; }}
    .card {{ background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:16px 18px; box-shadow:0 1px 2px rgba(15,23,42,.04); }}
    .sns-btn {{ display:flex; align-items:center; justify-content:center; gap:8px; width:100%; padding:11px; border-radius:10px; font-weight:700; font-size:14px; border:none; cursor:pointer; color:#fff; margin-bottom:10px; }}
    .btn {{ display:inline-block; text-decoration:none; font-size:13px; font-weight:700; padding:8px 14px; border-radius:8px; border:none; cursor:pointer; }}
    .btn-primary {{ background:var(--accent); color:#fff; }}
    .btn-secondary {{ background:#f1f5f9; color:var(--slate); border:1px solid var(--border); }}
    .badge {{ display:inline-block; padding:2px 9px; border-radius:999px; font-size:11px; font-weight:700; }}
    table {{ width:100%; border-collapse:collapse; font-size:13px; }}
    th {{ text-align:left; padding:10px 12px; background:#f8fafc; color:var(--muted); font-size:12px; border-bottom:1px solid var(--border); }}
    td {{ padding:10px 12px; border-bottom:1px solid var(--border); }}
    label {{ font-size:12px; font-weight:700; color:var(--slate); display:block; margin-bottom:4px; }}
    input, select {{ width:100%; padding:8px 10px; border:1px solid #cbd5e1; border-radius:8px; font-size:13px; font-family:inherit; }}
  </style>
</head>
<body>
  <header class="topbar">
    <div class="brand">
      <span>🍽️ まちなか飲食店サポート</span>
      <span class="brand-badge">店長・スタッフ共通ポータル</span>
    </div>
    <nav class="nav-links">{nav_html}</nav>
  </header>
  <section class="subbar">
    <div>
      <h1>{escape(title)}</h1>
      <p class="subtitle">{escape(subtitle)}</p>
    </div>
    <div class="subtabs">{subtab_html}</div>
  </section>
  <main class="container">{body_html}</main>
</body>
</html>
"""


def create_ui_router(
    store: TakeoutStore,
    menu_client: MenuClient,
    order_client: OrderClient,
) -> APIRouter:
    """Create FastAPI router providing HTML UI screens for takeout-ordering."""
    router = APIRouter(tags=["ui"])

    @router.get("/ui/takeout/login", response_class=HTMLResponse)
    def login_page() -> str:
        sessions = list(store.sessions.values())
        session_rows = "".join(
            f"<tr><td><strong>{escape(s.display_name)}</strong></td>"
            f'<td><span class="badge" style="background:{PROVIDER_BADGES.get(s.provider, (s.provider, "#475569"))[1]};color:#fff">'
            f"{escape(PROVIDER_BADGES.get(s.provider, (s.provider, ''))[0])}</span></td>"
            f"<td><code>{escape(s.customer_id)}</code></td>"
            f"<td><code>{escape(s.access_token[:12])}...</code></td></tr>"
            for s in sessions
        ) or '<tr><td colspan="4" style="text-align:center;color:#64748b">ログイン中のお客様はいません。</td></tr>'

        body = f"""
        <div class="grid-2">
          <div class="card">
            <h2 style="margin:0 0 12px;font-size:16px">店外持ち帰り予約・SNSログイン</h2>
            <p style="font-size:13px;color:#475569;margin-top:0">
              Google・Facebook・LINE のアカウントでログインして、事前注文と受取予約を行います。
            </p>
            <div style="margin-bottom:14px">
              <label>表示名（ニックネーム）</label>
              <input type="text" id="t-name" value="鈴木一郎">
            </div>
            <button class="sns-btn" style="background:#ea4335" onclick="snsLogin('google')">G Google アカウントでログイン</button>
            <button class="sns-btn" style="background:#1877f2" onclick="snsLogin('facebook')">f Facebook でログイン</button>
            <button class="sns-btn" style="background:#06c755" onclick="snsLogin('line')">LINE でかんたんログイン</button>
          </div>
          <div class="card">
            <h2 style="margin:0 0 12px;font-size:16px">アクティブ SNS 認証セッション</h2>
            <table>
              <thead><tr><th>お名前</th><th>プロバイダ</th><th>顧客ID</th><th>トークン</th></tr></thead>
              <tbody>{session_rows}</tbody>
            </table>
            <div style="margin-top:14px;text-align:right">
              <a class="btn btn-primary" href="/ui/takeout/reserve">持ち帰り予約画面へ進む →</a>
            </div>
          </div>
        </div>
        """ + """
        <script>
          async function snsLogin(provider) {
            const res = await fetch('/auth/login', {
              method: 'POST', headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({
                provider: provider,
                oauth_token: 'oauth-' + provider + '-token',
                display_name: document.getElementById('t-name').value || 'Guest'
              })
            });
            if (res.ok) window.location.href = '/ui/takeout/reserve';
          }
        </script>
        """
        return _render_shell(
            title="持ち帰り注文 › SNS認証ログイン",
            subtitle="Google / Facebook / LINE 対応のSNS認証で店外からの事前予約注文を開始します",
            active_subtab="login",
            body_html=body,
        )

    @router.get("/ui/takeout/reserve", response_class=HTMLResponse)
    def reserve_page() -> str:
        menus = _safe_takeout_menus(menu_client)
        sessions = list(store.sessions.values())
        customer_id = sessions[-1].customer_id if sessions else "cust-google-demo"
        customer_name = sessions[-1].display_name if sessions else "ゲスト"

        menu_blocks = []
        for m in menus:
            m_title = escape(str(m.get("title", "お持ち帰り専用")))
            cat_html = ""
            for cat in m.get("categories", []):
                pids = cat.get("product_ids") or []
                items = cat.get("items") or [{"product_id": pid, "name": f"商品 #{pid}"} for pid in pids]
                items_str = "".join(
                    f'<div style="display:flex;justify-content:space-between;align-items:center;'
                    f'border:1px solid #e2e8f0;border-radius:8px;padding:10px 12px;margin-bottom:8px">'
                    f'<div><strong>{escape(str(it.get("name", it.get("product_id"))))}</strong>'
                    f'<div style="font-size:11px;color:#64748b">商品ID: {escape(str(it.get("product_id", "-")))}</div></div>'
                    f'<span class="badge" style="background:#dcfce7;color:#166534">持ち帰り対象</span></div>'
                    for it in items
                )
                cat_html += f'<div style="font-size:12px;font-weight:700;color:#ea580c;margin:8px 0 4px">{escape(str(cat.get("name", "")))}</div>{items_str}'
            menu_blocks.append(f'<h3 style="margin:4px 0 8px;font-size:15px">{m_title}</h3>{cat_html}')
        menus_html = "".join(menu_blocks) or '<p style="color:#64748b">公開中の持ち帰りメニューはありません。</p>'

        body = f"""
        <div class="grid-2">
          <div class="card">
            <h2 style="margin:0 0 12px;font-size:16px">公開中・持ち帰り専用メニュー（I-5）</h2>
            {menus_html}
          </div>
          <div class="card">
            <h2 style="margin:0 0 12px;font-size:16px">店頭受取時刻の予約・注文確定（I-2）</h2>
            <div style="background:#f8fafc;padding:10px 12px;border-radius:8px;font-size:12px;margin-bottom:12px">
              ログイン会員: <strong>{escape(customer_name)}</strong> (<code>{escape(customer_id)}</code>)
            </div>
            <div style="margin-bottom:12px">
              <label>受取希望日時（ISO 8601）</label>
              <input type="text" value="2026-11-16T19:00:00+09:00">
            </div>
            <div style="margin-bottom:12px">
              <label>受取店舗</label>
              <select><option>まちなか本店 店頭カウンター</option></select>
            </div>
            <div style="display:flex;justify-content:flex-end;gap:10px;margin-top:16px">
              <a class="btn btn-secondary" href="/ui/takeout/login">戻る</a>
              <a class="btn btn-primary" href="/ui/takeout/status">注文状況・受取通知を確認 →</a>
            </div>
          </div>
        </div>
        """
        return _render_shell(
            title="持ち帰り注文 › メニュー選択＆受取時刻予約",
            subtitle="持ち帰り可能商品のみで構成されたメニューから商品を選び、受取希望時刻を指定します",
            active_subtab="reserve",
            body_html=body,
        )

    @router.get("/ui/takeout/status", response_class=HTMLResponse)
    def status_and_notify_page() -> str:
        orders = _safe_takeout_orders(order_client)
        notified_map = {n["order_id"]: n for n in store.notifications}

        order_rows = []
        for o in orders:
            oid = str(o.get("order_id", "-"))
            notif = notified_map.get(oid)
            notif_badge = (
                '<span class="badge" style="background:#dcfce7;color:#166534">受取通知済み ✓</span>'
                if notif
                else '<span class="badge" style="background:#fef3c7;color:#92400e">未通知</span>'
            )
            order_rows.append(
                f"<tr><td><code>{escape(oid)}</code></td>"
                f"<td><code>{escape(str(o.get('customer_id', '-')))}</code></td>"
                f"<td>{escape(str(o.get('pickup_at', '-')))}</td>"
                f"<td><strong>¥{int(o.get('total_amount', 0)):,}</strong></td>"
                f"<td>{escape(str(o.get('status', '-')))}</td>"
                f"<td>{notif_badge}</td></tr>"
            )
        rows_html = "".join(order_rows) or (
            '<tr><td colspan="6" style="text-align:center;color:#64748b">持ち帰り注文はまだありません。</td></tr>'
        )

        notif_cards = "".join(
            f'<div style="border-left:4px solid #16a34a;background:#f0fdf4;padding:10px 14px;border-radius:8px;margin-bottom:8px">'
            f'<div style="font-weight:700;color:#166534">{escape(n["message"])}</div>'
            f'<div style="font-size:11px;color:#475569;margin-top:2px">'
            f'注文ID: <code>{escape(n["order_id"])}</code> ／ 送信時刻: {escape(n["notified_at"])}</div></div>'
            for n in store.notifications
        ) or '<p style="color:#64748b;font-size:13px">まだ受取通知は送信されていません。</p>'

        body = f"""
        <div class="grid-2">
          <div class="card">
            <h2 style="margin:0 0 12px;font-size:16px">持ち帰り予約注文一覧</h2>
            <table>
              <thead><tr><th>注文ID</th><th>顧客ID</th><th>受取予定</th><th>金額</th><th>調理状況</th><th>通知</th></tr></thead>
              <tbody>{rows_html}</tbody>
            </table>
          </div>
          <div class="card">
            <h2 style="margin:0 0 12px;font-size:16px">お客様への受取可能通知履歴</h2>
            {notif_cards}
          </div>
        </div>
        """
        return _render_shell(
            title="持ち帰り注文 › 注文状況・受取可能通知",
            subtitle="予約注文の調理状況と「ご注文の品の準備が整いました」通知の配信状態を確認します",
            active_subtab="status",
            body_html=body,
        )

    return router
