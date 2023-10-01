from datetime import datetime
import re
import os
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from io import BytesIO
from nonebot.adapters.onebot.v11 import MessageSegment


async def log_analyze(path, lines, fpath):
	folder_path = Path(path)

	log_files = list(folder_path.glob("*.log"))

	if log_files:
		latest_log = max(log_files, key=lambda x: x.stat().st_mtime)

		lines_to_read = lines
		with latest_log.open(encoding='utf-8') as f:
			lines = f.readlines()[-lines_to_read:]

		log_content = ''.join(lines)

		width, height = 1000, 600
		fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100)
		ax.set_facecolor("white")
		ax.set_axis_off()

		font_path = fpath
		font = FontProperties(fname=font_path)

		x, y = 0.05, 0.9
		ax.text(x, y, log_content, fontsize=14, fontproperties=font, verticalalignment='top')

		img_stream = BytesIO()
		plt.savefig(img_stream, format="png", bbox_inches="tight")
		img_stream.seek(0)

		img_segment = MessageSegment.image(img_stream)
		return img_segment

__all__ = ['log_analyze']