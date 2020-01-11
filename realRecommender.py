import pandas as pd
import numpy as np
import math
import random

train_sample = pd.read_csv('example.csv')
problem_sample = pd.read_csv('problem_sample.csv')
user_sample = pd.read_csv('user_sample.csv')
missing = {'tags':'mcq', 'level_type': 'N'}
problem_sample.fillna(value = missing, inplace = True)
problemsToPredict = []
users = []
previousProblems = []
tags_relations = [['math', 'constructive algorithms', 'binary search'],
['strings', 'sortings', 'constructive algorithms', 'binary search', 'ternary search', 'two pointers', 'data structures', 'hashing', 'implementation','string suffix structures'],
['greedy', 'dp', 'divide and conquer', 'brute force', 'meet-in-the-middle', 'matrices', 'data structures', 'implementation'],
['binary search', 'trees', 'data structures', 'ternary search', 'string suffix structures', 'dfs and similar', 'implementation'],
['math', 'number theory', 'probabilities', 'chinese remainder theorem', 'fft', 'geometry'],
['*special', 'implementation'],
['dp', 'bitmasks'],
['graphs', 'graph matchings', 'shortest paths', 'dfs and similar', 'dsu', 'flows'],
['2-sat', 'dfs and similar', 'dp'],
['expression parsing', 'math', 'data structures'],
['games', 'dp'],
['combinatorics', 'dp', 'data structures', 'graphs', 'math', 'number theory'],
['flows', 'graphs', 'graph matchings'],
['brute force', 'math', 'constructive algorithms'],
['implementation','schedules']]

i = 0

def findTags(userTable, allProblems):
	user_problem_tags_notRep = []
	user_problem_tags_rep = []
	original_tags = []
	for index, row in userTable.iterrows():
		if row['status'] == 'Accepted':
			current_problem = row['problem_id']
			index_of_problem = allProblems.index[allProblems['problem_id'] == current_problem]
			problem_row = allProblems.loc[index_of_problem]
			for index2, row2 in problem_row.iterrows():
				tags = row2['tags']
				original_tags.append(tags)
				tags = tags.split(",")
				for tag in tags:
					user_problem_tags_rep.append(tag)
					if tag not in user_problem_tags_notRep:
						user_problem_tags_notRep.append(tag)

	return user_problem_tags_notRep, user_problem_tags_rep, original_tags

def findLeastAndMostSolved(user_problem_tags_notRep, user_problem_tags_rep):
	numOfTimes = []
	allLeast = []
	allMost = []
	for tag in user_problem_tags_notRep:
		count = user_problem_tags_rep.count(tag)
		numOfTimes.append(count)
	least = min(numOfTimes)
	most = max(numOfTimes)
	difference = most - least
	j = 0
	for num in numOfTimes:
		if difference > 1:
			if num == least or num == least + 1:
				allLeast.append(user_problem_tags_notRep[j])
		else:
			if num == least:
				allLeast.append(user_problem_tags_notRep[j])

		if num == most:
			allMost.append(user_problem_tags_notRep[j])
		j = j + 1

	return allLeast, allMost

def findMostSolvedTag(user_problem_tags_notRep, user_problem_tags_rep):
	numOfTimes = []
	allMost = []
	for tag in user_problem_tags_notRep:
		count = user_problem_tags_rep.count(tag)
		numOfTimes.append(count)
	most = max(numOfTimes)
	j = 0
	for num in numOfTimes:
		if num == most:
			allMost.append(user_problem_tags_notRep[j])
		j = j + 1

	return allMost

