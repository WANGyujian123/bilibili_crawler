#!/usr/bin/env python3
"""B站内容爬虫和分析工具"""
import click
from loguru import logger
import sys
from pathlib import Path

from bilibili import BilibiliAPI, SubtitleDownloader
from analyzer import ClaudeAnalyzer
from database import Database
import config


# 配置日志
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    level=config.LOG_LEVEL
)
logger.add(
    config.LOG_DIR / "bilibili_crawler.log",
    rotation="10 MB",
    retention="7 days",
    level="DEBUG"
)


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """B站内容爬虫和分析工具

    爬取B站UP主的视频内容，提取字幕，并使用Claude AI分析UP主的思想和观点。
    """
    pass


@cli.command()
@click.argument('uid')
@click.option('--max-videos', '-m', type=int, default=None, help='最多爬取的视频数量')
@click.option('--with-subtitle', '-s', is_flag=True, help='同时下载字幕')
@click.option('--season-id', type=int, default=None, help='指定合集ID（先用list-series查看）')
@click.option('--series-id', type=int, default=None, help='指定视频列表ID（先用list-series查看）')
def crawl(uid: str, max_videos: int, with_subtitle: bool, season_id: int, series_id: int):
    """爬取UP主的视频信息

    UID: UP主的用户ID
    """
    logger.info(f"开始爬取UP主 {uid} 的内容")

    # 初始化
    api = BilibiliAPI()
    db = Database()

    # 获取UP主信息
    user_info = api.get_user_info(uid)
    if not user_info:
        logger.error("获取UP主信息失败")
        return

    # 保存UP主信息
    db.save_user(user_info)
    click.echo(f"✓ UP主: {user_info['name']}")
    click.echo(f"  签名: {user_info.get('sign', 'N/A')}")
    click.echo(f"  粉丝: {user_info.get('follower', 0)}")

    # 获取视频列表
    click.echo("\n正在获取视频列表...")

    if season_id:
        # 获取指定合集的视频
        click.echo(f"从合集 {season_id} 中获取视频...")
        videos = api.get_season_videos(season_id)
    elif series_id:
        # 获取指定视频列表的视频
        click.echo(f"从视频列表 {series_id} 中获取视频...")
        videos = api.get_series_videos(series_id, uid)
    else:
        # 获取所有视频
        videos = api.get_all_user_videos(uid, max_videos)

    if not videos:
        logger.error("未获取到任何视频")
        return

    click.echo(f"✓ 共获取 {len(videos)} 个视频\n")

    # 保存视频信息
    with click.progressbar(videos, label='保存视频信息') as bar:
        for video in bar:
            db.save_video(uid, video)

    # 下载字幕
    if with_subtitle:
        click.echo("\n开始下载字幕...")
        subtitle_downloader = SubtitleDownloader()

        success_count = 0
        with click.progressbar(videos, label='下载字幕') as bar:
            for video in bar:
                bvid = video['bvid']
                cid = video.get('cid')

                if not cid:
                    # 尝试获取CID
                    cid = api.get_video_cid(bvid)

                if cid:
                    subtitle_text = subtitle_downloader.get_video_subtitle(bvid, cid)
                    if subtitle_text:
                        db.save_subtitle(bvid, subtitle_text)
                        success_count += 1

        click.echo(f"✓ 成功下载 {success_count}/{len(videos)} 个视频的字幕")

    db.close()
    click.echo(f"\n✓ 爬取完成！数据已保存到数据库: {config.DATABASE_PATH}")


@cli.command()
@click.argument('uid')
@click.option('--max-videos', '-m', type=int, default=10, help='分析的视频数量')
def download_subtitle(uid: str, max_videos: int):
    """单独下载字幕

    UID: UP主的用户ID
    """
    logger.info(f"开始为UP主 {uid} 下载字幕")

    db = Database()
    api = BilibiliAPI()
    subtitle_downloader = SubtitleDownloader()

    # 获取视频列表
    videos = db.get_user_videos(uid)
    if not videos:
        logger.error(f"数据库中没有UP主 {uid} 的视频，请先执行crawl命令")
        return

    videos = videos[:max_videos]
    click.echo(f"准备为 {len(videos)} 个视频下载字幕\n")

    success_count = 0
    with click.progressbar(videos, label='下载字幕') as bar:
        for video in bar:
            bvid = video['bvid']
            cid = video.get('cid')

            if not cid:
                cid = api.get_video_cid(bvid)

            if cid:
                subtitle_text = subtitle_downloader.get_video_subtitle(bvid, cid)
                if subtitle_text:
                    db.save_subtitle(bvid, subtitle_text)
                    success_count += 1

    db.close()
    click.echo(f"\n✓ 成功下载 {success_count}/{len(videos)} 个视频的字幕")


