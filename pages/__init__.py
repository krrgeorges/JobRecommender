from flask import Blueprint,render_template
import sys
import os
sys.path.append(os.path.abspath(os.path.join('miner')))
from miner import Miner

pages_bp = Blueprint('pages',__name__)


@pages_bp.route("/JobPosts")
def get_job_posts():
	jobs = Miner().mine()
	return render_template("job_posts.html",jobs=jobs)