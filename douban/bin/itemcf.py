#!/usr/bin/env python
#-*- coding: gbk -*-

import sys
import random
import math
import os
from operator import itemgetter

random.seed(0)

class ItemBasedCF(object):
	
	def __init__(self):
		self.trainset = {}
		self.testset = {}

		self.n_sim_movie = 10
		self.n_rec_movie = 10

		self.movie_sim_mat = {}
		self.movie_popular = {}
		self.movie_count = 0

		print >> sys.stderr, 'Similar movie number = %d' % self.n_sim_movie
		print >> sys.stderr, 'Recommended movie number = %d' % self.n_rec_movie

	
	@staticmethod
	def loadfile(filename):
		'''load a file, return a generator'''
		fp = open(filename, 'r')
		for i, line in enumerate(fp):
			yield line.strip('\r\n')
			if i % 10000 == 0:
				print >> sys.stderr, 'loading %s(%s)' % (filename, i)

		fp.close()
		print >> sys.stderr, 'load %s succ' % filename
	

	def generate_dataset(self, filename, pivot = 0.7):
		'''load rating data and split'''
		trainset_len = 0
		testset_len = 0

		for line in self.loadfile(filename):
			user, movie, rating = line.split('\t')
			if random.random() < pivot:
				self.trainset.setdefault(user, {})
				self.trainset[user][movie] = int(rating)
				trainset_len += 1
			else:
				self.testset.setdefault(user, {})
				self.testset[user][movie] = int(rating)
				testset_len += 1


		print >> sys.stderr, 'split training set and test succ'
		print >> sys.stderr, 'train set = %s' % trainset_len
		print >> sys.stderr, "test set = %s" % testset_len
	

	def calc_movie_sim(self):
		'''calculate movie similarity matrix '''
		print >> sys.stderr, 'counting movies number and popularity'

		for user,movies in self.trainset.iteritems():
			for movie in movies:
				if movie not in self.movie_popular:
					self.movie_popular[movie] = 0
				self.movie_popular[movie] += 1
		print >> sys.stderr, 'count movies number and popularity succ'

		#save the total number of movie
		self.movie_count = len(self.movie_popular)
		print >> sys.stderr, 'total movies number %s' % self.movie_count

		#count co-rated user between items:
		itemsim_mat = self.movie_sim_mat
		print >> sys.stderr, 'building co-rated users matrix ...'

		for user, movies in self.trainset.iteritems():
			for m1 in movies:
				for m2 in movies:
					if m1 == m2:
						continue
					itemsim_mat.setdefault(m1, {})
					itemsim_mat[m1].setdefault(m2,0)
					itemsim_mat[m1][m2] += 1
		print >> sys.stderr, 'build co_rated users matrix succ'

		#calculate similarity matrix
		print >> sys.stderr, 'calculating movie similarity matrix ...'
		simfactor_count = 0
		PRINT_STEP = 2000000

		for m1, related_movies in itemsim_mat.iteritems():
			for m2, count in related_movies.iteritems():
				itemsim_mat[m1][m2] = count / math.sqrt(
					self.movie_popular[m1] * self.movie_popular[m2]) 
				simfactor_count += 1
				if simfactor_count % PRINT_STEP == 0:
					print sys.stderr, 'caculating movie similarity factor(%d)' % simfactor_count

		print >> sys.stderr, 'calculate movie similarity matrix(similarity factor) succ'
		print >> sys.stderr, 'Total similarity factor number = %d ' % simfactor_count

	def recommend(self, user):
		K = self.n_sim_movie
		N =self.n_rec_movie
		rank = {}
		watched_movies = self.trainset[user]

		for movie, rating in watched_movies.iteritems():
			for related_movie, similarity_factor in sorted(self.movie_sim_mat[movie].items(),
															key = itemgetter(1), reverse=True)[:K]:
				if related_movie in watched_movies:
					continue
				rank.setdefault(related_movie, 0)
				rank[related_movie] += similarity_factor * rating
		return sorted(rank.items(), key=itemgetter(1), reverse=True)[:N]




if __name__ == '__main__':
	#sys.argv[1] = ratings.sort
	#sys.argv[2] = movie.dat

	ratingfile = sys.argv[1]
	itemcf = ItemBasedCF()
	itemcf.generate_dataset(ratingfile)
	itemcf.calc_movie_sim()
	rcm_dict = itemcf.recommend('101817400')

	movie_dict = {}
	for line in open(sys.argv[2]):
		line = line.rstrip('\n')
		segs = line.split('\t')
		movie_dict[segs[0]] = line

	print '看过的电影'
	watched_movie = itemcf.trainset['101817400']
	for item, score in watched_movie.iteritems():
		print movie_dict[item]

	print '#################################################'
	print '推荐的电影'
	for key in rcm_dict:
		movieid, score = key
		print movie_dict[movieid]
