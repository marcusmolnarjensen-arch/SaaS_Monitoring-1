import os
import psycopg
from dotenv import load_dotenv
from pathlib import Path
from flask import Flask, render_template

load_dotenv(Path(__file__).parent / "password.env", override=True)

app = Flask(__name__)


def get_connection():
    return psycopg.connect(
        host=os.environ["POSTGRES_HOST"],
        port=os.environ["POSTGRES_PORT"],
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )


@app.route("/")
def index():
    try:
        with get_connection() as conn:
            latest = conn.execute(
                """
                SELECT DISTINCT ON (website_url)
                       website_url, is_healthy, status_code, response_time_ms
                FROM monitoring_results
                ORDER BY website_url, ctid DESC
                """
            ).fetchall()

            stats = conn.execute(
                """
                SELECT website_url,
                       ROUND(100.0 * SUM(CASE WHEN is_healthy THEN 1 ELSE 0 END) / COUNT(*), 1),
                       ROUND(AVG(response_time_ms))
                FROM monitoring_results
                GROUP BY website_url
                """
            ).fetchall()

            history = conn.execute(
                """
                SELECT website_url, status_code, response_time_ms, is_healthy
                FROM monitoring_results
                ORDER BY ctid DESC
                LIMIT 15
                """
            ).fetchall()

        stats_by_url = {url: (uptime, avg_ms) for url, uptime, avg_ms in stats}
        sites = []
        for url, healthy, code, ms in latest:
            uptime, avg_ms = stats_by_url[url]
            sites.append(
                {"url": url, "healthy": healthy, "code": code, "ms": ms,
                 "uptime": uptime, "avg_ms": avg_ms}
            )
        up = sum(1 for s in sites if s["healthy"])
        return render_template("index.html", sites=sites, history=history,
                               up=up, total=len(sites), error=None)
    except Exception as e:
        return render_template("index.html", sites=[], history=[], up=0,
                               total=0, error=str(e)), 500


if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000)