def detailsOfPrevTagQuestion(userTable, tags, tagsToAvoid, originalTags, allProblems):
	i = 0
	problems = []
	difficulties = []
	allAttempts = []
	found = False
	fit1 = True #Has none of the most solved tags
	fit2 = False #
	indices = []
	for eachOriginalTag in originalTags: #[[math,greedy],[geometry, dp]]
		eachOriginalTag = eachOriginalTag.split(',') 
		for eachTag in eachOriginalTag: #[math,greedy]
			if eachTag in tagsToAvoid:
				fit1 = False
				break
		if fit1 == True:
			for eachTag in eachOriginalTag:
				if eachTag in tags:
					fit2 = True

		if fit1 == True and fit2 == True:
			indices.append(i)
		i = i + 1
		fit1 = True
		fit2 = False

	k = 0
	if len(indices) > 0:
		for index, row in userTable.iterrows():
			if row['status'] == 'Rejected':
				continue
			if k in indices:
				problem = row['problem_id']
				attempts = row['attempts_range']
				if problem not in problems:
					problems.append(problem)
					allAttempts.append(attempts)
			k = k + 1
		for eachProblem in problems:
			index_of_problem = allProblems.index[allProblems['problem_id'] == eachProblem]
			problem_row = allProblems.loc[index_of_problem]
			for index2, row2 in problem_row.iterrows():
				difficulty = row2['level_type']
				difficulties.append(difficulty)
	else:
		for eachOriginalTag in originalTags:
			eachOriginalTagSeparated = eachOriginalTag.split(',')
			if tags[k] in eachOriginalTagSeparated:
				indices.append(originalTags.index(eachOriginalTag))
				k = k + 1
				if k == len(tags):
					break
		k = 0
		for index, row in userTable.iterrows():
			if row['status'] == 'Rejected':
				continue
			if k in indices:
				problem = row['problem_id']
				attempts = row['attempts_range']
				if problem not in problems:
					problems.append(problem)
					allAttempts.append(attempts)
			k = k + 1
		for eachProblem in problems:
			index_of_problem = allProblems.index[allProblems['problem_id'] == eachProblem]
			problem_row = allProblems.loc[index_of_problem]
			for index2, row2 in problem_row.iterrows():
				difficulty = row2['level_type']
				difficulties.append(difficulty)

	return problems, difficulties, allAttempts

def findSimilarTagQuestion2(problemsAlreadySolved, difficulties, attempts, targetTags, tagsToAvoid, allProblems, relatedTags, number, allProblemsSolved):
	i = 0
	allFitProblems = []
	found1 = True
	found2 = True
	previousProblem = -1
	upgraded = False
	downgraded = False
	notChanged = False
	for eachProblem in problemsAlreadySolved:
		subListOfPossiblemProblems = []
		if i == len(attempts):
			break
		if attempts[i] < 4:
			if difficulties[i] != 'N':
				difficulty = chr(ord(difficulties[i])+1)
				upgraded = True
			else:
				difficulty = 'N'
				notChanged = True
		else:
			if difficulties[i] != 'A':
				difficulty = chr(ord(difficulties[i])-1)
				downgraded = True
			else:
				difficulty = 'A'
				notChanged = True

		index_of_problem = allProblems.index[allProblems['problem_id'] == eachProblem]
		problem_row = allProblems.loc[index_of_problem]
		if notChanged == True:
			index_of_table = allProblems.index[allProblems['level_type'] == difficulty]
			tableWithDifficulty = allProblems.loc[index_of_table] 
		elif upgraded == True and ord(difficulty) != 78:
			index_of_table = allProblems.index[allProblems['level_type'] >= difficulty]
			initialTableWithDifficulty = allProblems.loc[index_of_table] 
			index_of_table = initialTableWithDifficulty.index[initialTableWithDifficulty['level_type'] <= chr(ord(difficulty)+1)]
			tableWithDifficulty = initialTableWithDifficulty.loc[index_of_table] 
		elif downgraded == True and ord(difficulty) != 65:
			index_of_table = allProblems.index[allProblems['level_type'] <= difficulty]
			initialTableWithDifficulty = allProblems.loc[index_of_table] 
			index_of_table = initialTableWithDifficulty.index[initialTableWithDifficulty['level_type'] >= chr(ord(difficulty)-1)]
			tableWithDifficulty = initialTableWithDifficulty.loc[index_of_table] 

		for index, r in problem_row.iterrows():
			previousProblem = r['problem_id']
			its_tags = r['tags']

		its_tags = its_tags.split(',')

		for eachOne in its_tags: #tags of the i-th question with the least tags 		
			if eachOne in targetTags: 
				theTag = eachOne 
			else:
				continue
			if theTag == 'mcq':
				for index2, row in tableWithDifficulty.iterrows():
					if row['problem_id'] not in allProblemsSolved:
						if theTag == row['tags']:
							subListOfPossiblemProblems.append(row['problem_id'])			
			else:
				indexOfTagRelation = targetTags.index(theTag)
				allowedTags = relatedTags[indexOfTagRelation] 
				for index2, row in tableWithDifficulty.iterrows():
					if row['problem_id'] not in allProblemsSolved:
						tags = row['tags'].split(',')
						for tag in tags:
							if tag in tagsToAvoid:
								found1 = False
								break
						if found1 == True:
							for tag in tags:
								if tag not in allowedTags:
									found2 = False

						if found1 == True and found2 == True:
							subListOfPossiblemProblems.append(row['problem_id'])			
						found1 = True
						found2 = True

		allFitProblems.append(subListOfPossiblemProblems)
		i = i + 1

	return allFitProblems

