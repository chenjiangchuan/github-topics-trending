"""
Email Reporter - 生成 HTML 邮件报告
GitHub Topics Trending 专业邮件排版
"""
from typing import Dict, List
from src.config import TOPIC, get_theme, format_number


class EmailReporter:
    """生成 HTML 邮件报告"""

    def __init__(self, theme: str = "blue"):
        """
        初始化

        Args:
            theme: 主题名称
        """
        self.theme = get_theme(theme)
        self.topic = TOPIC

    def generate_email_html(self, trends: Dict, date: str) -> str:
        """
        生成完整的 HTML 邮件

        Args:
            trends: 趋势数据
            date: 日期

        Returns:
            HTML 字符串
        """
        html_parts = []

        # HTML 头部
        html_parts.append(self._get_header(date))

        # Top 20 榜单
        html_parts.append(self._render_top_20(trends.get("top_20", [])))

        # 星标增长 Top 5
        rising = trends.get("rising_top5", [])
        if rising:
            html_parts.append(self._render_rising_top5(rising))

        # 新晋项目
        new_entries = trends.get("new_entries", [])
        if new_entries:
            html_parts.append(self._render_new_entries(new_entries))

        # 活跃项目
        active = trends.get("active", [])
        if active:
            html_parts.append(self._render_active(active))

        # 统计信息
        html_parts.append(self._render_stats(trends))

        # HTML 尾部
        html_parts.append(self._get_footer(date))

        return "\n".join(html_parts)

    def _get_header(self, date: str) -> str:
        """生成 HTML 头部"""
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Topics Daily - {self.topic}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #eef3f8;
            color: #18212f;
            -webkit-font-smoothing: antialiased;
        }}
        .container {{
            max-width: 680px;
            margin: 0 auto;
            background-color: #f6f8fb;
        }}
        .header {{
            background: linear-gradient(135deg, #0969da 0%, #54aeff 100%);
            color: white;
            padding: 38px 40px 34px;
            text-align: left;
        }}
        .header h1 {{
            margin: 0;
            font-size: 34px;
            font-weight: 700;
            letter-spacing: 0;
        }}
        .header p {{
            margin: 12px 0 0;
            font-size: 17px;
            opacity: 0.86;
            font-weight: 400;
        }}
        .section {{
            padding: 32px 40px 40px;
            border-bottom: 1px solid #d8e1ec;
        }}
        .section:last-child {{
            border-bottom: none;
        }}
        .section-heading {{
            margin: 0 0 18px;
            padding-bottom: 14px;
            border-bottom: 1px solid #d8e1ec;
        }}
        .section-heading-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .section-title {{
            margin: 0;
            font-size: 19px;
            font-weight: 700;
            color: #1f2937;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .section-caption {{
            color: #6b7280;
            font-size: 13px;
            font-weight: 500;
            text-align: right;
            white-space: nowrap;
        }}
        .repo-card {{
            margin-bottom: 16px;
            padding: 20px 22px;
            background-color: #ffffff;
            border: 1px solid #d9e2ec;
            border-radius: 12px;
            box-shadow: 0 8px 22px rgba(16, 24, 40, 0.07);
        }}
        .repo-card:last-child {{
            margin-bottom: 0;
        }}
        .repo-card.featured {{
            border-color: #9cc9ff;
            background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
        }}
        .repo-layout {{
            width: 100%;
            border-collapse: collapse;
        }}
        .repo-rank-cell {{
            width: 58px;
            vertical-align: top;
            padding: 0 14px 0 0;
        }}
        .repo-rank {{
            display: inline-block;
            min-width: 42px;
            padding: 7px 10px;
            border-radius: 999px;
            background-color: #e8f2ff;
            color: #0969da;
            font-size: 14px;
            font-weight: 750;
            text-align: center;
        }}
        .repo-body-cell {{
            vertical-align: top;
        }}
        .repo-star-cell {{
            width: 104px;
            vertical-align: top;
            text-align: right;
            padding-left: 14px;
            white-space: nowrap;
        }}
        .repo-main {{
            min-width: 0;
        }}
        .repo-name {{
            color: #111827;
            font-size: 21px;
            line-height: 1.25;
            font-weight: 760;
        }}
        .repo-name a {{
            color: #111827;
            text-decoration: none;
        }}
        .repo-name a:hover {{
            text-decoration: underline;
        }}
        .repo-stats {{
            white-space: nowrap;
            color: #374151;
            font-size: 15px;
            font-weight: 650;
        }}
        .rank-change {{
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 999px;
            font-size: 12px;
        }}
        .rank-up {{
            color: #166534;
            background-color: #dcfce7;
        }}
        .rank-down {{
            color: #b91c1c;
            background-color: #fee2e2;
        }}
        .stars {{
            color: #374151;
            font-size: 15px;
            font-weight: 650;
        }}
        .repo-summary {{
            margin: 14px 0 8px;
            color: #273449;
            font-size: 16px;
            line-height: 1.55;
            font-weight: 650;
        }}
        .repo-meta {{
            margin: 0;
            color: #596579;
            font-size: 14px;
            line-height: 1.65;
        }}
        .badge {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 650;
            margin-right: 8px;
            margin-bottom: 8px;
        }}
        .badge-category {{
            background-color: #dbeafe;
            color: #0757b8;
        }}
        .badge-language {{
            background-color: #f3f4f6;
            color: #374151;
        }}
        .badge-new {{
            background-color: #dcfce7;
            color: #166534;
        }}
        .solves-list {{
            display: inline;
        }}
        .solve-tag {{
            display: inline-block;
            background-color: #eef2f6;
            color: #4b5563;
            padding: 5px 10px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 650;
            margin-right: 8px;
            margin-bottom: 8px;
        }}
        .stats-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .stat-cell {{
            width: 33.333%;
            padding: 0 6px;
        }}
        .stat-item {{
            text-align: center;
            padding: 16px;
            background-color: #ffffff;
            border: 1px solid #d9e2ec;
            border-radius: 12px;
            box-shadow: 0 8px 22px rgba(16, 24, 40, 0.06);
        }}
        .stat-value {{
            font-size: 24px;
            font-weight: 700;
            color: #0969da;
        }}
        .stat-label {{
            font-size: 12px;
            color: #596579;
            margin-top: 4px;
        }}
        .footer {{
            text-align: center;
            padding: 28px 20px;
            font-size: 12px;
            color: #596579;
            background-color: #eef3f8;
        }}
        .footer a {{
            color: #0969da;
            text-decoration: none;
            font-weight: 500;
        }}
        .footer a:hover {{
            text-decoration: underline;
        }}
        .compact-card {{
            padding: 16px 18px;
            margin-bottom: 12px;
            background-color: #ffffff;
            border: 1px solid #d9e2ec;
            border-radius: 10px;
            box-shadow: 0 6px 16px rgba(16, 24, 40, 0.05);
        }}
        .compact-card:last-child {{
            margin-bottom: 0;
        }}
        .compact-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .compact-rank {{
            color: #0969da;
            font-weight: 700;
            width: 40px;
            font-size: 13px;
            white-space: nowrap;
            padding-right: 10px;
        }}
        .compact-name {{
            padding: 0 8px;
        }}
        .compact-name a {{
            color: #111827;
            text-decoration: none;
            font-size: 14px;
            font-weight: 650;
        }}
        .compact-meta {{
            color: #596579;
            font-size: 12px;
            white-space: nowrap;
            text-align: right;
            width: 120px;
        }}
        .compact-summary {{
            padding: 10px 0 0;
            font-size: 13px;
            color: #596579;
            line-height: 1.5;
        }}
        .compact-badge-cell {{
            width: 62px;
            padding-right: 12px;
            white-space: nowrap;
            vertical-align: top;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>GitHub Topics Daily</h1>
            <p>#{self.topic} - {date}</p>
        </div>"""

    def _get_footer(self, date: str) -> str:
        """生成 HTML 尾部"""
        return f"""        <div class="footer">
            <p>GitHub Topics Trending - #{self.topic}</p>
            <p style="margin-top: 8px;">Data source: <a href="https://github.com/topics/{self.topic}">github.com/topics/{self.topic}</a></p>
        </div>
    </div>
</body>
</html>"""

    def _render_top_20(self, repos: List[Dict]) -> str:
        """渲染 Top 20 榜单"""
        if not repos:
            return self._section_html("Top 20 榜单", '<p style="text-align:center;color:#9ca3af;padding:24px;">暂无数据</p>')

        cards = []
        for repo in repos[:20]:
            cards.append(self._format_repo_card(repo, show_details=True))

        return self._section_html("Top 20 经典榜单", "\n".join(cards))

    def _render_rising_top5(self, repos: List[Dict]) -> str:
        """渲染星标增长 Top 5"""
        cards = []
        for repo in repos:
            cards.append(self._format_compact_card(repo, trend="up"))

        return self._section_html("星标增长 Top 5", "\n".join(cards))

    def _render_new_entries(self, repos: List[Dict]) -> str:
        """渲染新晋项目"""
        if not repos:
            return ""

        cards = []
        for repo in repos[:10]:
            cards.append(self._format_compact_card(repo, is_new=True))

        return self._section_html(f"新晋项目 ({len(repos)})", "\n".join(cards))

    def _render_active(self, repos: List[Dict]) -> str:
        """渲染活跃项目"""
        if not repos:
            return ""

        cards = []
        for repo in repos[:10]:
            cards.append(self._format_active_card(repo))

        return self._section_html("活跃项目", "\n".join(cards))

    def _render_stats(self, trends: Dict) -> str:
        """渲染统计信息"""
        new_count = len(trends.get("new_entries", []))
        rising_count = len(trends.get("rising_top5", []))
        surging_count = len(trends.get("surging", []))
        active_count = len(trends.get("active", []))

        return self._section_html("趋势概览", f"""
        <table class="stats-table" role="presentation">
            <tr>
                <td class="stat-cell">
                    <div class="stat-item">
                        <div class="stat-value">{new_count}</div>
                        <div class="stat-label">新晋项目</div>
                    </div>
                </td>
                <td class="stat-cell">
                    <div class="stat-item">
                        <div class="stat-value">{rising_count}</div>
                        <div class="stat-label">上升项目</div>
                    </div>
                </td>
                <td class="stat-cell">
                    <div class="stat-item">
                        <div class="stat-value">{active_count}</div>
                        <div class="stat-label">活跃项目</div>
                    </div>
                </td>
            </tr>
        </table>
        """)

    def _format_repo_card(self, repo: Dict, show_details: bool = True) -> str:
        """格式化单个仓库卡片"""
        rank = repo.get("rank", 0)
        repo_name = repo.get("repo_name", "")
        stars_delta = repo.get("stars_delta", 0)
        stars = repo.get("stars", 0)
        forks = repo.get("forks", 0)
        language = repo.get("language", "")
        url = repo.get("url", f"https://github.com/{repo_name}")

        # 星标变化指示；无变化时不展示占位符，避免邮件里出现突兀的灰色 "-"
        if stars_delta > 0:
            stars_indicator = f'<span class="rank-change rank-up">+{format_number(stars_delta)}</span>'
        elif stars_delta < 0:
            stars_indicator = f'<span class="rank-change rank-down">{format_number(stars_delta)}</span>'
        else:
            stars_indicator = ""

        # 语言标签
        language_badge = ""
        if language:
            language_badge = f'<span class="badge badge-language">{language}</span>'

        # 分类标签
        category_badge = ""
        if repo.get("category_zh"):
            category_badge = f'<span class="badge badge-category">{repo.get("category_zh")}</span>'

        # 解决的问题标签
        solves_html = ""
        if show_details and repo.get("solves"):
            solves_tags = [f'<span class="solve-tag">{s}</span>' for s in repo.get("solves", [])[:4]]
            solves_html = f'<div class="solves-list">{"".join(solves_tags)}</div>'

        # 详细信息
        details_html = ""
        if show_details:
            summary = repo.get("summary", "")
            description = repo.get("description", "")

            detail_parts = []
            if summary:
                detail_parts.append(f'<p class="repo-summary">{summary}</p>')
            if description:
                detail_parts.append(f'<p class="repo-meta">{description}</p>')

            details_html = "\n".join(detail_parts)

        featured_class = " featured" if rank == 1 else ""

        return f"""        <div class="repo-card{featured_class}">
            <table class="repo-layout" role="presentation">
                <tr>
                    <td class="repo-rank-cell"><span class="repo-rank">#{rank}</span></td>
                    <td class="repo-body-cell">
                        <div class="repo-main">
                            <div class="repo-name"><a href="{url}">{repo_name}</a></div>
                        </div>
                    </td>
                    <td class="repo-star-cell">
                        <div class="repo-stats">{stars_indicator} <span class="stars">★ {format_number(stars)}</span></div>
                    </td>
                </tr>
                <tr>
                    <td></td>
                    <td class="repo-body-cell" colspan="2">
                    {details_html}
                    <div style="margin-top: 16px;">
                        {category_badge}
                        {language_badge}
                        {solves_html}
                    </div>
                    </td>
                </tr>
            </table>
        </div>"""

    def _format_compact_card(self, repo: Dict, trend: str = None, is_new: bool = False) -> str:
        """格式化紧凑卡片"""
        rank = repo.get("rank", 0)
        repo_name = repo.get("repo_name", "")
        url = repo.get("url", f"https://github.com/{repo_name}")
        stars = repo.get("stars", 0)

        # 变化指示
        change_html = ""
        if is_new:
            change_html = '<span class="badge badge-new">NEW</span>'
        elif trend == "up":
            stars_delta = repo.get("stars_delta", 0)
            change_html = f'<span class="rank-change rank-up">+{format_number(stars_delta)}</span>'

        summary = repo.get("summary", "")
        summary_html = f'<div class="compact-summary">{summary}</div>' if summary else ""

        return f"""            <div class="compact-card">
                <table class="compact-table" role="presentation">
                    <tr>
                        <td class="compact-badge-cell" rowspan="2">{change_html}</td>
                        <td class="compact-rank">#{rank}</td>
                        <td class="compact-name"><a href="{url}">{repo_name}</a></td>
                        <td class="compact-meta">★ {format_number(stars)}</td>
                    </tr>
                    <tr>
                        <td></td>
                        <td colspan="2">{summary_html}</td>
                    </tr>
                </table>
            </div>"""

    def _format_active_card(self, repo: Dict) -> str:
        """格式化活跃项目卡片"""
        repo_name = repo.get("repo_name", "")
        url = repo.get("url", f"https://github.com/{repo_name}")
        stars = repo.get("stars", 0)
        updated_at = repo.get("updated_at", "")

        # 简单的时间格式化
        time_ago = "最近"
        if updated_at:
            time_ago = updated_at.split("T")[0]

        summary = repo.get("summary", "")
        summary_html = f'<div class="compact-summary">{summary}</div>' if summary else ""

        return f"""            <div class="compact-card">
                <table class="compact-table" role="presentation">
                    <tr>
                        <td class="compact-name"><a href="{url}">{repo_name}</a></td>
                        <td class="compact-meta">★ {format_number(stars)} &nbsp;&middot;&nbsp; 更新: {time_ago}</td>
                    </tr>
                    <tr>
                        <td colspan="2">{summary_html}</td>
                    </tr>
                </table>
            </div>"""

    def _section_html(self, title: str, content: str) -> str:
        """生成一个完整的 section"""
        caption_html = '<span class="section-caption">按 stars 排名</span>' if "Top 20" in title else ""
        return f"""        <div class="section">
            <div class="section-heading">
                <table class="section-heading-table" role="presentation">
                    <tr>
                        <td><h2 class="section-title">{title}</h2></td>
                        <td class="section-caption">{caption_html}</td>
                    </tr>
                </table>
            </div>
            {content}
        </div>"""


def generate_email_html(trends: Dict, date: str, theme: str = "blue") -> str:
    """便捷函数：生成邮件 HTML"""
    reporter = EmailReporter(theme)
    return reporter.generate_email_html(trends, date)
