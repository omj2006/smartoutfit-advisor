from __future__ import annotations

import sqlite3
from typing import Any, Dict, List, Optional

from app.tools.builtin.ecommerce_api import (
    JD_PRODUCTS,
    PDD_PRODUCTS,
    TAOBAO_PRODUCTS,
    _make_item_id,
    _make_image_url,
    _make_jd_url,
    _make_pdd_url,
    _make_taobao_url,
)
from app.tools.builtin.product_db import DB_PATH, get_connection, init_db


class ProductSync:
    def __init__(self) -> None:
        init_db()

    def _ensure_sync_table(self, conn: sqlite3.Connection) -> None:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS synced_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_platform TEXT NOT NULL,
                source_id TEXT NOT NULL,
                name TEXT NOT NULL,
                brand TEXT,
                price REAL,
                original_price REAL,
                category TEXT,
                url TEXT,
                image_url TEXT,
                sales INTEGER DEFAULT 0,
                rating REAL DEFAULT 0.0,
                synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(source_platform, source_id)
            )
        """)
        conn.commit()

    def _sync_platform(
        self,
        conn: sqlite3.Connection,
        products: List[Dict[str, Any]],
        platform: str,
        url_fn: Any,
    ) -> int:
        cursor = conn.cursor()
        synced_count = 0
        for p in products:
            item_id = _make_item_id(p["name"], platform)
            url = url_fn(item_id)
            image_url = _make_image_url(platform, item_id)
            try:
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO synced_products
                        (source_platform, source_id, name, brand, price, original_price,
                         category, url, image_url, sales, rating)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        platform,
                        item_id,
                        p["name"],
                        p.get("brand", ""),
                        p.get("price", 0.0),
                        p.get("original_price", 0.0),
                        p.get("category", ""),
                        url,
                        image_url,
                        p.get("sales", 0),
                        p.get("rating", 0.0),
                    ),
                )
                synced_count += 1
            except sqlite3.Error:
                continue
        conn.commit()
        return synced_count

    def sync_from_platforms(
        self,
        platforms: Optional[List[str]] = None,
    ) -> Dict[str, int]:
        conn = get_connection()
        self._ensure_sync_table(conn)

        platform_map = {
            "taobao": (TAOBAO_PRODUCTS, _make_taobao_url),
            "jd": (JD_PRODUCTS, _make_jd_url),
            "pdd": (PDD_PRODUCTS, _make_pdd_url),
        }

        results: Dict[str, int] = {}
        targets = platforms if platforms else list(platform_map.keys())

        for plat in targets:
            if plat not in platform_map:
                results[plat] = 0
                continue
            products, url_fn = platform_map[plat]
            count = self._sync_platform(conn, products, plat, url_fn)
            results[plat] = count

        conn.close()
        return results

    def get_synced_products(
        self,
        platform: Optional[str] = None,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        conn = get_connection()
        cursor = conn.cursor()

        conditions = []
        params: List[Any] = []

        if platform:
            conditions.append("source_platform = ?")
            params.append(platform)
        if category:
            conditions.append("category = ?")
            params.append(category)
        if min_price is not None:
            conditions.append("price >= ?")
            params.append(min_price)
        if max_price is not None:
            conditions.append("price <= ?")
            params.append(max_price)

        where_clause = " AND ".join(conditions) if conditions else "1=1"
        query = f"SELECT * FROM synced_products WHERE {where_clause} ORDER BY rating DESC, sales DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_sync_stats(self) -> Dict[str, int]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT source_platform, COUNT(*) FROM synced_products GROUP BY source_platform")
        rows = cursor.fetchall()
        conn.close()
        return {row[0]: row[1] for row in rows}