def findSimilarTagQuestion(problemsAlreadySolved, difficulties, attempts, targetTags, tagsToAvoid, allProblems, relatedTags, number, allProblemsSolved):
	i = 0
	allFitProblems = []
	found1 = True
	found2 = True
	previousProblem = -1
	upgraded = False
	downgraded = False
	notChanged = False
	for eachProblem in problemsAlreadySolved:
		subListOfPossiblemProblems = []
		if i == len(attempts):
			break
		if attempts[i] < 4:
			if difficulties[i] != 'N':
				difficulty = chr(ord(difficulties[i])+1)
				upgraded = True
			else:
				difficulty = 'N'
				notChanged = True
		else:
			if difficulties[i] != 'A':
				difficulty = chr(ord(difficulties[i])-1)
				downgraded = True
			else:
				difficulty = 'A'
				notChanged = True

		index_of_problem = allProblems.index[allProblems['problem_id'] == eachProblem]
		problem_row = allProblems.loc[index_of_problem]

		index_of_table = allProblems.index[allProblems['level_type'] == difficulty] #Just for assignment
		tableWithDifficulty = allProblems.loc[index_of_table] #Just for assignment
		if notChanged == True:
			index_of_table = allProblems.index[allProblems['level_type'] == difficulty]
			tableWithDifficulty = allProblems.loc[index_of_table] 
			
		elif upgraded == True and ord(difficulty) != 78:
			firstIndex_of_table = allProblems.index[allProblems['level_type'] >= difficulty]
			initialTableWithDifficulty = allProblems.loc[firstIndex_of_table] 
			index_of_table = initialTableWithDifficulty.index[initialTableWithDifficulty['level_type'] <= chr(ord(difficulty)+1)]
			tableWithDifficulty = initialTableWithDifficulty.loc[index_of_table] 

		elif downgraded == True and ord(difficulty) != 65:
			firstIndex_of_table = allProblems.index[allProblems['level_type'] <= difficulty]
			initialTableWithDifficulty = allProblems.loc[firstIndex_of_table] 
			index_of_table = initialTableWithDifficulty.index[initialTableWithDifficulty['level_type'] >= chr(ord(difficulty)-1)]
			tableWithDifficulty = initialTableWithDifficulty.loc[index_of_table] 

		for index, r in problem_row.iterrows():
			previousProblem = r['problem_id']
			its_tags = r['tags']

		its_tags = its_tags.split(',')

		for eachOne in its_tags: #tags of the i-th question with the least tags 		
			if eachOne in targetTags: 
				theTag = eachOne 
			else:
				continue

			if theTag == 'mcq':
				for index2, row in tableWithDifficulty.iterrows():
					if row['problem_id'] not in allProblemsSolved:
						if theTag == row['tags']:
							subListOfPossiblemProblems.append(row['problem_id'])			
			else:
				indexOfTagRelation = targetTags.index(theTag)
				allowedTags = relatedTags[indexOfTagRelation] 	
				for index, row in tableWithDifficulty.iterrows():
					if row['problem_id'] not in allProblemsSolved:
						tags = row['tags'].split(',')
						for tag in tags:
							if tag in tagsToAvoid:
								found1 = False
								break
						if found1 == True:
							# print(theTag)
							if theTag in tags:
								for tag in tags:
									if tag not in allowedTags:
										found2 = False
							else:
								found2 = False
						if found1 == True and found2 == True:
							subListOfPossiblemProblems.append(row['problem_id'])			
						found1 = True
						found2 = True

		allFitProblems.append(subListOfPossiblemProblems)
		i = i + 1

	empty = True
	for eachList in allFitProblems:
		if len(eachList) > 0:
			empty = False
	i = 0
	found1 = True
	found2 = True

	if empty == True:
		allFitProblems = []
		for eachProblem in problemsAlreadySolved:
			subListOfPossiblemProblems = []
			if attempts[i] < 4:
				if difficulties[i] != 'N':
					difficulty = chr(ord(difficulties[i])+1)
				else:
					difficulty = 'N'
			else:
				if difficulties[i] != 'A':
					difficulty = chr(ord(difficulties[i])-1)
				else:
					difficulty = 'A'

			index_of_problem = allProblems.index[allProblems['problem_id'] == problemsAlreadySolved[i]]
			problem_row = allProblems.loc[index_of_problem]
			index_of_table = allProblems.index[allProblems['level_type'] == difficulty]
			tableWithDifficulty = allProblems.loc[index_of_table] 

			for index, r in problem_row.iterrows():
				previousProblem = r['problem_id']
				its_tags = r['tags']

			its_tags = its_tags.split(',')

			for eachOne in its_tags: #tags of the i-th question with the least tags 		
				if eachOne in targetTags: 
					theTag = eachOne 
				else:
					continue

				if theTag == 'mcq':
					for index2, row in tableWithDifficulty.iterrows():
						if row['problem_id'] not in allProblemsSolved:
							if theTag == row['tags']:
								subListOfPossiblemProblems.append(row['problem_id'])			
				else:
					indexOfTagRelation = targetTags.index(theTag)
					allowedTags = relatedTags[indexOfTagRelation] 
					for index2, row in tableWithDifficulty.iterrows():
						if row['problem_id'] not in allProblemsSolved:
							tags = row['tags'].split(',')
							for tag in tags:
								if tag in tagsToAvoid:
									found1 = False
									break
							if found1 == True:
								if theTag in tags:
									subListOfPossiblemProblems.append(row['problem_id'])					
							found1 = True

			allFitProblems.append(subListOfPossiblemProblems)
			i = i + 1
	empty = True
	for eachList in allFitProblems:
		if len(eachList) > 0:
			empty = False

	return allFitProblems, empty