@cli.command()
@click.argument('uid')
@click.option('--max-videos', '-m', type=int, default=10, help='分析的视频数量')
@click.option('--analysis-type', '-t', type=click.Choice(['ideology', 'themes', 'style', 'comprehensive']),
              default='comprehensive', help='分析类型')
def analyze(uid: str, max_videos: int, analysis_type: str):
    """分析UP主的内容

    UID: UP主的用户ID
    """
    logger.info(f"开始分析UP主 {uid} 的内容")

    db = Database()

    # 获取UP主信息
    user_info = db.get_user(uid)
    if not user_info:
        logger.error(f"数据库中没有UP主 {uid} 的信息，请先执行crawl命令")
        return

    user_name = user_info['name']
    click.echo(f"正在分析UP主: {user_name}\n")

    # 获取视频列表
    videos = db.get_user_videos(uid)[:max_videos]
    if not videos:
        logger.error("没有找到视频")
        return

    click.echo(f"共 {len(videos)} 个视频")

    # 收集字幕
    subtitles = []
    videos_with_subtitle = []

    with click.progressbar(videos, label='读取字幕') as bar:
        for video in bar:
            subtitle = db.get_video_subtitle(video['bvid'])
            if subtitle:
                subtitles.append(subtitle)
                videos_with_subtitle.append(video['title'])

    if not subtitles:
        logger.error("没有找到任何字幕，请先执行download-subtitle命令")
        return

    click.echo(f"\n✓ 找到 {len(subtitles)} 个视频的字幕")
    click.echo("\n正在使用Claude AI进行分析...\n")

    # 初始化分析器
    try:
        analyzer = ClaudeAnalyzer()
    except ValueError as e:
        logger.error(str(e))
        click.echo(f"\n❌ 错误: {e}")
        click.echo("请在.env文件中设置CLAUDE_API_KEY")
        return

    # 执行分析
    if analysis_type == 'ideology':
        result = analyzer.analyze_ideology(subtitles, user_name)
        if result:
            db.save_analysis(uid, "思想分析", result)
            click.echo("\n" + "="*60)
            click.echo(f"思想分析结果:")
            click.echo("="*60 + "\n")
            click.echo(result)

    elif analysis_type == 'themes':
        result = analyzer.analyze_themes(subtitles)
        if result:
            db.save_analysis(uid, "主题分析", result)
            click.echo("\n" + "="*60)
            click.echo(f"主题分析结果:")
            click.echo("="*60 + "\n")
            click.echo(result)

    elif analysis_type == 'style':
        result = analyzer.analyze_style(subtitles)
        if result:
            db.save_analysis(uid, "风格分析", result)
            click.echo("\n" + "="*60)
            click.echo(f"风格分析结果:")
            click.echo("="*60 + "\n")
            click.echo(result)

    else:  # comprehensive
        results = analyzer.comprehensive_analysis(subtitles, user_name)
        for analysis_name, result in results.items():
            db.save_analysis(uid, analysis_name, result)
            click.echo("\n" + "="*60)
            click.echo(f"{analysis_name}:")
            click.echo("="*60 + "\n")
            click.echo(result)
            click.echo()

    db.close()
    click.echo("\n✓ 分析完成！结果已保存到数据库")


@cli.command()
@click.argument('uid')
@click.option('--format', '-f', type=click.Choice(['text', 'markdown', 'json']),
              default='text', help='输出格式')
