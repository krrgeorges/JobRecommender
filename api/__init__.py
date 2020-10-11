import sys, os
sys.path.append(os.path.abspath(os.path.join('miner')))

print(sys.path)

from flask import Flask,Blueprint,Response,request
from flask_restful import Resource, Api
from miner import Miner

class GatherJobPosts(Resource):
	def get(self):
		jobs = Miner().mine()
		return jobs