def findMostSolvedProblem(candidates, train_sample):
	# print(candidates)
	largest = 0
	index_of_largest = -1
	i = 0
	for eachProblem in candidates:
		index_of_problem = train_sample.index[train_sample['problem_id'] == eachProblem]
		table = train_sample.loc[index_of_problem] 
		if table.size > largest:
			largest = table.size
			index_of_largest = i
		i = i + 1
	return candidates[index_of_largest]

def findMostSolvedProblem2(oldProblems, listsOfCandidates, train_sample):
	largest = -1
	index_of_array = -1
	index_inside_array = -1
	i = 0
	j = 0
	for eachList in listsOfCandidates:
		for eachProblem in eachList:
			index_of_problem = train_sample.index[train_sample['problem_id'] == eachProblem]
			table = train_sample.loc[index_of_problem] 
			if table.size > largest:
				largest = table.size
				index_of_array = i
				index_inside_array = j
			j = j + 1
		j = 0
		i = i + 1
	return oldProblems[index_of_array], listsOfCandidates[index_of_array][index_inside_array]

def pickRandomQuestion(rank, userTable, allProblems):
	possibleProblems = []
	attempts = 0 
	i = 0
	j = 0
	for index, row in userTable.iterrows():
		if row['status'] == 'Accepted':
			attempts = attempts + row['attempts_range']
			i = i + 1
	average = attempts // i
	if rank == 'beginner':
		if average == 1:
			difficulty = 'E'
		elif average == 2:
			difficulty = 'D'
		elif average == 3:
			difficulty = 'C'
		elif average == 4:
			difficulty = 'B'
		else:
			difficulty = 'A'
	elif rank == 'intermediate':
		if average < 3:
			difficulty = 'I'
		elif average < 5:
			difficulty = 'H'
		else:
			difficulty = 'G'
	else:
		if average == 1:
			difficulty = 'N'
		elif average == 2:
			difficulty = 'M'
		elif average == 3:
			difficulty = 'L'
		elif average == 4:
			difficulty = 'K'
		else:
			difficulty = 'J'

	index_of_table = allProblems.index[allProblems['level_type'] == difficulty]
	tableWithDifficulty = allProblems.loc[index_of_table]
	numberOfPossibleProblems = len(tableWithDifficulty['problem_id'].unique())
	allProblemsSolved = userTable['problem_id'].unique()
	while j < 10:
		randomIndex = random.randint(0,numberOfPossibleProblems-1)
		if tableWithDifficulty['problem_id'].unique()[randomIndex] not in allProblemsSolved and tableWithDifficulty['problem_id'].unique()[randomIndex] not in possibleProblems:
			possibleProblems.append(tableWithDifficulty['problem_id'].unique()[randomIndex])
			j = j + 1
	return possibleProblems

