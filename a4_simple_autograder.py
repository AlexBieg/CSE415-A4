# Simple Autograder for CSE415 Assignment 4
# April 2017
# Rob Thompson
# Adapted from Dianmu Zhang's autograder for Assignment 1

import unittest, os, sys, importlib

'''remove the file extension if it was included'''
problem_name = os.path.splitext(sys.argv[1])[0]

'''import the problem'''
problem = importlib.import_module(problem_name)
del(sys.argv[1])

class TestCases(unittest.TestCase):
	
	def test_create_initial_state_defined(self):
		'''tests if INITIAL_STATE is defined'''
		msg = 'INITIAL_STATE not defined fail'
		try:
			problem.INITIAL_STATE
		except (Exception) as e:
			print(msg)
			print(e)
			
	def test_operators_defined(self):
		'''tests if OPERATORS is defined and non-empty'''
		msg = 'OPERATORS not defined fail'
		try:
			problem.OPERATORS
			problem.OPERATORS[0]
		except (Exception) as e:
			print(msg)
			print(e)
	
	def test_goal_test_defined(self):
		'''tests if GOAL_TEST is defined and works (not required if you are doing option A)'''
		msg = 'GOAL_TEST not defined fail (not required if you are doing option A)'
		try:
			problem.GOAL_TEST
			problem.GOAL_TEST(problem.INITIAL_STATE)
		except (Exception) as e:
			print(msg)
			print(e)
			
	def test_str_defined(self):
		'''tests if State.__str__ is defined and works'''
		msg = 'State.__str__ not defined fail'
		try:
			str(problem.INITIAL_STATE)[0]
		except (Exception) as e:
			print(msg)
			print(e)
	
	def test_heuristics_defined(self):
		'''tests if at least one heuristic is defined and works'''
		msg = 'HEURISTICS is not defined,empty, or does not work fail'
		try:
			problem.HEURISTICS[0](problem.INITIAL_STATE)
		except (Exception) as e:
			print(msg)
			print(e)
			
if __name__ == '__main__':
	unittest.main()