@click.option('--output', '-o', type=click.Path(), help='输出文件路径（留空则输出到终端）')
def show(uid: str, format: str, output: str):
    """查看UP主的分析结果，支持导出为Markdown或JSON

    UID: UP主的用户ID
    """
    from analyzer import AnalysisExporter

    db = Database()

    # 获取UP主信息
    user_info = db.get_user(uid)
    if not user_info:
        logger.error(f"数据库中没有UP主 {uid} 的信息")
        db.close()
        return

    # 根据格式导出
    exporter = AnalysisExporter(db)

    try:
        if format == 'markdown':
            if output:
                result = exporter.export_to_markdown(uid, output)
                click.echo(f"✓ Markdown报告已导出到: {result}")
            else:
                content = exporter.export_to_markdown(uid)
                click.echo(content)

        elif format == 'json':
            if output:
                result = exporter.export_to_json(uid, output)
                click.echo(f"✓ JSON报告已导出到: {result}")
            else:
                content = exporter.export_to_json(uid)
                click.echo(content)

        else:  # text format (原有逻辑)
            click.echo(f"\nUP主: {user_info['name']}")
            click.echo(f"签名: {user_info.get('sign', 'N/A')}")
            click.echo(f"粉丝: {user_info.get('follower', 0)}")

            # 获取视频统计
            videos = db.get_user_videos(uid)
            click.echo(f"\n视频数量: {len(videos)}")

            # 获取分析结果
            analyses = db.get_user_analysis(uid)
            if analyses:
                click.echo(f"\n分析结果 ({len(analyses)} 条):\n")
                for analysis in analyses:
                    click.echo("="*60)
                    click.echo(f"{analysis['analysis_type']} ({analysis['created_at']})")
                    click.echo("="*60)
                    click.echo(analysis['analysis_result'])
                    click.echo()
            else:
                click.echo("\n还没有分析结果")
    except Exception as e:
        logger.error(f"导出失败: {e}")
        click.echo(f"❌ 导出失败: {e}")
    finally:
        db.close()


@cli.command()
@click.argument('uid')
def list_series(uid: str):
    """列出UP主的所有合集和视频列表

    UID: UP主的用户ID
    """
    logger.info(f"获取UP主 {uid} 的合集列表")

    # 初始化
    api = BilibiliAPI()

    # 获取UP主信息
    user_info = api.get_user_info(uid)
    if user_info:
        click.echo(f"\n✓ UP主: {user_info['name']}\n")

    # 获取合集和视频列表
    series_data = api.get_user_series_list(uid)

    if not series_data:
        click.echo("该UP主没有合集或视频列表")
        return

    # 显示合集列表
    seasons_list = series_data.get("seasons_list", [])
    if seasons_list:
        click.echo(f"{'='*60}")
        click.echo(f"合集列表 (共 {len(seasons_list)} 个)")
        click.echo(f"{'='*60}\n")

        for i, season in enumerate(seasons_list, 1):
            meta = season.get("meta", {})
            click.echo(f"{i}. {meta.get('name')}")
            click.echo(f"   - 合集ID: {meta.get('season_id')}")
            click.echo(f"   - 视频数: {meta.get('total')}")
            if meta.get('description'):
                click.echo(f"   - 描述: {meta.get('description')}")
            click.echo()

        click.echo("使用方法：")
        click.echo(f"  python3 main.py crawl {uid} --season-id <合集ID> --with-subtitle")
        click.echo()

    # 显示视频列表
    series_list = series_data.get("series_list", [])
    if series_list:
        click.echo(f"{'='*60}")
        click.echo(f"视频列表 (共 {len(series_list)} 个)")
        click.echo(f"{'='*60}\n")

        for i, series in enumerate(series_list, 1):
            meta = series.get("meta", {})
            click.echo(f"{i}. {meta.get('name')}")
            click.echo(f"   - 列表ID: {meta.get('series_id')}")
            click.echo(f"   - 视频数: {meta.get('total')}")
            if meta.get('description'):
                click.echo(f"   - 描述: {meta.get('description')}")
            click.echo()

        click.echo("使用方法：")
        click.echo(f"  python3 main.py crawl {uid} --series-id <列表ID> --with-subtitle")
        click.echo()


if __name__ == '__main__':
    cli()