def getRelatedTags(leastSolvedTags, allRelatedTags, tagsToAvoid):

	relatedTags = []
	for eachTag in leastSolvedTags:
		bag = []
		for eachRelation in allRelatedTags:
			if eachTag in eachRelation:
				bag.append(eachRelation)

		flat_list = []

		for eachList in bag:
			for eachItem in eachList:
				if eachItem not in tagsToAvoid and eachItem not in flat_list:
					flat_list.append(eachItem)
		relatedTags.append(flat_list)
	return relatedTags

def pickRandomQuestionWithoutTag(rank, tagsToAvoid, userTable, allProblems):
	attempts = 0 
	i = 0
	j = 0
	found = True
	possibleProblems = []
	for index, row in userTable.iterrows():
		if row['status'] == 'Accepted':
			attempts = attempts + row['attempts_range']
			i = i + 1
	average = attempts // i
	if rank == 'beginner':
		if average == 1:
			difficulty = 'E'
		elif average == 2:
			difficulty = 'D'
		elif average == 3:
			difficulty = 'C'
		elif average == 4:
			difficulty = 'B'
		else:
			difficulty = 'A'
	elif rank == 'intermediate':
		if average < 3:
			difficulty = 'I'
		elif average < 5:
			difficulty = 'H'
		else:
			difficulty = 'G'
	else:
		if average == 1:
			difficulty = 'N'
		elif average == 2:
			difficulty = 'M'
		elif average == 3:
			difficulty = 'L'
		elif average == 4:
			difficulty = 'K'
		else:
			difficulty = 'J'
	index_of_table = allProblems.index[allProblems['level_type'] == difficulty]
	tableWithDifficulty = allProblems.loc[index_of_table]
	allProblemsSolved = (userTable['problem_id'].unique()).tolist()
	for index, row in tableWithDifficulty.iterrows():
		if j == 10:
			break
		tags = row['tags'].split(",")
		for tag in tags: 
			if tag in tagsToAvoid:
				found = False
				break
		if found == True and row['problem_id'] not in allProblemsSolved and row['problem_id'] not in possibleProblems:
			possibleProblems.append(row['problem_id'])
			j = j + 1
		found = True
	return possibleProblems

while i < len(train_sample['user_id'].unique()):
	users.append(train_sample['user_id'].unique()[i])
	user_index = train_sample.index[train_sample['user_id'] == train_sample['user_id'].unique()[i]] 
	user_train_table = train_sample.loc[user_index]
	allProblemsSolved = user_train_table['problem_id'].unique().tolist()
	user_problem_tags, user_problem_tags_rep, original_tags = findTags(user_train_table, problem_sample)
	index_of_user = user_sample.index[user_sample['user_id'] == train_sample['user_id'].unique()[i]]
	tableOfUser = user_sample.loc[index_of_user]
	for index, row in tableOfUser.iterrows():
		rank = row['rank']
	# print("-------------------------------------------------------------------------")
	print("User " + str(train_sample['user_id'].unique()[i]))
	if len(original_tags) < 3:
		print("got a random question 1")
		possibleProblems = pickRandomQuestion(rank, user_train_table, problem_sample)
		final_problem = findMostSolvedProblem(possibleProblems, train_sample)
		previousProblems.append(0)
		# print(possibleProblems)
		# print("-------------------------------------------------------------------------")
	elif len(user_problem_tags) < 6 and len(original_tags) < 7: 
		print("got a random question 2") 
		previousProblems.append(0)
		tags_to_avoid = findMostSolvedTag(user_problem_tags, user_problem_tags_rep)		
		possibleProblems = pickRandomQuestionWithoutTag(rank, tags_to_avoid, user_train_table, problem_sample)
		final_problem = findMostSolvedProblem(possibleProblems, train_sample)
		# print(possibleProblems)
		# print("-------------------------------------------------------------------------")
	else:
		tags_of_new_question, tags_to_avoid = findLeastAndMostSolved(user_problem_tags, user_problem_tags_rep)
		# print("Least solved tags:")
		# print(tags_of_new_question)
		# print("\nMost solved tags:")
		# print(tags_to_avoid)
		# for eachSingleTag in original_tags:
		# 	print(eachSingleTag)
		problems, itsDifficulties, itsAttempts = detailsOfPrevTagQuestion(user_train_table, tags_of_new_question, tags_to_avoid, original_tags, problem_sample)
		# print("\nThe old problems:")
		# print(problems)
		# print()
		relatedTags = getRelatedTags(tags_of_new_question, tags_relations, tags_to_avoid)
		# print("-------")
		# print(relatedTags)
		# print("------")
		possibleProblems, empty = findSimilarTagQuestion(problems, itsDifficulties, itsAttempts, tags_of_new_question, tags_to_avoid, problem_sample, relatedTags, train_sample['user_id'].unique()[i], allProblemsSolved)
		if empty == True:
			possibleProblems = findSimilarTagQuestion2(problems, itsDifficulties, itsAttempts, tags_of_new_question, tags_to_avoid, problem_sample, relatedTags, train_sample['user_id'].unique()[i], allProblemsSolved)
		previous_problem, final_problem = findMostSolvedProblem2(problems, possibleProblems, train_sample)
		

		# print("\nThe problem is")
		# print(final_problem)
		previousProblems.append(previous_problem)
		# print(tags_of_new_question)
		# print(tags_to_avoid)
		# print("-------------------------")
		# print(problems)
		# print(possibleProblems)
		# print("-------------------------")
		# print(previous_problem)
		# print(final_problem)
		# print("-------------------------------------------------------------------------")
	
	problemsToPredict.append(final_problem) 
	i = i + 1

print()
print(users)
print(problemsToPredict)
print(previousProblems)


